from app import db

class Venue(db.Model):
    __tablename__ = 'venues' # It doesn't like capital V in table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    genres = db.Column(db.String(256))
    website = db.Column(db.String(512))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    # relationship.backref is a shortcut for 2 relationship.back_populates in both classes,
    # in this case, Venue and Show class.
    # https://docs.sqlalchemy.org/en/14/orm/backref.html#relationships-backref
    shows = db.relationship('Show', backref="venues", lazy=True)

    def __init__(self, data):
      self.name = data['name']
      self.city = data['city']
      self.state = data['state']
      self.address = data['address']
      self.phone = data['phone']
      self.image_link = data['image_link']
      self.facebook_link = data['facebook_link']
      self.genres = data['genres']
      self.website = data['website']
      self.seeking_talent = data['seeking_talent']
      self.seeking_description = data['seeking_description']

    def update(self, data):
      self.name = data['name']
      self.city = data['city']
      self.state = data['state']
      self.address = data['address']
      self.phone = data['phone']
      self.image_link = data['image_link']
      self.facebook_link = data['facebook_link']
      self.genres = data['genres']
      self.website = data['website']
      self.seeking_talent = data['seeking_talent']
      self.seeking_description = data['seeking_description']

class Artist(db.Model):
    __tablename__ = 'artists' # It doesn't like capital A in table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(256))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    website = db.Column(db.String(512))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)

    # relationship.backref is a shortcut for 2 relationship.back_populates in both classes,
    # in this case, Artist and Show class.
    # https://docs.sqlalchemy.org/en/14/orm/backref.html#relationships-backref
    shows = db.relationship('Show', backref="artists", lazy=True)

    def __init__(self, data):
      self.name = data['name']
      self.city = data['city']
      self.state = data['state']
      self.phone = data['phone']
      self.image_link = data['image_link']
      self.facebook_link = data['facebook_link']
      self.genres = data['genres']
      self.website = data['website']
      self.seeking_venue = data['seeking_venue']
      self.seeking_description = data['seeking_description']

    def update(self, data):
      self.name = data['name']
      self.city = data['city']
      self.state = data['state']
      self.phone = data['phone']
      self.image_link = data['image_link']
      self.facebook_link = data['facebook_link']
      self.genres = data['genres']
      self.website = data['website']
      self.seeking_venue = data['seeking_venue']
      self.seeking_description = data['seeking_description']

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), primary_key = True, nullable = False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), primary_key = True, nullable = False)
    start_time = db.Column(db.String(20))

    def __init__(self, data):
      self.artist_id = data['artist_id']
      self.venue_id = data['venue_id']
      self.start_time = data['start_time']
