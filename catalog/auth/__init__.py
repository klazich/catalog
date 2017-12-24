from flask import Blueprint

auth = Blueprint('auth', __name__)

from catalog.auth import views

