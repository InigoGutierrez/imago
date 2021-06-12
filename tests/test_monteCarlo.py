"""Tests for the MonteCarlo algorithm."""

import unittest

from imago.gameLogic.gameBoard import GameBoard
from imago.gameLogic.gameMove import GameMove
from imago.engine.monteCarlo import MCTSNode

TEST_BOARD_SIZE = 19

class TestMonteCarlo(unittest.TestCase):
    """Test MonteCarlo algorithm."""

    def testSimulation(self):
        """Test calculation of group liberties."""
        board = GameBoard(TEST_BOARD_SIZE, TEST_BOARD_SIZE)
        move = GameMove(board)
        node = MCTSNode(move, None)
        node.simulation()

if __name__ == '__main__':
    unittest.main()
