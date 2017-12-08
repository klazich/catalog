import json

from flask import render_template, Blueprint
from sqlalchemy import asc, desc

from catalog.database import db_session
from catalog.models import User, Category, Item

# CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = 'FSND Catalog App'

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/catalog/')
def index():
    return render_template('index.html')


@home.route('/raw/')
def raw():
    items = db_session.query(Item).order_by(Item.date_created)
    return render_template('test.html', items=items)
