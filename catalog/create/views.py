import flask
from flask import render_template, request, redirect, flash, url_for

from catalog.create import create
from catalog.create.forms import CreateItemForm
from catalog.database import Session
from catalog.models import Category, Item, User


def get_category_by_slug(category_slug):
    return Session.query(Category).filter(Category.slug == category_slug).one_or_none()


@create.route('/catalog/new', methods=['GET', 'POST'])
@create.route('/catalog/<string:category_slug>/new', methods=['GET', 'POST'])
def create_item(category_slug=None):
    if not flask.session['logged_in']:
        flash('Must be logged in to create a new item.', 'warning')
        return redirect(url_for('read.index'))

    form = CreateItemForm()

    if request.method == 'POST':
        return 'Form posted.'

    elif request.method == 'GET':
        category = get_category_by_slug(category_slug)
        return render_template('create_item.html', form=form, category=category)
