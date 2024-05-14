import pandas as pd
import numpy as np

def elim_ms(str_):
        """Pandas and Monzo doing complete bs on datetime formatting.
        Hence we need to manually fix the ms_ part of 'YYYY-MM-DD HH:mm:ss.ms_'"""
        return str_ if len(str_) == 19 else str_[0:19]

def format_transactions(df_staging: pd.DataFrame) -> pd.DataFrame: #path: str = 'data/transactions_all.csv'):
    """Function to update the transactions csv so that 
    it is in the correct state before carrying out any edits or analysis
    
    Returns dataframe of correctly-formatted transactions.
    """
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
    
    df_staging['tr_datetime'] = df_staging['tr_datetime'].astype(str)
    replacements = {'T' : ' ', '000+00:00' : ''}
    df_staging['tr_datetime'] = df_staging['tr_datetime'].str.strip('Z').replace(replacements, regex=True).apply(elim_ms)
    df_staging['tr_datetime'] = pd.to_datetime(df_staging['tr_datetime'])

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
    cols_rename = {
        'id' : 'transaction_id',
        'created' : 'tr_datetime'
    }
    cols_drop = ['categories', 'fees']
    df_ = df_.rename(cols_rename, axis=1).drop(cols_drop, axis=1)
    df_['amount'] = df_['amount']/100
    # df_['tr_datetime'] = pd.to_datetime(df_['tr_datetime'], format='ISO8601')
    df_['tr_datetime'] = pd.to_datetime(df_['tr_datetime'], format='ISO8601')
    # pd.to_datetime(df['tr_datetime'].dt.strftime("%Y-%m-%d %H:%M:%S"))
    # Make and populate money in/out columns
    df_['money_in'] = np.where(df_['amount']>=0, df_['amount'], np.nan)
    df_['money_out'] = np.where(df_['amount']<0, df_['amount'], np.nan)
    return df_
