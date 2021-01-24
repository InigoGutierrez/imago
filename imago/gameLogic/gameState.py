"""Storing state of the game."""

from imago.data.enums import Player
from imago.gameLogic.gameTree import GameTree
from imago.gameLogic.gameMove import GameMove
from imago.gameLogic.gameBoard import GameBoard, cellToString

class GameState:
    """Stores the state of the game."""

    def __init__(self, size):
        self.size = size
        self.gameTree = None
        self.lastMove = None
        self.initState()

    def getCurrentPlayer(self):
        """Gets the player who should make the next move."""
        if self.lastMove is None:
            return Player.BLACK
        return Player.otherPlayer(self.lastMove.player)

    def getPlayerCode(self):
        """Gets a string representation of the current player."""
        return cellToString(self.getCurrentPlayer())

    def getBoard(self):
        """Returns the board as of the last move."""
        if self.lastMove is None:
            return GameBoard(self.size)
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

        newBoard = self.getBoard().getDeepCopy()

        newBoard.board[row][col] = player

        groupLiberties = newBoard.getGroupLiberties(row, col)

        # Check suicide
        killed = newBoard.moveCapture(row, col, player)
        if killed == 0 and len(groupLiberties) == 0:
            print("Invalid move! (Suicide)")
            return False

        # Check ko
        if self.lastMove is not None:
            illegalKoVertex = self.lastMove.makesKo
            if illegalKoVertex is not None:
                if row == illegalKoVertex[0] and col == illegalKoVertex[1]:
                    print("Invalid move! (Ko)")
                    return False

        # Move is legal

        # Check if move makes ko
        makesKo = None
        if killed == 1 and len(groupLiberties) == 1:
            makesKo = groupLiberties[0]

        self.__addMove(player, row, col, makesKo, newBoard)
        return True

    def undo(self):
        """Sets the move before the last move as the new last move."""
        self.lastMove = self.lastMove.previousMove

    def initState(self):
        """Starts current player, captured stones, board and game tree."""
        self.capturesBlack = 0
        self.capturesWhite = 0
        self.gameTree = GameTree()
        self.lastMove = None

    def clearBoard(self):
        """Clears the board, captured stones and game tree."""
        self.initState()

    def prevalidateMove(self, row, col):
        """Returns True if move is valid, False if not."""
        if (row < 0 or row >= self.size
            or col < 0 or col >= self.size):
            return False
        if self.getBoard().board[row][col] != Player.EMPTY:
            return False
        return True

    def __addMove(self, player, row, col, makesKo, newBoard):
        if self.lastMove is None:
            self.lastMove = GameMove(player, row, col, makesKo, newBoard)
            self.gameTree.firstMoves.append(self.lastMove)
        else:
            self.lastMove = self.lastMove.addMove(player, row, col, makesKo, newBoard)
        return self.lastMove
