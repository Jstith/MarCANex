from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
import random
import os

auth = Blueprint('auth', __name__)

# Random choice for login quips
random.seed(os.urandom(5))
basedir = os.path.abspath(os.path.dirname(__file__))
login_lines = open(os.path.join(basedir, 'static/txt/login_sayings.txt')).readlines()

# Default route, redirects to login
@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    # check if user exists
    # take user-supplied password, hash it, compare to hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Invalid Credentials. Garbage-CAN is too stronk for you.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or passwo>
    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.table'))

@auth.route('/signup')
@login_required
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
@login_required
def signup_post():
    # code to validate and add user to database goes here
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already e>

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# @auth.route('/logout')
# def logout():
#     session.pop("user", None)
#     flash('You have been logged out. Happy hacking!')
#     return redirect(url_for('login'))
