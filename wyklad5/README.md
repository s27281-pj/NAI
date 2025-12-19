Narzędzia Sztucznej Inteligencji (NAI) – Projekt Laboratoryjny
Autor: s27281-pj

Repozytorium zawiera kompletny zbiór ćwiczeń i projektów realizowanych w ramach przedmiotu NAI. Skupia się na praktycznym zastosowaniu algorytmów uczenia maszynowego przy użyciu języka Python.

📂 Struktura Projektu
[Wykład 4] – Klasyfikacja i Inferencja
Praca z modelami klasycznymi (Drzewa Decyzyjne, SVM).

Problem: Przewidywanie jakości wina na podstawie składu chemicznego.

Lokalizacja: /wyklad4

Kluczowe pliki: wine_inference.py, dane w folderze /data.

[Wykład 5] – Sieci Neuronowe (MLP)
Implementacja i optymalizacja wielowarstwowych perceptronów (MLP).

Tematyka: Klasyfikacja gatunków irysów, analiza regresji oraz autorski przypadek użycia.

Lokalizacja: /wyklad5

Główny skrypt: cancer_classification.py

🌟 Zadanie 4: Autorski przypadek użycia (Wykład 5)
Zgodnie z wymaganiami, zaproponowano autorski problem klasyfikacji przy użyciu sieci neuronowych, który nie był omawiany podczas wykładu.

🧬 Klasyfikacja Nowotworów (Breast Cancer Classification)
Cel: Automatyczna diagnostyka binarna: nowotwór łagodny (benign) vs złośliwy (malignant).

Dane: Zbiór Breast Cancer Wisconsin (30 cech medycznych, 569 próbek).

Model: Wielowarstwowa Sieć Neuronowa (MLP) z dwiema warstwami ukrytymi po 30 neuronów każda.

Skuteczność: Model osiągnął wysoką celność na poziomie 96%.

📊 Wyniki i Ewaluacja
W folderze /wyklad5 znajdują się dowody poprawności działania modelu:

confusion_matrix_cancer.png: Wizualizacja macierzy pomyłek, pokazująca niską liczbę błędów typu False Positive/Negative.

scenariusz_testowy.png: Zrzut ekranu z konsoli prezentujący raport klasyfikacji (Precision, Recall, F1-Score).

🛠️ Instrukcja uruchomienia
1. Wymagania
Wszystkie niezbędne biblioteki znajdują się w pliku requirements.txt.

Bash

pip install -r wyklad5/requirements.txt
2. Uruchomienie projektu (Przykład)
Aby uruchomić najnowszą część projektu (klasyfikacja nowotworów):

Bash

cd wyklad5
python cancer_classification.py
📝 Dokumentacja Techniczna
Kod źródłowy: Każdy plik posiada dokumentację typu Docstring opisującą funkcje, parametry oraz zwracane wartości.

Komentarze: Rozwiązania poprzedzone są nagłówkiem zawierającym opis problemu, autora oraz instrukcję użycia.

Dane: Zbiory danych znajdują się w folderach /data lub są ładowane bezpośrednio z biblioteki scikit-learn (dla pełnej przenośności kodu).