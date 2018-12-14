import sqlite3
from flask import render_template, g

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
    categories = list(query_db(
        """SELECT
          categories.id as category_id,
          categories.category,
          COUNT(*) AS cnt
        FROM
          categories
          INNER JOIN classifications
            ON categories.id = classifications.category_id
          INNER JOIN clues
            ON clues.id = classifications.clue_id
        WHERE
          categories.id IN (
            SELECT
              categories.id
            FROM
              categories INNER JOIN classifications
                ON categories.id = classifications.category_id
            ORDER BY RANDOM() LIMIT 10)
        GROUP BY 1,2
        ;"""))
    return render_template('index.html', categories=categories)

@app.route('/category/<category_id>')
def category(category_id):
    clues = list(query_db(
        """SELECT
          clues.id,
          clues.game,
          clues.round,
          clues.value,
          documents.clue,
          documents.answer,
          categories.category,
          airdates.airdate
        FROM
          documents
          INNER JOIN clues
            ON documents.id = clues.id
          INNER JOIN classifications
            ON clues.id = classifications.clue_id
          INNER JOIN categories
            ON classifications.category_id = categories.id
          INNER JOIN airdates
            ON clues.game = airdates.game
        WHERE
          classifications.category_id = ?
          AND clues.game in (SELECT
              clues.game
            FROM
              clues
              INNER JOIN classifications
                ON clues.id = classifications.clue_id
            WHERE
              classifications.category_id = ?
            ORDER BY RANDOM() LIMIT 1)
          """, args=(category_id, category_id)))
    return render_template('category.html', clues=clues)
