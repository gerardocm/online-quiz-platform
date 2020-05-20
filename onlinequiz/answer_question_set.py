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
from .main import InvalidUsage
from onlinequiz import db
from sqlalchemy.exc import IntegrityError
from flask import jsonify
import json

answer_question_set = Blueprint('answer_question_set', __name__)

@answer_question_set.route('/answer-question-set/<int:set_id>/user/<int:uid>')
@login_required
def answer_question_set_get(set_id, uid):
  question_set = QuestionSet.query.filter_by(id=set_id).first()

  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))

  if question_set.is_public:
    question_set.is_public_label = "public"
  if question_set.is_public:
    question_set.is_public_label = "private"

  question_set_user = QuestionSetUser.query.filter_by(question_set_id=set_id, user_id=uid).first()
  if question_set_user is None:
    return redirect(url_for('main.not_auth'))

  questions = __get_question_set_with_answers(question_set_user)

  return render_template(
    'answer-question-set.html',
    set_id=set_id,
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

  unanswered_count = len(manual_questions) + len(multichoice_questions) + len(voting_questions)
  for question in manual_questions:
    answer = UserManualQuestion.query.filter_by(
      manual_question=question,
      question_set_user_id=question_set_user.id
    ).first()
    if answer:
      question.answer = answer
      unanswered_count = unanswered_count-1

  for question in multichoice_questions:
    question.options = MultichoiceOption.query.filter_by(multichoice_question=question.id).all()
    answer = UserMultichoiceQuestion.query.filter_by(
      multichoice_question=question,
      question_set_user_id=question_set_user.id
    ).first()
    if answer:
      question.answer = answer
      unanswered_count = unanswered_count-1

  for question in voting_questions:
    question.options = VotingOption.query.filter_by(voting_question=question.id).all()
    answer = UserVotingQuestion.query.filter_by(
      voting_question=question,
      question_set_user_id=question_set_user.id
    ).first()
    if answer:
      question.answer = answer
      unanswered_count = unanswered_count-1

  return {
    "multichoice_questions": multichoice_questions,
    "manual_questions": manual_questions,
    "voting_questions": voting_questions,
    "unanswered_questions_count": unanswered_count
  }

@answer_question_set.route('/question-set/<int:set_id>/manual-question/<int:question_id>/answer/', methods=['POST'])
@login_required
def answer_manual_question(set_id, question_id):
  user = current_user
  manual_question = ManualQuestion.query.filter_by(
    id=question_id
  ).first()
  question_set = QuestionSet.query.filter_by(
    id=set_id
  ).first()
  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))
  
  question_set_user = QuestionSetUser.query.filter_by(
    user_id=current_user.id,
    question_set_id=set_id
  ).first()

  if question_set_user is None:
    return redirect(url_for('main.not_auth'))
  
  user_manual_question = UserManualQuestion.query.filter_by(
    manual_question_id=manual_question.id,
    question_set_user_id=question_set_user.id
  ).first()

  if user_manual_question is not None:
    raise InvalidUsage('This questions has been answered.')

  try:
    answer = request.form.get('answer')
    user_manual_question = UserManualQuestion(
      manual_question_id=manual_question.id,
      question_set_user_id=question_set_user.id,
      answer=answer
    )
    db.session.add(user_manual_question)
    db.session.commit()
  except:
    raise InvalidUsage('An error occur while updating.')

  response = jsonify({
    "answer": answer
  })
  response.status_code = 200
  return response

@answer_question_set.route('/question-set/<int:set_id>/multichoice-question/<int:question_id>/answer/', methods=['POST'])
@login_required
def answer_multichoice_question(set_id, question_id):
  user = current_user
  multichoice_question = MultichoiceQuestion.query.filter_by(
    id=question_id
  ).first()
  question_set = QuestionSet.query.filter_by(
    id=set_id
  ).first()

  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))
  
  question_set_user = QuestionSetUser.query.filter_by(
    user_id=current_user.id,
    question_set_id=set_id
  ).first()

  if question_set_user is None:
    return redirect(url_for('main.not_auth'))
  
  multichoice_option_id = request.form.get('answer')
  user_multichoice_question = UserMultichoiceQuestion.query.filter_by(
    multichoice_question_id=multichoice_question.id,
    multichoice_option_id=multichoice_option_id,
    question_set_user_id=question_set_user.id
  ).first()

  if user_multichoice_question is not None:
    raise InvalidUsage('This questions has been answered.')
  print("So far so good")
  try:
    user_multichoice_question = UserMultichoiceQuestion(
      multichoice_question_id=multichoice_question.id,
      multichoice_option_id=multichoice_option_id,
      question_set_user_id=question_set_user.id
    )
    db.session.add(user_multichoice_question)
    db.session.commit()
  except:
    raise InvalidUsage('An error occur while updating.')

  response = jsonify({
    "answer": user_multichoice_question.id
  })
  response.status_code = 200
  return response

@answer_question_set.route('/question-set/<int:set_id>/voting-question/<int:question_id>/answer/', methods=['POST'])
@login_required
def answer_voting_question(set_id, question_id):
  user = current_user
  voting_question = VotingQuestion.query.filter_by(
    id=question_id
  ).first()
  question_set = QuestionSet.query.filter_by(
    id=set_id
  ).first()

  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))
  
  question_set_user = QuestionSetUser.query.filter_by(
    user_id=current_user.id,
    question_set_id=set_id
  ).first()

  if question_set_user is None:
    return redirect(url_for('main.not_auth'))
  
  voting_option_id = request.form.get('answer')
  user_voting_question = UserVotingQuestion.query.filter_by(
    voting_question_id=voting_question.id,
    voting_option_id=voting_option_id,
    question_set_user_id=question_set_user.id
  ).first()

  if user_voting_question is not None:
    raise InvalidUsage('This questions has been answered.')
  print("So far so good")
  try:
    user_voting_question = UserVotingQuestion(
      voting_question_id=voting_question.id,
      voting_option_id=voting_option_id,
      question_set_user_id=question_set_user.id
    )
    db.session.add(user_voting_question)
    db.session.commit()
  except:
    raise InvalidUsage('An error occur while updating.')

  response = jsonify({
    "answer": user_voting_question.id
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

@answer_question_set.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response