from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignUpForm(FlaskForm):
  first_name = StringField(
    'First Name', 
    validators=[DataRequired(), Length(min=3, max=25)]
  )
  last_name = StringField(
    'Last Name', 
    validators=[DataRequired(), Length(min=3, max=25)]
  )
  email = StringField(
    'Email', 
    validators=[DataRequired(), Length(min=3)]
  )
  password = PasswordField(
    'Password', 
    validators=[DataRequired(), Length(min=8, max=25)]
  )
  password_confirm = PasswordField(
    'Confirm Password', 
    validators=[DataRequired(), Length(min=8, max=25), EqualTo('password')]
  )
  submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
  email = StringField(
    'Email', 
    validators=[DataRequired(), Length(min=3)]
  )
  password = PasswordField(
    'Password', 
    validators=[DataRequired(), Length(min=8, max=25)]
  )
  submit = SubmitField('Login')

class QuestionSetForm(FlaskForm):
  name = StringField(
    'Name', 
    validators=[DataRequired(), Length(min=3, max=35)]
  )
  is_public = BooleanField(
    'Public question set', 
  )
  due_date = DateTimeField(
    'Due date'
  )
  submit = SubmitField('Create')

class QuestionForm(FlaskForm):
  question = StringField(
    'Question', 
    validators=[DataRequired(), Length(min=3, max=100)]
  )
  submit = SubmitField('Save')