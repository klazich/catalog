from flask import Blueprint

read = Blueprint('read', __name__)

from . import views
