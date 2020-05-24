from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from onlinequiz.forms import QuestionSetForm, QuestionForm
from onlinequiz.models import (
  QuestionSet,
  QuestionSetUser,
  ManualQuestion,
  MultichoiceQuestion,
  MultichoiceOption,
  VotingQuestion,
  VotingOption
)
from onlinequiz import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from flask import jsonify
import json
from datetime import datetime

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

@main.route('/quizzes', methods=['GET'])
@login_required
def quizzes():
  queryParams = request.args.get('filter')
  if queryParams:
    queryParams = queryParams.split(',')
    is_public,assigned = False, False
    owner,submitted = False, False

    for queryParam in queryParams:
      if queryParam == "ispublic":
        is_public = True
      if queryParam == "assigned":
        assigned = True
      if queryParam == "owner":
        owner = True
      if queryParam == "submitted":
        submitted = True
  else:
    is_public,assigned,owner = True, True, True
    submitted = False

  question_set_user_list = []
  if assigned:
    question_set_user_list = QuestionSetUser.query.filter_by(
      user_id=current_user.id
    )

  question_set_list = []
  if owner is True:
    if submitted is True:
      if is_public is True:
        question_set_list = QuestionSet.query.filter(
          or_(
            and_(
              QuestionSet.owner == current_user.id,
              QuestionSet.submitted == submitted,
            ),
            and_(
              QuestionSet.is_public == True,
              QuestionSet.submitted == True
            ),
            QuestionSet.id.in_([i.question_set_id for i in question_set_user_list])
          )
        ).distinct()
      else:
        question_set_list = QuestionSet.query.filter(
          or_(
            and_(
              QuestionSet.owner == current_user.id,
              QuestionSet.submitted == submitted
            ),
            QuestionSet.id.in_([i.question_set_id for i in question_set_user_list])
          )
        ).distinct()
    else:
      if is_public is True:
        question_set_list = QuestionSet.query.filter(
          or_(
            and_(
              QuestionSet.owner == current_user.id,
            ),
            and_(
              QuestionSet.is_public == True,
              QuestionSet.submitted == True
            ),
            QuestionSet.id.in_([i.question_set_id for i in question_set_user_list])
          )
        ).distinct()
      else:
        question_set_list = QuestionSet.query.filter(
          or_(
            and_(
              QuestionSet.owner == current_user.id
            ),
            QuestionSet.id.in_([i.question_set_id for i in question_set_user_list])
          )
        ).distinct()
  else:
    if is_public is True:
      question_set_list = QuestionSet.query.filter(
        or_(
          and_(
            QuestionSet.is_public == is_public,
            QuestionSet.submitted == True
          ),
          QuestionSet.id.in_([i.question_set_id for i in question_set_user_list])
        )
      ).distinct()
    else:
      question_set_list = QuestionSet.query.filter(
        QuestionSet.id.in_([i.question_set_id for i in question_set_user_list])
      ).distinct()

  qset_list = []
  if question_set_user_list and question_set_user_list.count() > 0:
    for question_set_user in question_set_user_list:
      for question_set in question_set_list:
        if question_set.id == question_set_user.question_set_id:
          is_assigned = True
        else:
          is_assigned = False

        exists = next((qset for qset in qset_list if qset["id"] == question_set.id), None)
        if exists is None:
          qset_list.append({
            "id":question_set.id,
            "name":question_set.name,
            "owner":question_set.owner,
            "submitted":question_set.submitted,
            "is_public":question_set.is_public,
            "due_date":question_set.due_date,
            "date_created":question_set.date_created.strftime("%m / %d / %Y"),
            "is_assigned":is_assigned
          })
        elif is_assigned is True:
          exists['is_assigned'] = is_assigned

  else:
    for question_set in question_set_list:
      qset_list.append({
        "id":question_set.id,
        "name":question_set.name,
        "owner":question_set.owner,
        "submitted":question_set.submitted,
        "is_public":question_set.is_public,
        "due_date":question_set.due_date,
        "date_created":question_set.date_created.strftime("%m / %d / %Y"),
        "is_assigned":False
      })

  try:
    number_of_question_sets = len(qset_list)
  except:
    number_of_question_sets = -1

  return render_template(
    'quizzes.html',
    question_set_list=qset_list,
    cuser=current_user,
    number_of_question_sets=number_of_question_sets
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