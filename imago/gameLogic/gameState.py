"""Storing state of the game."""

from imago.data.enums import Player
from imago.gameLogic.gameTree import GameTree
from imago.gameLogic.gameMove import GameMove
from imago.gameLogic.gameBoard import GameBoard, cellToString

class GameState:
    """Stores the state of the game."""

    def __init__(self, size):
        self.size = size
        self.gameTree = GameTree()
        newBoard = GameBoard(self.size, self.size)
        self.lastMove = GameMove(newBoard)
        self.gameTree.firstMoves.append(self.lastMove)

    def getCurrentPlayer(self):
        """Gets the player who should make the next move."""
        if self.lastMove is None:
            return Player.BLACK
        if self.lastMove.getPlayer() is Player.EMPTY:
            return Player.BLACK
        return Player.otherPlayer(self.lastMove.getPlayer())

    def getPlayerCode(self):
        """Gets a string representation of the current player."""
        return cellToString(self.getCurrentPlayer())

    def getBoard(self):
        """Returns the board as of the last move."""
        if self.lastMove is None:
            return GameBoard(self.size, self.size)
        return self.lastMove.board

    def playMove(self, row, col):
        """Execute a move on the board for the current player and switches players."""
        return self.playMoveForPlayer(row, col, self.getCurrentPlayer())

    def playMoveForPlayer(self, row, col, player):
        """Execute a move on the board for the given player."""

        prevBoards = self.lastMove.getThisAndPrevBoards()
        playable, message = self.lastMove.board.isPlayable(row, col, player, prevBoards)
        if playable:
            self.__addMove(player, row, col)
            return True
        print("Invalid Move! %s" % message)
        return False

    def playPass(self):
        """Passes the turn for the given player."""
        self.lastMove.addPass()

    def undo(self):
        """Sets the move before the last move as the new last move."""
        self.lastMove = self.lastMove.previousMove

    def __addMove(self, player, row, col):

        # Check a last move already exists
        if self.lastMove is None:
            raise RuntimeError("Last move of the GameState is None.")

        # Add and return the new move
        self.lastMove = self.lastMove.addMoveForPlayer(row, col, player)
        return self.lastMove
