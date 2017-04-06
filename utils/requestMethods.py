import requests
from requests_oauthlib import OAuth1

# POST for qbo sandbox
def do_post(url, headers, payload, auth):
    req = requests.post(url, auth=auth, headers=headers, json=payload)
    response_data = {}
    response_data['status_code'] = req.status_code
    response_data['content'] = req.content
    return response_data

def get(url, headers, payload, auth):
    req = requests.get(url, auth=auth, headers=headers, data=payload)
    return req.content

def request(req_data, req_context, method):
    headers = {'Accept': 'application/json', 'content-type': 'application/json; charset=utf-8', 'User-Agent': 'PythonSampleApp1'}
    payload = req_data['payload']
    url = req_data['url']
    auth = OAuth1(req_context.consumer_key, req_context.consumer_secret, req_context.access_key, req_context.access_secret)
    if method == 'POST':
        response_data = do_post(url, headers, payload, auth)
        return response_data
    # else GET method

    
        
