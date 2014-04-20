import os
import simplejson
import sqlite3
import parser 
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__, static_url_path='')


app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'fake.db'),
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
    g.cursor.execute('''SELECT * FROM FINANCE ORDER BY Period,CompanyID,ItemName''')
    r = [dict((g.cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in g.cursor.fetchall()]
    return simplejson.dumps(r) 

@app.route('/')
def home():
  return render_template('visualiser.html')

#replace this with a mapping from id to company when tawfiq writes it
@app.route('/company')
def listCompanies():
  return simplejson.dumps(os.listdir('bin/raw/'))

@app.route('/company/<cik>')
def filingList(cik):
  return simplejson.dumps(map(lambda x: os.path.splitext(x)[0], os.listdir('bin/raw/'+cik)))

@app.route('/company/<cik>/<path>')
def parseListing(cik, path):
  print cik, path
  p = os.path.join('bin/raw',cik,path+".txt") 
  res = parser.parseListing(p)
  return simplejson.dumps([])
  #parseListing needs to return the result of the parsing
  
  
  
    

if __name__ == '__main__':
    app.run()
