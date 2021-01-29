"""Representation of a board. Contains played stones and captured stones."""

from copy import deepcopy

from imago.data.enums import Player

def _getNewBoard(size):
    """Return a new board."""
    board = []
    for row in range(size):
        board.append([])
        for _ in range(size):
            board[row].append(Player.EMPTY)
    return board

class GameBoard:
    """Logic and state related to the board."""

    def __init__(self, size):
        self.board = _getNewBoard(size)
        self.capturesBlack = 0
        self.capturesWhite = 0
        self.lastStone = None

    def getDeepCopy(self):
        """Returns a copy GameBoard."""
        newBoard = GameBoard(len(self.board))
        newBoard.capturesBlack = self.capturesBlack
        newBoard.capturesWhite = self.capturesWhite
        newBoard.lastStone = self.lastStone
        newBoard.board = deepcopy(self.board)
        return newBoard

    def getGroupLibertiesCount(self, row, col):
        return len(self.getGroupLiberties(row, col))

    def getGroupLiberties(self, row, col):
        """Returns the empty vertexes adjacent to the group occupying a vertex (its
        liberties) as a set. An empty set is returned if the vertex is empty.
        """
        groupColor = self.board[row][col]
        if groupColor == Player.EMPTY:
            return {}
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
        if col < len(self.board[0])-1:
            self.__exploreLiberties(row, col+1, groupColor, emptyCells, exploredCells)

        # Down
        if row < len(self.board)-1:
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
        if col < len(self.board[0])-1:
            self.__exploreGroup(row, col+1, groupColor, cells)

        # Down
        if row < len(self.board)-1:
            self.__exploreGroup(row+1, col, groupColor, cells)

        # Left
        if col > 0:
            self.__exploreGroup(row, col-1, groupColor, cells)


    def moveCapture(self, row, col, player):
        """Checks surrounding captures of a move, removes them and returns the number of
        stones captured.
        """
        captured = 0
        if row > 0:
            if (self.board[row-1][col] != player
                and self.board[row-1][col] != Player.EMPTY
                and len(self.getGroupLiberties(row-1, col)) == 0):
                captured += self.__captureGroup(row-1, col)
        if row < len(self.board)-1:
            if (self.board[row+1][col] != player
                and self.board[row+1][col] != Player.EMPTY
                and len(self.getGroupLiberties(row+1, col)) == 0):
                captured += self.__captureGroup(row+1, col)
        if col > 0:
            if (self.board[row][col-1] != player
                and self.board[row][col-1] != Player.EMPTY
                and len(self.getGroupLiberties(row, col-1)) == 0):
                captured += self.__captureGroup(row, col-1)
        if col < len(self.board[0])-1:
            if (self.board[row][col+1] != player
                and self.board[row][col+1] != Player.EMPTY
                and len(self.getGroupLiberties(row, col+1)) == 0):
                captured += self.__captureGroup(row, col+1)
        return captured

    def __captureGroup(self, row, col):
        """Removes all the stones from the group occupying the given cell and returns the
        number of removed stones.
        """
        cellsToCapture = self.getGroupCells(row, col)
        count = 0
        for cell in cellsToCapture:
            self.board[cell[0]][cell[1]] = Player.EMPTY
            count += 1
        return count

    def printBoard(self):
        """Print the board."""
        colTitle = 'A'
        rowTitlePadding = 2

        # Print column names
        rowText = " " * (rowTitlePadding + 2)
        for col in range(len(self.board[0])):
            rowText += colTitle + " "
            colTitle = chr(ord(colTitle)+1)
            if colTitle == "I": # Skip I
                colTitle = "J"
        print(rowText)

        # Print rows
        rowTitle = len(self.board)
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
