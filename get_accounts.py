from creds import get_creds
from datetime import datetime
from monzo.authentication import Authentication
from monzo.endpoints.account import Account
# from monzo.exceptions import MonzoError
import pytz

creds = get_creds()

# Set up monzo session
monzo = Authentication(
    client_id=creds['Client ID'],
    client_secret=creds['Client Secret'],
    redirect_url=creds['redirect_url'],
    access_token=creds['access_token'],
    access_token_expiry=creds['token_expiry'],
    refresh_token=creds['refresh_token']
)

accounts = Account.fetch(monzo)
# Convert Unix timestamp to datetime
datetime_object = datetime.fromtimestamp(creds['token_expiry'], tz=pytz.timezone('GMT'))
print(f'Token expires at {datetime_object.strftime("%d-%B-%Y %H:%M:%S")}')