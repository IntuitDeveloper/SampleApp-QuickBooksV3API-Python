from flask import Flask, request, redirect, url_for, session, g, flash, render_template
from flask_oauth import OAuth
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

if config.AUTH_TYPE == 'OAuth1':
    oauth = OAuth()

    qbo = oauth.remote_app('qbo',
        base_url=config.OAUTH1_BASE,
        request_token_url=config.REQUEST_TOKEN_URL,
        access_token_url=config.ACCESS_TOKEN_URL,
        authorize_url=config.AUTHORIZE_URL,
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET
    )

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
    
    if config.AUTH_TYPE == 'OAuth1':
        request_context = context.RequestContextOAuth1(session['realm_id'], session['access_token'], session['access_secret'])
    else:
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
    if config.AUTH_TYPE == 'OAuth1':
        request_context = context.RequestContextOAuth1(session['realm_id'], session['access_token'], session['access_secret'])
    else:
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
    if config.AUTH_TYPE == "OAuth1":
        return qbo.authorize(callback=url_for('oauth_authorized')) 
    else:
        # OAuth2 initiate authorization flow
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

if config.AUTH_TYPE == 'OAuth1':
    @app.route('/oauth-authorized')
    @qbo.authorized_handler
    def oauth_authorized(resp):
        """Handles callback for OAuth1 only"""
        realm_id = str(request.args.get('realmId'))
        next_url = url_for('index')
        if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(next_url)

        session['is_authorized'] = True 
        session['access_token'] = resp['oauth_token']
        session['realm_id'] = realm_id
        session['access_secret'] = resp['oauth_token_secret']

        return redirect(url_for('index'))

if config.AUTH_TYPE == 'OAuth1':
    @qbo.tokengetter
    def get_qbo_token(token=None):
        """Get OAuth1 QBO token"""
        return session.get('qbo_token')

def csrf_token():
    token = session.get('csrfToken', None)
    if token is None:
        token = OAuth2Helper.secret_key()
        session['csrfToken'] = token
    return token

if __name__ == '__main__':
    app.run()