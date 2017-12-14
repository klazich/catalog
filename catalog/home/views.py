from flask import render_template
# from flask_login import login_required

from . import home
from .. import db_session
from ..models import Category, Item
from ..helpers import latest


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    categories = db_session.query(Category).all()
    return render_template('index.html', categories=categories, title="Welcome", latest_items=latest(40))
