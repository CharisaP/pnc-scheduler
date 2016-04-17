# import the Flask class from the flask module

from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf import Form
from tempform import RegisterForm
from tempform import MessageForm
from functools import wraps
import json
from sqlite3 import dbapi2 as sqlite3
import os
import uuid
app = Flask(__name__, static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])
DATABASE = './db/test.db'
#create connection and cursor

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None: db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('./db/events.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#from models import * #must be done after db is defined

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # return "Hello, World!"  # return a string
    #posts = db.session.query(BlogPost).all() #change this
    #g.db = connect_db()
    #cur = g.db.execute('select * from posts')
    #posts = [dict(title = row[0], description = row[1]) for row in cur.fetchall()]
    #g.db.close()

    #first, need to query the database for existing posts. 
    #then:
    db = get_db()
    form = MessageForm(request.form) #create blank message form
    
    if form.validate_on_submit():
        title = request.form['title']
        descript = request.form['description']
        author = "temp_author"
        #return "post added"
        sql = "INSERT INTO posts (title, description, author) VALUES('%s', '%s' ,'%s')" %(title, descript, author)
        db = get_db()
        db.execute(sql)
        db.commit()
        flash("Post added")
        return redirect(url_for('home'))
    else:
        posts = query_db('SELECT * FROM posts')
        #for post in query_db('SELECT * FROM posts '):
            #posts.append(post)
        return render_template('index.html', form=form, posts=posts)

        #return render_template('index.html',form=form)  # render a template

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/sample')
@login_required
def sample():
    f = open('templates/sample3.html')
    return f.read()
    #return #render_template('sample.html') #create test calendar

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():  
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

def connect_db():
    return sqlite3.connect(app.database)
    

@app.route('/eventdata')
def return_data():
    mstart = request.args.get('start')
    mend = request.args.get('end')
    myevents = []
    for event in query_db('SELECT * FROM events WHERE start >= ? AND end <= ?', (mstart, mend,)):
        event_dict = {
                        'id' : event['id'],
                        'title' : event['title'],
                        'start' : event['start'],
                        'end' : event['end'],
                        'details' : event['details']
                      }
        myevents.append(event_dict)
    return json.dumps(myevents)
    #return 'okay'

@app.route('/deletedata', methods=['POST'])
def delete_data():
    eid = request.form['id']
    db = get_db()
    event = query_db('SELECT * FROM events WHERE id = ?', (eid,), one = True)
    event_dict = {
                    'id' : event['id'],
                    'title' : event['title'],
                    'start' : event['start'],
                    'end' : event['end'],
                    'details' : event['details']
                    }
    db.execute('DELETE FROM events WHERE id = ?', (eid,))
    db.commit()
    return jsonify(event_dict)


@app.route('/register', methods=['GET', 'POST'])
def save_user():
    form = RegisterForm() 
    db = get_db()  
    if form.validate_on_submit():
                                         #database is referenced through "db"
        eid = uuid.uuid4()   
                                  #id is created automatically. (never seen by user)
        eusername = request.form['username']    
        epassword = request.form['password']
        efn = request.form['first_name']
        eln = request.form['last_name']
        testo = query_db('SELECT * FROM users WHERE username = ?', (eusername,), one = True)
        if testo != None:
            flash('error: username already exists')
                #error checking to make sure that the username doesnt already exist
        sql = "INSERT INTO users (id, username, password, first_name, last_name) VALUES('%s', '%s', '%s', '%s', '%s')" %(eid, eusername, epassword, efn, eln)
        db.execute(sql)
        db.commit()
        return redirect(url_for('home'))
    else:
        return render_template('register.html',form=form)

@app.route('/savedata', methods=['POST'])
def save_data():
    #init_db()
    db = get_db()
    eid = request.form['id']
    etitle = request.form['title']
    estart = request.form['start']
    eend = request.form['end']
    edetails = request.form['details']

    testo = query_db('SELECT * FROM events WHERE id = ?', (eid,), one = True)
    if testo != None:
        db.execute('DELETE FROM events WHERE id = ?', (eid,))
        db.commit()

    eid = uuid.uuid4()
    sql = "INSERT INTO events (id, title, start, end, details) VALUES('%s', '%s', '%s', '%s', '%s')" %(eid, etitle, estart, eend, edetails)
    db = get_db()
    db.execute(sql)
    db.commit()
    event_dict = {
                    'id' : eid,
                    'title' : etitle,
                    'start' : estart,
                    'end' : eend,
                    'details' : edetails
                    }
    return jsonify(event_dict)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.debug = True
    app.run()