"""Information about one move."""

from imago.data.enums import Player

class GameMove:
    """Stores information about a move. A move in this context is one position of the Game
    Tree: the board can be empty, or the move can consist of more than one added or
    removed stones."""

    def __init__(self, board, coords=None, isPass=False, playerWhoPassed=None):
        self.board = board
        self.nextMoves = []
        self.previousMove = None
        self.isPass = isPass
        self.coords = coords
        self.playerWhoPassed = playerWhoPassed

    def getRow(self):
        """Returns the row of the vertex the move was played on."""
        if self.coords is None:
            return None
        return self.coords[0]

    def getCol(self):
        """Returns the column of the vertex the move was played on."""
        if self.coords is None:
            return None
        return self.coords[1]

    def getPlayer(self):
        """Returns the player who placed the last stone or passed."""
        if self.isPass:
            if self.previousMove is None:
                return Player.BLACK
            return self.playerWhoPassed

        if self.coords is None: # Not pass and no coordinates: root move of the tree
            return Player.EMPTY

        return self.board.getBoard()[self.getRow()][self.getCol()]

    def getNextPlayer(self):
        """Returns the player who should place the next stone."""
        selfPlayer = self.getPlayer()
        if selfPlayer == Player.EMPTY:
            return Player.BLACK
        return Player.otherPlayer(selfPlayer)

    def getGameLength(self):
        """Returns the number of (actual player-made) moves since the game started."""
        acc = 0
        prevMove = self.previousMove
        while prevMove is not None:
            acc += 1
            prevMove = prevMove.previousMove
        return acc

    def getThisAndPrevBoards(self):
        """Returns an array with all the boards of this and previous moves."""
        prevBoards = []
        checkedMove = self.previousMove
        while checkedMove is not None:
            prevBoards.append(checkedMove.board)
            checkedMove = checkedMove.previousMove
        return prevBoards

    def getPlayableVertices(self):
        """Returns a set with the playable vertices."""
        return self._getVerticesByFilter(self.board.isPlayable)

    def getSensibleVertices(self):
        """Returns a set with the sensible vertices."""
        return self._getVerticesByFilter(self.board.isSensible)

    def _getVerticesByFilter(self, filterFunction):
        """Returns a set with the vertices which fill a requirement."""
        vertices = set()
        player = self.getNextPlayer()
        prevBoards = self.getThisAndPrevBoards()
        for row in range(self.board.getBoardHeight()):
            for col in range(self.board.getBoardWidth()):
                valid, _ = filterFunction(row, col, player, prevBoards)
                if valid:
                    vertices.add((row, col))
        return vertices

    def addMoveByCoords(self, coords):
        """Adds a move to the next moves list creating its board from this move's board
        plus a new stone at the specified coordinates.
        """
        return self.addMove(coords[0], coords[1])


    def addMove(self, row, col):
        """Adds a move to the next moves list creating its board from this move's board
        plus a new stone at the specified row and column.
        """
        if self.getPlayer() == Player.EMPTY:
            player = Player.BLACK
        else:
            player = Player.otherPlayer(self.getPlayer())
        return self.addMoveForPlayer(row, col, player)

    def addMoveForPlayer(self, row, col, player):
        """Adds a move to the next moves list creating its board from this move's board
        plus a new stone at the specified row and column.
        """
        newBoard = self.board.getDeepCopy()
        newBoard.moveAndCapture(row, col, player)
        newMove = GameMove( newBoard, (row, col) )
        newMove.previousMove = self
        self.nextMoves.append(newMove)
        return newMove

    def addPass(self):
        """Adds a pass move to the next moves list."""
        return self.addPassForPlayer(self.getNextPlayer())

    def addPassForPlayer(self, player):
        """Adds a pass move for the given player to the next moves list."""
        newBoard = self.board.getDeepCopy()
        newMove = GameMove(newBoard, isPass=True, playerWhoPassed=player)
        newMove.previousMove = self
        self.nextMoves.append(newMove)
        return newMove

    def toString(self):
        """Returns the coordinates of the move as a string."""
        if self.isPass:
            return "Pass"
        if self.coords is None:
            return "Root move"
        return "(%d, %d)" % (self.getRow(), self.getCol())

    def printBoard(self):
        """Prints the board as of this move."""
        self.board.printBoard()
