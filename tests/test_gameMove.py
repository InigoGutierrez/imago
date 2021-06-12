"""Tests for gameMove module."""

import unittest

from imago.data.enums import Player
from imago.gameLogic.gameBoard import GameBoard
from imago.gameLogic.gameMove import GameMove

TEST_BOARD_SIZE = 19

class TestGameMove(unittest.TestCase):
    """Test gameMove module."""

    def testAddMove(self):
        """Test adding new moves to existing moves."""
        board = GameBoard(TEST_BOARD_SIZE, TEST_BOARD_SIZE)
        firstMove = GameMove(board)

        self.assertIsNone(firstMove.coords)

        secondMove = firstMove.addMove(1, 2)

        self.assertIsNone(firstMove.coords)
        self.assertEqual(secondMove.coords[0], 1)
        self.assertEqual(secondMove.coords[1], 2)

        thirdMove = secondMove.addMove(5, 7)

        self.assertIsNone(firstMove.coords)
        self.assertIsNone(thirdMove.previousMove.previousMove.coords)

        self.assertEqual(secondMove.coords[0], 1)
        self.assertEqual(secondMove.coords[1], 2)
        self.assertEqual(thirdMove.previousMove.coords[0], 1)
        self.assertEqual(thirdMove.previousMove.coords[1], 2)

        self.assertEqual(thirdMove.coords[0], 5)
        self.assertEqual(thirdMove.coords[1], 7)
        self.assertEqual(firstMove
                .nextMoves[0]
                .nextMoves[0]
                .coords[0], 5)
        self.assertEqual(firstMove
                .nextMoves[0]
                .nextMoves[0]
                .coords[1], 7)

        self.assertEqual(firstMove.board.getBoard()[1][2], Player.EMPTY)
        self.assertEqual(secondMove.board.getBoard()[1][2], Player.BLACK)
        self.assertEqual(thirdMove.board.getBoard()[1][2], Player.BLACK)

        self.assertEqual(firstMove.board.getBoard()[5][7], Player.EMPTY)
        self.assertEqual(secondMove.board.getBoard()[5][7], Player.EMPTY)
        self.assertEqual(thirdMove.board.getBoard()[5][7], Player.WHITE)

    def testGetPlayableVertices(self):
        """Test getting the set of valid moves."""
        boardSize = 3
        board = GameBoard(boardSize, boardSize)

        firstMove = GameMove(board)
        self.assertSetEqual(
            firstMove.getPlayableVertices(),
            set(((0,0), (0,1), (0,2),
            (1,0), (1,1), (1,2),
            (2,0), (2,1), (2,2)))
        )

        secondMove = firstMove.addMove(1, 2)
        self.assertSetEqual(
            secondMove.getPlayableVertices(),
            set(((0,0), (0,1), (0,2),
            (1,0), (1,1),
            (2,0), (2,1), (2,2)))
        )

if __name__ == '__main__':
    unittest.main()
