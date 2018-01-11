from flask import Blueprint, jsonify

from catalog.views.helpers import get_item_by, get_category_by, get_all_categories

api = Blueprint('json', __name__)


@api.route('/', methods=['GET'])
def json_catalog():
    catalog = get_all_categories()
    return jsonify(catalog=[c.serialize for c in catalog])


@api.route('/<string:category_slug>', methods=['GET'])
def json_category(category_slug):
    category = get_category_by.slug(category_slug)
    return jsonify(category=category.serialize)


@api.route('/<string:category_slug>/<string:item_slug>', methods=['GET'])
def json_item(category_slug, item_slug):
    category = get_category_by.slug(category_slug)
    item = get_item_by.slug(item_slug)
    return jsonify(item=item.serialize)
