import flask
from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

from catalog.auth import auth
# from forms import LoginForm, RegistrationForm
from catalog.auth.oauth2 import GoogleOAuth2, FacebookOAuth2
import catalog.helpers as h


@auth.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if provider not in ['google', 'facebook']:
        return

    if provider == 'google':
        google = GoogleOAuth2().session

        authorization_url, state = google.authorization_url(
            GoogleOAuth2.AUTHORIZATION_BASE_URL,
            access_type='offline',
            prompt='select_account')

        flask.session['oauth_state'] = state
        flask.session['redirected_from'] = h.redirect_url()

        return redirect(authorization_url)

    if provider == 'facebook':
        facebook = FacebookOAuth2().session
        authorization_url, state = facebook.authorization_url(
            FacebookOAuth2.AUTHORIZATION_BASE_URL)

        flask.session['oauth_state'] = state

        return redirect(authorization_url)


@auth.route('/callback/<provider>')
def oauth2_callback(provider):
    if provider == 'google':
        state = flask.session['oauth_state']
        redirect_back = flask.session['redirected_from']
        flash('You were successfully logged in.')
        flash('You were successfully logged in.')
        flash('You were successfully logged in.')
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
