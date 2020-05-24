# online-quiz-platform
CITS5505 Agile Web Development /Project 2


# Steps to run
-- activate the virtual environment
-- go to main path
-- command: python run.py

# Create DB
1- Activate the virtual environmnet (if it's not activated yet)
2- Type "python" in the command line and hit enter
3- Import the modules:
    "from onlinequiz import db, create_app"
4- Create the DB:
    "db.create_all(app=create_app())"

* You should see a new file created named "quiz.db" under onlinequiz directory
* To exit the python command line type exit() and press enter

# Steps to run the unit tests
Run the command:
    python -m unittest

* Make sure you have the virtual environment acitve