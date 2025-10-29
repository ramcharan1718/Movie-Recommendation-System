import requests
import pandas as pd

API_KEY = "6c26c8168d0b08a3e5a0c6efb5c2b056"  # Replace with your TMDB API key
MOVIE_PATH = 'data/movies.csv'

GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
    99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
    27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance",
    878: "Science Fiction", 10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}

def fetch_popular_movies(pages=5):
    all_movies = []

    for page in range(1, pages + 1):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Failed to fetch page {page}")
            continue

        data = response.json()
        for movie in data.get('results', []):
            movie_id = movie['id']
            title = movie['title']
            genre_ids = movie['genre_ids']
            genres = ', '.join([GENRE_MAP.get(gid, "Unknown") for gid in genre_ids])
            language = movie['original_language']

            all_movies.append({
                'movie_id': movie_id,
                'title': title,
                'genre': genres,
                'language': language
            })

    new_movies_df = pd.DataFrame(all_movies)

    try:
        existing_movies_df = pd.read_csv(MOVIE_PATH)
    except FileNotFoundError:
        existing_movies_df = pd.DataFrame(columns=['movie_id', 'title', 'genre', 'language'])

    # Combine new with existing, drop duplicates by title
    combined_df = pd.concat([existing_movies_df, new_movies_df], ignore_index=True)
    combined_df.drop_duplicates(subset='title', keep='first', inplace=True)
    combined_df.to_csv(MOVIE_PATH, index=False)

    print(f"✅ {len(new_movies_df)} new movies fetched and merged. Total: {len(combined_df)}")
