from flask import Blueprint

update = Blueprint('update', __name__)

from catalog.views.update import views
