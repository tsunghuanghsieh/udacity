import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy
from mock import patch

from app import create_app
from models import setup_db, Actor, Audition, Movie

from test_app_config import JWT_TOKEN_ASSISTANT, JWT_TOKEN_DIRECTOR, JWT_TOKEN_PRODUCER

class CastingTestCase(unittest.TestCase):
  """This class represents the Casting Agency test case"""

  def setUp(self):
    """Define test variables and initialize app."""
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "casting_test"
    self.database_path = "postgresql://{}/{}".format('zonghuan@localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()

  def tearDown(self):
    """Executed after reach test"""
    self.db.get_engine(self.app).execute('DROP TABLE auditions')
    self.db.get_engine(self.app).execute('DROP TABLE actors')
    self.db.get_engine(self.app).execute('DROP TABLE movies')
    pass

  def make_actor(self, actor_name, actor_age, actor_gender):
    return {"name": actor_name, "age": actor_age, "gender": actor_gender}

  def make_movie(self, title, release_date):
    return {"title": title, "release_date": release_date}

  def make_audition(self, actor_id, movie_id):
    return {"actor_id": actor_id, "movie_id": movie_id}

  # Endpoint unit tests for Assistant
  # Only GET are 200, the rest are 403
  def test_get_actors_token_assistant(self):
    """Test GET Retrieve All Actors Assistant"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    actor2 = Actor(self.make_actor("Actor 2", 50, "F"))
    actor2.insert()
    actors = [ actor1.name, actor2.name ]
    endpoint = "/actors"
    response = self.client().get(endpoint, headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['actors'], actors)
  def test_post_actors_token_assistant(self):
    """Test POST Add Actor Assistant"""
    actor1_json = self.make_actor("Actor 1", 50, "M")
    endpoint = "/actors"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)}, json = actor1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)
  def test_patch_actors_token_assistant(self):
    """Test PATCH Update Actor Assistant"""
    actor1_json = self.make_actor("Actor 1", 50, "M")
    actor1 = Actor(actor1_json)
    actor1.insert()
    endpoint = "/actors/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)}, json = actor1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)
  def test_delete_actors_token_assistant(self):
    """Test DELETE Delete Actor Assistant"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    endpoint = "/actors/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)

  def test_get_movies_token_assistant(self):
    """Test GET Retrieve All Movies Assistant"""
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    movie2 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie2.insert()
    movies = [ movie1.title, movie2.title ]
    endpoint = "/movies"
    response = self.client().get(endpoint, headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['movies'], movies)
  def test_post_movies_token_assistant(self):
    """Test POST Add Movie Assistant"""
    movie1_json = self.make_movie("Movie 1", "Apr 1, 2022")
    endpoint = "/movies"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)}, json = movie1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)
  def test_patch_movies_token_assistant(self):
    """Test PATCH Update Movie Assistant"""
    movie1_json = self.make_movie("Movie 1", "Apr 1, 2022")
    movie1 = Movie(movie1_json)
    movie1.insert()
    endpoint = "/movies/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)}, json = movie1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)
  def test_delete_movies_token_assistant(self):
    """Test DELETE Delete Movie Assistant"""
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    endpoint = "/movies/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)

  def test_get_auditions_token_assistant(self):
    """Test GET Retrieve All Auditions Assistant"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    actor2 = Actor(self.make_actor("Actor 2", 50, "F"))
    actor2.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    movie2 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie2.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    audition2 = Audition(self.make_audition(2, 2))
    audition2.insert()
    endpoint = "/auditions"
    response = self.client().get(endpoint, headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(data['auditions']), 2)
  def test_post_auditions_token_assistant(self):
    """Test POST Add Audition Assistant"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    audition1_json = self.make_audition(1, 1)
    endpoint = "/auditions"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)}, json = audition1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)
  def test_patch_auditions_token_assistant(self):
    """Test PATCH Update Audition Assistant"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    movie2 = Movie(self.make_movie("Movie 2", "May 1, 2022"))
    movie2.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    audition1_json = self.make_audition(1, 2)
    endpoint = "/auditions/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)}, json = audition1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)
  def test_delete_auditions_token_assistant(self):
    """Test DELETE Delete Audition Assistant"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    endpoint = "/auditions/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_ASSISTANT)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)

  # Endpoint unit tests for Director
  def test_get_actors_token_director(self):
    """Test GET Retrieve All Actors Director"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    actor2 = Actor(self.make_actor("Actor 2", 50, "F"))
    actor2.insert()
    actors = [ actor1.name, actor2.name ]
    endpoint = "/actors"
    response = self.client().get(endpoint, headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['actors'], actors)
  def test_post_actors_token_director(self):
    """Test POST Add Actor Director"""
    actor1_json = self.make_actor("Actor 1", 50, "M")
    endpoint = "/actors"
    response = self.client().post(endpoint, json = actor1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 401)
  def test_patch_actors_token_director(self):
    """Test PATCH Update Actor Director"""
    actor1_json = self.make_actor("Actor 1", 50, "M")
    actor1 = Actor(actor1_json)
    actor1.insert()
    endpoint = "/actors/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 400)
  def test_delete_actors_token_director(self):
    """Test DELETE Delete Actor Director"""
    endpoint = "/actors/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 404)

  def test_get_movies_token_director(self):
    """Test GET Retrieve All Movies Director"""
    endpoint = "/movies"
    response = self.client().get(endpoint)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 401)
  def test_post_movies_token_director(self):
    """Test POST Add Movie Director"""
    movie1_json = self.make_movie("Movie 1", "Apr 1, 2022")
    endpoint = "/movies"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)}, json = movie1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)
  def test_patch_movies_token_director(self):
    """Test PATCH Update Movie Director"""
    movie1_json = self.make_movie("Movie 1", "Apr 1, 2022")
    movie1 = Movie(movie1_json)
    movie1.insert()
    endpoint = "/movies/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)}, json = movie1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['updated'], 1)
  def test_delete_movies_token_director(self):
    """Test DELETE Delete Movie Director"""
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    endpoint = "/movies/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 403)

  def test_get_auditions_token_director(self):
    """Test GET Retrieve All Auditions Director"""
    endpoint = "/auditions"
    response = self.client().get(endpoint)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 401)
  def test_post_auditions_token_director(self):
    """Test POST Add Audition Director"""
    endpoint = "/auditions"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 400)
  def test_patch_auditions_token_director(self):
    """Test PATCH Update Audition Director"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    movie2 = Movie(self.make_movie("Movie 2", "May 1, 2022"))
    movie2.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    audition1_json = self.make_audition(1, 3)
    endpoint = "/auditions/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)}, json = audition1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 404)
  def test_delete_auditions_token_director(self):
    """Test DELETE Delete Audition Director"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    endpoint = "/auditions/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_DIRECTOR)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['deleted'], 1)

  # Endpoint unit tests for Producer
  # All 200
  def test_get_actors_token_producer(self):
    """Test GET Retrieve All Actors Producer"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    actor2 = Actor(self.make_actor("Actor 2", 50, "F"))
    actor2.insert()
    actors = [ actor1.name, actor2.name ]
    endpoint = "/actors"
    response = self.client().get(endpoint, headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['actors'], actors)
  def test_post_actors_token_producer(self):
    """Test POST Add Actor Producer"""
    actor1_json = self.make_actor("Actor 1", 50, "M")
    endpoint = "/actors"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)}, json = actor1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['actor'], 1)
  def test_patch_actors_token_producer(self):
    """Test PATCH Update Actor Producer"""
    actor1_json = self.make_actor("Actor 1", 50, "M")
    actor1 = Actor(actor1_json)
    actor1.insert()
    endpoint = "/actors/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)}, json = actor1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['updated'], 1)
  def test_delete_actors_token_producer(self):
    """Test DELETE Delete Actor Producer"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    endpoint = "/actors/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['deleted'], 1)

  def test_get_movies_token_producer(self):
    """Test GET Retrieve All Movies Producer"""
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    movie2 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie2.insert()
    movies = [ movie1.title, movie2.title ]
    endpoint = "/movies"
    response = self.client().get(endpoint, headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['movies'], movies)
  def test_post_movies_token_producer(self):
    """Test POST Add Movie Producer"""
    movie1_json = self.make_movie("Movie 1", "Apr 1, 2022")
    endpoint = "/movies"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)}, json = movie1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['movie'], 1)
  def test_patch_movies_token_producer(self):
    """Test PATCH Update Movie Producer"""
    movie1_json = self.make_movie("Movie 1", "Apr 1, 2022")
    movie1 = Movie(movie1_json)
    movie1.insert()
    endpoint = "/movies/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)}, json = movie1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['updated'], 1)
  def test_delete_movies_token_producer(self):
    """Test DELETE Delete Movie Producer"""
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    endpoint = "/movies/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['deleted'], 1)

  def test_get_auditions_token_producer(self):
    """Test GET Retrieve All Auditions Producer"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    actor2 = Actor(self.make_actor("Actor 2", 50, "F"))
    actor2.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    movie2 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie2.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    audition2 = Audition(self.make_audition(2, 2))
    audition2.insert()
    endpoint = "/auditions"
    response = self.client().get(endpoint, headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(data['auditions']), 2)
  def test_post_auditions_token_producer(self):
    """Test POST Add Audition Producer"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    audition1_json = self.make_audition(1, 1)
    endpoint = "/auditions"
    response = self.client().post(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)}, json = audition1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['audition'], 1)
  def test_patch_auditions_token_producer(self):
    """Test PATCH Update Audition Producer"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    movie2 = Movie(self.make_movie("Movie 2", "May 1, 2022"))
    movie2.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    audition1_json = self.make_audition(1, 2)
    endpoint = "/auditions/1"
    response = self.client().patch(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)}, json = audition1_json)
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['updated'], 1)
  def test_delete_auditions_token_producer(self):
    """Test DELETE Delete Audition Producer"""
    actor1 = Actor(self.make_actor("Actor 1", 50, "M"))
    actor1.insert()
    movie1 = Movie(self.make_movie("Movie 1", "Apr 1, 2022"))
    movie1.insert()
    audition1 = Audition(self.make_audition(1, 1))
    audition1.insert()
    endpoint = "/auditions/1"
    response = self.client().delete(endpoint,
      headers={"Authorization": "Bearer {}".format(JWT_TOKEN_PRODUCER)})
    data = json.loads(response.data)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['deleted'], 1)

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()