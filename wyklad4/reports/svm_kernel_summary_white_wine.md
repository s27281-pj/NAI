# Podsumowanie wpływu funkcji jądra (Kernel Function) w SVM - Białe Wino

Analiza przeprowadzona na zbiorze **Wine Quality (White)** (w ramach notatnika `wine_analysis.ipynb`) przy użyciu `GridSearchCV` pozwoliła na zbadanie wpływu różnych funkcji jądra (linear, rbf, poly, sigmoid) oraz hiperparametrów (C, gamma, degree) na skuteczność klasyfikacji binarnej jakości wina.

### Główne wnioski:

1.  **Znaczenie Skalowania:** Potwierdzono, że standaryzacja danych (np. `StandardScaler`) jest absolutnie krytyczna dla działania SVM na danych o winie, gdzie cechy mają różne zakresy (np. wysoka zawartość siarczanów vs. niskie pH).

2.  **Kernel RBF (Radial Basis Function) - Najlepszy Wybór:**
    * Kernel RBF konsekwentnie osiągał najlepsze wyniki w walidacji krzyżowej.
    * Najlepsze rezultaty uzyskano przy użyciu automatycznego skalowania parametru `gamma` (`gamma='scale'`) oraz umiarkowanie wysokiej wartości parametru regularyzacji `C` (np. C=10 lub C=100). Wskazuje to, że granica decyzyjna jest dość złożona, a model korzysta na silniejszym dopasowaniu do danych treningowych (przy jednoczesnej kontroli marginesu).

3.  **Kernel Wielomianowy (Poly):**
    * Stopnie wielomianu wyższe niż 2 (np. `degree=3`) dawały wyniki zbliżone do RBF, ale przy znacznie dłuższym czasie obliczeń.

4.  **Kernel Liniowy (Linear):**
    * Osiągnął przyzwoite wyniki, ale zauważalnie gorsze od RBF i Poly. Oznacza to, że relacja między parametrami chemicznymi a wysoką jakością wina nie jest w pełni liniowa i wymaga bardziej elastycznej granicy decyzyjnej.

5.  **Kernel Sigmoidalny (Sigmoid):**
    * Sprawdził się najgorzej, dając wyniki często niewiele lepsze od losowego zgadywania, szczególnie w przypadku niezbalansowanych klas.

**Konkluzja:** Do klasyfikacji jakości białego wina rekomendowane jest użycie SVM z kernelem **RBF**, po uprzednim przeskalowaniu danych. Dobór parametrów `C` i `gamma` metodą przeszukiwania siatki (GridSearch) jest kluczowy dla uzyskania optymalnych wyników.
