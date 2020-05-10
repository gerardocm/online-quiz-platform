from flask import render_template, url_for, flash, redirect
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from onlinequiz.forms import SignUpForm, LoginForm
from onlinequiz.models import User
from onlinequiz import db
from sqlalchemy.exc import IntegrityError

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))

  form = SignUpForm()
  return render_template('signup.html', title='Sign up', form=form)

@auth.route('/signup', methods=['POST'])
def signup_post():
  form = SignUpForm()
  if form.validate_on_submit():
    try:
      new_user = User(
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name'),
        email=request.form.get('email'),
        password=generate_password_hash(request.form.get('password'), method='sha256')
      )
      db.session.add(new_user)
      db.session.commit()
    except IntegrityError:
      flash('Email address already exists')
      return render_template('signup.html', title='Sign up', form=form)

    user = User.query.filter_by(email=new_user.email).first()
    login_user(user, remember=True)
    return redirect(url_for('main.quizzes'))
  return render_template('signup.html', title='Sign up', form=form)
  

@auth.route('/login')
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  
  form = LoginForm()
  return render_template('login.html', title='Log in', form=form)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    form = LoginForm()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return render_template('login.html', title='Log in', form=form)

    login_user(user, remember=True)
    return redirect(url_for('main.quizzes'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))