from flask import render_template, redirect, url_for, session, flash, request
# from flask_login import login_required

from . import read
from catalog.database import Session
from catalog.models import Category, Item


def get_category_by_slug(category_slug):
    return Session.query(Category).filter(Category.slug == category_slug).one_or_none()


def get_item_by_slug(item_slug):
    return Session.query(Item).filter(Item.slug == item_slug).one_or_none()


@read.route('/')
@read.route('/catalog/')
def index():
    return render_template('read_all_categories.html', title="Home")


@read.route('/catalog/<category_slug>/')
def read_category(category_slug):
    category = get_category_by_slug(category_slug)
    return render_template('read_category.html', category=category, title=category.name)


@read.route('/catalog/<category_slug>/<item_slug>')
def read_item(category_slug, item_slug):
    category = get_category_by_slug(category_slug)
    item = get_item_by_slug(item_slug)
    return render_template('read_item.html', category=category, item=item, title=item.name)
