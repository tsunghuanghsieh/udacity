import os
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path is "":
  database_path = 'postgresql://zonghuan@localhost:5432/casting'
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)
  db.create_all()

class Actor(db.Model):
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String(20))

  # relationship.backref is a shortcut for 2 relationship.back_populates in both classes,
  # in this case, Actor and Audition class.
  # https://docs.sqlalchemy.org/en/14/orm/backref.html#relationships-backref
  auditions = db.relationship('Audition', backref="actors", lazy=True, cascade="all, delete-orphan")

  def __init__(self, data):
    self.name = data['name']
    self.age = data['age']
    self.gender = data['gender']

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    self.name = data['name']
    self.age = data['age']
    self.gender = data['gender']
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      "id": self.id,
      "name": self.name,
      "age": self.age,
      "gender": self.gender
    }

class Movie(db.Model):
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(String(20))

  # relationship.backref is a shortcut for 2 relationship.back_populates in both classes,
  # in this case, Movie and Audition class.
  # https://docs.sqlalchemy.org/en/14/orm/backref.html#relationships-backref
  auditions = db.relationship('Audition', backref="movies", lazy=True, cascade="all, delete-orphan")

  def __init__(self, data):
    self.title = data['title']
    self.release_date = data['release_date']

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    self.title = data['title']
    self.release_date = data['release_date']
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      "id": self.id,
      "title": self.title,
      "release_date": self.release_date
    }

class Audition(db.Model):
  __tablename__ = 'auditions'

  id = Column(Integer, primary_key=True)
  actor_id = Column(Integer, ForeignKey('actors.id'), nullable = False)
  movie_id = Column(Integer, ForeignKey('movies.id'), nullable = False)

  def __init__(self, data):
    self.actor_id = data['actor_id']
    self.movie_id = data['movie_id']

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    self.actor_id = data['actor_id']
    self.movie_id = data['movie_id']
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      "id": self.id,
      "actor_id": self.actor_id,
      "movie_id": self.movie_id
    }
