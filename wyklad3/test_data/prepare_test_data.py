import json
import pandas as pd


# === 1. Wczytanie danych JSON ===
with open("export.json", "r", encoding="utf-8") as f:
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


# === 3. Tworzenie DataFrame dla ocen, filmów i użytkowników ===
df_ratings = pd.DataFrame(ratings_list)
df_movies = pd.DataFrame(
    [{"movieId": mid, "movieName": title} for title, mid in movie_to_id.items()]
)
df_users = pd.DataFrame(
    [{"userId": uid, "userName": uname} for uname, uid in user_to_id.items()]
)

# === 4. Merging danych w jeden plik test_data.csv ===
# Połączenie ocen z danymi użytkowników i filmów
df_combined = (
    df_ratings
    .merge(df_users, on="userId")  # Połączenie z użytkownikami
    .merge(df_movies, on="movieId")  # Połączenie z filmami
    [["userId", "userName", "movieId", "movieName", "rating"]]  # Wybór kolumn w odpowiedniej kolejności
)

# Zapis złączonych danych
df_combined.to_csv("test_data.csv", index=False)

print("Gotowe! Zapisano test_data/test_data.csv")
