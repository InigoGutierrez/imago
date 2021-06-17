"""Monte Carlo Tree Search module."""

import sys
import random

from imago.data.enums import Player

class MCTS:
    """Monte Carlo tree."""

    def __init__(self, move):
        self.root = MCTSNode(move, None)

    def forceNextMove(self, coords):
        """Selects given move as next move."""
        for node in self.root.children:
            if (node.move.getRow() == coords[0]
                and node.move.getCol() == coords[1]):
                self.root = node
                return
        self.root = self.root.expansionForCoords(coords)

    def pickMove(self):
        """
        Performs an exploratory cycle, updates the root to the best node and returns its
        corresponding move."""
        #NOTE: with only one selection-expansion the match is
        #      completely random
        for _ in range(5):
            self.root.selection().expansion().simulation(10, 20)
        self.root = self.selectBestNextNode()
        return self.root.move

    def selectBestNextNode(self):
        """Returns best ucb node available for the current player."""

        # Assumes at least one expansion has occured
        bestUCB = -sys.maxsize - 1
        bestNode = None
        for node in self.root.children:
            ucb = node.ucbForPlayer()
            if ucb > bestUCB:
                bestUCB = ucb
                bestNode = node

        return bestNode

class MCTSNode:
    """Monte Carlo tree node."""

    def __init__(self, move, parent):
        self.visits = 0
        self.score = 0
        self.move = move
        self.parent = parent
        self.children = set()
        self.unexploredVertices = move.getPlayableVertices()

    def ucb(self):
        """Returns Upper Confidence Bound of node"""
        # UCB = meanVictories + 1/visits
        if self.visits == 0:
            return 0
        mean = self.score / self.visits
        adjust = 1/self.visits
        return mean + adjust

    def ucbForPlayer(self):
        """
        Returns Upper Confidence Bound of node changing the symbol if the move is for the
        wite player."""

        # Account for white player score being negative
        if self.move.getPlayer() == Player.WHITE:
            return self.ucb() * -1
        return self.ucb()

    def selection(self):
        """Select the most promising node with unexplored children."""
        bestNode = self.selectionRec(self)
        return bestNode

    def selectionRec(self, bestNode):
        """Searches this node and its children for the node with the best UCB value."""

        # Check if node has unexplored children and better UCB than previously explored
        if len(self.unexploredVertices) > 0:
            if self.ucbForPlayer() > bestNode.ucbForPlayer():
                bestNode = self

        # Recursively search children for better UCB
        for child in self.children:
            bestChildNode = child.selectionRec(bestNode)
            if bestChildNode.ucbForPlayer() > bestNode.ucbForPlayer():
                bestNode = bestChildNode

        return bestNode

    def expansion(self):
        """Pick an unexplored vertex from this node and add it as a new MCTSNode."""
        newVertex = random.choice(list(self.unexploredVertices))
        return self.expansionForCoords(newVertex)

    def expansionForCoords(self, coords):
        """
        Adds a move for the given coordinates as a new node to the children of this
        node."""
        newMove = self.move.addMove(coords[0], coords[1])
        newNode = MCTSNode(newMove, self)
        self.children.add(newNode)
        self.unexploredVertices.remove((coords[0], coords[1]))
        return newNode

    def simulation(self, nMatches, scoreDiffHeur):
        """Play random matches to accumulate reward information on the node."""
        scoreAcc = 0
        for _ in range(nMatches):
            result = self._randomMatch(scoreDiffHeur)
            self.visits += 1
            scoreDiff = result[0]-result[1]
            if scoreDiff != 0:
                scoreAcc += scoreDiff / abs(scoreDiff)
        # Backup
        node = self
        while node is not None:
            node.score += scoreAcc
            node.visits += nMatches
            node = node.parent

    def _randomMatch(self, scoreDiffHeur):
        """Play a random match and return the resulting score."""
        #IMPORTANT: the score heuristic doesn't work for the first move of the game, since
        #the black player holds all except for one vertex!
        currentMove = self.move
        score = currentMove.board.score()
        while currentMove.getGameLength() < 5 or abs(score[0] - score[1]) < scoreDiffHeur:
            if currentMove.isPass and currentMove.previousMove.isPass:
                return score
            sensibleMoves = currentMove.getSensibleVertices()
            if len(sensibleMoves) == 0:
                currentMove = currentMove.addPass()
            else:
                selectedMove = random.choice(list(sensibleMoves))
                currentMove = currentMove.addMoveByCoords(selectedMove)
            score = currentMove.board.score()
            print("Current move: %s" % (currentMove.toString()))
            print("Current move game length: ", currentMove.getGameLength())
            print("Score of the board: %d, %d (%d)"
                    % (score[0],
                        score[1],
                        score[0]-score[1])
                )
            currentMove.printBoard()
        return score

    def _printBoardInfo(self):
        """Prints the visits and score for debugging purposes."""
        print("Visits: %d" % self.visits)
        print("Score: %d" % self.score)
