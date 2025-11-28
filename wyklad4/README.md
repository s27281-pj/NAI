# Klasyfikacja Jakości Wina: Drzewa Decyzyjne i SVM

Projekt realizuje zadanie klasyfikacji binarnej jakości wina na dwóch różnych zbiorach danych (białe i czerwone wino) przy użyciu Drzew Decyzyjnych oraz Maszyn Wektorów Nośnych (SVM - SVC).

Celem jest przewidzenie, czy wino zostanie ocenione jako "Wysokiej Jakości" (ocena >= 7) na podstawie jego parametrów fizykochemicznych.

## Zawartość Repozytorium

* `notebooks/wine_analysis.ipynb` - **Główny plik projektu**. Notatnik Jupyter zawierający:
    * Ładowanie, eksplorację (EDA) i preprocessing dwóch zbiorów danych o winie.
    * Transformację zadania do klasyfikacji binarnej (Dobre vs. Przeciętne).
    * Trening i ewaluację modeli Drzewa Decyzyjnego i SVM dla obu zbiorów.
    * Szczegółową analizę funkcji jądra (kernels) SVM z użyciem GridSearchCV na zbiorze białego wina.
* `reports/svm_kernel_summary_white_wine.md` - Podsumowanie wniosków dotyczących wpływu funkcji jądra i hiperparametrów na wyniki klasyfikacji SVM (dla białego wina).
* `scripts/wine_inference.py` - Samodzielny skrypt Python, który trenuje modele i pokazuje, jak wykonać predykcję (inferencję) dla nowych próbek wina.
* `data/` - Katalog na pliki z danymi.

## Źródła Danych

Aby uruchomić projekt, pobierz poniższe zbiory danych i zapisz je w katalogu `data/`:

1.  **Wine Quality Dataset (White)** - Zbiór dotyczący białego wina "Vinho Verde".
    * Źródło: UCI Machine Learning Repository / ML Mastery.
    * Bezpośredni link do pliku: `http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv`
    * **Ważne:** Zapisz plik jako `winequality-white.csv` w katalogu `data/`.

2.  **WineQT Dataset** - Zbiór dotyczący czerwonego wina (podzbiór większego zbioru).
    * Źródło: Kaggle.
    * Link: `https://www.kaggle.com/datasets/yasserh/wine-quality-dataset` (pobierz plik `WineQT.csv`)
    * Zapisz plik jako `WineQT.csv` w katalogu `data/`.

## Instrukcja Uruchomienia

1.  Sklonuj repozytorium.
2.  Pobierz pliki CSV do katalogu `data/`.
3.  Zainstaluj zależności: `pip install -r requirements.txt`
4.  Uruchom analizę: `jupyter notebook notebooks/wine_analysis.ipynb`
5.  Uruchom przykład predykcji: `python scripts/wine_inference.py`
6. 