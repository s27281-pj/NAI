# 👁️ Ludovico AI: Etyczny koszmar wymuszonych reklam

### **Live Demo:** [https://bad-advertising.pages.dev/](https://bad-advertising.pages.dev/)

---

## 👥 Autorzy
* **Cyprian Czerwiński**
* **Roland Liedke**

---

## 📖 Opis projektu
Projekt jest eksperymentem edukacyjnym mającym na celu ukazanie zagrożeń związanych z tzw. **Dark Patterns** (mrocznymi wzorcami projektowymi) oraz inwazyjnym wykorzystaniem sztucznej inteligencji w technologiach reklamowych.

Inspiracją dla projektu była **"Technika Ludovico"** z filmu Stanleya Kubricka *Mechaniczna Pomarańcza (1971)*. Platforma wymusza na użytkowniku konsumpcję treści reklamowej poprzez monitorowanie jego danych biometrycznych w czasie rzeczywistym. Jeśli użytkownik spróbuje uniknąć reklamy, system stosuje agresywne techniki "korekcyjne".

---

## 🛠 Funkcjonalności~~~~
Platforma implementuje trzy główne mechanizmy inwigilacyjne:

* **Detekcja obecności twarzy:** Reklama automatycznie zatrzymuje się, gdy twarz użytkownika nie jest wykrywana w polu widzenia kamery.
* **Detekcja zamkniętych oczu:** Wykorzystując algorytm **EAR (Eye Aspect Ratio)**, system sprawdza, czy widz nie zamknął oczu w celu uniknięcia przekazu.
* **Agresywne wymuszanie uwagi:** W przypadku wykrycia naruszenia (odwrócenie wzroku lub zamknięcie oczu), platforma:
    * Natychmiast wstrzymuje odtwarzanie wideo.
    * Wyświetla jaskrawoczerwony alert systemowy.
    * Emituje wysoki, irytujący pisk (częstotliwość **3000 Hz**, fala piłokształtna) wygenerowany przez **Web Audio API**.

---

## 🔬 Szczegóły techniczne

### **Algorytm EAR (Eye Aspect Ratio)**
System analizuje 68 punktów charakterystycznych twarzy (*landmarks*), aby obliczyć stopień otwarcia powiek. 



Zastosowany wzór matematyczny:

$$EAR = \frac{||P_2 - P_6|| + ||P_3 - P_5||}{2 ||P_1 - P_4||}$$

Gdy wartość **EAR** spadnie poniżej progu **0.21**, system uznaje, że oczy są zamknięte i aktywuje alarm dźwiękowy oraz wizualny.

### **Zależności i technologie**
* **face-api.js:** Biblioteka zbudowana na **TensorFlow.js**, służąca do detekcji twarzy i punktów charakterystycznych bezpośrednio w przeglądarce.
* **Web Audio API:** Wykorzystane do generowania syntetycznego dźwięku (oscylatora) w czasie rzeczywistym.
* **Clockwork-orange-1971.m4v:** Symboliczny zasób wideo nawiązujący do motywu przymusowego oglądania treści.

---


### **🚀 Uruchomienie lokalne**
Ze względu na wykorzystanie kamery i modeli SI, projekt musi być uruchomiony przez **serwer lokalny** (protokół `http/https`), aby przeglądarka mogła uzyskać dostęp do funkcji biometrycznych.

1.  **Sklonuj repozytorium** na swój dysk lokalny.
2.  **Sprawdź modele:** Upewnij się, że w folderze `models/` znajdują się wymagane pliki wag (`.json` oraz `shard1`).
3.  **Uruchom serwer lokalny:**
    * **PyCharm:** Otwórz plik `index.html` i kliknij ikonę przeglądarki Chrome w prawym górnym rogu edytora.
    * **VS Code:** Zainstaluj rozszerzenie "Live Server", kliknij prawym przyciskiem na `index.html` i wybierz "Open with Live Server".
    * **Python:** W terminalu (w folderze projektu) wpisz `python -m http.server 8000`.
4.  **Zezwól na dostęp:** Po otwarciu strony zaakceptuj **Disclaimer** oraz przyznaj przeglądarce uprawnienia do korzystania z **kamery internetowej**.


### **Zależności i technologie**
* **face-api.js:** Biblioteka zbudowana na **TensorFlow.js**, służąca do detekcji twarzy i punktów charakterystycznych bezpośrednio w przeglądarce.
* **Web Audio API:** Wykorzystane do generowania syntetycznego dźwięku (oscylatora) w czasie rzeczywistym.
* **Clockwork-orange-1971.m4v:** Symboliczny zasób wideo nawiązujący do motywu przymusowego oglądania treści.

---

### **⚖️ Nota etyczna**
> **Projekt powstał wyłącznie w celach edukacyjnych.** Jego zadaniem jest demonstracja, w jaki sposób monitorowanie biometryczne i algorytmy śledzenia wzroku mogą zostać wykorzystane przeciwko autonomii i prywatności użytkownika (tzw. **dark patterns**). 
> 
> **Prywatność:** Aplikacja **nie zapisuje**, nie przetwarza w chmurze ani nie przesyła obrazu z kamery użytkownika. Wszystkie obliczenia związane z detekcją twarzy i punktów charakterystycznych odbywają się w czasie rzeczywistym, lokalnie na urządzeniu klienta.



## 📂 Struktura repozytorium
```plaintext
/
├── index.html        # Interfejs główny (Disclaimer & Player)
├── style.css         # Style wizualne i animacje alertów
├── app.js            # Serce systemu (Logika AI, Audio, Sterowanie)
├── assets/           # Materiały wideo (Clockwork-orange-1971.m4v)
└── models/           # Wagi modeli SI (TinyFaceDetector & Landmark68)






