from flask import flash, redirect, render_template, url_for
# from flask_login import login_required, login_user, logout_user

from . import auth
# from forms import LoginForm, RegistrationForm
from .. import db_session
from ..models import User


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
