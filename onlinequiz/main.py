from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template('index.html')

@main.route('/quizzes')
@login_required
def quizzes():
  full_name = current_user.first_name + current_user.last_name
  return render_template('quizzes.html', full_name=full_name)