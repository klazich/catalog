import flask
from flask import Blueprint, abort, render_template, g, request, redirect, flash, url_for
from sqlalchemy.exc import IntegrityError

from ..database import session
from ..models import Item, Category, User
from ..forms import ItemForm
from . import login_required

item_bp = Blueprint('item', __name__)


@item_bp.route('/item/new', methods=['GET', 'POST'])
@login_required
def create():
    all_items = session.query(Item).all()
    all_categories = session.query(Category).all()
    user = session.query(User).filter(User.id == flask.session['user']['db_id']).one_or_none()

    form = ItemForm(request.form)
    form.category.choices = [(c.name, c.name) for c in all_categories]

    if request.method == 'POST' and form.validate():
        category_name = (form.new_category.data or form.category.data).lower()
        category = session.query(Category).filter(Category.name == category_name).one_or_none()
        if not category:
            category = Category(category_name)

        if form.name.data.lower() in map(lambda i: i.name, all_items):
            flash('that item name is already in use', 'warning')
            return redirect(request.referrer)

        item = Item(
            name=form.name.data.lower(),
            description=form.description.data,
            category=category,
            user=user)

        session.add(item)
        try:
            session.commit()
        except IntegrityError:
            flash('oops! database error, could not add item', 'error')
            return redirect(request.referrer)

        flash('created item {}'.format(item.name), 'info')

        return redirect(url_for('item.read', item_id=item.id))

    if request.method == 'GET':
        return render_template('create_item.html', form=form)


@item_bp.route('/item/<int:item_id>/', methods=['GET'])
def read(item_id):
    item = session.query(Item).filter(Item.id == item_id).one_or_none()
    if not item:
        abort(404)
    g.item = item
    g.category = item.category
    g.categories = sorted(session.query(Category).all(), key=lambda c: c.name)
    return render_template('read_item.html')


@item_bp.route('/item/<int:item_id>/update', methods=['GET', 'POST', 'UPDATE'])
@login_required
def update(item_id):
    all_items = session.query(Item).all()
    all_categories = session.query(Category).all()
    item = session.query(Item).filter(Item.id == item_id).one_or_none()
    category = item.category
    user = session.query(User).filter(User.id == flask.session['user']['db_id']).one_or_none()

    if item.user.id != user.id:
        flash('item must be yous to edit/delete', 'warning')
        return redirect(url_for('item.read', item_id=item_id))

    form = ItemForm(
        name=item.name,
        description=item.description,
        category=category.name)
    form.category.choices = [(c.name, c.name) for c in all_categories]

    if request.method == 'POST' and form.validate():
        category_name = (form.new_category.data or form.category.data).lower()
        category_new = session.query(Category).filter(Category.name == category_name).one_or_none()
        if not category_new:
            category_new = Category(category_name)

        print(form.name.data.lower())

        if item.name != form.name.data.lower() and form.name.data.lower() in map(lambda i: i.name, all_items):
            flash('that item name is already in use', 'warning')
            return redirect(request.referrer)

        item.name = form.name.data.lower()
        item.description = form.description.data
        item.category = category_new

        if category_new.id != category.id and not category.items:
            session.delete(category)

        session.commit()

        return redirect(url_for('item.read', item_id=item.id))

    if request.method == 'GET':
        g.item = item
        return render_template('update_item.html', form=form)


@login_required
@item_bp.route('/item/<int:item_id>/delete', methods=['GET', 'DELETE'])
def delete(item_id):
    item = session.query(Item).filter(Item.id == item_id).one_or_none()
    category = item.category
    user = session.query(User).filter(User.id == flask.session['user']['db_id']).one_or_none()

    if item.user.id != user.id:
        flash('item must be yous to edit/delete', 'warning')
        return redirect(url_for('item.read', item_id=item_id))

    session.delete(item)
    session.commit()

    flash('item removed', 'info')

    if not category.items:
        session.delete(category)
        session.commit()
        return redirect(url_for('catalog.index'))
    else:
        return redirect(url_for('category.read', category_id=category.id))
