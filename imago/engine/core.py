"""Imago GTP engine"""

from random import randrange

from imago.data.enums import Player
from imago.engine.monteCarlo import MCTS
from imago.gameLogic.gameState import GameState

DEF_SIZE = 7
DEF_KOMI = 5.5

class GameEngine:
    """Plays the game of Go."""

    def __init__(self):
        self.komi = DEF_KOMI
        self.gameState = GameState(DEF_SIZE)
        self.mcts = MCTS(self.gameState.lastMove)

    def setBoardsize(self, newSize):
        """Changes the size of the board.
        Board state, number of stones and move history become arbitrary.
        It is wise to call clear_board after this command.
        """
        self.gameState = GameState(newSize)

    def clearBoard(self):
        """The board is cleared, the number of captured stones reset to zero and the move
        history reset to empty.
        """
        self.gameState.clearBoard()

    def setKomi(self, komi):
        """Sets a new value of komi."""
        self.komi = komi

    def setFixedHandicap(self, stones):
        """Sets handicap stones in fixed vertices."""
        if stones < 1 or stones > 9:
            raise Exception("Wrong number of handicap stones")
        # TODO: Set handicap stones
        return [[0,0], [0,1]]

    def play(self, color, vertex):
        """Plays in the vertex passed as argument"""
        if vertex == "pass":
            self.gameState.passForPlayer(color)
            return
        row = vertex[0]
        col = vertex[1]
        self.gameState.playMoveForPlayer(row, col, color)
        self.mcts.forceNextMove(vertex)

    def genmove(self, color):
        """Returns a list representing coordinates of the board in the form (row, col)."""
        coords = self.mcts.pickMove().coords
        #TODO: The move should NOT be played in its generation. This method is just for
        #suggesting a move.
        self.gameState.playMoveForPlayer(coords[0], coords[1], color)
        return coords

    def undo(self):
        """The board configuration and number of captured stones are reset to the state
            before the last move, which is removed from the move history.
        """
        self.gameState.undo()
