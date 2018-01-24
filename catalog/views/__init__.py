from functools import wraps

import flask
from flask import flash, redirect, request, url_for
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix


def get_oauth2_session(config, state=None, token=None):
    """Creates a OAuth2 session from config specs."""
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
    """A route decorator for views requiring a logged in user."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in flask.session or not flask.session['logged_in']:
            flash('login required @ {}'.format(request.path), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
