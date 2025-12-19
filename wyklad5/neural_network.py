import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.utils import to_categorical


# Wczytanie danych
data = pd.read_csv("data/winequality-white.csv", sep=";")
print(data.head())


# Podział na cechy i etykiety
X = data.drop("quality", axis=1).values
y = data["quality"].values


# Normalizacja cech
scaler = StandardScaler()
X = scaler.fit_transform(X)


# Przygotowanie etykiet (one-hot)
y = y - y.min()  # np. 3–8 → 0–5
y = to_categorical(y)


# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# Budowa sieci neuronowej
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(11,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(y.shape[1], activation='softmax')
])


# Kompilacja modelu
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)


# Trenowanie
history = model.fit(
    X_train,
    y_train,
    epochs=30,
    batch_size=16,
    validation_split=0.2
)


# Test modelu
loss, accuracy = model.evaluate(X_test, y_test)
print("Dokładność modelu:", accuracy)

