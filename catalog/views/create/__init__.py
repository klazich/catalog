from flask import Blueprint

create = Blueprint('create', __name__)

from catalog.views.create import views
