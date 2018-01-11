from flask import Blueprint, jsonify

from catalog.views.helpers import get_item_by, get_category_by, get_all_categories

json = Blueprint('json', __name__)


@json.route('/catalog/json')
def json_catalog():
    catalog = get_all_categories()
    return jsonify(catalog=[c.serialize for c in catalog])


@json.route('/catalog/<string:category_slug>/json', methods=['GET'])
def json_category(category_slug):
    category = get_category_by.slug(category_slug)
    return jsonify(category=category.serialize)


@json.route('/catalog/<string:category_slug>/<string:item_slug>/json', methods=['GET'])
def json_item(category_slug, item_slug):
    category = get_category_by.slug(category_slug)
    item = get_item_by.slug(item_slug)
    return jsonify(item=item.serialize)
