DEBUG = False
SQLALCHEMY_ECHO = False

# Specify which OAuth your app uses; default is OAuth2
# Change this flag to 1 for OAUth1 apps
AUTH_TYPE = 'OAuth2'
# AUTH_TYPE = 'OAuth1'

# OAuth2
CLIENT_ID= 'EnterClientIDHere'
CLIENT_SECRET = 'EnterClientSecretHere'
REDIRECT_URI = 'http://localhost:5000/callback'

# OAuth1
CONSUMER_KEY = 'EnterConsumerKeyHere'
CONSUMER_SECRET = 'EnterConsumerSecretHere'

# OAuth1 Base URLs
OAUTH1_BASE = 'https://oauth.intuit.com'
REQUEST_TOKEN_URL = 'https://oauth.intuit.com/oauth/v1/get_request_token'
ACCESS_TOKEN_URL = 'https://oauth.intuit.com/oauth/v1/get_access_token'
AUTHORIZE_URL = 'https://appcenter.intuit.com/Connect/Begin'

# Choose environment; default is sandbox
ENVIRONMENT = 'Sandbox'
# ENVIRONMENT = 'Production'

# Set to latest at the time of updating this app, can be be configured to any minor version
API_MINORVERSION = '23'

