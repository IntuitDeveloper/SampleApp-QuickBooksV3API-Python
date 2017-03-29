from ConfigParser import SafeConfigParser
import os.path 

def get_filepath(relative_filepath):
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, relative_filepath)
    return path

config_file = get_filepath('../config.ini')

parser = SafeConfigParser()
parser.read(config_file)

class consumerTokens:
    def __init__(self):
        self.consumer_key = parser.get('Tokens', 'consumer_key')
        self.consumer_sec = parser.get('Tokens', 'consumer_sec')

class oauthUrl:
    def __init__(self):
        self.base_url = parser.get('OAuth URLs', 'base_url')
        self.request_token_url = parser.get('OAuth URLs', 'request_token_url')
        self.access_token_url = parser.get('OAuth URLs', 'access_token_url')
        self.authorize_url = parser.get('OAuth URLs', 'authorize_url')

def get_api_url():
    return parser.get('API URL', 'base_url')

def get_minorversion(minor_version):
    return '?minorversion='+str(minor_version)


