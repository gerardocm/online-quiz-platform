from flask import render_template, url_for, flash, redirect
from onlinequiz.forms import SignUpForm, LoginForm
from onlinequiz.models import User
from onlinequiz import app

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignUpForm()
  if form.validate_on_submit():
    flash('Account created!', 'success')
    return redirect(url_for('home'))
  return render_template('signup.html', title='Sign up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Account created!', 'success')
    return redirect(url_for('home'))
  return render_template('login.html', title='Log in', form=form)