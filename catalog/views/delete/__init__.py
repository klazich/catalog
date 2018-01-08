from flask import Blueprint

delete = Blueprint('delete', __name__)

from catalog.views.delete import views
