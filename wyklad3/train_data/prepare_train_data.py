import pandas as pd

# === 1. Wczytanie danych ===
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")


# === 2. Czyszczenie danych ===
# Usuwanie wierszy z brakującymi wartościami
ratings.dropna(subset=['userId', 'movieId', 'rating'], inplace=True)
movies.dropna(subset=['movieId', 'title'], inplace=True)

# Konwersja typów danych na liczby całkowite dla ID
ratings['userId'] = ratings['userId'].astype(int)
ratings['movieId'] = ratings['movieId'].astype(int)


# Usuwanie duplikatów
ratings.drop_duplicates(subset=['userId', 'movieId'], keep='first', inplace=True)
movies.drop_duplicates(subset=['movieId'], keep='first', inplace=True)

# === 3. Przygotowanie danych do scalenia ===
# Zmiana nazwy kolumny 'title' na 'movieName' dla spójności
movies.rename(columns={'title': 'movieName'}, inplace=True)

# Generowanie danych użytkowników (userName), ponieważ nie ma pliku users.csv
unique_user_ids = ratings['userId'].unique()
users = pd.DataFrame({'userId': unique_user_ids, 'userName': [f'User_{uid}' for uid in unique_user_ids]})

# === 4. Scalanie danych w jeden zbiór ===
# Połączenie ratings z movies na podstawie 'movieId'
df_combined = pd.merge(ratings, movies[['movieId', 'movieName']], on='movieId', how='left')

# Połączenie z danymi użytkowników na podstawie 'userId'
df_combined = pd.merge(df_combined, users, on='userId', how='left')

# Usunięcie wierszy, gdzie nie udało się dopasować filmu (jeśli takie istnieją)
df_combined.dropna(subset=['movieName'], inplace=True)

# Ustawienie ostatecznej kolejności kolumn
final_columns = ['userId', 'userName', 'movieId', 'movieName', 'rating']
df_final = df_combined[final_columns]

# Konwersja rating z 0–5 na 0–10
df_final['rating'] = (df_final['rating'] * 2)


# === 5. Zapis do jednego pliku train_data.csv ===
df_final.to_csv("train_data.csv", index=False)

print("Gotowe! Zapisano scalony plik train_data.csv w katalogu train_data/")
