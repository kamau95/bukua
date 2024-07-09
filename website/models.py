from sqlalchemy import Column, String, Integer, ForeignKey, Table, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, sessionmaker
from flask_login import UserMixin
from sqlalchemy.sql import func

#Initialize SQLAlchemy instance
db = SQLAlchemy()


## Association table for the many-to-many relationship between Users and Movies
favorites_association = Table('favorites', db.metadata,
        db.Column('user_id', db.Integer, ForeignKey('users.id'), primary_key=True),
        db.Column('movie_id', db.Integer, ForeignKey('movies.id'), primary_key=True)
)


class User(db.Model, UserMixin):
    """
     Represents a user table with columns id, email,
     password, first_name, and created_at.
     It also includes the UserMixin from flask_login for user management.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(150), unique=True, nullable=False)
    password =db.Column(db.String(150), nullable=False)
    first_name =db.Column(db.String(150), nullable=False)
    created_at =db.Column(db.DateTime(timezone=True), server_default=func.now())
    favorite_movies = db.relationship('Movie', secondary=favorites_association, back_populates='favorited_by')


class Movie(db.Model):
    """
    Represents a movie table with columns id, title, api_id,
    release_year, and poster_path.
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(250), nullable=False)
    api_id = db.Column(db.String(255), unique=True, nullable=False)  # Unique ID from the external API
    release_year =db.Column(db.Integer)
    poster_path = db.Column(db.String(255))
    favorited_by = db.relationship('User', secondary=favorites_association, back_populates='favorite_movies')



