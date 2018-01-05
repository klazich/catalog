import flask
from flask import render_template, request, redirect, flash, url_for

from catalog.create import create
from catalog.create.forms import CreateItemForm
from catalog.database import Session
from catalog.models import Category, Item, User


def get_category_by_slug(category_slug):
    return Session.query(Category).filter(Category.slug == category_slug).one_or_none()


def get_category_by_name(category_name):
    return Session.query(Category).filter(Category.name == category_name).one_or_none()


def get_item_by_slug(item_slug):
    return Session.query(Item).filter(Item.slug == item_slug).one_or_none()


def get_user_by_id(user_id):
    return Session.query(User).filter(User.id == user_id).one_or_none()


@create.route('/catalog/new', methods=['GET', 'POST'])
def create_item():
    if not flask.session['logged_in'] and flask.session['user']:
        flash('Must be logged in to create a new item', 'warning')
        return redirect(url_for('read.index'))

    categories = Session.query(Category).all()

    form = CreateItemForm(request.form)
    form.category.choices = [(c.name, c.name) for c in categories]

    if request.method == 'POST':
        if form.new_category:
            category_name = (form.new_category.data or form.category.data).title()
            category = get_category_by_name(category_name)
            if not category:
                category = Category(category_name)
                flash('"{}" category created'.format(category.name), 'info')
        else:
            category = get_category_by_name(form.category.data)

        item = Item(
            name=form.name.data,
            description=form.description.data,
            user=get_user_by_id(flask.session['user']['db_id']),
            category=category)

        Session.add(item)
        Session.commit()

        flash('New item "{}" in category "{}" created'.format(item.name, item.category.name), 'info')

        return redirect(url_for('read.read_item', category_slug=category.slug, item_slug=item.slug))

    return render_template('create_item.html', form=form)


@create.route('/catalog/<string:category_slug>/<string:item_slug>/edit', methods=['GET', 'POST'])
def update_item(category_slug, item_slug):
    if not flask.session['logged_in']:
        flash('Must be logged in to edit your item', 'warning')
        return redirect(url_for('read.index'))

    category = get_category_by_slug(category_slug)
    item = get_item_by_slug(item_slug)

    if item.user.id != flask.session['user']['db_id']:
        flash('Must be creator of item to edit', 'warning')
        return redirect(url_for('read.index'))

    form = CreateItemForm(
        new_category=category.name,
        name=item.name,
        description=item.description)

    return render_template('update_item.html', form=form)
