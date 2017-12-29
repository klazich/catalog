from time import time

from sqlalchemy.exc import IntegrityError
import requests
import flask
from flask import abort, flash, redirect, render_template, request, url_for
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError

from catalog.auth import auth
from config import GoogleAuthConfig, FacebookAuthConfig
from catalog.database import Session
from catalog.models import User


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


def get_user_by_name(user_name):
    return Session.query(User).filter(User.name == user_name).one_or_none()


def get_user_by_email(user_email):
    return Session.query(User).filter(User.email == user_email).one_or_none()


def create_user(name, email):
    user = User(name, email)
    Session.add(user)
    try:
        Session.commit()
    except IntegrityError:
        Session.rollback()
        return None
    return user


@auth.route('/auth/<provider>')
def oauth2_authorize(provider):
    if not request.args.get('state'):
        flask.session['last'] = request.referrer or url_for('home.index')
    if 'next' in request.args:
        flask.session['next'] = url_for(request.args['next'])
    else:
        flask.session['next'] = flask.session['last']

    config = {'google': GoogleAuthConfig, 'facebook': FacebookAuthConfig}[provider]
    oauth2_session = get_oauth2_session(config)

    authorization_url, state = oauth2_session.authorization_url(
        config.AUTHORIZATION_BASE_URL,
        access_type='offline',
        prompt='select_account')

    flask.session['state'] = state
    flask.session['provider'] = provider

    return redirect(authorization_url)


@auth.route('/auth/callback')
def oauth2_callback():
    config = {'google': GoogleAuthConfig, 'facebook': FacebookAuthConfig}[flask.session['provider']]
    oauth2_session = get_oauth2_session(config, state=flask.session['state'])

    try:
        token = oauth2_session.fetch_token(
            token_url=config.TOKEN_URL,
            client_secret=config.CLIENT_SECRET,
            authorization_response=request.url)
    except MismatchingStateError:
        flash('Could not authenticate!', 'error')
        return redirect(flask.session['last'])

    user = oauth2_session.get(config.USER_INFO).json()

    user['token'] = token
    flask.session['user'] = user

    if not get_user_by_name(user['name']) or get_user_by_email(user['email']):
        create_user(user['name'], user['email'])

    flask.session['logged_in'] = True
    flash('You were successfully logged in.', 'info')
    return redirect(flask.session['next'])


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Login')


@auth.route('/auth/logout')
def logout():
    del flask.session['user']
    flask.session['logged_in'] = False
    flash('You were successfully logged out.', 'info')
    return redirect(flask.session['next'])
