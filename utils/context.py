import config

class RequestContext(object):
    """The context class sets the realm id with the app's Client tokens every time user authorizes an app for their QB company"""
    def __init__(self, realm_id, access_token, refresh_token):
        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET
        self.realm_id = realm_id
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def __str__(self):
        return self.realm_id

class RequestContextOAuth1(object):
    """The context class sets the realm id with the app's Consumer tokens every time user authorizes an app for their QB company"""
    def __init__(self, realm_id, access_key, access_secret):
        self.consumer_key = config.CONSUMER_KEY
        self.consumer_secret = config.CONSUMER_SECRET
        self.realm_id = realm_id
        self.access_key = access_key
        self.access_secret = access_secret
    
    def __str__(self):
        return self.realm_id

