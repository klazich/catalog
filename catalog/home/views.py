from flask import render_template, redirect, url_for
# from flask_login import login_required

from . import home
from catalog.database import Session
from catalog.models import Category, Item
from catalog import helpers as h

"""
URL 	        Method 	Description
/users/ 	    GET 	Gives a list of all users
/users/ 	    POST 	Creates a new user
/users/<id> 	GET 	Shows a single user
/users/<id> 	PUT 	Updates a single user
/users/<id> 	DELETE 	Deletes a single user
"""


@home.route('/')
@home.route('/catalog/')
def show_categories():
    """
    Render the homepage template on the / route
    :return: template
    """
    return render_template('home/index.html', title="Home")


@home.route('/catalog/<category_slug>/')
def show_category(category_slug):
    """
    Render category template
    :param category_slug: string
    :return: template
    """
    category = h.get_category_by_slug(category_slug)
    return render_template('home/show_category.html', category=category, title=category.name)


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
    return render_template('home/show_item.html', category=category, item=item, title=item.name)
