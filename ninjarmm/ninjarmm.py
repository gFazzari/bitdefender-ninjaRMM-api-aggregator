import requests
import sys
import ninjarmm.utils as utils
from datetime import datetime
import time

def list_devices(client_id: str, client_secret: str):
    HOST = 'https://eu-api.ninjarmm.com/v2/devices-detailed'
    try:
        token = utils.authenticate(client_id, client_secret)
        headers = {'Authorization': 'Bearer ' + token}
        response = requests.get(HOST, headers=headers)
        if response.status_code != 200:
            raise ValueError("Can't conctat NinjaRMM API: {}".format(response.json()))
        else:
            users = response.json()
            for user in users:
                name = user.get('systemName', 'None')
                last_seen = user.get('lastContact', time.time())
                last_login = user.get('lastLoggedInUser', 'None')
                serial_number = user['system'].get('serialNumber', 'None')
                user.clear()
                user['name'] = name
                user['last_seen'] = datetime.fromtimestamp(last_seen)
                user['last_user'] = last_login
                user['serial_number'] = serial_number
                user['timestamp'] = datetime.now()
        users = sorted(users, key=lambda d: d['name']) 
        return users
    except ValueError as err:
        print('Error during authentication: {}'.format(err))
        sys.exit(1)