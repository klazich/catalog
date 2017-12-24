from flask import flash, redirect, render_template, url_for
from flask import session as flask_session
# from flask_login import login_required, login_user, logout_user

from . import auth
# from forms import LoginForm, RegistrationForm
from catalog.database import Session
from catalog.models import User
from catalog.auth.google import GoogleOAuth2
from catalog.auth.facebook import FacebookOAuth2


@auth.route('/authorize/<provider>')
def oath2_authorize(provider):
    if provider not in ['google', 'facebook']:
        return

    if provider == 'google':
        google = GoogleOAuth2().session

        authorization_url, state = google.authorization_url(
            GoogleOAuth2.AUTHORIZATION_BASE_URL,
            access_type='offline',
            prompt='select_account')

        flask_session['oauth_state'] = state

        return redirect(authorization_url)

    if provider == 'facebook':
        facebook = FacebookOAuth2().session
        authorization_url, state = facebook.authorization_url(
            FacebookOAuth2.AUTHORIZATION_BASE_URL)

        flask_session['oauth_state'] = state

        return redirect(authorization_url)


@auth.route('/callback/<provider>')
def oath2_callback(provider):
    pass


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
