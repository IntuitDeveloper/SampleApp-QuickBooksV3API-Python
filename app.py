# This sample uses code from https://pythonhosted.org/Flask-OAuth/ for OAuth1 login with Twitter
from flask import Flask, request, redirect, url_for, session, g, flash, render_template
from flask_oauth import OAuth
from qb import create_customer, add_customer, req_context
from utils import excel, configRead 

# configuration
SECRET_KEY = 'dev key'
DEBUG = True
font_color = 'black'
consumerTokens = configRead.consumerTokens()
oauth_url = configRead.oauthUrl()

# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

qbo = oauth.remote_app('qbo',
    base_url=oauth_url.base_url,
    request_token_url=oauth_url.request_token_url,
    access_token_url=oauth_url.access_token_url,
    authorize_url=oauth_url.authorize_url,
    consumer_key=consumerTokens.consumer_key,
    consumer_secret=consumerTokens.consumer_sec
)
 
@qbo.tokengetter
def get_qbo_token(token=None):
    if session.has_key('qbo_token'):
        del session['qbo_token'] 
    return session.get('qbo_token')
 
@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('auth'))
 
    access_token = access_token[0]
    global customer_list
    customer_list = excel.load_excel()
    return render_template('index.html', 
        customer_dict=customer_list,
        title="QB Customer Leads",
        text_color=font_color)

# Update leads in html after adding a customer to QBO handled here for simplicity
@app.route('/', methods=['GET','POST'])
def update_table():
    customer_id = request.form['id']
    for customer in customer_list:
        if customer['Id'] == customer_id:
            # Create customer object, add customer to qbo and get response
            customer_obj = create_customer(customer)
            response_data = add_customer(customer_obj, req_context)
            status_code = response_data['status_code']
            message =  response_data['message']
            global font_color
            font_color = response_data['font_color']
            # If customer added successfully, remove them from html and excel file
            if (status_code == 200):
                new_customer_list = excel.remove_lead(customer_list, customer_id)
                flash(message)
                return render_template('index.html',
                                       customer_dict=new_customer_list,
                                       title="QB Customer Leads",
                                       text_color=font_color)
    flash(message)
    return redirect(url_for('index'))
 
@app.route('/auth')
def auth():
    return qbo.authorize(callback=url_for('oauth_authorized'))
 
@app.route('/reset-session')
def reset_session():
    session.pop('qbo_token', None)
    session['is_authorized'] = False
    return redirect(request.referrer or url_for('index'))

# If app is authorized, it ends up here with the response 
@app.route('/oauth-authorized')
@qbo.authorized_handler
def oauth_authorized(resp):
    realm_id = str(request.args.get('realmId'))
    next_url = url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    # Setting the session using flask session just for the simplicity of this Sample App. It's not the most secure way to do this.
    session['is_authorized'] = True
    session['realm_id'] = realm_id
    session['qbo_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    global req_context
    req_context = req_context()
    return redirect(url_for('index'))
 
if __name__ == '__main__':
    app.run()