import requests
import base64
import json
import random
import config

def get_bearer_token(auth_code):
    """Gets bearer token from authorization code"""
    token_endpoint = get_discovery_doc()['token_endpoint']
    auth_header = 'Basic ' + to_base64(config.CLIENT_ID + ':' + config.CLIENT_SECRET)
    headers = {
        'Accept': 'application/json', 
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': auth_header
    }
    payload = {
        'code': auth_code,
        'redirect_uri': config.REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    r = requests.post(token_endpoint, data=payload, headers=headers)
    if r.status_code != 200:
        return r.text
    bearer = json.loads(r.text)
    return bearer

def get_discovery_doc():
    """Gets OAuth2 discover document based on configured environment"""
    if config.ENVIRONMENT == "Sandbox":
        req = requests.get("https://developer.intuit.com/.well-known/openid_sandbox_configuration/")
    else:
        req = requests.get("https://developer.intuit.com/.well-known/openid_configuration/")
    if req.status_code >= 400:
        return ''
    discovery_doc = req.json()
    return discovery_doc

def to_base64(s):
    """String to Base64"""
    return base64.b64encode(bytes(s, 'utf-8')).decode()

def random_string(length, allowed_chars='abcdefghijklmnopqrstuvwxyz' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

def secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return random_string(40, chars)