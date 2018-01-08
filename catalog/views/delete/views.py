import flask
from flask import redirect, request, flash, url_for

from catalog.views.delete import delete
from catalog.views.helpers import get_item_by, get_category_by, get_user_by
from catalog.database import Session
from catalog.models import Item, Category


@delete.route('/catalog/<string:category_slug>/<string:item_slug>/delete', methods=['GET', 'POST'])
def delete_item(category_slug, item_slug):
    if 'user' not in flask.session:
        flash('must be logged in to delete items', 'warning')
        return redirect(request.referrer or url_for('read.index'))

    item = get_item_by.slug(item_slug)

    if item.user.id != flask.session['user']['db_id']:
        flash('must be item creator to delete item', 'warning')
        return redirect(request.referrer or url_for('read.index'))

    category = get_category_by.slug(category_slug)

    print(category.items)

    Session.delete(item)
    Session.commit()

    print(category.items)

    return redirect(url_for('read.index'))
