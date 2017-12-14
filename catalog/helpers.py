# from flask_login import login_required

from . import db_session
from .models import Category, Item


def latest(limit):
    """
    Helper function that returns the most recent items created
    """
    return db_session.query(Item).order_by(Item.date_updated).limit(limit)
