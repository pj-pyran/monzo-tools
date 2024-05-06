from monzo.authentication import Authentication
from creds import creds

creds = creds()

monzo = Authentication(
    client_id=creds['client_id'],
    client_secret=creds['client_secret'],
    redirect_url=creds['redirect_url']
)

# The user should visit this url
print(monzo.authentication_url)