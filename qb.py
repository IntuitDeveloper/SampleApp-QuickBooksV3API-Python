import Customer
from utils import configRead, requestMethods 
from flask import session
from utils import context
import json

# Create a customer object with customer data from working dictionary
def create_customer(my_customer):
    full_name = my_customer['Full Name']
    name_list = full_name.split(' ')
    first_name = name_list[0]
    last_name = name_list[-1]
    if len(name_list) > 2:
        middle_name = str(name_list[1:len(name_list) - 1])
    else:
        middle_name = ''
    customer = Customer.Customer(first_name, last_name, middle_name, my_customer['Phone'], my_customer['Email'])
    return customer

# Add selected lead as a customer to QBO
def add_customer(customer, req_context):
    req_body = json_body(customer)
    base_url = configRead.get_api_url() + req_context.realm_id 
    url = base_url + '/customer' + configRead.get_minorversion(4)
    request_data = {'payload': req_body, 'url': url}
    response_data = requestMethods.request(request_data, req_context, method='POST')
    handled_response =  handle_response(response_data)
    return handled_response

# Set the request body for create_customer    
def json_body(customer):
    req_body = {}
    try:
        req_body["GivenName"] = customer.given_name
        req_body["MiddleName"] = customer.middle_name
        req_body["FamilyName"] = customer.family_name
        req_body["PrimaryPhone"] = {}
        (req_body["PrimaryPhone"])["FreeFormNumber"] = customer.primary_phone
        req_body["PrimaryEmailAddr"] = {}
        (req_body["PrimaryEmailAddr"])["Address"] = customer.primary_email_addr
    except AttributeError:
        print 'Customer object has no attributes'
    return req_body

# Get error/success message after response
def handle_response(response_data):
    new_reponse = {}
    new_reponse['status_code'] = response_data['status_code']
    content = json.loads(response_data['content'])
    if response_data['status_code'] != 200:
        new_reponse['font_color'] = 'red'
        try:
            new_reponse['message'] = content['Fault']['Error'][0]['Message']
        except:
            new_reponse['message'] = "Some error occurred. Error message not found."
    else:
        new_reponse['font_color'] = 'green'
        new_reponse['message'] = "Success! Customer added to QBO"
        # More data from successful response can be retrieved like customer id
    return new_reponse

# Set and get context of the request
def req_context():
    try:
        access_tokens = session.get('qbo_token')
        access_key = access_tokens[0]
        access_sec = access_tokens[1]
        realm_id = session.get('realm_id')
    except (IndexError,KeyError) as e:
        access_key = None
        access_sec = None
        realm_id = None
        print 'ERROR: '+ e

    req_context = context.RequestContext(realm_id, access_key, access_sec)
    return req_context
