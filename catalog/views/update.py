import flask
from flask import render_template, request, redirect, flash, url_for, Blueprint

from catalog.database import session
from catalog.forms import ItemForm
from catalog.models import Category
from catalog.views.helpers import get_category_by, get_item_by, get_all_categories, login_required

update = Blueprint('update', __name__)


@update.route('/catalog/<string:category_slug>/<string:item_slug>/update', methods=['GET', 'POST'])
@login_required
def update_item(category_slug, item_slug):
    categories = get_all_categories()
    item = get_item_by.slug(item_slug)
    category = get_category_by.slug(category_slug)

    if item.user.id != flask.session['user']['db_id']:
        flash('Must be creator of item to edit', 'warning')
        return redirect(url_for('base.index'))

    form = ItemForm(
        category=item.category.name,
        name=item.name,
        description=item.description)
    form.category.choices = [(c.name, c.name) for c in categories]

    if request.method == 'POST' and form.validate():
        if form.new_category:
            category_name = (form.new_category.data or form.category.data).lower()
            category_new = get_category_by.name(category_name)
            if not category_new:
                category_new = Category(category_name)
        else:
            category_new = get_category_by.name(form.category.data)

        item.name = form.name.data.lower()
        item.description = form.description.data
        item.category = category_new

        if category_new.id != category.id and not category.items:
            session.delete(category)

        session.commit()

        return redirect(url_for('read.read_item', category_slug=item.category.slug, item_slug=item.slug))

    return render_template('update_item.html', form=form, item=item)
