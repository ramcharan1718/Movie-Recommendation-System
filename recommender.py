import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_movie_recommendations(username, ratings_df, movies_df, top_n=5):
    if ratings_df.empty:
        return pd.DataFrame()

    user_movie_matrix = ratings_df.pivot_table(index='username', columns='movie_title', values='rating').fillna(0)

    if username not in user_movie_matrix.index:
        return pd.DataFrame()

    similarity = cosine_similarity(user_movie_matrix)
    similarity_df = pd.DataFrame(similarity, index=user_movie_matrix.index, columns=user_movie_matrix.index)

    similar_users = similarity_df[username].sort_values(ascending=False)[1:]
    if similar_users.empty:
        return pd.DataFrame()

    similar_user = similar_users.index[0]

    current_user_movies = ratings_df[ratings_df['username'] == username]['movie_title'].tolist()
    similar_user_ratings = ratings_df[ratings_df['username'] == similar_user]

    recommendations = similar_user_ratings[~similar_user_ratings['movie_title'].isin(current_user_movies)]
    recommendations = recommendations.sort_values(by='rating', ascending=False).drop_duplicates('movie_title')

    recommended_titles = recommendations['movie_title'].head(top_n).tolist()

    return movies_df[movies_df['title'].isin(recommended_titles)]
