# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
## Endpoints
```
GET '/categories'
- Fetch a dictionary of categories
- Query String Parameter: None
- Path Parameters: None
- Request Payload: None
- Response Payload:
categories: dictionary of categories
success: status of response
{
  "success": True,
  "categories": {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
  }
}
```

```
GET '/categories/<int:cat_id>/questions'
- Fetch a paginated set of at most 10 questions at a time with specified category id
- Query String Parameter: None
- Path Parameters: cat_id (INT) category id
- Request Payload: None
- Response Payload:
current_category: id of current category
questions: a list of questions returned
success: status of response
total_questions: number of questions returned
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "def",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "abc"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

```
GET '/questions'
- Fetch a paginated set of at most 10 questions at a time
- Query String Parameter: page (INT) default to 1
- Path Parameter: None
- Request Payload: None
- Response Payload:
categories: dictionary of categories
questions: a list of questions returned
success: status of response
total_questions: number of questions returned
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ],
  "success": true,
  "total_questions": 20
}
```

```
DELETE '/questions/<int:question_id>'
- Delete a question
- Query String Parameter: None
- Path Parameter: question_id (INT) id of question to be deleted
- Request Payload: None
- Response Payload:
deleted: id of question deleted
success: status of response
{
  "deleted": 14,
  "success": true
}
```

```
POST '/questions'
- Add a question
- Query String Parameter: None
- Path Parameter: None
- Request Payload:
question: question string
answer: answer string
difficulty: 1 to 5
category: 1 to 6
{
  "question": "aaa",
  "answer": "zzz",
  "difficulty": 1,
  "category": 1
}
- Response Payload:
created: id of question created
success: status of response
{
  "created": 25,
  "success": true
}
```

```
POST '/quizzes'
- Play quizzes
- Query String Parameter: None
- Path Parameter: None
- Request Payload:
previous_questions: a list of id (INT) of questions previous played
quiz_category: object of category
{
    "previous_questions": [],
    "quiz_category": {
        "type": "Science",
        "id": "1"
    }
}
- Response Payload:
previous_questions: a list of id (INT) of questions previous played
question: object of question
success: status of response
{
  "previous_questions": [],
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
