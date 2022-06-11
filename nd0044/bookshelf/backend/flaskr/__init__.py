import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/books')
    def get_book():
        books = Book.query.order_by('id').all()
        formatted_books = [ book.format() for book in books ]
        # if page is not specified or value is not integer, default to page 1
        page = request.args.get('page', 1, type = int)
        # ignore negative page
        page = page if (page >= 1) else 1
        start = (page - 1) * BOOKS_PER_SHELF

        # requesting non-existent page
        if (start > len(formatted_books)):
            abort(404)

        return jsonify({
            'success': True,
            'books': formatted_books[start:(start + BOOKS_PER_SHELF)],
            'total_books': len(books)
        })

    @app.route('/books/<int:book_id>', methods = ['PATCH'])
    def update_book_rating(book_id):
        retcode = 200
        body = request.get_json()
        if (body is None or 'rating' not in body):
            abort(400)
        else:
            rating = body.get('rating')
        try:
            book = Book.query.get(book_id)
            if (book == None):
                retcode = 404
                raise Exception()
            book.rating = rating
            book.update()
            return jsonify({
                'success': True
            })
        except:
            if (retcode == 404):
                abort(retcode)
            else:
                abort(400)

    @app.route('/books/<int:book_id>', methods = ['DELETE'])
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if (book == None):
            abort(404)
        book.delete()
        #
        # empirical data shows we don't need to return book list
        #
        # books = Book.query.order_by('id').all()
        # formatted_books = [ book.format() for book in books ]
        return jsonify({
            'success': True,
            'deleted': book_id,
            # 'books': formatted_books[0:BOOKS_PER_SHELF],
            # 'total_books': len(books)
        })

    @app.route('/books', methods = ['POST'])
    def add_book():
        body = request.get_json()
        if (body is None):
            abort(400)

        if ('search' in body):
            search = body.get('search')
            books = Book.query.filter(Book.title.ilike("%{}%".format(search))).all()
            print("search " + search)
            print(len(books))
            return jsonify({
                'success': True,
                'total_books': len(books)
            })
        else:
            title = body.get('title', None)
            author = body.get('author', None)
            rating = body.get('rating', None)
            book = Book(title, author, rating)
            book.insert()
            #
            # empirical data shows the newly added book doesn't show up on frontend immediately
            # even in the solution provided in class. returning books doesn't seem to do anything.
            # not returning books doesn't trigger any visual error.
            #
            # books = Book.query.order_by('id').all()
            # formatted_books = [ book.format() for book in books ]
            # last_page_start = (int(len(formatted_books) / BOOKS_PER_SHELF) - 1) * BOOKS_PER_SHELF
            # end = last_page_start + BOOKS_PER_SHELF
            # print(len(formatted_books))
            return jsonify({
                'success': True,
                'created': book.id,
                # 'books': formatted_books[last_page_start:end],
                # 'total_books': len(formatted_books)
            })

    @app.errorhandler(400)
    def handle_bad_request(err):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
        }), 400

    @app.errorhandler(404)
    def handle_not_found(err):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Not Found"
        }), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(err):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method Not Allowed"
        }), 405

    return app
