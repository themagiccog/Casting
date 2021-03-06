import os
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
import json
from sqlalchemy.orm import relationship



# SQLite3 Config
database_filename = "casting.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

# Postgres Config
database_name = "casting"
user = "cog"
passwd = "1234"

# On Heroku CLI, run: heroku config:set IS_HEROKU=True
# This sets checks to see which environment the app is running on
is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
  database_path = os.environ.get('DATABASE_URL')
  #database_path = 'postgres://sdvnivydulpsms:5d8861784026360e455814f6d0cbd0ac02c3f91e881d14aea0ee047738493ced@ec2-52-5-176-53.compute-1.amazonaws.com:5432/d8i942aps7g7cl'
else:
  database_path = "postgres://{}:{}@{}/{}".format(user, passwd,'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app   # db = SQLAlchemy(app)
    db.init_app(app)
    db.create_all()
    #migrate = Migrate(app, db)

class Actor(db.Model):
    __tablename__ = 'actor'


    #id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    id = Column(Integer(), primary_key=True)
    name = Column(String(), unique=True)
    age = Column(Integer(), nullable=False)
    gender = Column(String(), nullable=False)

    movies = relationship('Movie', secondary = 'link')

    # Useful debuging statements when we print this object
    def __repr__(self):
      return f'<Actor {self.id} {self.name} {self.age} {self.gender}>'


class Movie(db.Model):
    __tablename__ = 'movie'

    #id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    id = Column(Integer(), primary_key=True)
    title = Column(String(), unique=True)
    releasedate = Column(Integer(), nullable=False)

    actors = relationship('Actor', secondary = 'link')

    # Useful debuging statements when we print this object
    def __repr__(self):
      return f'<Movie {self.id} {self.title} {self.releasedate}>'


class Link(db.Model):
    __tablename__ = 'link'

    actor_id = Column(Integer,ForeignKey('actor.id'),primary_key = True)
    movie_id = Column(Integer,ForeignKey('movie.id'),primary_key = True)

    # Useful debuging statements when we print this object
    def __repr__(self):
      return f'<Link {self.actor_id} {self.movie_id}>'

