import pandas as pd


# === 1. Wczytanie danych ===
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")


# === 2. Usuwanie braków danych ===
ratings = ratings.dropna()           # usuwa wiersze gdzie brak userId/movieId/rating
movies = movies.dropna()             # usuwa wiersze gdzie brak movieId/title


# === 3. Usuwanie duplikatów ===
# Duplikaty ocen użytkownika (ta sama para userId + movieId)
ratings = ratings.drop_duplicates(subset=['userId', 'movieId'], keep='first')
# Duplikaty filmów (ten sam tytuł lub movieId)
movies = movies.drop_duplicates(subset=['movieId'], keep='first')
movies = movies.drop_duplicates(subset=['title'], keep='first')


# === 4. Dodanie przeskalowanej oceny 0–10 ===
# mnożenie ×2 i zmiana na całkowite liczby
ratings["rating_10"] = (ratings["rating"] * 2).astype(int)


# === 5. Zapis oczyszczonych plików ===
ratings.to_csv("ratings_clean.csv", index=False)
movies.to_csv("movies_clean.csv", index=False)


print("Gotowe! Zapisano ratings_clean.csv i movies_clean.csv")
