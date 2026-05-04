import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# check what columns exist
print("movies columns:", movies.columns.tolist())
print("credits columns:", credits.columns.tolist())

# merge on title
movies = movies.merge(credits, on='title')

# check columns after merge
print("after merge columns:", movies.columns.tolist())

# keep only needed columns — poster_path may not exist
# so we handle both cases
if 'poster_path' in movies.columns:
    movies = movies[['id', 'title', 'overview', 'poster_path']].rename(
        columns={'id': 'movie_id'}
    )
else:
    print("poster_path not found! adding empty column")
    movies = movies[['id', 'title', 'overview']].rename(
        columns={'id': 'movie_id'}
    )
    movies['poster_path'] = ''

movies['overview'] = movies['overview'].fillna('')
movies['poster_path'] = movies['poster_path'].fillna('')
movies = movies.reset_index(drop=True)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['overview'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

with open('movie_data.pkl', 'wb') as file:
    pickle.dump((movies, cosine_sim), file)

print("movie_data.pkl created! total movies:", len(movies))