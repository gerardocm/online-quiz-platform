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

all_question_sets_available = Blueprint(
    '@all_question_sets_available', __name__)


@all_question_sets_available.route('/all-question-sets-available')
@login_required
def all_question_sets():

    QuestionSet.query.delete()

    qs1 = QuestionSet(name='Qs1', owner='Cameron', is_public=True)
    db.session.add(qs1)
    db.session.commit()
    qs2 = QuestionSet(name='Qs2', owner='Cameron', is_public=True)
    db.session.add(qs2)
    db.session.commit()
    qs3 = QuestionSet(name='Qs3', owner='Cameron', is_public=True)
    db.session.add(qs3)
    db.session.commit()

    public_question_sets = QuestionSet.query.filter_by(is_public=True).all()
    user_question_sets = QuestionSet.query.filter_by(
        owner=current_user.id).all()
    return render_template('all-question-sets.html', title='All Question Sets', pqs=public_question_sets, uqs=user_question_sets)


@all_question_sets_available.route('/quiz/<int:set_id>')
def quiz_to_complete(set_id):

    question_set = QuestionSet.query.filter_by(id=set_id).all()

    MultichoiceQuestion.query.delete()
    testQ1 = MultichoiceQuestion(
        question_set=1, question='Is this question number 1?')
    testQ2 = MultichoiceQuestion(
        question_set=1, question='Is this question number 2?')
    testQ3 = MultichoiceQuestion(
        question_set=1, question='Is this question number 3?')
    db.session.add(testQ1)
    db.session.add(testQ2)
    db.session.add(testQ3)
    db.session.commit()

    MultichoiceOption.query.delete()

    Q1ans1 = MultichoiceOption(option='option #1', multichoice_question=1)
    Q1ans2 = MultichoiceOption(option='option #2', multichoice_question=1, is_correct=True)
    Q1ans3 = MultichoiceOption(option='option #3', multichoice_question=1)
    db.session.add(Q1ans1)
    db.session.add(Q1ans2)
    db.session.add(Q1ans3)
    db.session.commit()

    Q2ans1 = MultichoiceOption(option='option #1', multichoice_question=2, is_correct=True)
    Q2ans2 = MultichoiceOption(option='option #2', multichoice_question=2)
    Q2ans3 = MultichoiceOption(option='option #3', multichoice_question=2)
    db.session.add(Q2ans1)
    db.session.add(Q2ans2)
    db.session.add(Q2ans3)
    db.session.commit()

    Q3ans1 = MultichoiceOption(option='option #1', multichoice_question=3)
    Q3ans2 = MultichoiceOption(option='option #2', multichoice_question=3)
    Q3ans3 = MultichoiceOption(option='option #3', multichoice_question=3, is_correct=True)
    db.session.add(Q3ans1)
    db.session.add(Q3ans2)
    db.session.add(Q3ans3)
    db.session.commit()

    multichoice_questions = MultichoiceQuestion.query.filter_by(
        question_set=set_id).all()
    manual_questions = ManualQuestion.query.filter_by(
        question_set=set_id).all()
    voting_questions = VotingQuestion.query.filter_by(
        question_set=set_id).all()
    for question in multichoice_questions:
        question.options = MultichoiceOption.query.filter_by(
            multichoice_question=question.id).all()
    for question in voting_questions:
        question.options = VotingOption.query.filter_by(
            voting_question=question.id).all()
    return render_template('complete-quiz.html', qs=question_set, mcq=multichoice_questions, mq=manual_questions, vq=voting_questions)
