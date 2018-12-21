import sqlite3
from flask import render_template, g
from . import utils

from .app import app

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DB_FILE'])
    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    categories = utils.get_n_random_lines(utils.CATEGORY_PATH, n=10)
    return render_template('index.html', categories=categories)

@app.route('/category/<category_id>')
def category(category_id):
    clues = utils.get_clues_from_cat(category_id)
    return render_template('category.html', clues=clues)
