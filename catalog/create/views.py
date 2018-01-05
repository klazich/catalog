import flask
from flask import render_template, request, redirect, flash, url_for

from catalog.create import create
from catalog.create.forms import CreateCategoryForm, CreateItemForm
from catalog.database import Session
from catalog.models import Category, Item, User


def get_category_by_slug(category_slug):
    return Session.query(Category).filter(Category.slug == category_slug).one_or_none()


def get_user_by_name(user_name):
    return Session.query(User).filter(User.name == user_name).one_or_none()


@create.route('/catalog/new', methods=['GET', 'POST'])
def create_category():
    if not flask.session['logged_in']:
        flash('Must be logged in to create a new item.', 'warning')
        return redirect(url_for('read.index'))

    form = CreateCategoryForm(request.form)
    categories = Session.query(Category).all()

    if request.method == 'POST':
        category = Category(form.new_category.data or form.categories.data)
        if category.name not in map(lambda x: x.name, categories):
            Session.add(category)
            Session.commit()
        flash('Category selected', 'info')
        return redirect(url_for('create.create_item', category_slug=category.slug))
    elif request.method == 'GET':
        return render_template('create_category.html', form=form, categories=categories)


@create.route('/catalog/<string:category_slug>/new', methods=['GET', 'POST'])
def create_item(category_slug):
    if not flask.session['logged_in']:
        flash('Must be logged in to create a new item.', 'warning')
        return redirect(url_for('read.index'))

    category = get_category_by_slug(category_slug)
    form = CreateItemForm(request.form)

    if request.method == 'POST' and form.validate():
        item = Item(
            name=form.name.data,
            description=form.description.data,
            user=get_user_by_name(flask.session['user']['name']),
            category=category)
        Session.add(item)
        Session.commit()
        flash('New item created', 'info')

        return redirect(url_for('read.read_item', category_slug=category.slug, item_slug=item.slug))
    elif request.method == 'GET':
        return render_template('create_item.html', form=form, category=category)
