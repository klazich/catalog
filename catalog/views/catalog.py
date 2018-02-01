from flask import render_template, Blueprint, g

from ..models import Category
from ..database import session

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/')
@catalog_bp.route('/catalog/')
def index():
    """
    App html entry point. Renders the homepage which list all categories in the database.

    :return: rendering of the read_catalog.html template
    """
    g.categories = sorted(session.query(Category).all(), key=lambda c: c.name)
    return render_template('read_catalog.html')
