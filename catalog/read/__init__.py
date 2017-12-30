from flask import Blueprint

home = Blueprint('read', __name__)

from . import views
