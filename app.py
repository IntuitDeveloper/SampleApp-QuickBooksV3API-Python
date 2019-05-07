from flask import Flask, request, redirect, url_for, session, g, flash, render_template
# from flask_oauth import OAuth
import requests
import urllib
from werkzeug.exceptions import BadRequest
from QBOService import create_customer, get_companyInfo
from utils import excel, context, OAuth2Helper
import config

# configuration
SECRET_KEY = 'dev key'
DEBUG = True

# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    """Index route"""
    global customer_list
    customer_list = excel.load_excel()
    return render_template(
        'index.html',
        customer_dict=customer_list,
        title="QB Customer Leads",
    )

@app.route('/', methods=['POST'])
def update_table():
    """Update Excel file after customer is added in QBO"""
    customer_id = request.form['id']
  
    request_context = context.RequestContext(session['realm_id'], session['access_token'], session['refresh_token'])

    for customer in customer_list:
        if customer['Id'] == customer_id:
            # Create customer object
            response = create_customer(customer, request_context)
            
            # If customer added successfully, remove them from html and excel file
            if (response.status_code == 200):
                font_color = 'green'
                new_customer_list = excel.remove_lead(customer_list, customer_id)
                flash('Customer successfully added!')
                return render_template(
                    'index.html',
                    customer_dict=new_customer_list,
                    title='QB Customer Leads',
                    text_color=font_color
                )
            else:
                font_color = 'red'
                flash('Something went wrong: ' + response.text)
    return redirect(url_for('index'))

@app.route('/company-info')
def company_info():
    """Gets CompanyInfo of the connected QBO account"""
    request_context = context.RequestContext(session['realm_id'], session['access_token'], session['refresh_token'])
    
    response = get_companyInfo(request_context)
    if (response.status_code == 200):
        return render_template(
            'index.html',
            customer_dict=customer_list,
            company_info='Company Name: ' + response.json()['CompanyInfo']['CompanyName'],
            title='QB Customer Leads',
        )
    else:
        return render_template(
            'index.html',
            customer_dict=customer_list,
            company_info=response.text,
            title='QB Customer Leads',
        )
    
@app.route('/auth')
def auth():
    """Initiates the Authorization flow after getting the right config value"""
    params = {
        'scope': 'com.intuit.quickbooks.accounting', 
        'redirect_uri': config.REDIRECT_URI,
        'response_type': 'code', 
        'client_id': config.CLIENT_ID,
        'state': csrf_token()
    }
    url = OAuth2Helper.get_discovery_doc()['authorization_endpoint'] + '?' + urllib.parse.urlencode(params)
    return redirect(url)
   
@app.route('/reset-session')
def reset_session():
    """Resets session"""
    session.pop('qbo_token', None)
    session['is_authorized'] = False
    return redirect(request.referrer or url_for('index'))

@app.route('/callback')
def callback():
    """Handles callback only for OAuth2"""
    #session['realmid'] = str(request.args.get('realmId'))
    state = str(request.args.get('state'))
    error = str(request.args.get('error'))
    if error == 'access_denied':
        return redirect(index)
    if state is None:
        return BadRequest()
    elif state != csrf_token():  # validate against CSRF attacks
        return BadRequest('unauthorized')
    
    auth_code = str(request.args.get('code'))
    if auth_code is None:
        return BadRequest()
    
    bearer = OAuth2Helper.get_bearer_token(auth_code)
    realmId = str(request.args.get('realmId'))

    # update session here
    session['is_authorized'] = True 
    session['realm_id'] = realmId
    session['access_token'] = bearer['access_token']
    session['refresh_token'] = bearer['refresh_token']

    return redirect(url_for('index'))

def csrf_token():
    token = session.get('csrfToken', None)
    if token is None:
        token = OAuth2Helper.secret_key()
        session['csrfToken'] = token
    return token

if __name__ == '__main__':
    app.run()