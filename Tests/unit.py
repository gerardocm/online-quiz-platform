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

    def test_pw_hash(self):
        u = User.query.filter_by(email='T1Testerson@gmail.com').first()
        # Check the password has been hashed from the original
        self.assertFalse(u.password=='password123')
        # Check against similar password
        self.assertFalse(u.password==generate_password_hash('passwOrd123', method='sha256'))

# Create question set (successful)
# Create MCQ question with options (successful)
# Create Voting question with options (successful)
# Create Free text question with options (successful)
# Create MCQ question without valid question set (unsuccessful)
# Create Voting question without valid question set (unsuccessful)
# Create Free text question without valid question set (unsuccessful)
# Update MCQ question with options (successful)
# Update Voting question with options (successful)
# Update Free text question with options (successful)
# Delete MCQ question with options (successful)
# Delete Voting question with options (successful)
# Delete Free text question with options (successful)

if __name__ == '__main__':
    unittest.main(verbosity=2)