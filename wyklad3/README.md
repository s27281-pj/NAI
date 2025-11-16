# Projekt: System Rekomendacji Filmów/Seriali oparty na Ocenach


## Wymagania
- Python 3.10+

---

## Instrukcja Instalacji i Konfiguracji

### 1. Tworzenie środowiska wirtualnego
Aby skonfigurować środowisko dla tego projektu:

1. Utwórz środowisko wirtualne:
   ```bash
   python3 -m venv venv
   ```

2. Aktywuj środowisko:
   - **Windows**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```

3. (Opcjonalnie) Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```

---

## Przygotowanie Danych

### 1. Dane Treningowe
Proces przygotowania danych treningowych wymaga następujących kroków:

1. **Pobierz dane treningowe**:
    - Zalecany do edukacji i rozwoju: [MovieLens Latest Datasets](https://grouplens.org/datasets/movielens/latest/)
    - Przykład: MovieLens Small, zawiera 100,000 ocen i 3,600 tagów dotyczących 9,000 filmów przez 600 użytkowników (Ostatnia aktualizacja: 09/2018).

2. **Konwersja skali ocen** (0-5 → 0-10):
   ```bash
   python3 convert_ratings.py
   ```

3. **Oczyszczanie danych**:
   Oczyść dane, aby przygotować je do dalszego użycia:
   ```bash
   python3 prepare_train_data.py
   ```

---

### 2. Dane Testowe
Dane testowe związane są z ocenami użytkowników w formacie .CSV:

1. **Eksportowanie ocen użytkownika**:
   Dane w formacie `.CSV` (comma-separated values). Przykład:
   ```plaintext
   Roland Liedtke,1670,10,Nowy Papież,10,Sukcesja,8,Ostre Przedmioty,8,Wielkie Kłamstewka,9
   ```

2. **Konwersja z formatu `.CSV` do `.JSON`**:
   Przykładowo:
   ```json
   {
       "Roland Liedtke": [
           {"title": "1670", "rating": 10},
           {"title": "Nowy Papież", "rating": 10},
           {"title": "Sukcesja", "rating": 8},
           {"title": "Ostre Przedmioty", "rating": 8},
           {"title": "Wielkie Kłamstewka", "rating": 9}
       ]
   }
   ```

3. **Przygotowanie danych testowych**:
   Dostosowanie danych testowych do formatu treningowego:
   ```bash
   python3 convert_data_test.py
   ```

---

## Struktura Plików Projektu

Poniżej znajduje się struktura katalogów oraz plików projektu:

      ├── data_train/                                   # Dane treningowe 
      ├── test_data/                                    # Dane testowe 
      │ ├── export.csv                                  # Surowe dane testowe .CSV
      │ ├── export.json                                 # Dane testowe w formacie JSON
      │ ├── prepare_test_data.py                        # Skrypt przekształcania danych testowych
      │ ├── test_movies.csv                             # Dane testowe (filmy)
      │ ├── test_ratings.csv                            # Dane testowe (oceny)
      │ └── test_users.csv                              # Dane testowe (użytkownicy) 
      ├── venv/                                         # Środowisko wirtualne 
      ├── main.py                                       # Główny plik projektu 
      ├── recommender.py                                # Moduł rekomendacji filmów 
      ├── requirements.txt                              # Lista zależności 
      └── README.md                                     # Dokumentacja projektu

## Autorzy

Projekt został stworzony przez:

- **Roland**
- **Cyprian**
