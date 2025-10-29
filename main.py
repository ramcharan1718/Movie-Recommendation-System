import fetchmovies
from datahandler import load_movies, load_ratings, add_rating, add_movie
from recommender import get_movie_recommendations
from utils import print_movies

LANGUAGE_MAP = {
    'en': 'English', 'hi': 'Hindi', 'te': 'Telugu', 'fr': 'French', 'es': 'Spanish',
    'cn': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'ml': 'Malayalam',
    'no': 'Norwegian', 'pt': 'Portuguese', 'tl': 'Tagalog', 'zh': 'Chinese',
    'it': 'Italian'
}

def get_all_genres(movies_df):
    genres = set()
    for genre_str in movies_df['genre'].dropna():
        for genre in genre_str.split(','):
            genres.add(genre.strip())
    return sorted(genres)

def get_all_languages(movies_df):
    langs = sorted(movies_df['language'].dropna().unique())
    return [(code, LANGUAGE_MAP.get(code, code)) for code in langs]

def main():
    print("🎬 Welcome to the Movie Recommender!")

    fetchmovies.fetch_popular_movies(pages=5)

    movies_df = load_movies()
    if movies_df.empty:
        print("❌ No movies available. Please check your API key or connection.")
        return

    ratings_df = load_ratings()

    username = input("\nEnter your username: ").strip()
    print_movies(movies_df)

    print("\nOptions:")
    print("(r) Rate a movie")
    print("(c) Get custom recommendations")
    print("(v) View my rated movies")
    print("(a) Add a new movie and rate it")
    choice = input("Enter your choice: ").lower()

    if choice == 'r':
        movie_title = input("Enter Movie Title exactly as shown: ").strip()
        if movie_title not in movies_df['title'].values:
            print("❌ Movie not found.")
            return
        rating = int(input("Enter rating (1-5): "))
        add_rating(username, movie_title, rating)
        print("✅ Rating saved.")

    elif choice == 'c':
        genres = get_all_genres(movies_df)
        print("\nAvailable Genres:")
        print(", ".join(genres))
        genre_input = input("Enter preferred genre (e.g., Romance, Action): ").strip()

        languages = get_all_languages(movies_df)
        print("\nAvailable Languages:")
        for code, name in languages:
            print(f"{code} : {name}")
        language_input = input("Enter preferred language code (or leave blank to skip): ").strip().lower()

        print(f"\nFiltering movies for genre '{genre_input}' and language '{language_input or 'Any'}'")

        if language_input:
            filtered_movies = movies_df[
                movies_df['genre'].str.contains(genre_input, case=False, na=False) &
                (movies_df['language'].str.lower() == language_input)
            ]
        else:
            filtered_movies = movies_df[
                movies_df['genre'].str.contains(genre_input, case=False, na=False)
            ]

        print(f"Movies found after filtering: {len(filtered_movies)}")

        if filtered_movies.empty:
            print("🙁 No movies found for that genre/language.")
            return

        recommendations = get_movie_recommendations(username, ratings_df, filtered_movies)
        if recommendations.empty:
            print("\nNo personalized recommendations available. Here are movies matching your filters:\n")
            for _, row in filtered_movies.iterrows():
                print(f"- {row['title']} ({row['genre']}) [{row['language']}]")
        else:
            print("\n📽️ Recommended Movies:")
            for _, row in recommendations.iterrows():
                print(f"- {row['title']} ({row['genre']}) [{row['language']}]")

    elif choice == 'v':
        user_ratings = ratings_df[ratings_df['username'] == username]
        if user_ratings.empty:
            print("\nYou have not rated any movies yet.")
        else:
            print(f"\nMovies rated by {username}:")
            for _, row in user_ratings.iterrows():
                print(f"- {row['movie_title']} : {row['rating']} stars")

    elif choice == 'a':
        title = input("Enter movie title: ").strip()
        genre = input("Enter genre (e.g., Action, Drama): ").strip()
        language = input("Enter language code (e.g., en, hi): ").strip().lower()

        add_movie(title, genre, language)
        rating = int(input(f"Enter your rating for '{title}' (1-5): "))
        add_rating(username, title, rating)
        print("✅ Movie added and rated.")

    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()
