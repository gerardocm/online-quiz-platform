import unittest, os
from onlinequiz import create_test_app, db
from werkzeug.security import generate_password_hash
from onlinequiz.models import (
  User,
  QuestionSetUser,
  QuestionSet,
  ManualQuestion,
  MultichoiceQuestion,
  MultichoiceOption,
  VotingQuestion,
  VotingOption
)

class UserModelTest(unittest.TestCase):
    test_app = None

    def create_app(self):
        # pass in test configuration
        return create_test_app(self)

    def setUp(self):
        self.test_app = create_test_app()
        with self.test_app.app_context():
            db.create_all()
            user1 = User(first_name='TestOne', last_name='Testerson', email='T1Testerson@gmail.com', password=generate_password_hash('password123', method='sha256'))
            # Password field from auth.py
            db.session.add(user1)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        
## Helper Functions ##
    def signup(self, first_name, last_name, email, password):
        return self.test_app.post(
            '/signup',
            data=dict(first_name=first_name, last_name=last_name, email=email, password=password),
            follow_redirects=True
        )
 
    def login(self, email, password):
        return self.test_app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )
 
    def logout(self):
        return self.test_app.get(
            '/logout',
            follow_redirects=True
        )
## auth.py
    def test_pw_hash(self):
        u = User.query.filter_by(email='T1Testerson@gmail.com').first()
        # Check the password has been hashed from the original
        self.assertFalse(u.password=='password123')
        # Check the password hash can be replicated
        self.assertTrue(u.password==generate_password_hash('password123', method='sha256'))
        # Check against similar password
        self.assertFalse(u.password==generate_password_hash('passwOrd123', method='sha256'))

    def test_signup_same_email(self):
        response = self.signup('Tester', 'Testoforsson', 'T1Testerson@gmail.com', 'pw')
        self.assertIn(b'Email address already exists', response.data)

    def test_login_diff_password(self):
        response = self.login('T1Testerson@gmail.com', 'password123')
        self.assertIn(b'Please check your login details and try again.', response.data)

# class SystemTest(unittest.TestCase):
#     driver = None

#     def setUp(self):
#         sel.driver = webDriver(Chrome(executable_path=))


if __name__ == '__main__':
    unittest.main(verbosity=2)