from flask import Blueprint

views = Blueprint('views', __name__)

from catalog.views import auth, create, delete, read, update
