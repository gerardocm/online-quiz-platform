import unittest, os, time
from onlinequiz import onlinequiz, db
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

  def setUp(self):
    self.driver = webdriver.Chrome(executable_path=os.path.join(basedir,'chromedriver'))
    if not self.driver:
      self.skipTest
    else:
      db.init_app(onlinequiz)
      db.create_all()
      db.session.query(User).delete()
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
      db.session.dropall()

  def test_login(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[@href="/login"]')
    login_page.click()
    time.sleep(1)

    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    submit = self.driver.find_element_by_id('submit')

    email_field.send_keys('T1Testerson@gmail.com')
    password_field.send_keys('password123')
    submit.click()
    time.sleep(1)

    current_url = self.driver.getCurrentUrl()
    self.assertEqual(current_url, 'http://localhost:5000/')

  def test_login_fail(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[@href="/login"]')
    login_page.click()
    time.sleep(1)

    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    submit = self.driver.find_element_by_id('submit')

    email_field.send_keys('T1Testerson@gmail.com')
    password_field.send_keys('notactualPassword')
    submit.click()
    time.sleep(1)

    flashed_message = self.driver.find_element_by_class.innerHTML('alert alert-danger')
    self.assertEqual(flashed_message, 'Please check your login details and try again.')

  def test_logout(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[@href="/login"]')
    login_page.click()
    time.sleep(1)

    email_field = self.driver.find_element_by_id('email')
    password_field = self.driver.find_element_by_id('password')
    submit = self.driver.find_element_by_id('submit')

    email_field.send_keys('T1Testerson@gmail.com')
    password_field.send_keys('password123')
    submit.click()
    time.sleep(1)

    current_url = self.driver.getCurrentUrl()

    if (current_url == 'http://localhost:5000/'):
        self.driver.get('http://localhost:5000/logout')
        time.sleep(1)

    login_html = self.driver.find_element_by_xpath.innerHTML('//a[@href="/login"]')
    self.assertEqual(login_html, 'Login')

  def test_signup(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[@href="/signup"]')
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

    first_name_field.send_keys(new_user_first_name)
    last_name_field.send_keys(new_user_last_name)
    email_field.send_keys(new_user_email)
    password_field.send_keys(new_user_password)
    confirm_password_field.send_keys(new_user_password)
    submit.click()
    time.sleep(1)

    current_url = self.driver.getCurrentUrl()
    self.assertEqual(current_url, 'http://localhost:5000/quizzes')

  def test_signup_confirm_password_wrong(self):
    self.driver.get('http://localhost:5000')
    time.sleep(1)
    login_page = self.driver.find_element_by_xpath('//a[@href="/signup"]')
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

    flashed_message = self.driver.find_element_by_class.innerHTML('invalid-feedback')
    self.assertEqual(flashed_message, 'Field must be equal to password.')

# http://localhost:5000/

# alert alert-danger
if __name__=='__main__':
  unittest.main(verbosity=2)