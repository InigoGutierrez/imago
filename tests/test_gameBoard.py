"""Tests for gameBoard module."""

import unittest

from imago.data.enums import Player
from imago.gameLogic.gameBoard import GameBoard

TEST_BOARD_SIZE = 19

class TestGameBoard(unittest.TestCase):
    """Test gameBoard module."""

    def testGetGroupLiberties(self):
        """Test calculation of group liberties."""
        board = GameBoard(TEST_BOARD_SIZE, TEST_BOARD_SIZE)

        #Empty cell liberties
        self.assertEqual(board.getGroupLiberties(0,0), set())
        self.assertEqual(board.getGroupLibertiesCount(0,0), 0)

        # Lone stone liberties
        board.board[3][3] = Player.WHITE
        self.assertEqual(board.getGroupLiberties(3,3),
                {(2,3), (3,2), (4,3), (3,4)})
        self.assertEqual(board.getGroupLibertiesCount(3,3), 4)

    def testIsCellEye(self):
        """Tests the isCellEye method."""
        board = GameBoard(TEST_BOARD_SIZE, TEST_BOARD_SIZE)

        # Empty board is eye
        self.assertEqual(Player.EMPTY, board.isCellEye(0, 0))
        self.assertEqual(Player.EMPTY, board.isCellEye(3, 3))
        self.assertEqual(Player.EMPTY, board.isCellEye(TEST_BOARD_SIZE-1, TEST_BOARD_SIZE-1))

        # Board with 1 stone is eye
        board.board[5][6] = Player.WHITE
        self.assertEqual(Player.WHITE, board.isCellEye(3, 3))

        # Board with 2 stones of different color is not eye
        board.board[9][9] = Player.BLACK
        self.assertEqual(Player.EMPTY, board.isCellEye(3, 3))

        # Surrounded cell is eye
        board.board[6][5] = Player.WHITE
        board.board[6][7] = Player.WHITE
        board.board[7][6] = Player.WHITE

        self.assertEqual(Player.WHITE, board.isCellEye(6, 6))

        # Surrounded cell with 2 different colors is not eye
        board.board[6][5] = Player.BLACK
        self.assertEqual(Player.EMPTY, board.isCellEye(6, 6))

    def testScore(self):
        """Tests the score method."""
        board = GameBoard(TEST_BOARD_SIZE, TEST_BOARD_SIZE)

        # Empty board has no score.
        self.assertEqual((0, 0), board.score())

        # Board with 1 black stone has totalVertices-1 points for black.
        board.board[3][3] = Player.BLACK
        self.assertEqual((TEST_BOARD_SIZE*TEST_BOARD_SIZE-1, 0), board.score())

        # Board with 2 black stones has totalVertices-2 points for black.
        board.board[5][5] = Player.BLACK
        self.assertEqual((TEST_BOARD_SIZE*TEST_BOARD_SIZE-2, 0), board.score())

        # Board with lone stones of different colors has no score.
        board.board[7][7] = Player.WHITE
        self.assertEqual((0, 0), board.score())

        # Black group with surrounded territory.
        board.board[2][3] = Player.BLACK
        board.board[1][3] = Player.BLACK
        board.board[0][3] = Player.BLACK
        board.board[3][2] = Player.BLACK
        board.board[3][1] = Player.BLACK
        board.board[3][0] = Player.BLACK
        self.assertEqual((9, 0), board.score())

        # White group besides black group.
        board.board[6][7] = Player.WHITE
        board.board[5][7] = Player.WHITE
        board.board[5][6] = Player.WHITE
        board.board[5][5] = Player.WHITE
        board.board[5][4] = Player.WHITE
        board.board[5][3] = Player.WHITE
        board.board[5][2] = Player.WHITE
        board.board[5][1] = Player.WHITE
        board.board[5][0] = Player.WHITE
        board.board[8][7] = Player.WHITE
        board.board[9][7] = Player.WHITE
        board.board[9][6] = Player.WHITE
        board.board[9][5] = Player.WHITE
        board.board[9][4] = Player.WHITE
        board.board[9][3] = Player.WHITE
        board.board[9][2] = Player.WHITE
        board.board[9][1] = Player.WHITE
        board.board[9][0] = Player.WHITE
        self.assertEqual((9, 21), board.score())


if __name__ == '__main__':
    unittest.main()
