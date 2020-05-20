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

result_question_set = Blueprint('result_question_set', __name__)

@result_question_set.route('/result-question-set/<int:set_id>/user/<int:uid>')
@login_required
def result_question_set_get(set_id, uid):
  question_set = QuestionSet.query.filter_by(id=set_id).first()

  if question_set.submitted is False:
    return redirect(url_for('create_question_set.question_set_update', set_id=set_id))

  if question_set.is_public:
    question_set.is_public_label = "public"
  if not question_set.is_public:
    question_set.is_public_label = "private"

  question_set_user = QuestionSetUser.query.filter_by(question_set_id=set_id, user_id=uid).first()
  print(question_set.owner)
  print(uid)
  if question_set_user is None or \
    (current_user.id != uid and \
    question_set.owner != current_user.id):
    return redirect(url_for('main.not_auth'))

  questions = __get_question_set_with_answers(question_set_user)

  return render_template(
    'result-question-set.html',
    set_id=set_id,
    question_set=question_set,
    questions=questions,
    cuser=current_user,
    uid=uid
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
    total_votes = UserVotingQuestion.query.filter_by(
      voting_question=question
    ).count()
    question.total_votes = total_votes
    for option in question.options:
      votes = UserVotingQuestion.query.filter_by(
        voting_question=question,
        # question_set_user_id=question_set_user.id,
        voting_option_id=option.id
      ).count()
      if total_votes > 0 and votes > 0:
        option.votes_percent = int((votes * 100) / total_votes)
        option.votes = votes
      else:
        option.votes_percent = 0
        option.votes = votes

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