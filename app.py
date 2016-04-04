# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
import json
import sqlite3

# create the application object
app = Flask(__name__, static_url_path='')

# config

import os
app.config.from_object(os.environ['APP_SETTINGS'])
app.database = 'sample.db'
#create connection and cursor


# create sqlalchemy object

#db = SQLAlchemy(app)



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
@app.route('/')
@login_required
def home():
	# return "Hello, World!"  # return a string
    #posts = db.session.query(BlogPost).all() #change this
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title = row[0], description = row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html', posts=posts)  # render a template


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/sample')
@login_required
def sample():
	f = open('templates/sample2.html')
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
    
'''
@app.route('/data')
def return_data():
    pass


@app.route('/deletedata')
def return_data():
    pass
'''
@app.route('/savedata')
def return_data():
    event_obj = request.args.get('data')
    # event obj needs to be json
    print event_obj
 
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()
