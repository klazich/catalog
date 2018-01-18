import flask
from flask import flash, redirect, render_template, request, url_for, Blueprint

from catalog.database import session
from catalog.models import User
from catalog.views.helpers import get_user_by, get_oauth2_session, clear_user, login_required
from config import GoogleAuthConfig, FacebookAuthConfig

auth = Blueprint('auth', __name__)


@auth.route('/auth/login', methods=['GET'])
def login():
    flask.session['redirect_back'] = request.referrer or url_for('base.index')
    return render_template('login.html')


@auth.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    # clear user data from session and flag as logged out
    clear_user()
    flask.session['logged_in'] = False

    flash('logout successful', 'info')
    return redirect(request.referrer or url_for('base.index'))


@auth.route('/auth/<provider>')
def oauth2_authorize(provider):
    # get config object for OAuth2 session
    config = {'google': GoogleAuthConfig, 'facebook': FacebookAuthConfig}[provider]
    oauth2_session = get_oauth2_session(config)

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


@auth.route('/auth/callback')
def oauth2_callback():
    # get config object for OAuth2 session
    config = {'google': GoogleAuthConfig, 'facebook': FacebookAuthConfig}[flask.session['provider']]

    # check for state mismatch
    if request.args.get('state') != flask.session['state']:
        clear_user()
        flash('Authentication failed: request/session state mismatch', 'error')
        return redirect(url_for('auth.login'))

    oauth2_session = get_oauth2_session(config, state=request.args.get('state'))

    token = oauth2_session.fetch_token(
        token_url=config.TOKEN_URL,
        client_secret=config.CLIENT_SECRET,
        authorization_response=request.url)

    # grab user info from OAuth2 session
    user_data = oauth2_session.get(config.USER_INFO).json()
    # get the user from database or create if none
    db_user = get_user_by.name(user_data['name']) or get_user_by.email(user_data['email'])
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
