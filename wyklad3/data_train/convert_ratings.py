import pandas as pd


# === 1. Wczytanie danych z CSV ===
df = pd.read_csv("ratings.csv")
# print(df.head())


# === 2. Dodanie przeskalowanej oceny 0–10 ===
# mnożenie ×2 i zmiana na całkowite liczby
df["rating_10"] = (df["rating"] * 2).astype(int)


# # === 3. Zapis wyniku do pliku ===
df.to_csv("data_train/ratings_10.csv", index=False)

print("Gotowe! Zapisano jako: filmy_z_ocenami_10.csv")
