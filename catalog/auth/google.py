from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

from config import GoogleAuth

google = OAuth2Session(
    GoogleAuth.CLIENT_ID,
    scope=GoogleAuth.SCOPE,
    redirect_uri=GoogleAuth.REDIRECT_URI)

authorization_url, state = google.authorization_url(
    GoogleAuth.AUTH_URI,
    access_type='offline',
    prompt='select_account')

setattr(GoogleAuth, 'state', lambda: state)
