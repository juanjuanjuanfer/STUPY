# import the necessary libraries
# utils.py contains only the necessary functions for the code 
# to interact with the database. However it need another called
# mongo_connection.py where you add your own credentials to connect to the db.

from flask import Flask, render_template, request, redirect, url_for, session
import utils
from flask_session import Session
import os

# create the flask app
app = Flask(__name__)

# Im not sure what are this for, but the app.secret_key is a token 
# to keep some pages unavailable for non-logged users
# also not sure about the cookies, thats why they are named like that
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'galletagalletametralleta'
app.config['PERMANENT_SESSION_LIFETIME'] = 7200  
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  
app.config['SESSION_TYPE'] = 'filesystem'

# important, the seesion(app) must be after anything from the settings
# and the token
Session(app)

# main route, nothing special
@app.route('/')
def index():
    return render_template('index.html')

# singup route, only uses post yet
# if the user exists, it will return a message
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # the function create_new_user is detailed in the utils.py file
        user_creation = utils.create_new_user(username,password)
        if not user_creation: 
            return 'User already exists' # if the user exists, it will return this message only
        return render_template('user_created.html', username=username) # if the user is created correctly, it will return this template in the same url
    else: return render_template('signup.html')

    
# login  route, only uses post yet
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # the function get_user is detailed in the utils.py file
        if utils.get_user(username, password):
            # here the session is created, and the user is logged in
            # this is necessary for the user to access dashboard
            session['user_logged_in'] = True
            session['username'] = username
            # if identification works, redirect to the dashboard route
            return redirect(url_for('dashboard'))
        else:
            return 'Login Failed'
    return render_template('login.html')

# dashboard route, uses get and post
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # do not allow if the user is not logged in and redirects to login
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    
    # if the request is post it will create a new thread
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = session.get('username')
        # the function new_thread is detailed in the utils.py file
        new_thread = utils.new_thread(title, content, username)
        # if the function does not work, it will return a message
        if not new_thread:
            return 'Could not create thread'
        return redirect(url_for('dashboard'))

    # if user is logged in, the dashboard will show the username and the threads
    if session.get('user_logged_in'):
        username = session.get('username')
        # the function get_threads is detailed in the utils.py file
        threads = utils.get_threads()
        return render_template('dashboard.html', username=username, threads=threads)
    else:
        return 'Not logged in'

# logout route, only logs out the user, not an url
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)