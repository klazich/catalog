import flask
from flask import flash, redirect, render_template, request, url_for

from catalog.database import Session
from catalog.models import User
from catalog.views.auth import auth
from catalog.views.helpers import get_user_by, get_oauth2_session, clear_user, login_required
from config import GoogleAuthConfig, FacebookAuthConfig


@auth.route('/login', methods=['GET'])
def login():
    flask.session['redirect_back'] = request.referrer or url_for('read.index')
    return render_template('login.html')


@auth.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    clear_user()
    flask.session['logged_in'] = False

    flash('logout successful', 'info')
    return redirect(request.referrer or url_for('read.index'))


@auth.route('/auth/<provider>')
def oauth2_authorize(provider):
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
    if request.args.get('state') != flask.session['state']:
        clear_user()
        flash('Authentication failed: request/session state mismatch', 'error')
        return redirect(url_for('auth.login'))

    oauth2_session = get_oauth2_session(config, state=request.args.get('state'))

    token = oauth2_session.fetch_token(
        token_url=config.TOKEN_URL,
        client_secret=config.CLIENT_SECRET,
        authorization_response=request.url)

    user = oauth2_session.get(config.USER_INFO).json()
    db_user = get_user_by.name(user['name']) or get_user_by.email(user['email'])
    if not db_user:
        db_user = User(user['name'], user['email'])
        Session.add(db_user)
        Session.commit()

    user['db_id'] = db_user.id
    user['token'] = token

    flask.session['user'] = user
    flask.session['logged_in'] = True

    flash('login successful', 'info')

    redirect_back = flask.session['redirect_back']
    del flask.session['redirect_back']

    return redirect(redirect_back)
