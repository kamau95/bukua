import requests
from .models import db, Movie
from datetime import datetime, timedelta
import os
from flask import current_app


# Load environment variables
#TMDB_API_KEY = os.getenv('TMDB_API_KEY')

#base url
#base_url = "https://api.themoviedb.org/3/search/movie"


#headers
#headers = {
       # "accept": "application/json",
        #"Authorization": f"Bearer {TMDB_API_KEY}"
       #}



def fetch_movies(query, year):
    # Load environment variables
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    if not TMDB_API_KEY:
        current_app.logger.error("TMDB_API_KEY is not set")
        return None


    #base url
    base_url = "https://api.themoviedb.org/3/search/movie"


    #headers
    headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_API_KEY}"
            }


    #Query parameters
    query_params = {
            'query': query,
            'primary_release_year': year,
            'include_adult': 'false',
            'language': 'en-US',
            'page': 1
            }

    try:
        response = requests.get(base_url, params=query_params, headers=headers, timeout=10)
        response.raise_for_status() #Raise an error for bad status codes


         # Debugging logs
        current_app.logger.debug(f"Request URL: {response.url}")
        current_app.logger.debug(f"Response Status Code: {response.status_code}")
        current_app.logger.debug(f"Response Content: {response.content}")


        if response.status_code == 200:
            data = response.json()

        if data["results"]:
            movie_data = {
                    "api_id": data["results"][0]["id"],
                    "title": data["results"][0]["title"],
                    "release_year": data["results"][0]["release_date"].split('-')[0],
                    "poster_path": data["results"][0]["poster_path"]
                    }
            return [movie_data]  # Return list of movie data
        else:
            current_app.logger.warning("No movies found for query: %s, year: %s", query, year)
            return None  # Handle case where no results are found
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error fetching movies: {e}")
        return None  # Handle other response codes or errors



#fuction to get or create a movie in our db
def get_or_create(api_id, title, release_date, poster_path):
    # Check if movie already exists in database
    movie = db.session.query(Movie).filter_by(api_id = api_id).first()
    if not movie:
        movie = Movie(api_id=api_id, title=title, release_year=release_date, poster_path=poster_path)
        db.session.add(movie)
        db.session.commit()
    return movie


#we add movie to our favourite if its not in it
def add_movie_to_favorites(user, api_id):
    movie = get_or_create(api_id, title, release_date, poster_path)
    if movie not in user.favorite_movies:
        user.favorite_movies.append(movie)
        db.session.commit()
