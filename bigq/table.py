from google.cloud import bigquery
import os


def create_table(client, table_id, schema):
    table_id = bigquery.Table.from_string(table_id)
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(
        "Created table {}.".format(table_id)
    )

def delete_table(client, table_id):
    client.delete_table(table_id, not_found_ok=True)
    print("Deleted table {}.".format(table_id))

def get_table(client, table_id):
    table_id = bigquery.Table.from_string(table_id)
    return client.get_table(table_id)

def load_from_csv(client, file_path, table):
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        field_delimiter=',',
        source_format=bigquery.SourceFormat.CSV,
        allow_quoted_newlines = True,
        autodetect = False
    )
    with open(file_path, "rb") as file:
        load_job = client.load_table_from_file(file_obj=file, destination=table ,job_config=job_config)
        load_job.result()
    
    destination_table = get_table(client, table)
    print("Loaded {} rows for table {}.".format(destination_table.num_rows, destination_table))
