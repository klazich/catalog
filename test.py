from flask import render_template, request, redirect, url_for, Blueprint, Flask

app = Flask(__name__)


@app.route('/')
@app.route('/catalog/')
@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/<int:item_id>')
def index(category_id=None, item_id=None):
    if item_id:
        # render item info
        return 'catalog -> category -> item -> {}'.format(item_id)
    elif category_id:
        # render category items
        return 'catalog -> category -> {}'.format(category_id)
    else:
        # render catalog categories
        return 'catalog -> list'


if __name__ == '__main__':
    app.run()
