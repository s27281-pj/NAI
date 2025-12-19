# Przykład: uczenie sieci CNN do rozpoznawania zwierząt ze zbioru CIFAR-10
# Framework: TensorFlow / Keras
# Zwierzęta w CIFAR-10: bird, cat, deer, dog, frog, horse

import tensorflow as tf
from tensorflow.keras import layers, models

# 1. Parametry
BATCH_SIZE = 128
EPOCHS = 10

# 2. Wczytanie danych CIFAR-10
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# Normalizacja [0,1]
x_train = x_train.astype("float32") / 255.0
x_test  = x_test.astype("float32") / 255.0

# Spłaszczenie etykiet
y_train = y_train.squeeze()
y_test  = y_test.squeeze()

# 3. Definicja klas
class_names = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck"
]

animal_classes = [2, 3, 4, 5, 6, 7]

# 4. Augmentacja danych
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])

# 5. Model CNN
model = models.Sequential([
    data_augmentation,
    layers.Conv2D(32, 3, activation="relu", padding="same", input_shape=(32, 32, 3)),
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, activation="relu", padding="same"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, 3, activation="relu", padding="same"),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(256, activation="relu"),
    layers.Dense(10, activation="softmax")  # 10 klas CIFAR-10
])

model.summary()

# 6. Kompilacja
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# 7. Trening
history = model.fit(
    x_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.1
)

# 8. Ewaluacja tylko dla zwierząt
import numpy as np

y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis=1)

mask = np.isin(y_test, animal_classes)

animal_accuracy = np.mean(y_pred_classes[mask] == y_test[mask])
print(f"Dokładność dla klas zwierząt: {animal_accuracy * 100:.2f}%")
