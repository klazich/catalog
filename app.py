import json

from flask import Flask, render_template, request, redirect, jsonify, url_for, make_response
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker

from db_setup import Base, User, Category, Item


app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'FSND Catalog App'

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
@app.route('/catalog/')
def show_main():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).order_by(asc(Item.title))
    return


if __name__ == '__main__':
    # app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
