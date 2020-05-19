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

create_question_set = Blueprint('create_question_set', __name__)

@create_question_set.route('/create-question-set')
@login_required
def question_set():
  form = QuestionSetForm()
  return render_template(
    'create-question-set.html',
    form=form,
    cuser=current_user
  )

@create_question_set.route('/create-question-set', methods=['POST'])
@login_required
def question_set_post():
  name = request.form.get('name')
  is_public = True if request.form.get('is_public') is not None else False
  # date = request.form.get('due_date')
  form = QuestionSetForm()
  if not form.validate_on_submit():
    flash('There was an error while creating the question set.')
    return render_template(
      'create-question-set.html',
      form=form,
      cuser=current_user
    )

  try:
    new_question_set = QuestionSet(
      name=name,
      is_public=is_public,
      owner =current_user.id
    )
    db.session.add(new_question_set)
    db.session.commit()
  except IntegrityError:
    flash('There was an error while saving your question set')
    return render_template(
      'create-question-set.html',
      form=form,
      cuser=current_user
    )

  return redirect(url_for('create_question_set.question_set_update',set_id=new_question_set.id))


@create_question_set.route('/create-question-set/<int:set_id>')
@login_required
def question_set_update(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  if question_set.submitted is True:
    return redirect(url_for('admin_question_set.admin_question_set_get', set_id=set_id))

  form = QuestionSetForm(
    name=question_set.name,
    is_public=question_set.is_public
  )
  questions = __get_full_question_set(set_id)
  return render_template(
    'create-question-set.html',
    form=form,
    set_id=set_id,
    questions=questions,
    cuser=current_user
  )

def __get_full_question_set(set_id):
  multichoice_questions = MultichoiceQuestion.query.filter_by(question_set=set_id).all()
  manual_questions = ManualQuestion.query.filter_by(question_set=set_id).all()
  voting_questions = VotingQuestion.query.filter_by(question_set=set_id).all()
  for question in multichoice_questions:
    question.options = MultichoiceOption.query.filter_by(multichoice_question=question.id).all()
  for question in voting_questions:
    question.options = VotingOption.query.filter_by(voting_question=question.id).all()

  return {
    "multichoice_questions": multichoice_questions,
    "manual_questions": manual_questions,
    "voting_questions": voting_questions
  }

@create_question_set.route('/create-question-set/<int:set_id>', methods=['POST'])
@login_required
def question_set_update_post(set_id):

  form = QuestionSetForm()
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  try:
    name = request.form.get('name')
    is_public = True if request.form.get('is_public') is not None else False
    question_set.name = name
    question_set.is_public = is_public
    db.session.commit()
  except:
    raise InvalidUsage('There was an error while updating the set.')

  response = jsonify({
    'id': question_set.id,
    'name': question_set.name
  })
  response.status_code = 200
  return response

@create_question_set.route('/create-question-set/<int:set_id>/submit', methods=['PUT'])
@login_required
def question_set_submit(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  try:
    question_set.submitted = True
    db.session.commit()
  except:
    raise InvalidUsage('There was an error while updating the set.')

  response = jsonify({
    'id': question_set.id,
    'submitted': question_set.submitted
  })
  response.status_code = 200
  return response

@create_question_set.route('/create-question-set/<int:set_id>/multichoice-question')
@login_required
def multichoice_question(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  form = QuestionForm(question_set=question_set.id)
  return render_template('forms/multichoice-question.html', form=form)

@create_question_set.route('/create-question-set/<int:set_id>/multichoice-question', methods=['POST'])
@login_required
def multichoice_question_post(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  question = request.form.get('question')
  options = json.loads(request.form.get('options').replace("'", "\""))
  form = QuestionForm(question=question)
  if not question:
    raise InvalidUsage('There was an error while creating the quiz set.')
  for option in options:
    if not option['option']:
      raise InvalidUsage('There was an error while creating the quiz set.')

  try:
    new_question = MultichoiceQuestion(
      question=question,
      question_set=set_id
    )
    db.session.add(new_question)
    db.session.commit()
    for option in options:
      new_option = MultichoiceOption(
        option=option['option'],
        is_correct=option['is_correct'],
        multichoice_question=new_question.id
      )
      db.session.add(new_option)
      db.session.commit()
  except:
    raise InvalidUsage('There was an error while creating the quiz set.')

  response = jsonify({
    'id': new_question.id,
    'question': new_question.question
  })
  response.status_code = 200
  return response

@create_question_set.route('/create-question-set/<int:set_id>/multichoice-question/<int:question_id>', methods=['DELETE'])
@login_required
def multichoice_question_delete(set_id, question_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  question = MultichoiceQuestion.query.filter_by(id=question_id).first()
  if question is None:
    raise InvalidUsage('Multichoice question not found.', status_code=500)

  options = MultichoiceOption.query.filter_by(multichoice_question=question.id).all()
  for option in options:
    db.session.delete(option)
    db.session.commit()
  
  db.session.delete(question)
  db.session.commit()
  response = jsonify({})
  response.status_code = 200
  return response

@create_question_set.route('/create-question-set/<int:set_id>/manual-question')
@login_required
def manual_question(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  form = QuestionForm()
  return render_template('forms/manual-question.html', form=form)

@create_question_set.route('/create-question-set/<int:set_id>/manual-question', methods=['POST'])
@login_required
def manual_question_post(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  form = QuestionForm(request.form)
  if not form.validate_on_submit():
    raise InvalidUsage('There was an error while creating the quiz set.')

  try:
    question = request.form.get('question')
    new_question = ManualQuestion(
      question=question,
      question_set=set_id
    )
    db.session.add(new_question)
    db.session.commit()
  except e:
    raise InvalidUsage('There was an error while creating the quiz set.')

  response = jsonify({
    'id': new_question.id,
    'question': new_question.question
  })
  response.status_code = 200
  return response

@create_question_set.route('/create-question-set/<int:set_id>/manual-question/<int:question_id>', methods=['DELETE'])
@login_required
def manual_question_delete(set_id, question_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  question = ManualQuestion.query.filter_by(id=question_id).first()
  if question is None:
    raise InvalidUsage('Manual question not found.', status_code=500)
  
  db.session.delete(question)
  db.session.commit()
  response = jsonify({})
  response.status_code = 200
  return response


@create_question_set.route('/create-question-set/<int:set_id>/voting-question')
@login_required
def voting_question(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  form = QuestionForm(question_set=question_set.id)
  return render_template('forms/voting-question.html', form=form)

@create_question_set.route('/create-question-set/<int:set_id>/voting-question', methods=['POST'])
@login_required
def voting_question_post(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  question = request.form.get('question')
  options = json.loads(request.form.get('options').replace("'", "\""))
  form = QuestionForm(question=question)
  if not question:
    raise InvalidUsage('There was an error while creating the quiz set.')
  for option in options:
    if not option['option']:
      raise InvalidUsage('There was an error while creating the quiz set.')

  try:
    new_question = VotingQuestion(
      question=question,
      question_set=set_id
    )
    db.session.add(new_question)
    db.session.commit()
    for option in options:
      new_option = VotingOption(
        option=option['option'],
        voting_question=new_question.id
      )
      db.session.add(new_option)
      db.session.commit()
  except:
    raise InvalidUsage('There was an error while creating the quiz set.')

  response = jsonify({
    'id': new_question.id,
    'question': new_question.question
  })
  response.status_code = 200
  return response

@create_question_set.route('/create-question-set/<int:set_id>/voting-question/<int:question_id>', methods=['DELETE'])
@login_required
def voting_question_delete(set_id, question_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  question = VotingQuestion.query.filter_by(id=question_id).first()
  if question is None:
    raise InvalidUsage('Voting question not found.', status_code=500)

  options = VotingOption.query.filter_by(voting_question=question.id).all()
  for option in options:
    db.session.delete(option)
    db.session.commit()
  
  db.session.delete(question)
  db.session.commit()
  response = jsonify({})
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

@create_question_set.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response