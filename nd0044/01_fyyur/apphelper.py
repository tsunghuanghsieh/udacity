import re

DELIMITER = ";"

def deserialize_genres(genres):
  return genres.split(DELIMITER)

def getArtistData(form):
  return {
    "name": remove_extra_whitespace(form['name']),
    "genres": serialize_genres(form.getlist('genres')),
    "city": remove_extra_whitespace(form['city']),
    "state": form['state'],
    "phone": form['phone'],
    "website": form['website_link'],
    "facebook_link": form['facebook_link'],
    "seeking_venue": form['seeking_venue'] if ('seeking_venue' in form.keys()) else False,
    "seeking_description": form['seeking_description'],
    "image_link": form['image_link'],
  }

def getVenueData(form):
  return {
    "name": remove_extra_whitespace(form['name']),
    "genres": serialize_genres(form.getlist('genres')),
    "address": remove_extra_whitespace(form['address']),
    "city": remove_extra_whitespace(form['city']),
    "state": form['state'],
    "phone": form['phone'],
    "website": form['website_link'],
    "facebook_link": form['facebook_link'],
    "seeking_talent": form['seeking_talent'] if ('seeking_talent' in form.keys()) else False,
    "seeking_description": form['seeking_description'],
    "image_link": form['image_link'],
  }

def remove_extra_whitespace(sstring):
  return re.sub(' +', ' ', sstring.strip())

def serialize_genres(genres):
  return DELIMITER.join(genres)

