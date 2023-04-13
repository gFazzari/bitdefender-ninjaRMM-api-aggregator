import requests

def authenticate(client_id: str, client_secret: str):
    HOST = 'https://eu-api.ninjarmm.com/ws/oauth/token'
    params = {
        'grant_type': 'client_credentials',
        'scope': 'monitoring'
    }
    response = requests.post(HOST, params=params, auth=(client_id, client_secret))
    if 'error' in response.text:
        dict = response.json()
        raise ValueError(dict['error'])
    else:
        return response.json()['access_token']