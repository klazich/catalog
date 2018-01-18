from flask import render_template, request, redirect, url_for, Blueprint, abort, g

from ..models import Item, Category, User
from ..database import session

catalog = Blueprint('catalog', __name__)


@catalog.route('/')
@catalog.route('/catalog/')
@catalog.route('/catalog/<int:category_id>/')
@catalog.route('/catalog/<int:category_id>/<int:item_id>')
def index(category_id=None, item_id=None):
    g.categories = session.query(Category).all()
    if not category_id:
        return render_template('read_catalog.html')

    g.category = session.query(Category).filter(Category.id == category_id).one_or_none()
    if not g.category:
        abort(404)
    if not item_id:
        return render_template('read_category.html')

    g.item = session.query(Item).filter(Item.id == item_id).one_or_none()
    if not g.item:
        abort(404)
    return render_template('read_item.html')
