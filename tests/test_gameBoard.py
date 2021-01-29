"""Tests for gameBoard module."""

import unittest

from imago.data.enums import Player
from imago.gameLogic.gameBoard import GameBoard

#from imago.data.enums import Player

TEST_BOARD_SIZE = 19

class TestGameBoard(unittest.TestCase):
    """Test gameBoard module."""

    def testGetGroupLiberties(self):
        """Test calculation of group liberties."""
        board = GameBoard(TEST_BOARD_SIZE)

        #Empty cell liberties
        self.assertEqual(board.getGroupLiberties(0,0), {})
        self.assertEqual(board.getGroupLibertiesCount(0,0), 0)

        # Lone stone liberties
        board.board[3][3] = Player.WHITE
        self.assertEqual(board.getGroupLiberties(3,3),
                {(2,3), (3,2), (4,3), (3,4)})
        self.assertEqual(board.getGroupLibertiesCount(3,3), 4)

if __name__ == '__main__':
    unittest.main()
