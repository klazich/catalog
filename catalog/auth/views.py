import json

import flask
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from catalog.auth import auth
# from forms import LoginForm, RegistrationForm
from config import GoogleAuthConfig, FacebookAuthConfig


def redirect_url(default='home.index'):
    return request.args.get('next') \
           or request.referrer \
           or url_for(default)


def get_oauth2_session(config, state=None, token=None):
    session = OAuth2Session(
        client_id=config.CLIENT_ID,
        scope=config.SCOPE,
        redirect_uri=config.REDIRECT_URI,
        state=state,
        token=token)
    if config.PROVIDER == 'facebook':
        return facebook_compliance_fix(session)
    return session


@auth.route('/authorize/<provider>')
def oauth2_authorize(provider):
    config = {'google': GoogleAuthConfig, 'facebook': FacebookAuthConfig}[provider]

    oauth2_session = get_oauth2_session(config)

    authorization_url, state = oauth2_session.authorization_url(
        config.AUTHORIZATION_BASE_URL,
        access_type='offline',
        prompt='select_account')

    flask.session['oauth_state'] = state
    flask.session['redirected_from'] = redirect_url()

    return redirect(authorization_url)


@auth.route('/callback/<provider>')
def oauth2_callback(provider):
    config = {'google': GoogleAuthConfig, 'facebook': FacebookAuthConfig}[provider]

    oauth2_session = get_oauth2_session(config, state=flask.session['oauth_state'])

    token = oauth2_session.fetch_token(
        token_url=config.TOKEN_URL,
        client_secret=config.CLIENT_SECRET,
        authorization_response=request.url)

    flask.session['oauth_token'] = token

    flash('You were successfully logged in.')

    r = oauth2_session.get(config.USER_INFO)
    # data = json.loads(r)
    # print(data)

    print(type(r))
    print(r)
    print(r.content)
    print(r.text)
    print(token)

    back = flask.session['redirected_from']
    return redirect(back)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log a user in through the todo: login form
    """
    return render_template('auth/login.html', title='Login')


@auth.route('/logout')
# @login_required
def logout():
    """
    Handle requests to the /logout route
    Log a user out through the todo: logout link
    """
    pass
