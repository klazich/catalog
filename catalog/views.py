import json

from flask import render_template
from sqlalchemy import asc, desc

from catalog import app
from catalog.database import db_session
from catalog.models import User, Category, Item

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'FSND Catalog App'


@app.route('/')
@app.route('/catalog/')
def index():
    catagories = db_session.query(Category).order_by(asc(Category.name))
    items = db_session.query(Item).order_by(Item.created)

    return render_template('index.html')
