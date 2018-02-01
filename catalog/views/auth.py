import flask
from flask import flash, redirect, render_template, request, url_for, Blueprint

from ..database import session
from ..models import User
from . import get_oauth2_session, login_required
from config import GoogleAuthConfig, FacebookAuthConfig

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['GET'])
def login():
    """
    Login page

    :return: rendering of the login.html template
    """
    # set redirect to flask session
    # used to redirect after authentication finishes
    flask.session['redirect_back'] = request.referrer or url_for(
        'catalog.index')
    return render_template('login.html')


@auth_bp.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    """
    Clears user info from session and returns users to request referrer.

    :return: redirect to previous page
    """
    # clear user data from session and flag as logged out
    for x in ['provider', 'state', 'user']:
        if x in flask.session:
            del flask.session[x]
    flask.session['logged_in'] = False

    flash('logout successful', 'info')
    return redirect(request.referrer or url_for('catalog.index'))


@auth_bp.route('/auth/<provider>')
def oauth2_authorize(provider):
    """
    Handles OAuth2 initiating with Google/Facebook. Saves state to session to check
    against at callback.

    :param provider: google or facebook, button pressed from auth/login
    :type provider: str
    :return: a redirect to the authorization url from oauth2_session.
    """
    # get config object for OAuth2 session
    config = {'google': GoogleAuthConfig,
              'facebook': FacebookAuthConfig}[provider]
    oauth2_session = get_oauth2_session(
        config)  # see: catalog/views/__init__.py

    # get the authorization url and state
    authorization_url, state = oauth2_session.authorization_url(
        config.AUTHORIZATION_BASE_URL,
        access_type='offline',
        prompt='select_account')

    # set state and provider to flask session
    flask.session['state'] = state
    flask.session['provider'] = provider

    # redirect to authorization url to authenticate
    return redirect(authorization_url)


@auth_bp.route('/auth/callback')
def oauth2_callback():
    """
    Endpoint for OAuth2 provider callback after redirect to authorization_url in function
    oauth2_authorize. Confirms state and fetches token with authenticated credentials.
    Gets user from database or create new.

    :return: a redirect to the request referrer at login.html
    """
    # get config object for OAuth2 session
    config = {'google': GoogleAuthConfig, 'facebook': FacebookAuthConfig}[
        flask.session['provider']]

    # check for state mismatch
    if request.args.get('state') != flask.session['state']:
        for x in ['provider', 'state', 'user']:
            if x in flask.session:
                del flask.session[x]
        flask.session['logged_in'] = False
        flash('Authentication failed: request/session state mismatch', 'error')
        return redirect(url_for('auth.login'))

    oauth2_session = get_oauth2_session(
        config, state=request.args.get('state'))  # get state from flask session

    token = oauth2_session.fetch_token(
        token_url=config.TOKEN_URL,
        client_secret=config.CLIENT_SECRET,
        authorization_response=request.url)

    # grab user info from OAuth2 session
    user_data = oauth2_session.get(config.USER_INFO).json()
    # get the user from database or create if none
    db_user = session.query(User).filter(
        User.email == user_data['email']).one_or_none()
    if not db_user:
        db_user = User(user_data['name'], user_data['email'])
        session.add(db_user)
        session.commit()

    user_data['db_id'] = db_user.id
    user_data['token'] = token

    # save user data to flask session and flag as logged in
    flask.session['user'] = user_data
    flask.session['logged_in'] = True

    flash('login successful', 'info')

    # return user to page before login
    redirect_back = flask.session['redirect_back']
    del flask.session['redirect_back']

    return redirect(redirect_back)
