import flask
from flask import render_template, request, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError

from catalog.views.create import create
from catalog.forms import CreateItemForm
from catalog.database import Session
from catalog.models import Category, Item
from catalog.views.helpers import get_item_by, get_category_by, get_user_by


@create.route('/catalog/new', methods=['GET', 'POST'])
def create_item():
    if not flask.session['logged_in'] or 'user' not in flask.session:
        flash('Must be logged in to create a new item', 'warning')
        return redirect(url_for('views.index'))

    categories = Session.query(Category).all()

    form = CreateItemForm(request.form)
    form.category.choices = [(c.name, c.name) for c in categories]

    if request.method == 'POST':
        new_category = False
        if form.new_category:
            category_name = (form.new_category.data or form.category.data).lower()
            category = get_category_by.name(category_name)
            if not category:
                category = Category(category_name)
                new_category = True

        else:
            category = get_category_by.name(form.category.data)

        item = Item(
            name=form.name.data.lower(),
            description=form.description.data,
            user=get_user_by.id(flask.session['user']['db_id']),
            category=category)

        Session.add(item)
        try:
            Session.commit()
        except IntegrityError:
            Session.rollback()
            flash('database error: item already exists', 'error')
            return redirect(request.referrer)

        if new_category:
            flash('created new category: "{}"'.format(category.name), 'info')
        flash('created new item: "{}" in category "{}"'.format(item.name, item.category.name), 'info')

        return redirect(url_for('views.read_item', category_slug=category.slug, item_slug=item.slug))

    return render_template('create_item.html', form=form)


@create.route('/catalog/<string:category_slug>/<string:item_slug>/update', methods=['GET', 'POST'])
def update_item(category_slug, item_slug):
    if not flask.session['logged_in']:
        flash('Must be logged in to edit your item', 'warning')
        return redirect(url_for('views.index'))

    category = get_category_by.slug(category_slug)
    item = get_item_by.slug(item_slug)

    if item.user.id != flask.session['user']['db_id']:
        flash('Must be creator of item to edit', 'warning')
        return redirect(url_for('views.index'))

    form = CreateItemForm(
        new_category=category.name,
        name=item.name,
        description=item.description)

    return render_template('update_item.html', form=form)
