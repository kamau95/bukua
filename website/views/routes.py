from flask import Blueprint, current_app, jsonify, render_template, flash, url_for, request, redirect
from flask_login import login_required, current_user
from ..movie_service import fetch_movies, get_or_create
from ..models import db, Movie, User
from sqlalchemy.orm import joinedload
from datetime import datetime
from website.utils import construct_poster_url

# Define the Blueprint for the views
views = Blueprint('views', __name__)


@views.route('/')
def home():
    """where the root is visited what happens"""
    current_year = datetime.now().year
    return render_template("home.html", current_year=current_year, user=current_user)


@views.route('/search', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        query = request.form.get('query')
        primary_release_year = request.form.get('year')

        if not query or not primary_release_year:
            # Handle case where either query or year is missing
            flash('Enter title and the year', category='danger')
            return redirect(url_for('views.home'))

        # Fetch movies from the external API
        movies = fetch_movies(query, primary_release_year)
        current_app.logger.debug(f"Fetched movies: {movies}")
        if movies is None:
            current_app.logger.error("Failed to fetch movies from external API")
            flash('Failed to fetch movies. Please try again later.', category='danger')
            return redirect(url_for('views.home'))

        # Construct the full poster path URL for each movie
        movies = construct_poster_url(movies)


        return render_template('search_results.html', movies=movies)


    return redirect(url_for('views.home'))


@views.route('/favorites')
@login_required
def favorites():
    if current_user.is_authenticated:
        # Fetch favorite movies for the current user from the database
        favorite_movies = current_user.favorite_movies

        #Convert Movie objects to dictionaries
        favorite_movies = [
                {
                    'poster_path': movie.poster_path,
                    'title': movie.title,
                    'release_year': movie.release_year,
                    'api_id': movie.api_id
                    }
                for movie in favorite_movies
                ]

         # Construct poster URLs for the favorite movies
        favorite_movies = construct_poster_url(favorite_movies)
        return render_template('favorites.html', favorite_movies=favorite_movies)
    else:
        # Handle case where user is not authenticated
         return render_template('login.html', user=current_user)


@views.route('/add_favorites', methods=['POST'])
@login_required
def add_favorites():
    api_id = request.form.get('api_id')
    title = request.form.get('title')
    release_year = request.form.get('release_year')
    poster_path = request.form.get('poster_path')

    print(f"Received: api_id={api_id}, title={title}, release_year={release_year}, poster_path={poster_path}")

    # Try getting or creating the movie (using existing function
    movie = get_or_create(api_id, title, release_year, poster_path)

    if not movie:
        flash('movie not found', category='danger')
        return redirect(url_for('views.favorites'))


    if movie not in current_user.favorite_movies:
        current_user.favorite_movies.append(movie)
        db.session.commit()
        flash('movie added to favorite successfully', category='success')
    else:
        flash('Movie is already in favorites.', category='info')
    return redirect(url_for('views.favorites'))


@views.route('/delete-movie', methods=['DELETE'])
def delete_movie():
    data = request.get_json()  # Expecting JSON from index.js file
    print("Received data:", data) 
    if 'api_id' not in data:
        return jsonify({"error": "missing api_id."}), 400
    
    api_id = data['api_id']
    user = current_user

    # Find the movie by api_id
    movie = Movie.query.filter_by(api_id=api_id).first()
    if not movie:
        return jsonify({"error": "movie not found"}), 404
    
    # Remove the movie from the user's favorites
    if movie in user.favorite_movies:
        user.favorite_movies.remove(movie)
        db.session.commit()
        return jsonify({"success": "movie removed from favorites"}), 200
    else:
        return jsonify({"error": "movie not found in favorites"}), 400


@views.route('/landing')
def landing():
    return render_template('landing.html')


@views.route('/about')
def about():
        return render_template('about.html')
