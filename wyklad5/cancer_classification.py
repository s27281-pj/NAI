"""
PROBLEM: Klasyfikacja binarna zmian nowotworowych (złośliwy vs łagodny).
AUTOR: Cyprian, Roland
INSTRUKCJA UŻYCIA:
1. Upewnij się, że masz zainstalowane: pip install scikit-learn matplotlib seaborn pandas
2. Uruchom skrypt poleceniem: python cancer_classification.py
OPIS: Program wykorzystuje sieć neuronową Multi-layer Perceptron (MLP)
do analizy cech medycznych i klasyfikacji typu nowotworu.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report


def run_cancer_analysis():
    """
    Główna funkcja wykonująca ładowanie danych, trenowanie MLP i generowanie wykresów.
    """
    # 1. Załadowanie wbudowanego zbioru danych (zaskoczenie - spoza repozytorium)
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 2. Podział na zbiór treningowy i testowy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Skalowanie danych (wymagane dla stabilności sieci neuronowej)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 4. Inicjalizacja i trenowanie sieci neuronowej (MLP)
    # Wybieramy architekturę z dwiema warstwami ukrytymi
    mlp = MLPClassifier(hidden_layer_sizes=(30, 30), max_iter=1000, random_state=42)
    mlp.fit(X_train, y_train)

    # 5. Predykcja i raport w konsoli
    y_pred = mlp.predict(X_test)
    print("--- RAPORT KLASYFIKACJI ---")
    print(classification_report(y_test, y_pred, target_names=data.target_names))

    # 6. Generowanie Macierzy Pomyłek (Confusion Matrix)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',
                xticklabels=data.target_names, yticklabels=data.target_names)
    plt.xlabel('Przewidziana diagnoza')
    plt.ylabel('Rzeczywista diagnoza')
    plt.title('Macierz Pomyłek - Klasyfikacja Nowotworów')

    # Automatyczne zapisanie pliku do repozytorium
    plt.savefig('confusion_matrix_cancer.png')
    print("\n[INFO] Macierz pomyłek została zapisana jako: confusion_matrix_cancer.png")
    plt.show()


if __name__ == "__main__":
    run_cancer_analysis()