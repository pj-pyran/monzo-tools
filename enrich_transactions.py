from creds import get_creds, refresh_token
from datetime import datetime
import logging
import pandas as pd

PATH_TRANSACTIONS = 'data/transactions_all.csv'
PATH_SAVE_TRANSACTIONS = 'data/transactions_enriched.csv'

def main():
       df_transactions = pd.read_csv(PATH_TRANSACTIONS)
       # Dropping cols should maybe go in format_transactions finally but for now keep here
       cols_to_drop = ['date', 'time', 'type', 'emoji', 'category',
              # 'Local amount', 'Local currency',
              'currency',
              'notes_and_tags', 'address', 'receipt',
              'category_split']
       df_transactions = df_transactions.drop(cols_to_drop, axis=1)
       # Add balance column
       df_transactions['balance'] = df_transactions['amount'].cumsum()

       df_transactions.to_csv(PATH_SAVE_TRANSACTIONS, index=False)

if __name__ == '__main__':
       main()
