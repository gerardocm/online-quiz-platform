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
            # Create user
            user1 = User(first_name='TestOne', last_name='Testerson', email='T1Testerson@gmail.com', password=generate_password_hash('password123', method='sha256'))
            db.session.add(user1)
            db.session.commit()
            # Create test question set
            questionSet1 = QuestionSet(name='Test Question Set', owner=1, is_public=True, submitted=True)
            db.session.add(questionSet1)
            db.session.commit()
            # MCQ
            # Create test mcq question
            testQ1 = MultichoiceQuestion(question_set=1, question='Is this question number 1?')
            db.session.add(testQ1)
            db.session.commit()
            # Add test mcq answers
            Q1ans1 = MultichoiceOption(option='option #1', multichoice_question=1)
            Q1ans2 = MultichoiceOption(option='option #2', multichoice_question=1, is_correct=True)
            Q1ans3 = MultichoiceOption(option='option #3', multichoice_question=1)
            db.session.add(Q1ans1)
            db.session.add(Q1ans2)
            db.session.add(Q1ans3)
            db.session.commit()
            # Voting
            # Create test voting question
            testQ2 = VotingQuestion(question_set=1, question='Is this voting question number 1?')
            db.session.add(testQ2)
            db.session.commit()
            # Add test answers
            Q2ans1 = VotingOption(option='option #1', voting_question=1)
            Q2ans2 = VotingOption(option='option #2', voting_question=1)
            Q2ans3 = VotingOption(option='option #3', voting_question=1)
            db.session.add(Q2ans1)
            db.session.add(Q2ans2)
            db.session.add(Q2ans3)
            db.session.commit()
            # Manual
            # Add test question
            testQ3 = ManualQuestion(question_set=1, question='Is this manual question number 1?')
            db.session.add(testQ3)
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

    def test_create_questionset(self):
        # Add the question set
        qs1 = QuestionSet(name='Qs1', owner=1, is_public=True, submitted=True)
        db.session.add(qs1)
        db.session.commit()
        # Query the question set
        q = QuestionSet.query.filter_by(name='Qs1').first()
        self.assertTrue(q.name=='Qs1')
    
    def test_create_mcq_question(self):
        # Add test question
        testQ2 = MultichoiceQuestion(question_set=1, question='Is this question number 2?')
        db.session.add(testQ2)
        db.session.commit()
        # Add test answers
        Q2ans1 = MultichoiceOption(option='option #1', multichoice_question=2)
        Q2ans2 = MultichoiceOption(option='option #2', multichoice_question=2, is_correct=True)
        Q2ans3 = MultichoiceOption(option='option #3', multichoice_question=2)
        db.session.add(Q2ans1)
        db.session.add(Q2ans2)
        db.session.add(Q2ans3)
        db.session.commit()
        # Check question was created
        q = MultichoiceQuestion.query.filter_by(question='Is this question number 2?').first()
        self.assertTrue(q.question=='Is this question number 2?')
        # Check option count
        numberOfOptions = MultichoiceOption.query.filter_by(multichoice_question='2').count()
        self.assertTrue(numberOfOptions==3)
    
    def test_create_voting_question(self):
        # Add test question
        testQ2 = VotingQuestion(question_set=1, question='Is this voting question number 2?')
        db.session.add(testQ2)
        db.session.commit()
        # Add test answers
        Q2ans1 = VotingOption(option='option #1', voting_question=2)
        Q2ans2 = VotingOption(option='option #2', voting_question=2)
        Q2ans3 = VotingOption(option='option #3', voting_question=2)
        db.session.add(Q2ans1)
        db.session.add(Q2ans2)
        db.session.add(Q2ans3)
        db.session.commit()
        # Check question was created
        q = VotingQuestion.query.filter_by(question='Is this voting question number 2?').first()
        self.assertTrue(q.question=='Is this voting question number 2?')
        # Check option count
        numberOfOptions = VotingOption.query.filter_by(voting_question='2').count()
        self.assertTrue(numberOfOptions==3)
    
    def test_create_manual_question(self):
        # Add test question
        testQ2 = ManualQuestion(question_set=1, question='Is this manual question number 2?')
        db.session.add(testQ2)
        db.session.commit()
        # Check question was created
        q = ManualQuestion.query.filter_by(question='Is this manual question number 2?').first()
        self.assertTrue(q.question=='Is this manual question number 2?')
    
    def test_delete_mcq_question(self):
        # Delete question
        question = MultichoiceQuestion.query.filter_by(id=1).first()
        if question is None:
            raise InvalidUsage('Multichoice question not found.', status_code=500)

        options = MultichoiceOption.query.filter_by(multichoice_question=question.id).all()
        for option in options:
            db.session.delete(option)
            db.session.commit()
  
        db.session.delete(question)
        db.session.commit()
        # Assert deletions
        question_count = MultichoiceQuestion.query.filter_by(id=1).count()
        self.assertTrue(question_count==0)
        numberOfOptions = MultichoiceOption.query.filter_by(multichoice_question=1).count()
        self.assertTrue(numberOfOptions==0)

    def test_delete_voting_question(self):
        question = VotingQuestion.query.filter_by(id=1).first()
        if question is None:
            raise InvalidUsage('Voting question not found.', status_code=500)

        options = VotingOption.query.filter_by(voting_question=question.id).all()
        for option in options:
            db.session.delete(option)
            db.session.commit()
        
        db.session.delete(question)
        db.session.commit()
        # Assert deletions
        question_count = VotingQuestion.query.filter_by(id=1).count()
        self.assertTrue(question_count==0)
        numberOfOptions = VotingOption.query.filter_by(voting_question=1).count()
        self.assertTrue(numberOfOptions==0)
    
    def test_delete_manual_question(self):
        # Delete question
        question = ManualQuestion.query.filter_by(id=1).first()
        if question is None:
            raise InvalidUsage('Manual question not found.', status_code=500)

        db.session.delete(question)
        db.session.commit()
        # Assert deletion
        question_count = ManualQuestion.query.filter_by(id=1).count()
        self.assertTrue(question_count==0)

    def test_question_set_update(self):
        question_set = QuestionSet.query.filter_by(id=1).first()

        try:
            name = 'New Name'
            is_public = True
            question_set.name = name
            question_set.is_public = is_public
            db.session.commit()
        except:
            raise InvalidUsage('There was an error while updating the set.')

        # Query the question set
        q = QuestionSet.query.filter_by(name='New Name').first()
        self.assertTrue(q.name=='New Name')

# Create question set (successful)
# Create MCQ question with options (successful)
# Create Voting question with options (successful)
# Create Free text question with options (successful)

# Update MCQ question with options (successful)
# Update Voting question with options (successful)
# Update Free text question with options (successful)

# Delete MCQ question with options (successful)
# Delete Voting question with options (successful)
# Delete Free text question with options (successful)

if __name__ == '__main__':
    unittest.main(verbosity=2)