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
        self.lastMove = GameMove(Player.EMPTY, newBoard)
        self.gameTree.firstMoves.append(self.lastMove)

    def getCurrentPlayer(self):
        """Gets the player who should make the next move."""
        if self.lastMove is None:
            return Player.BLACK
        if self.lastMove.player is Player.EMPTY:
            return Player.BLACK
        return Player.otherPlayer(self.lastMove.player)

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

        # Check valid move
        if not self.prevalidateMove(row, col):
            print("Invalid move!")
            return False

        # Check suicide
        if self.getBoard().isMoveSuicidal(row, col, player):
            print("Invalid move! (Suicide)")
            return False

        # Check ko
        prevBoards = self.lastMove.getThisAndPrevBoards()
        if self.getBoard().isMoveKoIllegal(row, col, player, prevBoards):
            print("Invalid move! (Ko)")
            return False

        # Move is legal
        self.__addMove(player, row, col)
        return True

    def undo(self):
        """Sets the move before the last move as the new last move."""
        self.lastMove = self.lastMove.previousMove

    def prevalidateMove(self, row, col):
        """Returns True if move is inside bounds and cell is empty, False if not."""
        if not self.getBoard().isMoveInBoardBounds(row, col):
            return False
        if not self.getBoard().isCellEmpty(row, col):
            return False
        return True

    def __addMove(self, player, row, col):

        # Check a last move already exists
        if self.lastMove is None:
            raise RuntimeError("Last move of the GameState is None.")

        # Add and return the new move
        self.lastMove = self.lastMove.addMoveForPlayer(row, col, player)
        return self.lastMove
