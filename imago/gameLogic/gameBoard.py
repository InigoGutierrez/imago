"""Representation of a board. Contains played stones and captured stones."""

from copy import deepcopy

from imago.data.enums import Player

def _getNewBoard(height, width):
    """Return a new board."""
    board = []
    for row in range(height):
        board.append([])
        for _ in range(width):
            board[row].append(Player.EMPTY)
    return board

class GameBoard:
    """Logic and state related to the board."""

    def __init__(self, height, width):
        self.board = _getNewBoard(height, width)
        self.capturesBlack = 0
        self.capturesWhite = 0
        self.lastStone = None

    def getBoardHeight(self):
        """Returns the number of rows in the board."""
        return len(self.board)

    def getBoardWidth(self):
        """Returns the number of columns of the first row of the board. This number should
        be the same for all the rows."""
        return len(self.board[0])

    def getDeepCopy(self):
        """Returns a copy GameBoard."""
        newBoard = GameBoard(self.getBoardHeight(), self.getBoardWidth())
        newBoard.capturesBlack = self.capturesBlack
        newBoard.capturesWhite = self.capturesWhite
        newBoard.lastStone = self.lastStone
        newBoard.board = deepcopy(self.board)
        return newBoard

    def getGroupLibertiesCount(self, row, col):
        """Returns the number of liberties of a group."""
        return len(self.getGroupLiberties(row, col))

    def getGroupLiberties(self, row, col):
        """Returns the empty vertexes adjacent to the group occupying a vertex (its
        liberties) as a set. An empty set is returned if the vertex is empty.
        """
        groupColor = self.board[row][col]
        if groupColor == Player.EMPTY:
            return set()
        emptyCells = set()
        exploredCells = set()
        self.__exploreLiberties(row, col, groupColor, emptyCells, exploredCells)
        return emptyCells

    def __exploreLiberties(self, row, col, groupColor, emptyCells, exploredCells):
        """Adds surrounding empty cells to array if they have not been added yet
            and explores adjacent occupied cells of the same group.
        """
        if (row, col) in exploredCells:
            return

        exploredCells.add((row, col))

        cellColor = self.board[row][col]

        if cellColor != groupColor:
            if cellColor == Player.EMPTY:
                emptyCells.add((row, col))
            return

        # Up
        if row > 0:
            self.__exploreLiberties(row-1, col, groupColor, emptyCells, exploredCells)

        # Right
        if col < self.getBoardWidth()-1:
            self.__exploreLiberties(row, col+1, groupColor, emptyCells, exploredCells)

        # Down
        if row < self.getBoardHeight()-1:
            self.__exploreLiberties(row+1, col, groupColor, emptyCells, exploredCells)

        # Left
        if col > 0:
            self.__exploreLiberties(row, col-1, groupColor, emptyCells, exploredCells)

    def getGroupCells(self, row, col):
        """Returns a set containing the cells occupied by the group in the given cell."""
        groupColor = self.board[row][col]
        if groupColor == Player.EMPTY:
            return 0
        cells = set()
        self.__exploreGroup(row, col, groupColor, cells)
        return cells

    def __exploreGroup(self, row, col, groupColor, cells):
        if self.board[row][col] != groupColor or (row, col) in cells:
            return
        cells.add((row, col))

        # Up
        if row > 0:
            self.__exploreGroup(row-1, col, groupColor, cells)

        # Right
        if col < self.getBoardWidth()-1:
            self.__exploreGroup(row, col+1, groupColor, cells)

        # Down
        if row < self.getBoardHeight()-1:
            self.__exploreGroup(row+1, col, groupColor, cells)

        # Left
        if col > 0:
            self.__exploreGroup(row, col-1, groupColor, cells)

    def moveAndCapture(self, row, col, player):
        """Checks surrounding captures of a move, removes them and returns a set
        containing the vertices where stones were captured.
        """
        captured = set()

        if row > 0:
            if (self.board[row-1][col] != player
                and self.board[row-1][col] != Player.EMPTY
                and len(self.getGroupLiberties(row-1, col)) == 0):
                captured.add(self.__captureGroup(row-1, col))

        if row < self.getBoardHeight()-1:
            if (self.board[row+1][col] != player
                and self.board[row+1][col] != Player.EMPTY
                and len(self.getGroupLiberties(row+1, col)) == 0):
                captured.add(self.__captureGroup(row+1, col))

        if col > 0:
            if (self.board[row][col-1] != player
                and self.board[row][col-1] != Player.EMPTY
                and len(self.getGroupLiberties(row, col-1)) == 0):
                captured.add(self.__captureGroup(row, col-1))

        if col < self.getBoardWidth()-1:
            if (self.board[row][col+1] != player
                and self.board[row][col+1] != Player.EMPTY
                and len(self.getGroupLiberties(row, col+1)) == 0):
                captured.add(self.__captureGroup(row, col+1))

        return captured

    def __captureGroup(self, row, col):
        """Removes all the stones from the group occupying the given cell and returns a
        set containing them.
        """
        cellsToCapture = self.getGroupCells(row, col)
        for cell in cellsToCapture:
            self.board[cell[0]][cell[1]] = Player.EMPTY
        return cellsToCapture

    def isMoveInBoardBounds(self, row, col):
        """Returns True if move is inside board bounds, false otherwise."""
        return 0 <= row < self.getBoardHeight() and 0 <= col < self.getBoardWidth()

    def isCellEmpty(self, row, col):
        """Returns True if cell is empty, false otherwise."""
        return self.board[row][col] == Player.EMPTY

    def isMoveSuicidal(self, row, col, player):
        """Returns True if move is suicidal."""

        # Check vertex is empty
        if not self.isCellEmpty(row, col):
            raise RuntimeError("Cell to play should be empty when checking for suicide.")

        # Play and capture
        self.board[row][col] = player
        groupLiberties = self.getGroupLibertiesCount(row, col)
        captured = self.moveAndCapture(row, col, player)

        # If move didn't capture anything and its group is left without liberties, it's
        # suicidal
        if len(captured) == 0 and groupLiberties == 0:
            # Restore captured stones
            for vertex in captured:
                self.board[vertex[0]][vertex[1]] = Player.otherPlayer(player)
            self.board[row][col] = Player.EMPTY
            # Remove played stone
            return True

    def isMoveKoIllegal(self, row, col, player, prevBoards):
        """Returns True if move is illegal because of ko."""

        # Check vertex is empty
        if not self.isCellEmpty(row, col):
            raise RuntimeError("Cell to play should be empty when checking for ko.")

        illegal = False
        # Temporarily place stone to play for comparisons
        self.board[row][col] = player
        # Check previous boards
        for prevBoard in prevBoards:
            # A ko is possible in boards where the stone to play exists
            if prevBoard.board[row][col] == player:
                if self.equals(prevBoard):
                    illegal = True

        # Remove temporarily placed stone
        self.board[row][col] = Player.EMPTY
        return illegal

    def equals(self, otherBoard):
        """Returns true if this board is equal to another board. Only takes into account
        dimensions and placed stones.
        """
        if ( self.getBoardHeight() != otherBoard.getBoardHeight()
        or self.getBoardWidth() != otherBoard.getBoardWidth() ):
            return False
        for row in range(self.getBoardHeight()):
            for col in range(self.getBoardWidth()):
                if self.board[row][col] != otherBoard[row][col]:
                    return False
        return True

    def printBoard(self):
        """Print the board."""
        colTitle = 'A'
        rowTitlePadding = 2

        # Print column names
        rowText = " " * (rowTitlePadding + 2)
        for col in range(self.getBoardWidth()):
            rowText += colTitle + " "
            colTitle = chr(ord(colTitle)+1)
            if colTitle == "I": # Skip I
                colTitle = "J"
        print(rowText)

        # Print rows
        rowTitle = self.getBoardHeight()
        for row in self.board:
            rowText = ""
            for col in row:
                rowText += cellToString(col) + " "
            print(str(rowTitle) + " " * rowTitlePadding + rowText)
            rowTitle -= 1
            if rowTitle == 9:
                rowTitlePadding += 1

def cellToString(code):
    """Returns the text representation of a cell."""
    if code == Player.WHITE:
        return 'W'
    if code == Player.BLACK:
        return 'B'
    return '·'
