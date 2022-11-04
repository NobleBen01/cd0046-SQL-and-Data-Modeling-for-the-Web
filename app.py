#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from lib2to3.pytree import Base
from unicodedata import name
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from flask_migrate import Migrate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy_utils import database_exists, create_database
# from local_settings import postgresql as settings
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:09030993500@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  # def get_engine(postgres, 09030993500, localhost, 5000, fyyur):
  #   url = f"postgresql://postgres:09030993500@localhost:5000/fyyur"
  #   if not database_exists(url)

  


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    genre = db.Column(db.String())
    website_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    shows = db.relationship('Shows', backref='Venue', lazy=True)
    
    def __repr__(self):
     return f'<Venue {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
  
    facebook_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    looking_for_venues = db.Column(db.String())
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    # shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
     return f'<Venue {self.id} {self.name}>'


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(120), nullable=False)
    venue_name=db.Column(db.String)
    artist_name=db.Column(db.String)
    artist_image_link=db.Column(db.String(500))
    Artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    Venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

db.create_all()

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  venues = Venue.query.all()
  data= {
    "city": Venue.city,
    "state": Venue.state,
    "venues": [{
      "id": Venue.id,
      "name": Venue.name,
      "num_upcoming_shows": Venue.shows,
    }]
  }
        
  return render_template('pages/venues.html', areas=data)
  




  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
      q = request.args.get("")
      if q:
        response = db.session.query(Venue).query.filter(
          Venue.name.contains(q),
          q.lower(Venue.name) == Venue.name.lower())
      else:
        response = Venue.query.all()
        

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
      return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
 venue = Venue.query.filter_by(id=venue_id).first()
  
 venue.data = {
  "id": Venue.id,
  "name": Venue.name,
  "genres": Venue.genres,
  "address": Venue.address,
  "city": Venue.city,
  "state": Venue.state,
  "phone": Venue.phone,
  "website": Venue.website_link,
  "facebook_link": Venue.facebook_link,
  "seeking_talent": Venue.seeking_talent,
   "seeking_description": Venue.seeking_description,
    "image_link": Venue.image_link,
    "past_shows": [{
      "artist_id": Artist.id,
      "artist_name": Artist.name,
      "artist_image_link": Artist.image_link,
      "start_time": Artist.shows.start_time,
    }],
    "upcoming_shows": Artist.shows,
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
 }

  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
 return render_template('pages/show_venue.html', venue=venue.data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
 form = VenueForm(request.form)
 error = False
 try:
  venues = Venue (
   name=form.name.data,
   city=form.city.data,
   state=form.state.data,
   address=form.address.data,
   phone=form.phone.data,
   genres=form.genres.data,
   image_link=form.image_link.data,
   facebook_link=form.facebook_link.data,
   website_link=form.website_link.data,
   seeking_talent=form.seeking_talent.data,
   seeking_description=form.seeking_description.data,    
  ) 


  db.session.add(venues)
  db.session.commit()
 except:
  db.session.rollback()
  error = True
 finally:
  db.session.close()




  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  if error:
   flash('An error occurred. Venue ' + venues.name + ' could not be listed.')
  else: 
   flash('Venue ' + request.form['name'] + ' was successfully listed!')  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
   venue = Venue.query.get(venue_id)
   db.session.delete(venue)
   db.session.commit()

  except:
   error = True
   db.session.rollback()
  finally:
   db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artist = Artist.query.all()
  artist.data = {
  "id": Artist.id,
  "name": Artist.name,
}
 
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=artist.data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
      r = request.args.get("")
      if r:
        response = db.session.query(Artist).query.filter(
          Artist.name.contains(r),
          r.lower(Artist.name) == Artist.name.lower())
      else:
        response = Artist.query.all()
        
  # response={
  #   "count": 1,
  #    "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
      return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.filter_by(artist_id).first()
  artist.data = {
  "id": Artist.id,
  "name": Artist.name,
  "genres": Artist.genres,
  "city": Artist.city,
  "state": Artist.state,
  "phone": Artist.phone,
  "website": Artist.website_link,
  "facebook_link": Artist.facebook_link,
  "seeking_venue": Artist.seeking_venue,
   "seeking_description": Artist.seeking_description,
    "image_link": Artist.image_link,
    "past_shows": [{
      "artist_id": Artist.id,
      "artist_name": Artist.name,
      "artist_image_link": Artist.image_link,
      "start_time": Artist.shows.start_time,
    }],
    "upcoming_shows": Venue.shows,
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
 }
  
  
  
  return render_template('pages/show_artist.html', artist=artist.data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }

  artist = Artist.query.get(artist_id)
 # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  edit_artist = Artist.query.filter_by(artist_id=int(Artist.id)).first()
     
  edit_artist.name = request.form['name']
  edit_artist.city = request.form['city']
  edit_artist.state = request.form['state']
  edit_artist.phone = request.form['phone']
  edit_artist.genre = request.form['genre']
  edit_artist.image_link = request.form['image_link']
  edit_artist.facebook_link = request.form['facebook_link']
  edit_artist.website_link = request.form['website_link']
  edit_artist.looking_for_venues = request.form['looking_for_venues']
  edit_artist.seeking_description = request.form['seeking_description']
   
  edit_artist = db.session.merge(artist_id)
  db.session.add(edit_artist)
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }

  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
   edit_venue = Venue.query.filter_by(venue_id=int(Venue.id)).first()
     
   edit_venue.name = request.form['name']
   edit_venue.city = request.form['city']
   edit_venue.state = request.form['state']
   edit_venue.address = request.form['address']
   edit_venue.phone = request.form['phone']
   edit_venue.genre = request.form['genre']
   edit_venue.image_link = request.form['image_link']
   edit_venue.facebook_link = request.form['facebook_link']
   edit_venue.website_link = request.form['website_link']
   edit_venue.seeking_talent = request.form['seeking_talent']
   edit_venue.seeking_description = request.form['seeking_description']
   
   edit_venue = db.session.merge(Venue.id)
   db.session.add(edit_venue)
   db.session.commit()
   return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

 form = ArtistForm(request.form)
 error = False
 try:
  artist = Artist (
   name=form.name.data,
   city=form.city.data,
   state=form.state.data,
   phone=form.phone.data,
   genres=form.genres.data,
   image_link=form.image_link.data,
   facebook_link=form.facebook_link.data,
   website_link=form.website_link.data,
   looking_for_venues=form.seeking_venue.data,
   seeking_description=form.seeking_description.data,    
  )

  db.session.add(artist)
  db.session.commit()
 except:
  db.session.rollback()
  error = True
 finally:
  db.session.close()


#  on successful db insert, flash success
 # TODO: on unsuccessful db insert, flash an error instead.
 # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
 if error:
  flash('An error occured, Artist' + request.form['name'] + ' could not be listed.')
 else: 
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Shows.query.all()
  shows.data=[{
    "venue_id": Shows.Venue_id,
    "venue_name": Shows.venue_name,
    "artist_id": Shows.Artist_id,
    "artist_name": Shows.artist_name,
    "artist_image_link": Shows.artist_image_link,
    "start_time": Shows.start_time
    }]

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=shows.data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

 form = ShowForm(request.form)

 try:
  show = Shows (
   venue_name=form.venue_name.data ,
   artist_name=form.atrist_name.data,
   artist_image_link=form.artist_image_link.data,
   start_time=form.start_time.data,   
  )

  db.session.add(show)
  db.session.commit()
 except:
  db.session.rollback()
  error = True
 finally:
  db.session.close()



  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
 if error:
  flash('An error occured. Show could not be listed.')
 else: 
   flash('Show was successfully listed!')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
