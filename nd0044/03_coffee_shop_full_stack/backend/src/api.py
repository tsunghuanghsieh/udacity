import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES
@app.route("/drinks")
# @requires_auth('get:drinks')
def get_drinks():
    drinks = Drink.query.all()
    drinks = [ drink.short() for drink in drinks ]
    return jsonify({
        "success": True,
        "drinks": drinks
    })

@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drink_detail(token):
    drinks = Drink.query.all()
    drinks = [ drink.long() for drink in drinks ]
    return jsonify({
        "success": True,
        "drinks": drinks
    })

@app.route("/drinks", methods = ["POST"])
@requires_auth('post:drinks')
def create_drink(token):
    body = request.get_json()
    if (body is None):
        abort(400)
    if (len(Drink.query.filter(Drink.title.ilike("%{}%".format(body.get('title')))).all()) > 0):
        abort(422)
    drink = Drink(title = body.get('title'), recipe = json.dumps(body.get('recipe')))
    drink.insert()
    return jsonify({
        "success": True,
        "drinks": [ drink.long() ]
    })


@app.route("/drinks/<int:drink_id>", methods = ["PATCH"])
@requires_auth('patch:drinks')
def update_drink(token, drink_id):
    body = request.get_json()
    if (body is None):
        abort(400)
    drink = Drink.query.get(drink_id)
    if (drink is None):
        abort(404)
    drink.title = body.get('title')
    drink.recipe = json.dumps(body.get('recipe'))
    drink.update()
    return jsonify({
        "success": True,
        "drinks": [ drink.long() ]
    })


@app.route("/drinks/<int:drink_id>", methods = ["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):
    try:
        drink = Drink.query.get(drink_id)
        if (drink is None):
            raise FileNotFoundError()
        drink.delete()
        return jsonify({
            "success": True,
            "drinks": drink_id
        })
    except FileNotFoundError as e:
        abort(404)


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(401)
def handle_bad_request(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401

@app.errorhandler(403)
def handle_method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Method Not Allowed"
    }), 403

@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404

@app.errorhandler(422)
def handle_unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

def handle_auth_error(err):
    return jsonify({
        "success": False,
        "error": err.status_code,
        "message": err.error
    }), err.status_code
app.register_error_handler(AuthError, handle_auth_error)

if __name__ == "__main__":
    app.debug = True
    app.run()
