def print_movies(movies_df):
    print("\nAvailable Movies:")
    for _, row in movies_df.iterrows():  # removed .head(20)
        print(f"{row['title']} ({row['genre']}) [{row['language']}]")
