import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
import os
import sys

# =============================================
# KONFIGURACJA ŚCIEŻEK
# =============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

print("--- INICJALIZACJA SKRYPTU INFERENCJI WINA ---")
print(f"Szukam danych w katalogu: {DATA_DIR}")


# Funkcja pomocnicza do tworzenia targetu binarnego
# Jakość >= 7 uznajemy za "Dobre wino" (klasa 1)
def create_binary_target(quality_score):
    return 1 if quality_score >= 7 else 0


# ==========================================
# 1. Zbiór 1: BIAŁE WINO (White Wine)
# ==========================================
print("\n[1/2] Trenowanie modeli dla BIAŁEGO wina...")
white_path = os.path.join(DATA_DIR, 'winequality-white.csv')

if not os.path.exists(white_path):
    print(f"BŁĄD KRYTYCZNY: Nie znaleziono pliku {white_path}.")
    sys.exit(1)

try:
    # UWAGA: Ten plik często używa średnika ';' jako separatora!
    df_white = pd.read_csv(white_path, sep=';')
    df_white['target'] = df_white['quality'].apply(create_binary_target)
    X_white = df_white.drop(['quality', 'target'], axis=1)
    y_white = df_white['target']

    # Skalowanie (kluczowe dla SVM)
    scaler_white = StandardScaler()
    X_white_scaled = scaler_white.fit_transform(X_white)

    # Model 1: Drzewo Decyzyjne
    dt_model_white = DecisionTreeClassifier(random_state=42, max_depth=7)
    dt_model_white.fit(X_white, y_white)

    # Model 2: SVM (RBF, parametry dobrane empirycznie, class_weight dla balansu)
    svm_model_white = SVC(kernel='rbf', C=10, gamma='scale', class_weight='balanced', random_state=42)
    svm_model_white.fit(X_white_scaled, y_white)
    print("Modele dla białego wina gotowe.")

except Exception as e:
    print(f"Błąd przy białym winie: {e}")
    sys.exit(1)

# ==========================================
# 2. Zbiór 2: CZERWONE WINO (WineQT)
# ==========================================
print("\n[2/2] Trenowanie modeli dla CZERWONEGO wina (WineQT)...")
red_path = os.path.join(DATA_DIR, 'WineQT.csv')

if not os.path.exists(red_path):
    print(f"BŁĄD KRYTYCZNY: Nie znaleziono pliku {red_path}.")
    sys.exit(1)

try:
    # WineQT ma kolumnę 'Id', którą usuwamy
    df_red = pd.read_csv(red_path)
    if 'Id' in df_red.columns:
        df_red = df_red.drop('Id', axis=1)

    df_red['target'] = df_red['quality'].apply(create_binary_target)
    X_red = df_red.drop(['quality', 'target'], axis=1)
    y_red = df_red['target']

    # Skalowanie
    scaler_red = StandardScaler()
    X_red_scaled = scaler_red.fit_transform(X_red)

    # Model 1: Drzewo Decyzyjne
    dt_model_red = DecisionTreeClassifier(random_state=42, max_depth=6)
    dt_model_red.fit(X_red, y_red)

    # Model 2: SVM
    svm_model_red = SVC(kernel='rbf', C=1, gamma='scale', class_weight='balanced', random_state=42)
    svm_model_red.fit(X_red_scaled, y_red)
    print("Modele dla czerwonego wina gotowe.")

except Exception as e:
    print(f"Błąd przy czerwonym winie: {e}")
    sys.exit(1)

# ==========================================
# 3. INFERENCJA (Przykładowe predykcje)
# ==========================================
print("\n" + "=" * 60)
print(" ROZPOCZYNAMY PRZYKŁADOWĄ PREDYKCJĘ JAKOŚCI WINA")
print("=" * 60)
# Cechy: fixed acidity, volatile acidity, citric acid, residual sugar, chlorides,
#        free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol

# --- Przykład 1: Próbka Białego Wina (Wysokiej jakości) ---
print("\n--- PRZYKŁAD 1: Nowa próbka BIAŁEGO wina ---")
# Przykładowe dane dla dobrego białego wina (wyższy alkohol, wyższy cukier)
new_white_sample = np.array([[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 11.8]])

# Skalowanie
new_white_scaled = scaler_white.transform(new_white_sample)

# Predykcje
dt_pred_w = dt_model_white.predict(new_white_sample)
svm_pred_w = svm_model_white.predict(new_white_scaled)

print(f"Parametry (Alkohol): {new_white_sample[0][-1]}%")
print("-" * 30)
print(f"Drzewo Decyzyjne przewiduje: {'[WINO WYSOKIEJ JAKOŚCI]' if dt_pred_w[0] == 1 else '[WINO PRZECIĘTNE/SŁABE]'}")
print(f"SVM (RBF Kernel) przewiduje: {'[WINO WYSOKIEJ JAKOŚCI]' if svm_pred_w[0] == 1 else '[WINO PRZECIĘTNE/SŁABE]'}")

# --- Przykład 2: Próbka Czerwonego Wina (Przeciętnej jakości) ---
print("\n--- PRZYKŁAD 2: Nowa próbka CZERWONEGO wina ---")
# Przykładowe dane dla przeciętnego czerwonego wina (niższy alkohol, wyższa kwasowość lotna)
new_red_sample = np.array([[7.8, 0.76, 0.04, 2.3, 0.092, 15.0, 54.0, 0.997, 3.26, 0.65, 9.8]])

# Skalowanie
new_red_scaled = scaler_red.transform(new_red_sample)

# Predykcje
dt_pred_r = dt_model_red.predict(new_red_sample)
svm_pred_r = svm_model_red.predict(new_red_scaled)

print(f"Parametry (Alkohol): {new_red_sample[0][-1]}%, Kwasowość lotna: {new_red_sample[0][1]}")
print("-" * 30)
print(f"Drzewo Decyzyjne przewiduje: {'[WINO WYSOKIEJ JAKOŚCI]' if dt_pred_r[0] == 1 else '[WINO PRZECIĘTNE/SŁABE]'}")
print(f"SVM (RBF Kernel) przewiduje: {'[WINO WYSOKIEJ JAKOŚCI]' if svm_pred_r[0] == 1 else '[WINO PRZECIĘTNE/SŁABE]'}")
print("-" * 30)

print("\nSkrypt inferencji zakończył działanie.")