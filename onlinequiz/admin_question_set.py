from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from onlinequiz.forms import QuestionSetForm, QuestionForm
from onlinequiz.models import (
  User,
  QuestionSet,
  QuestionSetUser
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
  print("users")
  print(users)
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