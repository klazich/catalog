from flask import Blueprint

read = Blueprint('read', __name__)

from catalog.views.read import views
