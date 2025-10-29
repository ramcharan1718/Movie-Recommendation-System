import pandas as pd

MOVIE_PATH = 'data/movies.csv'
RATING_PATH = 'data/ratings.csv'

def load_movies():
    return pd.read_csv(MOVIE_PATH)

def load_ratings():
    try:
        return pd.read_csv(RATING_PATH)
    except FileNotFoundError:
        return pd.DataFrame(columns=['username', 'movie_title', 'rating'])

def add_rating(username, movie_title, rating):
    ratings = load_ratings()
    new_rating = pd.DataFrame([[username, movie_title, rating]], columns=['username', 'movie_title', 'rating'])
    updated = pd.concat([ratings, new_rating], ignore_index=True)
    updated.to_csv(RATING_PATH, index=False)

def add_movie(title, genre, language):
    movies = load_movies()
    new_id = movies['movie_id'].max() + 1 if not movies.empty else 1

    new_movie = {
        'movie_id': new_id,
        'title': title,
        'genre': genre,
        'language': language
    }

    updated_movies = pd.concat([movies, pd.DataFrame([new_movie])], ignore_index=True)
    updated_movies.to_csv(MOVIE_PATH, index=False)
    print(f"✅ Movie '{title}' added successfully.")
