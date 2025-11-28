from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

class GameOfBones( TwoPlayerGame ):
    """ In turn, the players remove one, two or three bones from a
    pile of bones. The player who removes the last bone loses. """

    def __init__(self, players=None):
        self.players = players
        self.pile = 20 # start with 20 bones in the pile
        self.current_player = 1 # player 1 starts

    def possible_moves(self): return ['1','2','3']
    def make_move(self,move): self.pile -= int(move) # remove bones.
    def win(self): return self.pile<=0 # opponent took the last bone ?
    def is_over(self): return self.win() # Game stops when someone wins.
    def show(self): print ("%d bones left in the pile" % self.pile)
    def scoring(self): return 100 if game.win() else 0 # For the AI

# Start a match (and store the history of moves when it ends)
ai = Negamax(13) # The AI will think 13 moves in advance
game = GameOfBones( [ Human_Player(), AI_Player(ai) ] )
history = game.play()
