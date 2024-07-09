# akmovie Search Application

## Introduction
Welcome to the Movie Search Application! This project allows users to search for movies, view details, and save their favorite movies. It leverages The Movie Database (TMDb) API to fetch movie details and displays them in a user-friendly interface.

[Deployed Site](https://akmovie3-spfd2ozc.b4a.run/)

[Final Project Blog Article](http://your-blog-article-url.com)

### Authors
https://www.linkedin.com/in/kamau-linus-1b9808238

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)
- Flask
- SQLAlchemy
- The Movie Database (TMDb) API Key
- Aiven MySQL Database (or any other preferred database)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/movie-search-app.git
    cd movie-search-app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the project root and add the following:
    ```env
    FLASK_APP=website:create_app
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    TMDB_API_KEY=your_tmdb_api_key
    DATABASE_URI=mysql+pymysql://user:password@host/dbname?ssl_ca=path/to/ca.cert
    ```

5. Run the application:
    ```bash
    flask run
    ```
    The development server should be up and running on `http://127.0.0.1:5000`.

## Usage

### Home Page
- Navigate to the home page to view the current year and a welcome message.
- [Home Page](http://127.0.0.1:5000/)

### Search Movies
- Use the search form to find movies by title and release year.
- [Search Movies](http://127.0.0.1:5000/search)

### View Favorites
- Login to view and manage your favorite movies.
- [Favorites](http://127.0.0.1:5000/favorites)

### Add to Favorites
- Click the "Add to Favorites" button on a movie to save it to your favorites.

### Delete from Favorites
- Click the "Remove" button on a favorite movie to delete it from your favorites.

## Contributing

### How to Contribute
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## Inspiration and Technical Challenge
The inspiration for creating this application came from the need for an intuitive and efficient way to search for and keep track of movies. As avid movie enthusiasts, we often found ourselves overwhelmed by the vast number of movies available and the difficulty of remembering which ones we wanted to watch. We set out to solve this by developing a streamlined application that not only allows users to search for movies but also to save their favorites for easy access later.

One of the primary technical challenges we aimed to address was integrating with an external API (TMDb) to fetch and display movie data dynamically. This required handling API requests, parsing responses, and ensuring the application could manage and display this data efficiently. Additionally, we focused on creating a robust user authentication system and a seamless user experience for managing favorite movies.

