from flask import render_template, Blueprint, abort

from catalog.views.helpers import get_item_by, get_category_by

read = Blueprint('read', __name__)


@read.route('/')
@read.route('/catalog/')
def index():
    return render_template('read_categories.html')


@read.route('/catalog/<category_slug>/')
def read_category(category_slug):
    category = get_category_by.slug(category_slug)
    return render_template('read_category.html', category=category)


@read.route('/catalog/<category_slug>/<item_slug>/')
def read_item(category_slug, item_slug):
    category = get_category_by.slug(category_slug)
    item = get_item_by.slug(item_slug)
    if not item:
        abort(404)
    return render_template('read_item.html', category=category, item=item)
