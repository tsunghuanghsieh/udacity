#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import sys
import re

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
import sqlalchemy
from forms import *

import apphelper

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import Artist, Venue, Show

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = db.session.query(Venue).group_by(Venue.id, Venue.state)
  state = city = None
  diffState = diffCity = False
  data = []
  for venue in venues:
    if state != venue.state:
      state = venue.state
      diffState = True
    else:
      diffState = False
    if city != venue.city:
      city = venue.city
      diffCity = True
    else:
      diffCity = False

    if (diffState or diffCity):
      data_area = {
        "city": city,
        "state": state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          # TODO QUESTION: num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
          "num_upcoming_shows": 0
        }]
      }
      data.append(data_area)
    else:
      data_venue = {
        "id": venue.id,
        "name": venue.name,
          # TODO QUESTION: num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
        "num_upcoming_shows": 1
      }
      data_area = data.pop()
      data_area['venues'].append(data_venue)
      data.append(data_area)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  sanitized_string = apphelper.remove_extra_whitespace(request.form['search_term'])
  terms = re.split(' |,', sanitized_string)
  result = Venue.query.filter(
            sqlalchemy.or_(
              Venue.name.ilike("%{}%".format(sanitized_string)),
              sqlalchemy.and_(
                Venue.state.ilike("%{}%".format(terms[-1])),
                Venue.city.ilike("%{}%".format(' '.join(terms[0:-1]).strip()))
              )
            )
          ).all()
  response = {
    "count": len(result),
    "data": []
  }
  for venue in result:
    data = {
      "id": venue.id,
      "name": venue.name,
      # TODO QUESTION: do i need num_upcoming_shows?
      "num_upcoming_shows": 0,
    }
    response['data'].append(data)
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  data.genres = apphelper.deserialize_genres(data.genres)
  data.past_shows = []
  data.past_shows_count = 0
  data.upcoming_shows = []
  data.upcoming_shows_count = 0
  for show in data.shows:
    artist = Artist.query.get(show.artist_id)
    show.artist_name = artist.name
    show.artist_image_link = artist.image_link
    if (datetime.strptime(show.start_time, "%Y-%m-%d %H:%M:%S") >= datetime.today()):
      data.upcoming_shows.append(show)
      data.upcoming_shows_count = data.upcoming_shows_count + 1
    else:
      data.past_shows.append(show)
      data.past_shows_count = data.past_shows_count + 1

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  data = apphelper.getVenueData(request.form)
  isVenueAdded = True
  try:
    venue = Venue(data)
    db.session.add(venue)
    db.session.commit()
  except:
    print(sys.exc_info())

    db.session.rollback()
    isVenueAdded = False
  finally:
    db.session.close()

  if (isVenueAdded):
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + data['name'] + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.order_by('id').all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  sanitized_string = apphelper.remove_extra_whitespace(request.form['search_term'])
  terms = re.split(' |,', sanitized_string)
  result = Artist.query.filter(
            sqlalchemy.or_(
              Artist.name.ilike("%{}%".format(sanitized_string)),
              sqlalchemy.and_(
                Artist.state.ilike("%{}%".format(terms[-1])),
                Artist.city.ilike("%{}%".format(' '.join(terms[0:-1]).strip()))
              )
            )
          ).all()
  response = {
    "count": len(result),
    "data": []
  }
  for artist in result:
    data = {
      "id": artist.id,
      "name": artist.name,
      # TODO QUESTION: do i need num_upcoming_shows?
      "num_upcoming_shows": 0,
    }
    response['data'].append(data)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get(artist_id)
  data.genres = apphelper.deserialize_genres(data.genres)
  data.past_shows = []
  data.past_shows_count = 0
  data.upcoming_shows = []
  data.upcoming_shows_count = 0
  for show in data.shows:
    venue = Venue.query.get(show.venue_id)
    show.venue_name = venue.name
    show.venue_image_link = venue.image_link
    if (datetime.strptime(show.start_time, "%Y-%m-%d %H:%M:%S") >= datetime.today()):
      data.upcoming_shows.append(show)
      data.upcoming_shows_count = data.upcoming_shows_count + 1
    else:
      data.past_shows.append(show)
      data.past_shows_count = data.past_shows_count + 1
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  artist.genres = apphelper.deserialize_genres(artist.genres)
  # See constructor parameters at https://wtforms.readthedocs.io/en/3.0.x/forms/
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    artist.update(apphelper.getArtistData(request.form))
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  venue.genres = apphelper.deserialize_genres(venue.genres)
  # See constructor parameters at https://wtforms.readthedocs.io/en/3.0.x/forms/
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    venue.update(apphelper.getVenueData(request.form))
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  data = apphelper.getArtistData(request.form)
  isArtistAdded = True
  try:
    artist = Artist(data)
    db.session.add(artist)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
    isArtistAdded = False
  finally:
    db.session.close()

  if (isArtistAdded):
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.order_by('id').all()
  data = []
  for show in shows:
    artist = Artist.query.get(show.artist_id)
    show.artist_name = artist.name
    show.artist_image_link = artist.image_link
    venue = Venue.query.get(show.venue_id)
    show.venue_name = venue.name
    data.append(show)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/search', methods=['POST'])
def search_showss():
  return render_template('pages/show.html')

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  data = {
    "artist_id": request.form['artist_id'],
    "venue_id": request.form['venue_id'],
    "start_time": request.form['start_time']
  }

  hasError = False
  # couldn't get validators to work on form, explicitly handle errors here
  if (not str.isdigit(request.form['artist_id'])) or (not str.isdigit(request.form['venue_id'])):
    flash('ID has to be an integer')
    hasError = True
  if (Artist.query.get(data['artist_id']) == None):
    flash('Artist ID does not exist in database')
    hasError = True
  if (Venue.query.get(data['venue_id']) == None):
    flash('Venue ID does not exist in database')
    hasError = True
  if (hasError):
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

  try:
    show = Show(data)
    db.session.add(show)
    db.session.commit()
  except:
    print(sys.exc_info())
    db.session.rollback()
    hasError = True
  finally:
    db.session.close()

  if (not hasError):
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
