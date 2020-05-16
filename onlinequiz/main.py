from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from onlinequiz.forms import QuestionSetForm, QuestionForm
from onlinequiz.models import (
  QuestionSet,
  ManualQuestion,
  MultichoiceQuestion,
  MultichoiceOption,
  VotingQuestion,
  VotingOption
)
from onlinequiz import db
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import json

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template(
    'index.html',
    cuser=current_user
  )

@main.route('/not-authorized')
def not_auth():
  return render_template(
    'not-authorized.html',
    cuser=current_user
  )

@main.route('/quizzes')
@login_required
def quizzes():
  return render_template(
    'quizzes.html',
    cuser=current_user
  )

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@main.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response