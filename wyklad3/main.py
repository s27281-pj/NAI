import pandas as pd


# Wczytaj dane treningowe i testowe
train_data = pd.read_csv('train_data/train_data.csv')
test_data = pd.read_csv('test_data/test_data.csv')


# Tworzymy macierz UserID x MovieID
user_movies_matrix = train_data.pivot( index='userId', columns='movieId', values = "rating" ).reset_index(drop=True)
user_movies_matrix.fillna( 0, inplace = True )
user_movies_matrix=pd.DataFrame(user_movies_matrix)


# Macierz UserID x UserID z wyliczonymi wartościami podobieństwa między każdym użytkownikiem.
from sklearn.metrics.pairwise import pairwise_distances
users_similarity = 1 - pairwise_distances( user_movies_matrix, metric="correlation" )
users_similarity_df = pd.DataFrame( users_similarity )


from sklearn.neighbors import NearestNeighbors

model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(train_data)


def recommend_for_user(user_id, n_neighbors=2):
    user = train_data.iloc[user_id].values.reshape(1, -1)
    distances, indices = model.kneighbors(user, n_neighbors=n_neighbors + 1)
    similar_users = indices[0][1:]  # pomijamy samego użytkownika

    user_ratings = train_data.iloc[user_id]
    unseen = user_ratings[user_ratings == 0].index  # filmy bez oceny

    scores = train_data.loc[similar_users, unseen].mean().sort_values(ascending=False)
    return scores

print("Polecane dla użytkownika 0:")
print(recommend_for_user(0))
