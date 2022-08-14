from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie, Audition
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
  def get_actors():
    actors = Actor.query.all()
    all_actors = [ actor.name for actor in actors ]

    return jsonify({
      "success": True,
      "actors": all_actors
    })

  @app.route("/actors/<int:actor_id>")
  def get_actor(actor_id):
    actor = Actor.query.get(actor_id)

    return jsonify({
      "success": True,
      "actors_detail": actor.format()
    })

  @app.route("/movies")
  def get_movies():
    movies = Movie.query.all()
    all_movies = [ movie.title for movie in movies ]

    return jsonify({
      "success": True,
      "movies": all_movies
    })

  @app.route("/movies/<int:movie_id>")
  def get_movie(movie_id):
    movie = Movie.query.get(movie_id)

    return jsonify({
      "success": True,
      "movies_detail": movie.format()
    })

  @app.route("/auditions")
  def get_auditions():
    auditions = Audition.query.all()
    all_auditions = [ audition.format() for audition in auditions ]

    return jsonify({
      "success": True,
      "auditions": all_auditions
    })

  @app.route("/auditions/<int:audition_id>")
  def get_audition(audition_id):
    audition = Audition.query.get(audition_id)

    return jsonify({
      "success": True,
      "auditions_detail": audition.format()
    })

  @app.route("/actors", methods = [ "POST" ])
  def create_actor():
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
  def create_movie():
    data = app_utils.parseRequestJson("movie", request.get_json())
    if (data['status_code'] != 200):
      abort(data['status_code'])
    movie = Movie(data)
    movie.insert()
    return jsonify({
      "success": True,
      "movie": movie.id
    })

  @app.route("/actors/<int:actor_id>", methods = [ "PATCH" ])
  def update_actor(actor_id):
    data = app_utils.parseRequestJson("actor", request.get_json())
    if (data['status_code'] != 200):
      abort(data['status_code'])
    actor = Actor.query.get(actor_id)
    actor.update(data)
    return jsonify({
      "success": True,
      "updated": actor_id
    })

  @app.route("/movies/<int:movie_id>", methods = [ "PATCH" ])
  def update_movie(movie_id):
    data = app_utils.parseRequestJson("movie", request.get_json())
    print(data)
    if (data['status_code'] != 200):
      abort(data['status_code'])
    movie = Movie.query.get(movie_id)
    movie.update(data)
    return jsonify({
      "success": True,
      "updated": movie_id
    })

  @app.route("/actors/<int:actor_id>", methods = [ "DELETE" ])
  def delete_actor(actor_id):
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
  def delete_movie(movie_id):
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

  @app.route("/audition/<int:audition_id>", methods = [ "DELETE" ])
  def delete_audition(audition_id):
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

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)