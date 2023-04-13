from google.cloud import bigquery
import os


def create_dataset(client, dataset_id):
    dataset_ref = bigquery.DatasetReference.from_string(dataset_id)
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "europe-west1"
    dataset = client.create_dataset(dataset)
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))


def list_datasets(client):
    datasets = list(client.list_datasets())
    project = client.project
    if datasets:
        print("Datasets in project {}:".format(project))
        for dataset in datasets:
            print("\t{}".format(dataset.dataset_id))
    else:
        print("{} project does not contain any datasets.".format(project))


def get_dataset(client, dataset_id):
    dataset = client.get_dataset(dataset_id)  # Make an API request.
    full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
    friendly_name = dataset.friendly_name
    print(
        "Got dataset '{}' with friendly_name '{}'.".format(
            full_dataset_id, friendly_name
        )
    )


def delete_dataset(client, dataset_id):
    client.delete_dataset(
        dataset_id, delete_contents=True, not_found_ok=True
    )
    print("Deleted dataset '{}'.".format(dataset_id))