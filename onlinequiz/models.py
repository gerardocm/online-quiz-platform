from onlinequiz import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(35), nullable=False)
  last_name = db.Column(db.String(35), nullable=False)
  email = db.Column(db.String(35), unique=True, nullable=False)
  password = db.Column(db.String(25), nullable=False)
  date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  # multichoice_questions_created =  db.relationship('MultichoiceQuestion', lazy=True)
  # multichoice_questions_assigned = db.relationship('UserMultichoiceQuestion', lazy=True)

  def __repr__(self):
    return f"User('{self.email}')'"

# class MultichoiceQuestion(db.Model):
#   __tablename__ = 'MultichoiceQuestion'
#   id = db.Column(db.Integer, primary_key=True)
#   question = db.Column(db.String(100), nullable=False)
#   owner =  db.Column(db.Integer, db.ForeignKey('User.id'))
#   is_public =  db.Column(db.Boolean(), nullable=True, default=False)
#   date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#   options =  db.relationship(db.Integer, backref='options', lazy=True)

#   def __repr__(self):
#     return f"MultichoiceQuestion('{self.id}')'"

# class MultichoiceOption(db.Model):
#   __tablename__ = 'MultichoiceOption'
#   id = db.Column(db.Integer, primary_key=True)
#   option = db.Column(db.String(100), nullable=False)
#   is_correct =  db.Column(db.Boolean(), nullable=True, default=False)
#   date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#   owner = db.Column(db.Integer, db.ForeignKey('MultichoiceQuestion.id'))

#   def __repr__(self):
#     return f"MultichoiceOption('{self.id}')'"

# class UserMultichoiceQuestion(db.Model):
#   __tablename__ = 'UserMultichoiceQuestion'
#   __table_args__ = (
#     db.UniqueConstraint(
#       'user_id',
#       'multichoice_question_id',
#       'multichoice_option_id',
#       name='unique_user_multichoice_question'
#     ),
#   )
#   id = db.Column(db.Integer, primary_key=True)
#   due_date = db.Column(db.DateTime, nullable=True)
#   date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#   user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
#   multichoice_question_id = db.Column(db.Integer, db.ForeignKey('MultichoiceQuestion.id'))
#   multichoice_option_id = db.Column(db.Integer, db.ForeignKey('MultichoiceOption.id'))
#   multichoice_question = db.relationship("MultichoiceQuestion")
#   multichoice_answer = db.relationship("MultichoiceOption")

#   def __repr__(self):
#     return f"UserMultichoiceQuestion('{self.id}')'"