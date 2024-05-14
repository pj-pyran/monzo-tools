"""
I've created tableau reporting which will be uploaded publically to demonstrate the reporting
capabilities. However of course I don't want to show my financial data publically.
Hence this script will create an anonymised dataset, based on the real data but with altered
transaction quantities and names. This will then be used by Tableau as the data source for
public display.
"""
import pandas as pd
import logging
import numpy as np

PATH_TRANSACTIONS = 'data/transactions_enriched.csv'
df_transactions = pd.read_csv(PATH_TRANSACTIONS)

# 'transaction_id', 'name', 'amount', 'local_amount', 'local_currency',
#    'description', 'money_out', 'money_in', 'tr_datetime', 'balance'

#  --- Obfuscations to apply:
# [description]: if name.isnull then assign name as description. else set to null (for now).
#              Investigate real data in tableau for whether it's any use
# [transaction_id]: hash
# [name]: business or personal name
# [tr_datetime]: add random duration between -10hr and +10hr
# 
# [amount]: apply randomisation. Multiply by factor between 0.8 and 1.25
# [local_amount]: drop this column
# [money_out]: amount if amount > 0
# [money_in]: amount if amount <= 0
# [balance]: re-calculate cumsum given new amounts

def randomise_col(col: pd.Series) -> pd.Series:
    """
    Semi-randomise the values in a numerical column using factor between min and max
    Parameters:
        col: The numerical column to randomise.
    
    Returns the randomised column.
    """
    # Min and max are reciprocals - should ensure a fairly even distrib between increase and decrease
    min_factor = 0.8
    max_factor = 1/min_factor
    # For each transaction generate a random scaling factor between min_factor and max_factor
    random_factors = np.random.uniform(min_factor, max_factor, size=len(col))
    # Multiply each value in the column by the corresponding random factor
    return col * random_factors
    

df_transactions['amount_rnd'] = randomise_col(df_transactions['amount'])
df_transactions['money_in_rnd'] = np.where(df_transactions['amount_rnd']>=0, df_transactions['amount_rnd'], np.nan)
df_transactions['money_out_rnd'] = np.where(df_transactions['amount_rnd']<0, df_transactions['amount_rnd'], np.nan)
df_transactions['balance_rnd'] = df_transactions['amount_rnd'].cumsum()

df_transactions.to_csv('data/transactions_obfsc_test.csv', index=False)