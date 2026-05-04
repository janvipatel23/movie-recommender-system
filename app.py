import streamlit as st
import pandas as pd
import pickle

# load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id', 'poster_path']].iloc[movie_indices]

# fetch poster directly from csv data — no API key needed
def fetch_poster(poster_path):
    if poster_path and poster_path != '':
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        # use a working placeholder instead
        return "https://placehold.co/500x750?text=No+Poster"

# streamlit UI
st.title("Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")

    # 2x5 grid layout
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                poster_path = recommendations.iloc[j]['poster_path']
                poster_url = fetch_poster(poster_path)
                with col:
                    st.image(poster_url, width=130)
                    st.write(movie_title)