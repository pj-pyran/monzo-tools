[Knowledge assumed: intermediate]

This package is intended for those with Monzo bank accounts, enabling them to analyse their financial history and understand their spending habits. I built it for my own use.

The **goal** (in-progress) is to have Tableau reporting running on top.


# Get started
## Prerequisites
1. **Monzo standard account** - free and easy to sign up to. If you don't have one already, this package isn't really for you.
2. **Monzo dev account** - you can make one in the [Monzo dev portal](https://developers.monzo.com).
3. **Monzo API client** - once you have the above you can set this up in the portal. Again, easy to make and Monzo provide docs.

## Process
There is a 1-time auth process to get your first access and refresh tokens. Once done, you shouldn't have to run this again - as long as tokens are refreshed continually. I myself do this via a cron job using the `creds.refresh_token()` function provided.
Once you have prerequisites satisfied and have cloned this repo, fill in your `creds.json` file:
1. Enter your `client_id`, `owner_id`, `client_secret` from your Monzo client.
2. Leave `redirect_url` as-is. You can change if you like but it's not crucial. This will form the domain and location for your authorisation URL (see steps below).

Now follow the 2-step process to get your access token:
1. First run `auth_0.py`; this will output a link - Ctrl+click it.
2. Enter your email address. Then follow the magic link emailed to you.
3. Copy the URL from the browser URL bar and paste into your `creds.json` as `authorisation_url`.
4. Run `auth_1.py`
5. Approve the request in your Monzo app.
6. Your token in `creds.json` will now have been refreshed and you may run scripts at will. Token expires after around 30 hours.

# How it works
To understand this package, start from `cron_orchestrate.py`. This orchestrates the whole data refresh, transformation and enrichment. I have it run daily (09:00) in order to keep data fresh and well-formatted to run analysis on demand.

In Tableau Public I am creating dashboards and tools to provide high-quality reports on the data retrieved by this package. This explains the purpose of `obfuscate_transactions.py`: for obvious reasons I don't want to upload my own financial data to Tableau Public. This file takes my private data and applies randomisation - I then use that data in the public-facing Tableau report.

# Future iteration improvements
In vague order of priority:

- [ ] Migrating data to MySQL rather than CSVs
- [ ] Better security for credentials (encryption)
- [ ] Integrating other next-gen banking services (Starling, Revolut)