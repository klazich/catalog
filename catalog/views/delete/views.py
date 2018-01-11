import flask
from flask import redirect, request, flash, url_for

from catalog.database import Session
from catalog.views.delete import delete
from catalog.views.helpers import get_item_by, get_category_by, login_required


@delete.route('/catalog/<string:category_slug>/<string:item_slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(category_slug, item_slug):
    item = get_item_by.slug(item_slug)

    if item.user.id != flask.session['user']['db_id']:
        flash('must be item creator to delete item', 'warning')
        return redirect(request.referrer or url_for('read.index'))

    Session.delete(item)
    Session.commit()

    flash('item removed', 'info')

    category = get_category_by.slug(category_slug)
    if not category.items:
        Session.delete(category)
        Session.commit()
        return redirect(url_for('read.index'))
    else:
        return redirect(url_for('read.read_category', category_slug=category_slug))
