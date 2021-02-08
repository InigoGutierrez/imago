"""Information about one move."""

class GameMove:
    """Stores information about a move. A move in this context is one position of the Game
    Tree: the board can be empty, or the move can consist of more than one added or
    removed stones."""

    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.nextMoves = []
        self.previousMove = None

    def getRow(self):
        """Returns the row of the vertex the move was played on."""
        return self.board.lastStone[0]

    def getCol(self):
        """Returns the column of the vertex the move was played on."""
        return self.board.lastStone[1]

    def addMove(self, row, col, player):
        """Adds a move to the next moves list creating its board from this move's board
        plus a new stone at the specified row and column.
        """
        newBoard = self.board.getDeepCopy()
        newBoard.board[row][col] = player
        return self.addMoveWithBoard(player, newBoard)

    def addMoveWithBoard(self, player, board):
        """Adds a move to the next moves list containing the provided board."""
        newMove = GameMove(player, board)
        newMove.previousMove = self
        self.nextMoves.append(newMove)
        return newMove
