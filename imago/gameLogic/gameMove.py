"""Information about one move."""

class GameMove:

    def __init__(self, player, row, col, makesKo, board):
        self.player = player
        self.row = row
        self.col = col
        self.makesKo = makesKo
        self.board = board
        self.nextMoves = []
        self.previousMove = None

    def addMove(self, player, row, col, makesKo, board):
        """Adds a move to the next moves list."""
        newMove = GameMove(player, row, col, makesKo, board)
        newMove.previousMove = self
        self.nextMoves.append(newMove)
        return newMove
