"""Imago GTP engine"""

from random import randrange

from imago.data.enums import Player
from imago.gameLogic.gameState import GameState

DEF_SIZE = 19
DEF_KOMI = 5.5

class GameEngine:
    """Plays the game of Go."""

    def __init__(self):
        self.komi = DEF_KOMI
        self.gameState = GameState(DEF_SIZE)

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
        """Sets handicap stones in fixed vertexes."""
        if stones < 1 or stones > 9:
            raise Exception("Wrong number of handicap stones")
        # TODO: Set handicap stones
        return [[0,0], [0,1]]

    def play(self, color, vertex):
        """Plays in the vertex passed as argument"""
        row = vertex[0]
        col = vertex[1]
        self.gameState.playMoveForPlayer(row, col, color)

    def genmove(self, color):
        """The key of this TFG."""
        validCells = []
        board = self.gameState.getBoard().board
        size = self.gameState.size
        for row in range(size):
            for col in range(size):
                if board[row][col] == Player.EMPTY:
                    validCells.append([row, col])
        randIndex = randrange(0, len(validCells))
        move = validCells[randIndex]
        self.gameState.playMoveForPlayer(move[0], move[1], color)
        return move

    def undo(self):
        """The board configuration and number of captured stones are reset to the state
            before the last move, which is removed from the move history.
        """
        self.gameState.undo()
