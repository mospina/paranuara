import json

from .models import Company

def load_data_from_file(file_path):
    """
    Save the data from a json file in the RDB
    """
    with open(file_path, newline='') as fh:
        load_data(fh)
    fh.close()

    return True

def load_data(filehandler):
    json_data = json.load(filehandler)
    companies = map(
        lambda entry: Company(index=entry['index'], name=entry['company']),
        json_data
    )
    Company.objects.bulk_create(companies)
