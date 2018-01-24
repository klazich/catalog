from flask import render_template, Blueprint, g

from ..models import Category
from ..database import session

catalog_bp = Blueprint('catalog', __name__)


@catalog_bp.route('/')
@catalog_bp.route('/catalog/')
def index():
    g.categories = sorted(session.query(Category).all(), key=lambda c: c.name)
    return render_template('read_catalog.html')
