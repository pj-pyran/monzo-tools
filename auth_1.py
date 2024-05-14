from creds import get_creds
from monzo.authentication import Authentication
# from monzo.exceptions import MonzoAuthenticationError, MonzoServerError
import json
from urllib.parse import parse_qs, urlparse

PATH_CREDS = 'creds.json'
creds = get_creds()

# auth_url will contain state and code parameters
# We'll parse them from the url
auth_url = creds['authorisation_url']
parsed_url = urlparse(auth_url)
query_params = parse_qs(parsed_url.query)
# state matches with the same param from the original request.
# Used to prove the requests are matching
state = query_params['state'][0]
# auth code that we will use to obtain an access token
code = query_params['code'][0]

# We can now initiate monzo session object
monzo = Authentication(client_id=creds['client_id'], client_secret=creds['client_secret'], redirect_url=creds['redirect_url'])
monzo.authenticate(authorization_token=code, state_token=state)

# Refresh creds file
creds['access_token'] = monzo.access_token
creds['token_expiry'] = monzo.access_token_expiry
creds['refresh_token'] = monzo.refresh_token
with open(PATH_CREDS, 'w') as json_file:
    json.dump(creds, json_file, indent=4)

print('>> Now authorise access in the Monzo app')