from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from onlinequiz.forms import QuestionSetForm
from onlinequiz.models import QuestionSet
from onlinequiz import db
from sqlalchemy.exc import IntegrityError


main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template('index.html')

@main.route('/not-authorized')
def not_auth():
  return render_template('not-authorized.html')

@main.route('/quizzes')
@login_required
def quizzes():
  full_name = current_user.first_name + current_user.last_name
  return render_template('quizzes.html', full_name=full_name)


@main.route('/create-question-set')
@login_required
def question_set():
  form = QuestionSetForm()
  print("get")
  return render_template('create-question-set.html', title='Create a new quiz set', form=form)

@main.route('/create-question-set', methods=['POST'])
@login_required
def question_set_post():
  name = request.form.get('name')
  print(request.form.get('is_public'))
  is_public = True if request.form.get('is_public') is not None else False
  # date = request.form.get('due_date')
  form = QuestionSetForm()
  if not form.validate_on_submit():
    flash('There was an error while creaating the quiz set.')
    return render_template('create-question-set.html', title='Create a new quiz set', form=form)

  try:
    new_question_set = QuestionSet(
      name=name,
      is_public=is_public,
      owner =current_user.id
    )
    db.session.add(new_question_set)
    db.session.commit()
    print(new_question_set.id)
  except IntegrityError:
    flash('There was an error while saving your question set')
    return render_template('create-question-set.html', title='Create a new quiz set', form=form)

  return redirect(url_for('main.question_set_update',set_id=new_question_set.id))


@main.route('/create-question-set/<int:set_id>')
@login_required
def question_set_update(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))

  form = QuestionSetForm(
    name=question_set.name,
    is_public=question_set.is_public
  )
  return render_template('create-question-set.html', title='Create a new quiz set', form=form, set_id=set_id)

@main.route('/create-question-set/<int:set_id>', methods=['POST'])
@login_required
def question_set_update_post(set_id):
  form = QuestionSetForm()
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))
  return render_template('create-question-set.html', title='Create a new quiz set', form=form, set_id=set_id)

@main.route('/create-question-set/<int:set_id>/multichoice-question')
@login_required
def multichoice_question(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))
  return render_template('create-multichoice-question.html')

@main.route('/create-question-set/<int:set_id>/manual-question')
@login_required
def manual_question(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))
  return render_template('create-manual-question.html')

@main.route('/create-question-set/<int:set_id>/voting-question')
@login_required
def voting_question(set_id):
  question_set = QuestionSet.query.filter_by(id=set_id).first()
  if question_set.owner != current_user.id:
    return redirect(url_for('main.not_auth'))
  return render_template('create-voting-question.html')