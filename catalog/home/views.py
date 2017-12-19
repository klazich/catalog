from flask import render_template, redirect, url_for
# from flask_login import login_required

from . import home
from .. import db_session
from ..models import Category, Item
from .. import helpers as h


@home.route('/')
@home.route('/catalog/')
def show_categories():
    """
    Render the homepage template on the / route
    :return: template
    """
    categories = db_session.query(Category).all()
    return render_template('show_categories.html', categories=categories, title="Welcome")


@home.route('/catalog/<category_slug>/')
def show_category(category_slug):
    """
    Render category template
    :param category_slug: string
    :return: template
    """
    category = h.get_category_by_slug(category_slug)
    return render_template('show_category.html', category=category, title=category.name)


@home.route('/catalog/<category_slug>/<item_slug>')
def show_item(category_slug, item_slug):
    """
    Render item template
    :param category_slug: string
    :param item_slug: string
    :return: template
    """
    category = h.get_category_by_slug(category_slug)
    item = h.get_item_by_slug(item_slug)
    return render_template('show_item.html', category=category, item=item, title=item.title)
