# Projekt: System rekomendacji filmów/seriali oparty na treści

## Przygotowanie Danych
### Dane testowe
- Exportowanie danych z ankiety w formacie .CSV (comma-separated values)
    > Roland Liedtke,1670,10,Nowy Papież,10,Sukcesja ,8,Ostre Przedmioty,8,Wielkie Kłamstewka,9

- Konwersja danch .CSV do formatu .JSON
    > "Roland Liedtke": [
    {"title": "1670", "rating": 10},
    {"title": "Nowy Papież", "rating": 10},
    {"title": "Sukcesja ", "rating": 8},
    {"title": "Ostre Przedmioty", "rating": 8},
    {"title": "Wielkie Kłamstewka", "rating": 9}]

### Dane treningowe

1. Wybór danych treningowych
   
    MovieLens Latest Datasets recommended for education and development
   
    These datasets will change over time, and are not appropriate for reporting research results. We will keep the download links stable for automated downloads. We will not archive or make available previously released versions.

    Small: 100,000 ratings and 3,600 tag applications applied to 9,000 movies by 600 users. Last updated 9/2018.
   
    Permalink: https://grouplens.org/datasets/movielens/latest/

3. Konwersja ocen ze skali 0-5 na 0-10.


## Przygotowanie Środowiska
- ```python3 -m venv venv```
- ```source venv/bin/activate```
- ```pip install pandas numpy scikit-learn requests openpyxl```
- ```python3 ratings_convert.py```


