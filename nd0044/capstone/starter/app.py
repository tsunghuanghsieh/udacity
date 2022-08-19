import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie, Audition
from auth.auth import AuthError, requires_auth
import app_utils

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

  @app.route("/actors")
  @requires_auth('get:actors')
  def get_actors(token):
    actors = Actor.query.all()
    all_actors = [ actor.name for actor in actors ]

    return jsonify({
      "success": True,
      "actors": all_actors
    })

  @app.route("/actors/<int:actor_id>")
  @requires_auth('get:actors')
  def get_actor(token, actor_id):
    try:
      actor = Actor.query.get(actor_id)
      if (actor is None):
        raise FileNotFoundError()

      return jsonify({
        "success": True,
        "actors_detail": actor.format()
      })
    except FileNotFoundError as e:
      abort(404)

  @app.route("/movies")
  @requires_auth('get:movies')
  def get_movies(token):
    movies = Movie.query.all()
    all_movies = [ movie.title for movie in movies ]

    return jsonify({
      "success": True,
      "movies": all_movies
    })

  @app.route("/movies/<int:movie_id>")
  @requires_auth('get:movies')
  def get_movie(token, movie_id):
    try:
      movie = Movie.query.get(movie_id)
      if (movie is None):
        raise FileNotFoundError()

      return jsonify({
        "success": True,
        "movies_detail": movie.format()
      })
    except FileNotFoundError as e:
      abort(404)

  @app.route("/auditions")
  @requires_auth('get:auditions')
  def get_auditions(token):
    auditions = Audition.query.all()
    all_auditions = [ audition.format() for audition in auditions ]

    return jsonify({
      "success": True,
      "auditions": all_auditions
    })

  @app.route("/auditions/<int:audition_id>")
  @requires_auth('get:auditions')
  def get_audition(token, audition_id):
    try:
      audition = Audition.query.get(audition_id)
      if (audition is None):
        raise FileNotFoundError()

      return jsonify({
        "success": True,
        "auditions_detail": audition.format()
      })
    except FileNotFoundError as e:
      abort(404)

  @app.route("/actors", methods = [ "POST" ])
  @requires_auth('post:actors')
  def create_actor(token):
    data = app_utils.parseRequestJson("actor", request.get_json())
    if (data['status_code'] != 200):
      abort(data['status_code'])
    actor = Actor(data)
    actor.insert()
    return jsonify({
      "success": True,
      "actor": actor.id
    })

  @app.route("/movies", methods = [ "POST" ])
  @requires_auth('post:movies')
  def create_movie(token):
    data = app_utils.parseRequestJson("movie", request.get_json())
    if (data['status_code'] != 200):
      abort(data['status_code'])
    movie = Movie(data)
    movie.insert()
    return jsonify({
      "success": True,
      "movie": movie.id
    })

  @app.route("/auditions", methods = [ "POST" ])
  @requires_auth('post:auditions')
  def create_audition(token):
    data = app_utils.parseRequestJson("audition", request.get_json())
    if (data['status_code'] != 200):
      abort(data['status_code'])
    audition = Audition(data)
    audition.insert()
    return jsonify({
      "success": True,
      "movie": audition.id
    })

  @app.route("/actors/<int:actor_id>", methods = [ "PATCH" ])
  @requires_auth('patch:actors')
  def update_actor(token, actor_id):
    data = app_utils.parseRequestJson("actor", request.get_json())
    if (data['status_code'] != 200):
      abort(data['status_code'])
    try:
      actor = Actor.query.get(actor_id)
      if (actor is None):
        raise FileNotFoundError()
      actor.update(data)
      return jsonify({
        "success": True,
        "updated": actor_id
      })
    except FileNotFoundError as e:
      abort(404)

  @app.route("/movies/<int:movie_id>", methods = [ "PATCH" ])
  @requires_auth('patch:movies')
  def update_movie(token, movie_id):
    data = app_utils.parseRequestJson("movie", request.get_json())
    if (data['status_code'] != 200):
      abort(data['status_code'])
    movie = Movie.query.get(movie_id)
    try:
      if (movie is None):
        raise FileNotFoundError()
      movie.update(data)
      return jsonify({
        "success": True,
        "updated": movie_id
      })
    except FileNotFoundError as e:
      abort(404)

  @app.route("/actors/<int:actor_id>", methods = [ "DELETE" ])
  @requires_auth('delete:actors')
  def delete_actor(token, actor_id):
    try:
      actor = Actor.query.get(actor_id)
      if (actor is None):
        raise FileNotFoundError()
      actor.delete()
      return jsonify({
        "success": True,
        "deleted": actor_id
      })
    except FileNotFoundError as e:
      abort(404)

  @app.route("/movies/<int:movie_id>", methods = [ "DELETE" ])
  @requires_auth('delete:movies')
  def delete_movie(token, movie_id):
    try:
      movie = Movie.query.get(movie_id)
      if (movie is None):
        raise FileNotFoundError()
      movie.delete()

      return jsonify({
        "success": True,
        "deleted": movie_id
      })
    except FileNotFoundError as e:
      abort(404)

  @app.route("/auditions/<int:audition_id>", methods = [ "DELETE" ])
  @requires_auth('delete:auditions')
  def delete_audition(token, audition_id):
    try:
      audition = Audition.query.get(audition_id)
      if (audition is None):
        raise FileNotFoundError()
      audition.delete()

      return jsonify({
        "success": True,
        "deleted": audition_id
      })
    except FileNotFoundError as e:
      abort(404)

  @app.errorhandler(400)
  def handle_bad_request(err):
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
        "message": "Forbidden"
    }), 403

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

  @app.errorhandler(500)
  def handle_internal_server_error(err):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }), 500

  def handle_auth_error(err):
      return jsonify({
        "success": False,
        "error": err.status_code,
        "message": err.error
      }), err.status_code

  app.register_error_handler(AuthError, handle_auth_error)

  return app

APP = create_app()

if __name__ == '__main__':
  # APP.run(host='0.0.0.0', port=8080, debug=True)
  APP.run()