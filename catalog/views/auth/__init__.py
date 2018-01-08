from flask import Blueprint

auth = Blueprint('auth', __name__)

from catalog.views.auth import views
