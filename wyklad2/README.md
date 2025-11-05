# MoonLanding: Fuzzy Autopilot Simulation
**MoonLanding** to symulacja lądowania statku kosmicznego na powierzchni księżyca, oparta na logice rozmytej typu 1. 
Gra została stworzona w Pygame i zawiera dynamiczny autopilot, który analizuje pozycję, wysokość i prędkość, 
aby bezpiecznie sprowadzić statek na płaską platformę.
Autopilot oraz modyfikacje gry zostały opracowane przez Cypriana i Rolanda.
Oryginalna wersja gry została udostępniona na licencji MIT przez pyrex8 (2016).

### Sterowanie
    ← / →        - Sterowanie poziome ręczne
    SPACE        - Hamowanie pionowe ręczne
    A            - Włącz/wyłącz autopilota
    R            - Restart gry
    ESC          - Wyjście z gry
    
#### Autopilot (Fuzzy Logic)
Autopilot analizuje trzy zmienne wejściowe:
- ``dx``: odległość pozioma od środka platformy
- ``dy``: wysokość nad platformą
- ``vy``: prędkość pionowa

Na podstawie przynależności do zbiorów rozmytych podejmuje decyzje:
- Sterowanie poziome: dynamiczne, zależne od stopnia odchylenia (``dx``)
- Hamowanie pionowe: aktywowane przy niskiej wysokości i dużej prędkości opadania

Dodatkowo autopilot ląduje tylko na płaskiej platformie (nachylenie ≤ 10 px).

#### Parametry techniczne
- Rozdzielczość: 400x400 px
- Paliwo początkowe: 5000
- Maksymalna prędkość lądowania: 30 px/frame
- Platforma lądowania: generowana dynamicznie, zawsze płaska

#### Instalacja
- Upewnij się, że masz zainstalowanego Pythona 3.8+
- Zainstaluj wymagane biblioteki:
- pip install -r requirements.txt
- Uruchom grę:
- python main.py

#### Struktura projektuMoonLanding/
    ├── main.py           - Główna pętla gry
    ├── requirements.txt  - Lista zależności
    ├── LICENSE.md        - Licencja MIT (oryginalna)
    ├── README.txt        - DokumentacjaLicencjaProjekt oparty na licencji MIT:

#### Copyright (c) 2016 pyrex8

### Autopilot i modyfikacje: Cyprian i Roland
Niniejsze oprogramowanie udostępniane jest bez żadnych gwarancji, z pełnym prawem do użycia, kopiowania, modyfikacji i dystrybucji.

> Szczegóły znajdziesz w pliku LICENSE.md
> 
> Referencje - Sahin, M., & Kumbasar, T. (2021). Type-2 fuzzy logic-based lunar lander control
> 
> Pygame documentation: https://www.pygame.org/docs
> 
> scikit-fuzzy documentation: https://scikit-fuzzy.github.io

### **Uwagi** - Autopilot działa tylko po aktywacji klawiszem A
- Lądowanie możliwe tylko na wyznaczonej platformie
- Kolizja następuje przy zetknięciu z terenem poza platformą lub zbyt dużej prędkości
