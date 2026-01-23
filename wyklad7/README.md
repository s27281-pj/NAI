# Pacman ALE Atari
---


## 👥 Autorzy
* **Cyprian Czerwiński**
* **Roland Liedtke**
---


## 📖 Opis projektu

#### Projekt demonstruje wykorzystanie środowiska Atari Pacman w Pythonie przy użyciu **Gymnasium** i **Arcade Learning Environment (ALE)**. Celem jest stworzenie prostego agenta RL (obecnie losowego) oraz nagrywanie rozgrywek wideo w celu analizy działania agenta. Projekt jest również przykładem przetwarzania obserwacji z gier Atari (skalowanie, grayscale, normalizacja) i integracji z wrapperem nagrywającym rozgrywki.
---


## 🛠 Funkcjonalności
* Integracja z Atari ALE poprzez Gymnasium
* Losowy agent RL dla gry Pacman
* Preprocessing obrazu:
  * Konwersja do odcieni szarości
  * Zmiana rozmiaru do 84x84
  * Normalizacja pikseli do [0,1]
* Nagrywanie rozgrywek wideo co drugi epizod
* Obsługa wielu epizodów i liczenie punktów
---


## 🔬 Szczegóły techniczne
* Język: **Python 3.10+**
* Biblioteki:
  * `gymnasium`
  * `ale-py`
  * `opencv-python`
  * `numpy`
* Środowisko Atari: `"ALE/Pacman-v5"`
* Wrapper `RecordVideo` do nagrywania wideo
* Wrapper `ObservationWrapper` do preprocessing obrazu
---


### **🚀 Uruchomienie lokalne**
- ```pip install -r requirements.txt```
- ```python3 main.py```
---


### Struktura plików
```plaintext
│
├── README.md              # Dokumentacja projektu
├── main.py                # Główny skrypt z agentem RL
├── q_learning.py          # Przykładowy skrypt z agentem RL 
├── recordings/            # Folder z nagraniami wideo epizodów
└── requirements.txt       # Lista zależności (opcjonalnie)

---
