# website/utils.py

def construct_poster_url(movies):
    base_url = "https://image.tmdb.org/t/p/"
    size = "w500"

    if isinstance(movies, list):
        for movie in movies:
            if 'poster_path' in movie and movie['poster_path']:
                movie['poster_path'] = f"{base_url}{size}{movie['poster_path']}"
    elif isinstance(movies, dict):
        if 'poster_path' in movies and movies['poster_path']:
            movies['poster_path'] = f"{base_url}{size}{movies['poster_path']}"

    return movies

