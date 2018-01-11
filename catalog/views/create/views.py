import flask
from flask import render_template, request, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError

from catalog.database import Session
from catalog.forms import ItemForm
from catalog.models import Category, Item
from catalog.views.create import create
from catalog.views.helpers import get_category_by, get_user_by, get_all_categories, login_required


@create.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def create_item():
    categories = get_all_categories()

    form = ItemForm(request.form)
    form.category.choices = [(c.name, c.name) for c in categories]

    if request.method == 'POST' and form.validate():
        if form.new_category:
            category_name = (form.new_category.data or form.category.data).lower()
            category = get_category_by.name(category_name)
            if not category:
                category = Category(category_name)
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

        flash('created new item: {}'.format(item.name, item.category.name), 'info')

        return redirect(url_for('read.read_item', category_slug=category.slug, item_slug=item.slug))

    return render_template('create_item.html', form=form)
