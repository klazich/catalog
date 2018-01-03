from flask import Blueprint

create = Blueprint('create', __name__)

from . import views