import json
import pandas as pd

# === 1. Wczytanie danych JSON ===
with open("data_test/dane.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ratings_list = []
movie_to_id = {}  # mapowanie tytuł → movieId
next_movie_id = 1

user_to_id = {}  # mapowanie użytkownik → userId
next_user_id = 1

# === 2. Przetwarzanie danych do ratingów i tworzenie map filmów ===
for user, movies in data.items():
    if user not in user_to_id:
        user_to_id[user] = next_user_id
        next_user_id += 1

    userId = user_to_id[user]

    for entry in movies:
        title = entry["title"].strip()
        rating = entry["rating"]

        if title not in movie_to_id:
            movie_to_id[title] = next_movie_id
            next_movie_id += 1

        movieId = movie_to_id[title]

        ratings_list.append({
            "userId": userId,
            "movieId": movieId,
            "rating": rating
        })

# === 3. Zapis ratings.csv ===
df_ratings = pd.DataFrame(ratings_list)
df_ratings.to_csv("data_test/test_ratings.csv", index=False)

# === 4. Zapis movies.csv ===
movies_list = [{"movieId": mid, "title": title} for title, mid in movie_to_id.items()]
df_movies = pd.DataFrame(movies_list).sort_values(by="movieId")
df_movies.to_csv("data_test/test_movies.csv", index=False)

print("Gotowe! Zapisano ratings.csv oraz movies.csv")
