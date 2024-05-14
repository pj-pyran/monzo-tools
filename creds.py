import json
import requests
from datetime import timedelta, datetime
import logging


def creds_check():
    """
    In each script we run we'll want to check token expiry.
    Use this one centralised function across the package to do this.
    Loads creds, checks token expiry and refreshes only if needed.
    """
    CREDS = get_creds()
    access_token = CREDS['access_token']
    token_expiry = datetime.fromtimestamp(CREDS['token_expiry'])
    logging.info(f'Token expires {token_expiry}')

    if token_expiry < datetime.now() + timedelta(hours=12):
        logging.info('Token expired/expiring soon: refreshing token...')
        refresh_token()
        CREDS = get_creds()
        token_expiry = datetime.fromtimestamp(CREDS['token_expiry'])
        logging.info(f'Token refreshed. New token expires {token_expiry}')
    return CREDS


def get_creds(path_creds: str = 'creds.json') -> dict:
    # Load stored creds from json. Implement something more secure later
    with open(path_creds, 'r') as json_file:
        dict_creds = json.load(json_file)
    return dict_creds

def refresh_token(path_creds: str = 'creds.json'):
    """Refresh our access token. This will be run by cron job every 24hr.
    Loads credentials, retrieves a new token from Monzo and saves new token in creds file.
    Returns True or Error on success/failure"""
    creds = get_creds()
    # Define the endpoint URL
    url = 'https://api.monzo.com/oauth2/token'
    # Define the form data
    data = {
        'grant_type': 'refresh_token',
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token']
    }

    # Make the POST request
    response = requests.post(url, data=data)
    # Success
    if response.status_code == 200:
        creds['refresh_token'] = response.json()['refresh_token']
        creds['access_token'] = response.json()['access_token']
        creds['token_expiry'] += response.json()['expires_in']
        with open(path_creds, 'w') as json_file:
            json.dump(creds, json_file, indent=4)
        return True
    # Failure
    else:
        return response.text
