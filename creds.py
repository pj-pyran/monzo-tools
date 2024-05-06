import json

PATH_CREDS = 'creds.json'

def creds() -> dict:
    # Load stored creds from json. Implement something more secure later
    with open(PATH_CREDS, 'r') as json_file:
        dict_creds = json.load(json_file)
    return dict_creds
