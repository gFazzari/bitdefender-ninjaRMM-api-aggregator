import os
from bigq import dataset, table
import bitdefender.bitdefender as bitdefender
import utils
import ninjarmm.ninjarmm as ninjarmm
from dotenv import load_dotenv
import sys
from google.cloud import bigquery
from datetime import datetime
from google.cloud.exceptions import Conflict
from google.oauth2 import service_account

# Remove comment to test in local environment
# load_dotenv()

def main():
    BITDEFENDER_API_KEY = os.getenv('BITDEFENDER_API_KEY')
    NINJA_CLIENT_ID = os.getenv('NINJA_CLIENT_ID')
    NINJA_CLIENT_SECRET = os.getenv('NINJA_CLIENT_SECRET')
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    PROJECT_ID=os.getenv('PROJECT_ID')
    DATASET_ID = os.getenv('DATASET_ID')
    BITDEFENDER_TABLE_ID = os.getenv('BITDEFENDER_TABLE_ID')
    NINJARMM_TABLE_ID = os.getenv('NINJARMM_TABLE_ID')

    client = bigquery.Client(project=PROJECT_ID)

    # Get Bitdefender data via API
    try:
        user_list = bitdefender.list_endpoints(BITDEFENDER_API_KEY)
    except ValueError as err:
        print('There was an error during endpoints listing: {}'.format(err))
        sys.exit(1)
    else:
        for user in user_list:
            try:
                user_details = bitdefender.get_endpoint_details(BITDEFENDER_API_KEY, user['id'])
                user['last_seen'] = datetime.strptime(user_details['result']['lastSeen'], '%Y-%m-%dT%H:%M:%S')
                del user['id']
            except ValueError as err:
                print('Error during evalutation of user {}: {}'.format(user['computer_name'], err))
                del user['id']
        keys = user_list[0].keys()
        utils.to_csv(headers=keys, users=user_list, filename='bitdefender.csv')

    # Get NinjaRMM data via API
    try:
        user_list = ninjarmm.list_devices(NINJA_CLIENT_ID, NINJA_CLIENT_SECRET)
    except ValueError as err:
        print('Error during devices enumeration: {}'.format(err))
    else:
        keys = user_list[0].keys()
        utils.to_csv(headers=keys, users=user_list, filename='ninjarmm.csv')

    # Create dataset in Bigquery
    try:
        dataset.create_dataset(client, DATASET_ID)
    except Conflict:
        print('Database {} already exists.'.format(DATASET_ID))
    
    # Create Bitdefender table in Bigquery
    try:
        schema = [
            bigquery.SchemaField("computer_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("operating_system_version", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "DATETIME"),
            bigquery.SchemaField("last_seen", "DATETIME")
        ]
        table.create_table(client, BITDEFENDER_TABLE_ID, schema)
    except Conflict:
        print('Table {} already exists.'.format(BITDEFENDER_TABLE_ID))

    # Create Ninja table in Bigquery
    try:
        schema = [
            bigquery.SchemaField("computer_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("last_seen", "DATETIME", mode="REQUIRED"),
            bigquery.SchemaField("last_user", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("serial_number", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("timestamp", "DATETIME")
        ]
        table.create_table(client, NINJARMM_TABLE_ID, schema)
    except Conflict:
        print('Table {} already exists.'.format(NINJARMM_TABLE_ID))

    # Load bitdefender table from CSV
    table.load_from_csv(client, 'bitdefender.csv', BITDEFENDER_TABLE_ID)
    # Load ninja table from CSV
    table.load_from_csv(client, 'ninjarmm.csv', NINJARMM_TABLE_ID)

if __name__ == "__main__":
    main()