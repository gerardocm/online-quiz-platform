from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = '589ac1807dbcda5df05d017c4903fbd3'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'

  db.init_app(app)

  # blueprint for auth routes in the app
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  # blueprint for auth routes in the app
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  # blueprint for create question set in the app
  from .create_question_set import create_question_set as create_question_set_blueprint
  app.register_blueprint(create_question_set_blueprint)

  # blueprint for admin question set in the app
  from .admin_question_set import admin_question_set as admin_question_set_blueprint
  app.register_blueprint(admin_question_set_blueprint)

  # blueprint for answer question set in the app
  from .answer_question_set import answer_question_set as answer_question_set_blueprint
  app.register_blueprint(answer_question_set_blueprint)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  from .models import User

  @login_manager.user_loader
  def load_user(user_id):
      # since the user_id is just the primary key of our user table, use it in the query for the user
      return User.query.get(int(user_id))

  return app
