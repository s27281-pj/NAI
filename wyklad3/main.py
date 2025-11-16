"""
    Projekt: System rekomendacji filmów/seriali oparty na ocenach
    Autor: Roland i Cyprian
    Zasady: https://github.com/s27281-pj/NAI/tree/master/wyklad3#readme
    Środowisko: Python 3.10+, venv, pandas, numpy, scikit-learn
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors

movies = pd.read_csv('data_train/movies.csv')
ratings = pd.read_csv('data_train/ratings.csv')

# Removing duplicate rows
movies.drop_duplicates(inplace=True)
ratings.drop_duplicates(inplace=True)

# Removing missing values
movies.dropna(inplace=True)
ratings.dropna(inplace=True)

# Extracting the genres column
genres = movies['genres']

# Creating an instance of the OneHotEncoder
encoder = OneHotEncoder()

# Fitting and transforming the genres column
genres_encoded = encoder.fit_transform(genres.values.reshape(-1, 1))


# Creating an instance of the NearestNeighbors class
recommender = NearestNeighbors(metric='cosine')

# Fitting the encoded genres to the recommender
recommender.fit(genres_encoded.toarray())

# Index of the movie the user has previously watched
movie_index = 0

# Number of recommendations to return
num_recommendations = 5

# Getting the recommendations
_, recommendations = recommender.kneighbors(genres_encoded[movie_index].toarray(), n_neighbors=num_recommendations)

# Extracting the movie titles from the recommendations
recommended_movie_titles = movies.iloc[recommendations[0]]['title']
