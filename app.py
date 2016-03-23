# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
#import sqlite3

# create the application object
app = Flask(__name__)

# config
#app.secret_key = 'my precious'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
import os
app.config.from_object(os.environ[APP_SETTINGS])

# create sqlalchemy object
db = SQLAlchemy(app)

from models import *

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
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)  # render a template


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/sample')
@login_required
def sample():
	return render_template('sample.html') #create test calendar


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
    
# connect to database
#def connect_db():
#    return sqlite3.connect(app.database)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run()
