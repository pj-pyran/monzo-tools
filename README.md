# Get started
To get started, you need to set up a client yourself in the [Monzo dev portal](https://developers.monzo.com). Then I've set up a 2-stage authentication process:
1. First run `auth_0.py`; this will print a link for you to follow.
2. Enter your email address. Then follow the magic link emailed to you.
3. Copy the redirect URL and paste into your `creds.json` as `"authorisation_url"`.
4. Run `auth_1.py`
5. Approve the request in your Monzo app.
6. Your token in `creds.json` will now have been refreshed and you may run scripts at will. Token expires after around 36 hours.
