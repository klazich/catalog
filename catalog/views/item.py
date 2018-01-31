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
    """
    Creates a new item and commits it to the database. 
    The user must be logged in to reach the html form and is redirected to the auth.login 
    if not. Form data is validated and item is checked for uniqueness to prevent SQLALchemy
    IntegretyError exceptions.
    :returns: (GET) a rendering of the create_item.html template with ItemForm form;
              (POST) a redirect to the item.read endpoint for created item
    """
    # get data from database
    all_items = session.query(Item).all()
    all_categories = session.query(Category).all()
    user = session.query(User).filter(User.id == flask.session['user']['db_id']).one_or_none()

    # create ItemForm form (Flask-WTF)
    form = ItemForm(request.form)
    # add all the database categories to the form's category select field
    form.category.choices = [(c.name, c.name) for c in all_categories]

    if request.method == 'POST' and form.validate():
        category_name = (form.new_category.data or form.category.data).lower()
        category = session.query(Category).filter(Category.name == category_name).one_or_none()
        if not category:
            category = Category(category_name)

        # check for item name is unique
        if form.name.data.lower() in map(lambda i: i.name, all_items):
            flash('that item name is already in use', 'warning')
            return redirect(request.referrer)

        # create the new Item object
        item = Item(
            name=form.name.data.lower(),
            description=form.description.data,
            category=category,
            user=user)

        # add the Item object to the database session and try to commit
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
    """
    Displays an items data 
    :param item_id: the databse id (Item.id) of the item to read
    :type item_id: int
    :return: a rendering of the read_item.html template
    """
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
    """
    Update an item in the database.
    :param item_id: the database id (Item.id) of the item to update
    :type item_id: int
    :returns: (GET) a rendering of the update_item.html template with ItemForm form;
              (POST) a redirect to the item.read endpoint for the updated item
    """
    # get data from the database
    all_items = session.query(Item).all()
    all_categories = session.query(Category).all()
    item = session.query(Item).filter(Item.id == item_id).one_or_none()
    category = item.category
    user = session.query(User).filter(User.id == flask.session['user']['db_id']).one_or_none()
    
    # check that the user is item's owner
    if item.user.id != user.id:
        flash('item must be yous to edit/delete', 'warning')
        return redirect(url_for('item.read', item_id=item_id))

    # create the ItemForm form with the item data
    form = ItemForm(
        name=item.name,
        description=item.description,
        category=category.name)
    # add all the database categories to the form's category select field    
    form.category.choices = [(c.name, c.name) for c in all_categories]

    if request.method == 'POST' and form.validate():
        category_name = (form.new_category.data or form.category.data).lower()
        category_new = session.query(Category).filter(Category.name == category_name).one_or_none()
        if not category_new:
            category_new = Category(category_name)
        
        # check the new item name is unique
        if item.name != form.name.data.lower() and form.name.data.lower() in map(lambda i: i.name, all_items):
            flash('that item name is already in use', 'warning')
            return redirect(request.referrer)

        # update the item object with new data
        item.name = form.name.data.lower()
        item.description = form.description.data
        item.category = category_new
        
        # remove the item's old category from the database if that category is now empty
        if category_new.id != category.id and not category.items:
            session.delete(category)

        # commit the session
        session.commit()

        return redirect(url_for('item.read', item_id=item.id))

    if request.method == 'GET':
        g.item = item
        return render_template('update_item.html', form=form)


@login_required
@item_bp.route('/item/<int:item_id>/delete', methods=['GET', 'DELETE'])
def delete(item_id):
    """
    Delete an item from the database.
    The user must be logged in and owner of the item.
    :param item_id: the database id (Item.id) of the item to delete
    :type item_id: int
    :return: a redirect to the deleted item's category or index
    """
    # get data from the database
    item = session.query(Item).filter(Item.id == item_id).one_or_none()
    category = item.category
    user = session.query(User).filter(User.id == flask.session['user']['db_id']).one_or_none()

    # check that the user is item's owner
    if item.user.id != user.id:
        flash('item must be yous to edit/delete', 'warning')
        return redirect(url_for('item.read', item_id=item_id))

    # delete the item from session and commit to database
    session.delete(item)
    session.commit()

    flash('item removed', 'info')

    # remove the category from the database if it is now empty
    if not category.items:
        session.delete(category)
        session.commit()
        return redirect(url_for('catalog.index'))
    else:
        return redirect(url_for('category.read', category_id=category.id))
