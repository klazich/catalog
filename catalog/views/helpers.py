from collections import namedtuple
from functools import wraps

import flask
from flask import g, request, redirect, url_for, flash
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from oauthlib.oauth2.rfc6749.errors import MismatchingStateError

from catalog.database import Session
from catalog.models import Item, Category, User

# general database helpers

Get = namedtuple('Get', ['name', 'slug', 'id', 'email'])


def _gets(model):
    return Get(
        name=lambda name: Session.query(model).filter(model.name == name).one_or_none(),
        slug=lambda slug: Session.query(model).filter(model.slug == slug).one_or_none(),
        id=lambda id: Session.query(model).filter(model.id == id).one_or_none(),
        email=lambda email: Session.query(model).filter(model.email == email).one_or_none())


get_item_by = _gets(Item)
get_category_by = _gets(Category)
get_user_by = _gets(User)


# auth helpers

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


def clear_user():
    for v in ['provider', 'state', 'user', 'logged_in']:
        if v in flask.session:
            del flask.session[v]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in flask.session:
            flash('login required at {}'.format(request.path), 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function
