from configRead import consumerTokens
# The context class sets the realm id with the consumer tokens every time user authorizes an app for their QB company

class RequestContext:
    
    def __init__(self, realm_id, access_key, access_secret):
        consumer_tokens = consumerTokens()
        self.consumer_key = consumer_tokens.consumer_key
        self.consumer_secret = consumer_tokens.consumer_sec
        self.realm_id = realm_id
        self.access_key = access_key
        self.access_secret = access_secret
    
    def print_context(self):
        print self.consumer_key, self.consumer_secret, self.realm_id, self.access_secret, self.access_key      

