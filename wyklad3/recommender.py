# recommender.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# === Ustawienia ===
RATINGS_CSV = "data_train/ratings_10.csv"       # columns: userId,movieId,rating
MOVIES_CSV = "data_train/movies_clean.csv"      # columns: movieId,title
TOP_N = 5                                       # ile rekomendacji zwrócić domyślnie


# === 1. Wczytanie danych ===
def load_data(ratings_path=RATINGS_CSV, movies_path=MOVIES_CSV):
    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)
    # upewnij się, że id są liczbami
    ratings['userId'] = ratings['userId'].astype(int)
    ratings['movieId'] = ratings['movieId'].astype(int)
    return ratings, movies


# === 2. Budowa macierzy użytkownik × film ===
def build_user_item_matrix(ratings):
    # pivot: wiersze = userId, kolumny = movieId, wartości = rating
    user_item = ratings.pivot_table(index='userId', columns='movieId', values='rating_10', aggfunc='mean')
    # zamień NaN na 0 (brak oceny)
    user_item_filled = user_item.fillna(0)
    return user_item_filled


# === 3. Obliczenie podobieństwa film-film (item-based) ===
def build_item_similarity_matrix(user_item_filled):
    # transponuj, bo chcemy wektory filmów (kolumny macierzy user_item)
    item_matrix = user_item_filled.T.values  # shape: (n_items, n_users)
    # cosine similarity między wierszami (filmami)
    sim = cosine_similarity(item_matrix)
    # indeksy odpowiadają movieId w user_item_filled.columns
    item_ids = user_item_filled.columns.to_numpy()
    sim_df = pd.DataFrame(sim, index=item_ids, columns=item_ids)
    return sim_df


# === 4. Prognozowanie oceny użytkownika dla konkretnego filmu ===
def predict_score_for_user_movie(user_id, movie_id, user_item_filled, item_sim_df, k=None):
    """
    Predykcja oceny użytkownika user_id dla filmu movie_id.
    Używa ważonej sumy ocen użytkownika dla innych filmów i podobieństwa.
    Jeśli k podane -> używa top-k najbardziej podobnych filmów jako wag.
    """
    if movie_id not in item_sim_df.index:
        return None  # brak filmu w macierzy

    # wektor ocen użytkownika (po wszystkim: 0 jeśli brak oceny)
    try:
        user_vector = user_item_filled.loc[user_id]
    except KeyError:
        # nieznany użytkownik
        return None

    # wektor podobieństw wybranego filmu do wszystkich pozostałych filmów
    sims = item_sim_df.loc[movie_id]

    # Jeśli k: weź tylko k najbardziej podobnych filmów (poza samym filmem)
    if k is not None:
        # sortuj malejąco, pobierz indeksy top k (pomijając sam movie_id)
        topk = sims.drop(index=movie_id).nlargest(k).index
        sims = sims.loc[topk]

    # weź oceny użytkownika tylko dla tych filmów, które mają wartość != 0
    user_ratings = user_vector.loc[sims.index]
    # oblicz ważoną sumę
    numerator = (sims * user_ratings).sum()
    denominator = sims.abs().sum()
    if denominator == 0:
        return 0.0
    return numerator / denominator


# === 5. Generowanie top-N rekomendacji dla użytkownika ===
def recommend_for_user(user_id, user_item_filled, item_sim_df, movies_df, top_n=TOP_N, k_sim=None):
    """
    Zwraca top_n rekomendacji (movieId, title, predicted_score) dla user_id.
    k_sim -> jeżeli chcesz ograniczyć liczbę podobnych filmów użytych do predykcji.
    """
    if user_id not in user_item_filled.index:
        raise ValueError(f"Nie znam użytkownika o userId = {user_id}")

    # filmy, które użytkownik jeszcze nie ocenił
    user_row = user_item_filled.loc[user_id]
    unrated_movie_ids = user_row[user_row == 0].index.tolist()

    preds = []
    for mid in unrated_movie_ids:
        score = predict_score_for_user_movie(user_id, mid, user_item_filled, item_sim_df, k=k_sim)
        preds.append((mid, score))

    # sortuj po score malejąco i wybierz top_n
    preds_sorted = sorted(preds, key=lambda x: (x[1] if x[1] is not None else -np.inf), reverse=True)
    top_preds = preds_sorted[:top_n]

    # dołącz tytuły
    movie_title_map = movies_df.set_index('movieId')['title'].to_dict()
    result = []
    for mid, score in top_preds:
        title = movie_title_map.get(mid, "<unknown>")
        result.append({"movieId": int(mid), "title": title, "predicted_score": float(score) if score is not None else None})
    return result


# === 6. Prosty przykład użycia ===
def main_example():
    ratings, movies = load_data()
    user_item = build_user_item_matrix(ratings)
    item_sim = build_item_similarity_matrix(user_item)

    # wybierz userId którego chcesz rekomendować
    sample_user_id = user_item.index[0]  # pierwszy użytkownik w danych
    print(f"Generuję rekomendacje dla userId = {sample_user_id}")

    recs = recommend_for_user(sample_user_id, user_item, item_sim, movies, top_n=TOP_N, k_sim=20)
    for i, r in enumerate(recs, 1):
        print(f"{i}. [{r['movieId']}] {r['title']}  — predicted_score: {r['predicted_score']:.3f}")

if __name__ == "__main__":
    main_example()
