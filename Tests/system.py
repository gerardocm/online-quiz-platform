import unittest, os, time
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
from selenium import webdriver
basedir = os.path.abspath(os.path.dirname(__file__))

class SystemTest(unittest.TestCase):
  driver = None
  test_app = None

  def create_app(self):
      # pass in test configuration
      return create_test_app(self)

  def setUp(self):
    # MacOS path
    self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    # Windows local path
    # self.driver = webdriver.Chrome(executable_path=os.path.join(basedir,'chromedriver'))
    if not self.driver:
      self.skipTest
    else:
      self.test_app = create_test_app()
      with self.test_app.app_context():
        #db.init_app(onlinequiz)
        db.drop_all()
        db.create_all()
        db.session.query(User).delete()
        db.session.commit()
        db.session.remove()
        db.session.commit()
        user1 = User(first_name='TestOne', last_name='Testerson', email='T1Testerson@gmail.com', password=generate_password_hash('password123', method='sha256'))
              # Password field from auth.py
        db.session.add(user1)
        db.session.commit()

        self.driver.maximize_window()
        self.driver.get('http://localhost:5000/')

  def tearDown(self):
    if self.driver:
      self.driver.close()
      db.session.remove()
      db.drop_all()


  def test_login(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[contains(@href,"login")]')
    login_page.click()
    time.sleep(1)

    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    submit = self.driver.find_element_by_id('submit')

    email_field.send_keys('T1Testerson@gmail.com')
    password_field.send_keys('password123')
    submit.click()
    time.sleep(1)
    
    self.assertEqual(self.driver.current_url, 'http://localhost:5000/quizzes')

  def test_login_fail(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[contains(@href,"login")]')
    login_page.click()
    time.sleep(1)

    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    submit = self.driver.find_element_by_id('submit')

    email_field.send_keys('T1Testerson@gmail.com')
    password_field.send_keys('notactualPassword')
    submit.click()
    time.sleep(1)

    flashed_message = self.driver.find_element_by_xpath('//div[@role="alert"]').text
    self.assertEqual(flashed_message, 'Please check your login details and try again.')

  def test_logout(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[contains(@href,"login")]')
    login_page.click()
    time.sleep(1)

    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    submit = self.driver.find_element_by_id('submit')

    email_field.send_keys('T1Testerson@gmail.com')
    password_field.send_keys('password123')
    submit.click()
    time.sleep(1)

    if (self.driver.current_url == 'http://localhost:5000/quizzes'):
        self.driver.get('http://localhost:5000/logout')
        time.sleep(1)

    login_html = self.driver.find_element_by_xpath('//a[contains(@href,"login")]').text
    self.assertEqual(login_html, 'Login')

  def test_signup_confirm_password_wrong(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[contains(@href,"signup")]')
    login_page.click()
    time.sleep(1)

    first_name_field = self.driver.find_element_by_id('first_name')
    last_name_field = self.driver.find_element_by_id('last_name')
    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    confirm_password_field = self.driver.find_element_by_id('password_confirm')
    submit = self.driver.find_element_by_id('submit')

    new_user_first_name = 'New'
    new_user_last_name = 'User'
    new_user_email = 'new.user@fake_email.com'
    new_user_password = 'poorpassword'
    new_user_wrong_confirm_password = 'notthesamepassword'

    first_name_field.send_keys(new_user_first_name)
    last_name_field.send_keys(new_user_last_name)
    email_field.send_keys(new_user_email)
    password_field.send_keys(new_user_password)
    confirm_password_field.send_keys(new_user_wrong_confirm_password)
    submit.click()
    time.sleep(1)

    flashed_message = self.driver.find_element_by_class_name('invalid-feedback').text
    self.assertEqual(flashed_message, 'Field must be equal to password.')


  def test_signup(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[contains(@href,"signup")]')
    login_page.click()
    time.sleep(1)

    first_name_field = self.driver.find_element_by_id('first_name')
    last_name_field = self.driver.find_element_by_id('last_name')
    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    confirm_password_field = self.driver.find_element_by_id('password_confirm')
    submit = self.driver.find_element_by_id('submit')

    new_user_first_name = 'New'
    new_user_last_name = 'User'
    new_user_email = 'new.user1@fake_email.com'
    new_user_password = 'poorpassword'

    first_name_field.send_keys(new_user_first_name)
    last_name_field.send_keys(new_user_last_name)
    email_field.send_keys(new_user_email)
    password_field.send_keys(new_user_password)
    confirm_password_field.send_keys(new_user_password)
    submit.click()
    time.sleep(1)

    self.assertEqual(self.driver.current_url, 'http://localhost:5000/quizzes')

if __name__=='__main__':
  unittest.main(verbosity=2)