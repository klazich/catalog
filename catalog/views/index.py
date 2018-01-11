from flask import Blueprint, redirect, url_for

base = Blueprint('base', __name__)


@base.route('/', methods=['GET'])
def index():
    return redirect(url_for('read.read_catalog'))
