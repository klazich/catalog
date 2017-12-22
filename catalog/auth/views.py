from flask import flash, redirect, render_template, url_for, session
# from flask_login import login_required, login_user, logout_user

from . import auth
# from forms import LoginForm, RegistrationForm
from catalog import db_session
from catalog.models import User
from catalog.auth.google import GoogleAuth


@auth.route('/authorize/<provider>')
def oath2_authorize(provider):
    if provider not in ['google', 'facebook']:
        return
    if provider == 'google':
        session['state'] = GoogleAuth.state
    if provider == 'facebook':
        pass





@auth.route('/callback/<provider>')
def oath2_callback(provider):
    pass


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add a user to the database through the todo: registration form
    """
    pass


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log a user in through the todo: login form
    """
    pass


@auth.route('/logout')
# @login_required
def logout():
    """
    Handle requests to the /logout route
    Log a user out through the todo: logout link
    """
    pass
