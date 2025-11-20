t# recommender.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime


# === Ustawienia ===
TOP_N = 5                                       # ile rekomendacji zwrócić domyślnie
# RATINGS_CSV = "test_data/test_ratings.csv"
# MOVIES_CSV = "test_data/test_movies.csv"
RATINGS_CSV = "train_data/ratings.csv"
MOVIES_CSV = "train_data/movies.csv"



# === Konfiguracja logowania ===
LOG_TO_FILE = True               # False = tylko konsola, True = zapis do pliku
LOG_FILE = "logs.txt"
PRINTED_FILE = "printed_output.txt"



# === Kolory ANSI ===
COLOR_INFO = "\033[94m"      # niebieski
COLOR_RESET = "\033[0m"



# === Logger ===
def log(message):
    """
    Loguje komunikat typu INFO, wypisuje go w kolorze oraz opcjonalnie zapisuje do pliku.

    Parameters
    ----------
    message : str - Treść komunikatu do zalogowania.
    """
    formatted = f"[INFO] {message}"
    print(f"{COLOR_INFO}{formatted}{COLOR_RESET}")   # kolorowa konsola

    if LOG_TO_FILE:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} {formatted}\n")



def save_printed_to_file(data, label):
    """
    Automatycznie zapisuje wydrukowane dane (tekst, DataFrame lub listę) do pliku.

    Parameters
    ----------
    data : Any - Dane przeznaczone do zapisania w pliku.
    label : str - Tytuł sekcji zapisywanej w pliku.
    """
    with open(PRINTED_FILE, "a", encoding="utf-8") as f:
        f.write("\n=== WYDRUK: " + label + " ===\n")
        f.write(str(data))
        f.write("\n===========================\n")
    log(f"Dane zapisane do {PRINTED_FILE} (sekcja: {label})")



def ask_to_print(data, label):
    """
    Zadaje pytanie użytkownikowi, czy dane mają być wydrukowane.
    Jeśli odpowiedź == 't', drukuje dane oraz zapisuje je automatycznie do pliku.

    Parameters
    ----------
    data : Any - Obiekt do wydrukowania / zapisania.
    label : str - Nazwa sekcji dla czytelności.
    """
    answer = input(f"Czy chcesz wydrukować {label}? (t/n): ").strip().lower()
    if answer == "t":
        print("\n=== WYDRUK:", label, "===\n")
        print(data)
        print("\n============================\n")
        save_printed_to_file(data, label)



# === 1. Wczytanie danych ===
def load_data(ratings_path=RATINGS_CSV, movies_path=MOVIES_CSV):
    """
        Wczytuje dane o ocenach i filmach z plików CSV.

        Parameters
        ----------
        ratings_path : str
            Ścieżka do pliku z ocenami (kolumny: userId, movieId, rating)
        movies_path : str
            Ścieżka do pliku z filmami (kolumny: movieId, title)

        Returns
        -------
        ratings : DataFrame
        movies : DataFrame
    """
    log("Wczytywanie danych...")
    ratings = pd.read_csv(ratings_path)
    movies = pd.read_csv(movies_path)
    # upewnij się, że id są liczbami
    ratings['userId'] = ratings['userId'].astype(int)
    ratings['movieId'] = ratings['movieId'].astype(int)
    log(f"Wczytano: {len(ratings)} ocen, {len(movies)} filmów")

    ask_to_print(ratings.head(), "pierwszych 5 rekordów ocen")
    ask_to_print(movies.head(), "pierwszych 5 rekordów filmów")

    return ratings, movies


# === 2. Budowa macierzy użytkownik × film ===
def build_user_item_matrix(ratings):
    """
        Tworzy macierz Użytkownik × Film: wiersze = użytkownicy, kolumny = filmy, wartości = średnie oceny.

        Parameters
        ----------
        ratings : DataFrame - Dane o ocenach

        Returns
        -------
        DataFrame - Macierz ocen z uzupełnionymi wartościami 0 dla brakujących ocen.
    """
    log("Budowanie macierzy Użytkownik × Film...")
    # pivot: wiersze = userId, kolumny = movieId, wartości = rating
    user_item = ratings.pivot_table(index='userId', columns='movieId', values='rating', aggfunc='mean')
    # zamień NaN na 0 (brak oceny)
    user_item_filled = user_item.fillna(0)
    log(f"Macierz ma wymiary: {user_item_filled.shape}")

    ask_to_print(user_item_filled, "macierzy Użytkownik × Film")

    return user_item_filled


