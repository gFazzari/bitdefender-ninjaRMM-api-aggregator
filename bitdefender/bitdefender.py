from datetime import datetime
import bitdefender.utils as utils
import requests

BASE_URL = 'https://cloudgz.gravityzone.bitdefender.com/api/'
NETWORK_API = 'v1.0/jsonrpc/network/'

def list_endpoints(API_KEY: str):
	authorization = utils.create_authorization(API_KEY)
	url = '{}{}'.format(BASE_URL, NETWORK_API)
	users = []
	for i in range(1, 50):
		params = {
			'filters': {
				'depth': {
					'allItemsRecursively': True
				}
			},
			'page': i,
			'perPage': 100
		}
		request = utils.create_body_request(method='getEndpointsList', params=params)
		response = requests.post(url, data=request, headers= {'Content-Type': 'application/json','Authorization': authorization}).json()
		if 'error' in response:
			if response['error']['message'] == 'Invalid params':
				break
			else:
				raise ValueError(response['error'])
		else:
			users = users + response['result']['items']
	extract = []
	[ extract.append({'id': user['id'], 'computer_name': user['name'], 'operating_system_version': user['operatingSystemVersion'], 'timestamp': datetime.now()}) for user in users]
	return extract

def get_endpoint_details(API_KEY: str, id: str):
	authorization = utils.create_authorization(API_KEY)
	url = '{}{}'.format(BASE_URL, NETWORK_API)
	params = {
		"endpointId": id
	}
	request = utils.create_body_request(method='getManagedEndpointDetails', params=params)
	response = requests.post(url, data=request, headers= {'Content-Type': 'application/json','Authorization': authorization}).json()
	if 'error' in response:
		raise ValueError(response['error'])
	else:
		return response
