import os
import simplejson
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)


app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'db/group-practical.dat'),
    DEBUG = True
    )
)
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.before_request
def before_request():
    print app.config['DATABASE']
    g.db = connect_db()
    g.cursor = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()  

@app.route('/companies')
def hello_world():
    g.cursor.execute('''SELECT name FROM companies''')
    r = [dict((g.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in g.cursor.fetchall()]
    return simplejson.dumps(r) 
    

if __name__ == '__main__':
    app.run()
