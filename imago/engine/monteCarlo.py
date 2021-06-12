"""Monte Carlo Tree Search module."""

class MCTS:
    """Monte Carlo tree."""

    def __init__(self, root):
        self.root = root

    def selection(self):
        """Select the most promising node with unexplored children."""
        bestNode = self.root.selectionRec(self.root)
        return bestNode

    def backup(self, node):
        """Update nodes backbards up to root."""

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
        mean = self.score / self.visits
        adjust = 1/self.visits
        return mean + adjust

    def selectionRec(self, bestNode):
        """Searches this node and its children for the node with the best UCB value."""

        # Check if node has unexplored children and better UCB than previously explored
        if len(self.unexploredVertices) > 0:
            if self.ucb() > bestNode.ucb():
                bestNode = self

        # Recursively search children for better UCB
        for child in self.children:
            bestNode = child.selectionRec(bestNode)

        return bestNode

    def expansion(self):
        """Pick an unexplored vertex from this node and add it as a new MCTSNode."""
        newVertex = self.unexploredVertices.pop() # Random?
        newMove = self.move.addMove(newVertex[0], newVertex[1])
        newNode = MCTSNode(newMove, self)
        self.children.add(newNode)
        return newNode

    def simulation(self):
        """Play random matches to accumulate reward information on the node."""
        matches = 10
        for _ in range(matches):
            result = self._randomMatch()
            self.visits += 1
            scoreDiff = result[0]-result[1]
            self.score += scoreDiff / abs(scoreDiff)
            self._printBoardInfo()

    def _randomMatch(self):
        """Play a random match and return the resulting score."""
        #IMPORTANT: the score heuristic doesn't work for the first move of the game, since
        #the black player holds all except for one vertex!
        currentMove = self.move
        scoreHeuristic = 15
        score = currentMove.board.score()
        while currentMove.getGameLength() < 5 or abs(score[0] - score[1]) < scoreHeuristic:
            validMoves = currentMove.getPlayableVertices()
            selectedMove = validMoves.pop()
            currentMove = currentMove.addMove(selectedMove[0], selectedMove[1])
            print("Current move: %d, %d" % (currentMove.getRow(), currentMove.getCol()))
            print("Current move game length: ", currentMove.getGameLength())
            score = currentMove.board.score()
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
