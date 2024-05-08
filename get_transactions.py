from creds import get_creds, refresh_token
from datetime import datetime
import logging
import pandas as pd
import requests
from format_transactions import format_transactions, format_new_transactions
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

CREDS = get_creds()
PATH_TRANSACTIONS = 'data/transactions_all.csv'
# Set up API endpoint and access token
endpoint = 'https://api.monzo.com/transactions'
access_token = CREDS['access_token']
token_expiry = datetime.fromtimestamp(CREDS['token_expiry'])
logging.info(f'Token expires {token_expiry}')
if token_expiry < datetime.now():
    logging.info(' Token expired: refreshing token...')
    refresh_token()
    CREDS = get_creds()
    token_expiry = datetime.fromtimestamp(CREDS['token_expiry'])
    logging.info(f'Token refreshed. New token expires {token_expiry}')


def call_endpoint(id_start_: str, creds: dict = CREDS) -> dict:
    """Call the endpoint, including error handling.
    Returns the response json."""
    access_token = creds['access_token']
    try:
        # Retrieve from endpoint, using the id
        response = requests.get(
            endpoint,
            params={'limit': 100, 'since': id_start_, 'account_id': creds['account_id']},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        response.raise_for_status()
    except HTTPError as http_err:
        logging.error(response.json())
        raise http_err
    except ConnectionError as conn_err:
        logging.error(response.json())
        raise conn_err
    except Timeout as timeout_err:
        logging.error(response.json())
        raise timeout_err
    except RequestException as req_err:
        logging.error(response.json())
        raise req_err
    return response.json()

def extract_response_data(response_json: str, call_type: str, cols_to_keep_: list[str]) -> list[dict]:
    """
    Takes in the bare respone json, extracts the list of data records,
    slims down by keeping only certain data columns.

    :call_type: type of data to be extracted, e.g. 'transactions'.

    Returns: list that may be directly appended to a df.
    """
    # Get the data from the response json
    data = response_json[call_type]
    # Now use list and dict comprehensions together to keep only wanted columns
    data = [{key: value for key, value in d.items() if key in cols_to_keep_} for d in data]
    # Return the data in sorted format
    return sorted(data, key=lambda x: x['created'])

def main():
    df_transactions = pd.read_csv(PATH_TRANSACTIONS).set_index('transaction_id')
    # Start from the final transaction for which we have data already
    dt_start = df_transactions['tr_datetime'].max()
    id_start = df_transactions[df_transactions['tr_datetime']==dt_start].index[0]

    df_new_transactions = pd.DataFrame()
    cols_to_keep = [
        'id',
        'amount',
        'categories',
        'category',
        'created',
        'currency',
        'description',
        'fees'
    ]
    trans_not_retrieved = True
    while trans_not_retrieved:
        # Retrieve from the endpoint
        transactions = call_endpoint(id_start, CREDS)

        trans_sorted = extract_response_data(transactions, 'transactions', cols_to_keep)
        # If no data was retrieved then we're finished; break loop
        if len(trans_sorted) == 0:
            break
        else:
            # Retrieve the id from final entry
            id_final = trans_sorted[-1]['id']
        
        # If final transaction retrieved is the same as the starting one from the call, 
        # then we're finished - break loop
        if id_start == id_final:
            break
        
        # If loop continues, append to df for later saving
        df_concat = pd.DataFrame(trans_sorted)
        df_new_transactions = pd.concat([df_new_transactions, df_concat], ignore_index=True)

        # Reassign id for next page of transactions
        id_start = id_final

    # Ensure we've got everything in the right format
    df_new_transactions = format_new_transactions(df_new_transactions)
    df_transactions = pd.concat([df_transactions.reset_index(), df_new_transactions], ignore_index=True)
    df_transactions = format_transactions(df_transactions)
    df_transactions.to_csv(PATH_TRANSACTIONS, index=False)


if __name__ == '__main__':
    main()