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

    def getBoard(self):
        """Gets the matrix representing the board."""
        return self.board

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
        newBoard.board = deepcopy(self.board)
        return newBoard

    def getGroupLiberties(self, row, col):
        """Returns the empty vertices adjacent to the group occupying a vertex (its
        liberties) as a set. An empty set is returned if the vertex is empty.
        """
        groupColor = self.board[row][col]
        if groupColor == Player.EMPTY:
            return set()
        emptyCells = set()
        exploredCells = set()
        self.__exploreLiberties(row, col, groupColor, emptyCells, exploredCells)
        return emptyCells

    def getGroupLibertiesCount(self, row, col):
        """Returns the number of liberties of a group."""
        return len(self.getGroupLiberties(row, col))

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

        for side in ((-1,0), (1,0), (0,-1), (0,1)):
            rowToExplore = row + side[0]
            colToExplore = col + side[1]
            if self.isMoveInBoardBounds(rowToExplore, colToExplore):
                self.__exploreLiberties(rowToExplore, colToExplore, groupColor,
                                        emptyCells, exploredCells)

    def getGroupCells(self, row, col):
        """
        Returns a set containing the cells occupied by the group in the given cell.
        This is also valid if the cell is empty."""
        groupColor = self.board[row][col]
        cells = set()
        self.__exploreGroup(row, col, groupColor, cells)
        return cells

    def getGroupCellsCount(self, row, col):
        """Returns the number of cells of a group."""
        return len(self.getGroupCells(row, col))

    def __exploreGroup(self, row, col, groupColor, cells):
        if self.board[row][col] != groupColor or (row, col) in cells:
            return
        cells.add((row, col))

        for side in ((-1,0), (1,0), (0,-1), (0,1)):
            rowToExplore = row + side[0]
            colToExplore = col + side[1]
            if self.isMoveInBoardBounds(rowToExplore, colToExplore):
                self.__exploreGroup(rowToExplore, colToExplore, groupColor, cells)

    def moveAndCapture(self, row, col, player):
        """Checks surrounding captures of a move, removes them and returns a set
        containing the vertices where stones were captured.
        """

        self.board[row][col] = player

        captured = set()

        for side in ((-1,0), (1,0), (0,-1), (0,1)):
            rowToExplore = row + side[0]
            colToExplore = col + side[1]
            if self.isMoveInBoardBounds(rowToExplore, colToExplore):
                if (self.board[rowToExplore][colToExplore] != player
                    and self.board[rowToExplore][colToExplore] != Player.EMPTY
                    and self.getGroupLibertiesCount(rowToExplore, colToExplore) == 0):
                    captured.update(self.__captureGroup(rowToExplore, colToExplore))

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

    def isCellEye(self, row, col):
        """Returns the surrounding color if the cell is part of an eye and Player.EMTPY
        otherwise.
        """
        # if isCellEmpty && all adjacent to group are same color
        if not self.isCellEmpty(row, col):
            return Player.EMPTY
        groupCells = self.getGroupCells(row, col)
        surroundingColor = Player.EMPTY
        # Check surrounding cells of each cell in the group
        for cell in groupCells:
            for side in ((-1,0), (1,0), (0,-1), (0,1)):
                rowChecked = cell[0]+side[0]
                colChecked = cell[1]+side[1]
                if self.isMoveInBoardBounds(rowChecked, colChecked):
                    otherColor = self.board[rowChecked][colChecked]
                    if otherColor != Player.EMPTY:
                        if surroundingColor == Player.EMPTY:
                            surroundingColor = otherColor
                        elif surroundingColor != otherColor:
                            return Player.EMPTY
        return surroundingColor

    def isMoveSuicidal(self, row, col, player):
        """Returns True if move is suicidal."""

        # Check vertex is empty
        if not self.isCellEmpty(row, col):
            raise RuntimeError("Cell to play should be empty when checking for suicide.")

        # Temporarily play and capture
        self.board[row][col] = player
        groupLiberties = self.getGroupLibertiesCount(row, col)
        captured = self.moveAndCapture(row, col, player)

        illegal = False
        # If move didn't capture anything and its group is left without liberties, it's
        # suicidal
        if len(captured) == 0 and groupLiberties == 0:
            illegal = True

        # Restore captured stones
        for vertex in captured:
            self.board[vertex[0]][vertex[1]] = Player.otherPlayer(player)
        # Remove temporarily played stone
        self.board[row][col] = Player.EMPTY
        return illegal

    def isMoveKoIllegal(self, row, col, player, prevBoards):
        """Returns True if move is illegal because of ko."""

        # Check vertex is empty
        if not self.isCellEmpty(row, col):
            raise RuntimeError("Cell to play should be empty when checking for ko.")

        illegal = False
        # Temporarily play and capture for comparisons
        captured = self.moveAndCapture(row, col, player)
        # Check previous boards
        for prevBoard in prevBoards:
            # A ko is possible in boards where the stone to play exists
            if prevBoard.board[row][col] == player:
                if self.equals(prevBoard):
                    illegal = True

        # Restore captured stones
        for vertex in captured:
            self.board[vertex[0]][vertex[1]] = Player.otherPlayer(player)
        # Remove temporarily played stone
        self.board[row][col] = Player.EMPTY
        return illegal

    def isPlayable(self, row, col, player, prevBoards):
        """Determines if a move is playable."""
        if not self.isMoveInBoardBounds(row, col):
            return False, "Move outside board bounds."
        if not self.isCellEmpty(row, col):
            return False, "Vertex is not empty."
        if self.isMoveSuicidal(row, col, player):
            return False, "Move is suicidal."
        if self.isMoveKoIllegal(row, col, player, prevBoards):
            return False, "Illegal by ko rule."
        return True, ""

    def isSensible(self, row, col, player, prevBoards):
        """Determines if a move is playable and sensible."""
        playable, playableText = self.isPlayable(row, col, player, prevBoards)
        if not playable:
            return playable, playableText
        if ( self.getGroupCellsCount(row, col) == 1
            and self.isCellEye(row, col) == player ):
            return False, "Move fills own eye."""
        return True, ""

    def score(self):
        """Gets the current score given by the already surrounded territory for Japanese
        rules. The format of the returned score is (black, white).
        """
        scores = []
        for player in Player:
            while len(scores) <= player.value:
                scores.append(0)
        checkedVertices = set()
        for row in range(0, self.getBoardHeight()):
            for col in range(0, self.getBoardWidth()):
                if not (row, col) in checkedVertices:
                    group = self.getGroupCells(row, col)
                    for cell in group:
                        checkedVertices.add(cell)
                    surroundingColor = self.isCellEye(row, col)
                    if surroundingColor != Player.EMPTY:
                        scores[surroundingColor.value] += len(group)
        return (scores[Player.BLACK.value], scores[Player.WHITE.value])

    def equals(self, otherBoard):
        """Returns true if this board is equal to another board. Only takes into account
        dimensions and placed stones.
        """
        if ( self.getBoardHeight() != otherBoard.getBoardHeight()
        or self.getBoardWidth() != otherBoard.getBoardWidth() ):
            return False
        for row in range(self.getBoardHeight()):
            for col in range(self.getBoardWidth()):
                if self.board[row][col] != otherBoard.board[row][col]:
                    return False
        return True

    def printBoard(self):
        """Print the board."""
        colTitle = 'A'
        rowTitlePadding = 2
        if self.getBoardHeight() >= 10:
            firstRowPadding = 2
        else:
            firstRowPadding = 1

        # Print column names
        rowText = " " * (rowTitlePadding + firstRowPadding)
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
