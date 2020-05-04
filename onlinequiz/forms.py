from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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