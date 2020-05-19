from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from onlinequiz.forms import QuestionSetForm, QuestionForm
from onlinequiz.models import (
  User,
  QuestionSet,
  QuestionSetUser,
  MultichoiceQuestion,
  MultichoiceOption,
  UserMultichoiceQuestion,
  ManualQuestion,
  UserManualQuestion,
  VotingQuestion,
  VotingOption,
  UserVotingQuestion
)
from onlinequiz import db
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import json

admin_question_set = Blueprint('admin_question_set', __name__)

@admin_question_set.route('/admin-question-set/<int:set_id>')
@login_required
def admin_question_set_get(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()

  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))

  if question_set.is_public:
    question_set.is_public_label = "public"
  if question_set.is_public:
    question_set.is_public_label = "private"

  qset_users = QuestionSetUser.query.filter_by(question_set_id=set_id).all()
  users = User.query.filter(User.id.in_([user.user_id for user in qset_users]))

  return render_template(
    'admin-question-set.html',
    set_id=set_id,
    question_set=question_set,
    users=users,
    cuser=current_user
  )

@admin_question_set.route('/users')
@login_required
def search_user():
  email = request.args.get('email')
  if email is None or email == '':
    response = jsonify({})
    response.status_code = 200
    return response
    
  users = User.query.filter(User.email.like('%' + email + '%')).all()[:2]
  user_list = []
  for user in users:
    user_list.append({
      "id": user.id,
      "full_name": user.first_name + " " + user.last_name
    })
  response = jsonify(users=user_list)
  response.status_code = 200
  return response

@admin_question_set.route('/question-set-user', methods=['POST'])
@login_required
def question_set_user_post():
  question_set_id = request.form.get('question_set')
  question_set = QuestionSet.query.filter_by(id=question_set_id).first()

  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  try:
    user_id = request.form.get('user')
    new_question_set_user = QuestionSetUser(
      user_id=user_id,
      question_set_id=question_set_id,
    )
    db.session.add(new_question_set_user)
    db.session.commit()
  except:
    raise InvalidUsage('There was an error while updating the set.')

  response = jsonify({
    'id': new_question_set_user.id,
  })
  response.status_code = 200
  return response

@admin_question_set.route('/question-set-user/user/<int:uid>', methods=['DELETE'])
@login_required
def question_set_user_delete(uid):
  question_set_user = QuestionSetUser.query.filter_by(user_id=uid).first()
  question_set_id = question_set_user.question_set_id
  question_set = QuestionSet.query.filter_by(id=question_set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  try:
    db.session.delete(question_set_user)
    db.session.commit()
  except:
    raise InvalidUsage('There was an error while updating the set.')

  response = jsonify({})
  response.status_code = 200
  return response

@admin_question_set.route('/mark-question-set/<int:set_id>/user/<int:uid>')
@login_required
def mark_question_set_get(set_id, uid):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))

  question_set_user = QuestionSetUser.query.filter_by(question_set_id=set_id, user_id=uid).first()
  questions = __get_question_set_with_answers(question_set_user)

  return render_template(
    'mark-question-set.html',
    question_set_id=set_id,
    user_id=set_id,
    question_set=question_set,
    questions=questions,
    cuser=current_user
  )


def __get_question_set_with_answers(question_set_user):
  question_set = question_set_user.question_set_id
  user = question_set_user.user_id
  multichoice_questions = MultichoiceQuestion.query.filter_by(question_set=question_set).all()
  manual_questions = ManualQuestion.query.filter_by(question_set=question_set).all()
  voting_questions = VotingQuestion.query.filter_by(question_set=question_set).all()

  for question in manual_questions:
    question.answer = UserManualQuestion.query.filter_by(
      manual_question=question,
      question_set_user_id=question_set_user.id
    ).first()

  for question in multichoice_questions:
    question.options = MultichoiceOption.query.filter_by(multichoice_question=question.id).all()
    question.answer = UserMultichoiceQuestion.query.filter_by(
      multichoice_question=question,
      question_set_user_id=question_set_user.id
    ).first()

  for question in voting_questions:
    question.options = VotingOption.query.filter_by(voting_question=question.id).all()
    question.answer = UserVotingQuestion.query.filter_by(
      voting_question=question,
      question_set_user_id=question_set_user.id
    ).first()

  return {
    "multichoice_questions": multichoice_questions,
    "manual_questions": manual_questions,
    "voting_questions": voting_questions
  }

@admin_question_set.route('/manual-question/answer/<int:question_ans_id>', methods=['POST'])
@login_required
def mark_manual_question(question_ans_id):
  user_manual_question = UserManualQuestion.query.filter_by(id=question_ans_id).first()
  manual_question = ManualQuestion.query.filter_by(
    id=user_manual_question.manual_question_id
  ).first()
  question_set = QuestionSet.query.filter_by(
    id=manual_question.question_set
  ).first()

  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))

  if user_manual_question.answer is None:
    raise InvalidUsage('This questions has not been answered yet.')

  try:
    mark = request.form.get('mark')
    user_manual_question.mark = mark
    db.session.commit()
  except:
    raise InvalidUsage('An error occur while updating.')

  response = jsonify({
    "mark": mark
  })
  response.status_code = 200
  return response

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

@admin_question_set.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response