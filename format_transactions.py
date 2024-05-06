import pandas as pd
import numpy as np


def format_transactions(df_staging: pd.DataFrame) -> pd.DataFrame: #path: str = 'data/transactions_all.csv'):
    """Function to update the transactions csv so that 
    it is in the correct state before carrying out any edits or analysis
    
    Returns dataframe of correctly-formatted transactions."""
    # df_staging = pd.read_csv(path)
    print(f'a index: {len(df_staging.index)}')
    df_staging.columns = df_staging.columns.str.lower().str.replace(' ', '_').str.replace('#', '')
    # Silly mixed-case columns
    cols_to_lower = ['type','name','category','currency','local_currency','notes_and_tags','address','description']
    for col in cols_to_lower:
        df_staging[col] = df_staging[col].str.lower()
    # Add or update datetime column
    if 'tr_datetime' not in df_staging.columns:
        df_staging['tr_datetime'] = pd.to_datetime(df_staging['date'] + ' ' + df_staging['time'], format='%d/%m/%Y %H:%M:%S')
    else:
        df_staging['tr_datetime'] = df_staging['tr_datetime'].fillna(pd.to_datetime(df_staging['date'] + ' ' + df_staging['time'], format='%d/%m/%Y %H:%M:%S'))
    # Make sure they're in time order
    df_staging = df_staging.sort_values(by='tr_datetime', ascending=True)
    # De-dupe on transaction_id just in case we've erroneously duped any
    df_staging = df_staging.drop_duplicates(subset=['transaction_id'])
    return df_staging

def format_new_transactions(df_: pd.DataFrame) -> pd.DataFrame:
    """
    Transactions data retrieved from API needs some wrangling
    before it can be appended to data file.
    Convert pennies amounts to pounds, change column names
    
    Return df in matching format to data at PATH_TRANSACTIONS
    """
    # ['amount', 'categories', 'category', 'created', 'currency',
    #    'description', 'fees', 'id']
    # df_transactions.columns
    # ['transaction_id', 'date', 'time', 'type', 'name', 'emoji', 'category',
    #     'amount', 'currency', 'local_amount', 'local_currency',
    #     'notes_and_tags', 'address', 'receipt', 'description', 'category_split',
    #     'money_out', 'money_in', 'tr_datetime']
    cols_rename = {
        'id' : 'transaction_id',
        'created' : 'tr_datetime'
    }
    cols_drop = ['categories', 'fees']
    df = df_.rename(cols_rename, axis=1).drop(cols_drop, axis=1)
    df['amount'] = df['amount']/100
    # Make and populate money in/out columns
    df['money_in'] = np.where(df['amount']>=0, df['amount'], np.nan)
    df['money_out'] = np.where(df['amount']<0, df['amount'], np.nan)
    return df