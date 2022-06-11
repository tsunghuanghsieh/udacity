import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from sqlalchemy import text
from models import setup_db, Book

class BookTestCase(unittest.TestCase):
    """This class represents the Book test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # TODO Add to populate mock data every time unit test is run
        #      Currently, I have to run setup.sh each time before running unit test.

    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_books(self):
        """Test GET Retrieve All Books"""
        res = self.client().get('/books')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'], True)

    def test_update_rating_with_no_data(self):
        """Test PATCH Update Book Rating without Rating"""
        res = self.client().patch('/books/1')
        self.assertEqual(res.status_code, 400)

    def test_update_rating(self):
        """Test PATCH Update Book Rating"""
        book_id = 2
        new_rating = 2
        endpoint = "/books/{}".format(book_id)
        res = self.client().patch(endpoint, json = { 'rating': new_rating })
        self.assertEqual(res.status_code, 200)
        book = Book.query.get(book_id)
        self.assertEqual(book.rating, new_rating)

    def test_delete_existing_book(self):
        """Test DELETE Existing Book"""
        book_id = 1
        endpoint = "/books/{}".format(book_id)
        res = self.client().delete(endpoint)
        self.assertEqual(res.status_code, 200)
        book = Book.query.get(book_id)
        self.assertEquals(book, None)

    def test_delete_nonexisting_book(self):
        """Test DELETE NonExisting Book"""
        book_id = 500
        endpoint = "/books/{}".format(book_id)
        res = self.client().delete(endpoint)
        self.assertEqual(res.status_code, 404)

    def test_add_book(self):
        """Test POST Add New Book"""
        res = self.client().post('/books', json = self.new_book)
        self.assertEqual(res.status_code, 200)

    def test_add_book(self):
        """Test POST Method Not Allowed"""
        book_id = 500
        endpoint = "/books/{}".format(book_id)
        res = self.client().post(endpoint, json = self.new_book)
        self.assertEqual(res.status_code, 405)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
