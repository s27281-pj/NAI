"""
Gra: Zdejmowanie bloków
Autor: Cyprian i Roland
Zasady: https://github.com/cypri/nai/blob/main/README.md
Instrukcja środowiska: Python 3.10+, brak dodatkowych bibliotek
"""

def get_possible_moves(blocks_left):
    """
    Zwraca możliwe ruchy w zależności od liczby pozostałych bloków.

    Parameters:
    blocks_left (int): Liczba bloków na stosie

    Returns:
    List[int]: Lista możliwych ruchów (1, 2 lub 3)
    """
    return [i for i in [1, 2, 3] if i <= blocks_left]

def is_terminal(blocks_left):
    """
    Sprawdza, czy gra się zakończyła.

    Parameters:
    blocks_left (int): Liczba bloków na stosie

    Returns:
    bool: True jeśli gra się skończyła
    """
    return blocks_left == 0

def minimax(blocks_left, maximizing_player, alpha, beta):
    """
    Algorytm Minimax z obcinaniem alfa-beta.

    Parameters:
    blocks_left (int): Liczba bloków na stosie
    maximizing_player (bool): Czy to tura AI?
    alpha (int): Wartość alfa
    beta (int): Wartość beta

    Returns:
    Tuple[int, int]: (ocena stanu, najlepszy ruch)
    """
    if is_terminal(blocks_left):
        return (-1 if maximizing_player else 1, None)

    best_value = float('-inf') if maximizing_player else float('inf')
    best_move = None

    for move in get_possible_moves(blocks_left):
        new_blocks = blocks_left - move
        value, _ = minimax(new_blocks, not maximizing_player, alpha, beta)

        if maximizing_player:
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)

        if beta <= alpha:
            break

    return best_value, best_move

def play_game(start_blocks=21):
    """
    Główna pętla gry.

    Parameters:
    start_blocks (int): Początkowa liczba bloków
    """
    blocks = start_blocks
    player_turn = True  # True = gracz, False = AI

    while not is_terminal(blocks):
        print(f"\nPozostało bloków: {blocks}")
        if player_turn:
            move = int(input("Twój ruch (1-3): "))
            if move not in get_possible_moves(blocks):
                print("Nieprawidłowy ruch. Spróbuj ponownie.")
                continue
        else:
            _, move = minimax(blocks, True, float('-inf'), float('inf'))
            print(f"AI zabiera {move} blok(i).")

        blocks -= move
        player_turn = not player_turn

    winner = "AI" if player_turn else "Gracz"
    print(f"\nKoniec gry! Wygrał: {winner}")

if __name__ == "__main__":
    play_game()