# === 3. Obliczenie podobieństwa film-film (item-based) ===
def build_item_similarity_matrix(user_item_filled):
    """
        Wylicza macierz podobieństwa między filmami metodą cosine similarity.

        Parameters
        ----------
        user_item_filled : DataFrame - Macierz ocen Użytkownik × Film

        Returns
        -------
        DataFrame - Kwadratowa macierz podobieństw (filmy × filmy)
    """
    log("Obliczanie macierzy podobieństwa filmów...")
    # transponuj, bo chcemy wektory filmów (kolumny macierzy user_item)
    item_matrix = user_item_filled.T.values  # shape: (n_items, n_users)
    # cosine similarity między wierszami (filmami)
    sim = cosine_similarity(item_matrix)
    # indeksy odpowiadają movieId w user_item_filled.columns
    item_ids = user_item_filled.columns.to_numpy()
    sim_df = pd.DataFrame(sim, index=item_ids, columns=item_ids)
    log("Macierz podobieństwa obliczona")

    ask_to_print(sim_df, "macierzy podobieństwa filmów")

    return sim_df


# === 4. Prognozowanie oceny użytkownika dla konkretnego filmu ===
def predict_score_for_user_movie(user_id, movie_id, user_item_filled, item_sim_df, k=None):
    """
    Predykcja oceny użytkownika dla konkretnego filmu metodą item-based CF.

    Zasady:
    - wykorzystywane są tylko dodatnie podobieństwa (ujemne ignorowane)
    - opcjonalnie można ograniczyć liczbę filmów do top-k najbardziej podobnych
    - wynik jest obcięty do zakresu ocen występujących w danych

    Parameters
    ----------
    user_id : int - Id użytkownika
    movie_id : int - Id filmu dla którego przewidywana jest ocena
    user_item_filled : DataFrame - Macierz ocen użytkownik × film
    item_sim_df : DataFrame - Macierz podobieństw filmów

    Returns
    -------
    float - Przewidywana ocena filmu (zaokrąglona do zakresu ocen)
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

    # opcjonalnie top-k najbardziej podobnych filmów (bez samego filmu)
    if k is not None:
        sims = sims.drop(index=movie_id).nlargest(k)

    # bierzemy tylko dodatnie podobieństwa (ujemne ignorujemy)
    sims = sims[sims > 0]
    if sims.empty:
        return 0.0  # brak podstaw do oszacowania

    # weź oceny użytkownika tylko dla tych filmów, które mają wartość != 0
    user_ratings = user_vector.loc[sims.index]
    # oblicz ważoną sumę
    numerator = (sims * user_ratings).sum()
    denominator = sims.sum()

    pred = numerator / denominator if denominator != 0 else 0.0

    # ===== KLUCZOWA LINIA — ograniczenie do zakresu 0–1 =====
    pred = max(0.0, min(1.0, pred))

    return float(pred)


# === 5. Generowanie top-N rekomendacji dla użytkownika ===
def recommend_for_user(user_id, user_item_filled, item_sim_df, movies_df, top_n=TOP_N, k_sim=None):
    """
    Generuje listę top-N najlepszych rekomendacji filmowych dla użytkownika.

    Parameters
    ----------
    user_id : int - Id użytkownika
    user_item_filled : DataFrame - Macierz ocen Użytkownik × Film
    item_sim_df : DataFrame - Macierz podobieństw filmów
    movies_df : DataFrame - Informacje o filmach (mapowanie movieId → title)
    top_n : int - Liczba rekomendacji do zwrócenia
    k_sim : int or None - Limit podobnych filmów branych pod uwagę przy predykcji

    Returns
    -------
    list[dict] - Lista słowników: movieId, title, predicted_score
    """
    log(f"Generowanie rekomendacji dla użytkownika {user_id}...")
    if user_id not in user_item_filled.index:
        raise ValueError(f"Nie znam użytkownika o userId = {user_id}")

    # filmy, które użytkownik jeszcze nie ocenił
    user_row = user_item_filled.loc[user_id]
    unrated_movie_ids = user_row[user_row == 0].index.tolist()
    log(f"Filmy nieocenione: {len(unrated_movie_ids)}")


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

    ask_to_print(pd.DataFrame(result), "tabeli rekomendacji")

    log("Rekomendacje wygenerowane")
    return result


# === 6. Prosty przykład użycia ===
def main_example():
    """
        Przykładowe uruchomienie systemu rekomendacji:
        1) Wczytanie danych
        2) Zbudowanie macierzy ocen i podobieństwa
        3) Wybranie użytkownika
        4) Wygenerowanie rekomendacji
    """
    log("Uruchamianie systemu rekomendacji")
    ratings, movies = load_data()
    user_item = build_user_item_matrix(ratings)
    item_sim = build_item_similarity_matrix(user_item)


    # =====> TUTAJ ZMIANA UŻYTKOWNIKA <=======
    # wybierz userId którego chcesz rekomendować
    sample_user_id = user_item.index[0]  # pierwszy użytkownik w danych
    print(f"[INFO] Wybrany userId: {sample_user_id}")

    recs = recommend_for_user(sample_user_id, user_item, item_sim, movies, top_n=TOP_N, k_sim=20)
    print("\n=== Wyniki rekomendacji ===")
    for i, r in enumerate(recs, 1):
        print(f"{i}. [{r['movieId']}] {r['title']}  — predicted_score: {r['predicted_score']:.3f}")


if __name__ == "__main__":
    main_example()
