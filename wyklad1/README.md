# Gra: Zdejmowanie bloków

## Opis gry

„Zdejmowanie bloków” to turowa, deterministyczna gra dwuosobowa o sumie zerowej. Gracze na zmianę zdejmują 1, 2 lub 3 bloki ze wspólnego stosu. Przegrywa ten, kto nie może wykonać ruchu, czyli gdy stos jest pusty przed jego turą.

## Zasady

- Początkowa liczba bloków: 21 (można zmienić w kodzie).
- Dozwolone ruchy: zdjęcie 1, 2 lub 3 bloków.
- Gracze wykonują ruchy naprzemiennie.
- Przegrywa ten, kto nie może wykonać ruchu.

## Sztuczna inteligencja

AI wykorzystuje algorytm Minimax z obcinaniem alfa-beta, aby podejmować optymalne decyzje. Ocena stanu gry opiera się na tym, czy AI może doprowadzić do wygranej w danym układzie.

## Wymagania

- Python 3.10+
- Brak dodatkowych bibliotek

## Instalacja środowiska

1. Utwórz środowisko wirtualne:
python -m venv .venv

2. Aktywuj środowisko:
- Windows:
  ```
  .\.venv\Scripts\Activate.ps1
  ```
- Linux/macOS:
  ```
  source .venv/bin/activate
  ```

3. (Opcjonalnie) Zainstaluj zależności:
pip install -r requirements.txt



## Uruchomienie gry

Przejdź do katalogu `wyklad1` i uruchom:
python main.py


## Autorzy

Cyprian i Roland

## Dokumentacja

Kod zawiera pełne docstringi zgodne z wymaganiami zadania. Funkcje są opisane pod względem parametrów, zwracanych wartości i działania.

