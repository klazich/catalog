from functools import wraps

import flask
from flask import flash, redirect, request, url_for
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from config import GoogleAuthConfig, FacebookAuthConfig, BaseConfig


def get_oauth2_session(config, state=None, token=None):
    """


    :param config: Google or Facebook config object from config.py
    :type config: Union[GoogleAuthConfig, FacebookAuthConfig]
    :param state: the state string
    :type state: str
    :param token: the token object
    :type token: object
    :return: a OAuth2 session initialized with parameters from config
    :rtype: OAuth2Session
    """
    oauth2_session = OAuth2Session(
        client_id=config.CLIENT_ID,
        scope=config.SCOPE,
        redirect_uri=config.REDIRECT_URI,
        state=state,
        token=token)
    if config.PROVIDER == 'facebook':
        return facebook_compliance_fix(oauth2_session)
    return oauth2_session


def login_required(f):
    """
    A route decorator for views requiring a logged in user.

    :return:
    :rtype:
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in flask.session or not flask.session['logged_in']:
            flash('login required @ {}'.format(request.path), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
