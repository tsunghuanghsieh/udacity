import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, PUT, POST, PATCH, DELETE, OPTIONS")
    return response

  @app.route("/categories")
  def get_categories():
    # {
    #    "1": "Science",
    #    "2": "Art",
    #    "3": "Geography",
    #    "4": "History",
    #    "5": "Entertainment",
    #    "6": "Sports"
    #  }
    categories = Category.query.all()
    categories_list = { category.id: category.type for category in categories }

    return jsonify({
      "success": True,
      "categories": categories_list
    })

  @app.route('/questions')
  def get_questions():
    categories = Category.query.all()
    categories_list = { category.id: category.type for category in categories }
    questions = Question.query.all()
    questions_array = [ question.format() for question in questions ]
    page = request.args.get("page", 1, type = int)
    page = page if (page >= 1) else 1 # handle page is 0 or negative
    start = (page - 1) * QUESTIONS_PER_PAGE
    return jsonify({
      "success": True,
      "questions": questions_array[start:start + QUESTIONS_PER_PAGE],
      "total_questions": len(questions_array),
      "categories": categories_list,
      "currentCategory": 3 # TODO Change mes
    })

  @app.route('/questions/<int:question_id>', methods = [ "DELETE" ])
  def delete_questions(question_id):
    error_success = 200
    try:
      question = Question.query.get(question_id)
      if (question is None):
        raise FileNotFoundError()
      question.delete()
      return jsonify({
        "success": True,
        "deleted": question_id
      })
    except FileNotFoundError as e:
      abort(404)

  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route("/questions", methods = [ "POST" ])
  def add_question():
    body = request.get_json()
    if (body is None):
      abort(400)
    try:
      question = Question(
        body.get('question'),
        body.get('answer'),
        body.get('category'),
        body.get('difficulty'))
      question.insert()
      return jsonify({
        "success": True,
        "created": question.id
      })
    except:
      print('except')

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route("/categories/<int:cat_id>/questions")
  def get_questions_by_category(cat_id):
    questions = Question.query.filter(Question.category == cat_id).all()
    formatted_questions = [ question.format() for question in questions ]
    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "currentCategory": cat_id
    })

  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  @app.errorhandler(400)
  def handle_bad_request(err):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400

  @app.errorhandler(404)
  def handle_not_found(err):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not Found"
    }), 404

  @app.errorhandler(405)
  def handle_method_not_allowed(err):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(422)
  def handle_unprocessable_entity(err):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Entity"
    }), 422

  return app

