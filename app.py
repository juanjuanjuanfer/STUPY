from flask import Flask, render_template, request, redirect, url_for, session
import utils
from flask_session import Session
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'galletagalletametralleta'
app.config['PERMANENT_SESSION_LIFETIME'] = 60  
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_creation = utils.create_new_user(username,password)
        if not user_creation:
            return 'User already exists'
        return render_template('user_created.html', username=username)
    else: return render_template('signup.html')

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if utils.get_user(username, password):
            session['user_logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Login Failed'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('user_logged_in'):
        return redirect(url_for('login'))
    
    if session.get('user_logged_in'):
        username = session.get('username')
        return render_template('dashboard.html', username=username)
    else:
        return 'Not logged in'

    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)