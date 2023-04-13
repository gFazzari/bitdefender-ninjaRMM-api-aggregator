import csv

def to_csv(headers: list, users: list, filename: str):
    with open(filename, 'w') as file:
        dict_writer = csv.DictWriter(file, headers)
        dict_writer.writeheader()
        dict_writer.writerows(users)