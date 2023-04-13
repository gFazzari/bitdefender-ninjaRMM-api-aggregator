import base64
import json

def create_authorization(api_key: str):
    loginString = "{}:".format(api_key)
    encodedBytes = base64.b64encode(loginString.encode())
    encodedUserPassSequence = str(encodedBytes,'utf-8')
    authorizationHeader = "Basic {}".format(encodedUserPassSequence)
    return authorizationHeader

def create_body_request(method: str, params: dict = {}):
    result = '{{"params": {},"jsonrpc": "2.0","method": "{}", "id":"1"}}'.format(json.dumps(params), method)
    return result