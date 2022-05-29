
DELIMITER = ";"

def deserialize_genres(genres):
  return genres.split(DELIMITER)

def getArtistData(form):
  return {
    "name": form['name'],
    "genres": serialize_genres(form.getlist('genres')),
    "city": form['city'],
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
    "name": form['name'],
    "genres": serialize_genres(form.getlist('genres')),
    "address": form['address'],
    "city": form['city'],
    "state": form['state'],
    "phone": form['phone'],
    "website": form['website_link'],
    "facebook_link": form['facebook_link'],
    "seeking_talent": form['seeking_talent'] if ('seeking_talent' in form.keys()) else False,
    "seeking_description": form['seeking_description'],
    "image_link": form['image_link'],
  }

def serialize_genres(genres):
  return DELIMITER.join(genres)

