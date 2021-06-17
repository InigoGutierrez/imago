"""Tests for the MonteCarlo algorithm."""

import unittest

from imago.gameLogic.gameState import GameState
from imago.engine.monteCarlo import MCTS
from imago.engine.monteCarlo import MCTSNode

TEST_BOARD_SIZE = 9

class TestMonteCarlo(unittest.TestCase):
    """Test MonteCarlo algorithm."""

    def testPickMove(self):
        """Test picking a move."""
        state = GameState(TEST_BOARD_SIZE)
        tree = MCTS(state)
        print(tree.pickMove().toString())

    #def testSimulation(self):
    #    """Test calculation of group liberties."""
    #    board = GameBoard(TEST_BOARD_SIZE, TEST_BOARD_SIZE)
    #    move = GameMove(board)
    #    node = MCTSNode(move, None)
    #    nMatches = 100
    #    scoreDiffHeur = 15
    #    node.simulation(nMatches, scoreDiffHeur)

if __name__ == '__main__':
    unittest.main()
