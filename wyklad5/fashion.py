import tensorflow as tf
import matplotlib.pyplot as plt


# Wczytanie zbioru Fashion-MNIST
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()


# Normalizacja danych
x_train = x_train / 255.0
x_test = x_test / 255.0


# Nazwy klas (do wizualizacji)
class_names = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
]


# Podgląd przykładowego obrazu
plt.imshow(x_train[0], cmap='gray')
plt.title(class_names[y_train[0]])
plt.axis('off')
plt.show()


# Budowa sieci neuronowej
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])


# Kompilacja modelu
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)


# Trenowanie sieci
history = model.fit(
    x_train,
    y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)


# Testowanie modelu
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Dokładność na zbiorze testowym:", test_acc)


# Predykcja dla jednego obrazu
prediction = model.predict(x_test[:1])
predicted_class = prediction.argmax()

print("Przewidziana klasa:", class_names[predicted_class])
print("Prawdziwa klasa:", class_names[y_test[0]])
