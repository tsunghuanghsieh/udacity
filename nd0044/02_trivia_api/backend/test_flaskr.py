import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """Test GET Retrieve All Categories"""
        categories = {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'}
        endpoint = "/categories"
        response = self.client().get(endpoint)
        data = json.loads(response.data)
        # data['categories'][id] to access value
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['categories'], categories)

    def test_get_questions(self):
        """Test GET Retrieve All Questions"""
        endpoint = "/questions"
        response = self.client().get(endpoint)
        data = json.loads(response.data)
        self.assertTrue("success")

    def test_delete_existing_question(self):
        """Test DELETE Existing Question"""
        # set up
        question = Question("Question 1", "Answer 1", 1, 1)
        question.insert()

        question_id = question.id
        endpoint = "/questions/{}".format(question_id)
        response = self.client().delete(endpoint)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

    def test_delete_nonexisting_question(self):
        """Test DELETE Non Existing Question"""
        question_id = 1
        endpoint = "/questions/{}".format(question_id)
        response = self.client().delete(endpoint)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_or_search_question(self):
        """Test POST Add A Question W JSON"""
        jsonbody = {
            "question": "question",
            "answer": "answer",
            "category": 3,
            "difficulty": 3
        }
        endpoint = "/questions"
        response = self.client().post(endpoint, json = jsonbody)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        print("created")
        print(data['created'])
        # Tear down
        question = Question.query.get(data['created'])
        question.delete()

    def test_add_or_search_question_no_body(self):
        """Test POST No JSON"""
        endpoint = "/questions"
        response = self.client().post(endpoint)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])

    def test_add_or_search_question_no_body(self):
        """Test POST Search Questions W JSON"""
        # set up
        question = Question("What's my name", "IYKYK", 5, 1)
        question.insert()

        jsonbody = {
            "searchTerm": "my name"
        }
        endpoint = "/questions"
        response = self.client().post(endpoint, json = jsonbody)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 1) # it can be only 1
        self.assertEqual(data['questions'][0]['answer'], "IYKYK")

        # tear down
        question = Question.query.filter(Question.answer.match("IYKYK")).all()
        question[0].delete()

    def test_get_questions_by_category(self):
        """Test GET List Questions By Category"""
        cat_id = 1
        endpoint = "/categories/{}/questions".format(cat_id)
        response = self.client().get(endpoint)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['currentCategory'], cat_id)

    def test_play_quiz(self):
        """Test POST Play Quiz"""
        jsonbody = {
            "previous_questions": [],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }
        endpoint = "/quizzes"
        response = self.client().post(endpoint, json = jsonbody)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['previous_questions']), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()