import json
import flask
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix

from catalog.auth import auth
# from forms import LoginForm, RegistrationForm
from config import GoogleAuthConfig, FacebookAuthConfig
import catalog.helpers as h


@auth.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if provider not in ['google', 'facebook']:
        return

    if provider == 'google':
        google = OAuth2Session(
            client_id=GoogleAuthConfig.CLIENT_ID,
            scope=GoogleAuthConfig.SCOPE,
            redirect_uri=GoogleAuthConfig.REDIRECT_URI)

        authorization_url, state = google.authorization_url(
            GoogleAuthConfig.AUTHORIZATION_BASE_URL,
            access_type='offline',
            prompt='select_account')

        flask.session['oauth_state'] = state
        flask.session['redirected_from'] = h.redirect_url()

        return redirect(authorization_url)

    if provider == 'facebook':
        facebook = OAuth2Session(
            client_id=FacebookAuthConfig.CLIENT_ID,
            redirect_uri=FacebookAuthConfig.REDIRECT_URI)
        facebook = facebook_compliance_fix(facebook)

        authorization_url, state = facebook.authorization_url(
            FacebookAuthConfig.AUTHORIZATION_BASE_URL)

        flask.session['oauth_state'] = state
        flask.session['redirected_from'] = h.redirect_url()

        return redirect(authorization_url)


@auth.route('/callback/<provider>')
def oauth2_callback(provider):
    if provider == 'google':
        google = OAuth2Session(
            client_id=GoogleAuthConfig.CLIENT_ID,
            scope=GoogleAuthConfig.SCOPE,
            redirect_uri=GoogleAuthConfig.REDIRECT_URI,
            state=flask.session['oauth_state'])

        token = google.fetch_token(
            token_url=GoogleAuthConfig.TOKEN_URL,
            client_secret=GoogleAuthConfig.CLIENT_SECRET,
            authorization_response=request.url)

        flask.session['oauth_token'] = token

        flash('You were successfully logged in.')

        r = google.get(GoogleAuthConfig.USER_INFO)

        redirect_back = flask.session['redirected_from']
        return redirect(redirect_back)

    if provider == 'facebook':
        facebook = OAuth2Session(
            client_id=FacebookAuthConfig.CLIENT_ID,
            redirect_uri=FacebookAuthConfig.REDIRECT_URI,
            state=flask.session['oauth_state'])
        facebook = facebook_compliance_fix(facebook)

        token = facebook.fetch_token(
            FacebookAuthConfig.TOKEN_URL,
            client_secret=FacebookAuthConfig.CLIENT_SECRET,
            authorization_response=request.url)

        flask.session['oauth_token'] = token

        flash('You were successfully logged in.')

        r = facebook.get(FacebookAuthConfig.USER_INFO)

        redirect_back = flask.session['redirected_from']
        return redirect(redirect_back)


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
