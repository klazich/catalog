from flask import Blueprint, abort, render_template, g

from ..database import session
from ..models import Category

category_bp = Blueprint('category', __name__)


@category_bp.route('/category/<int:category_id>')
def read(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter(Category.id == category_id).one_or_none()
    if not category:
        abort(404)

    g.categories = sorted(categories, key=lambda c: c.name)
    g.category = category

    return render_template('read_category.html')
