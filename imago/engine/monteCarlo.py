"""Monte Carlo Tree Search module."""

class MCTS:
    """Monte Carlo tree."""

    def __init__(self, root):
        self.root = root

    def selection(self):
        """Select the most promising node with unexplored children."""
        bestUCB = 0
        bestNode = None
        bestUCB, bestNode = self._selectionRec(self.root, bestUCB, bestNode)
        return bestNode

    def __selectionRec(self, node, bestUCB, bestNode):

        # Check if node has unexplored children and better UCB than previously explored
        if len(node.unexploredVertices) > 0:
            ucb = node.ucb()
            if ucb > bestUCB:
                bestUCB = ucb
                bestNode = node

        # Recursively search children for better UCB
        for child in node.children:
            bestUCB, bestNode = self._selectionRec(child, bestUCB, bestNode)

        return bestUCB, bestNode

    def expansion(self, node):
        # Get a random unexplored vertex and remove it from the set
        newVertex = node.unexploredVertices.pop()
        newNode = MCTSNode(newVertex[0], newVertex[1], node)
        parent.children.add(self)
        return newNode

    def simulation(self, node):

    def backup(self, node):


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
        # meanVictories + 1/visits
        mean = self.score / self.visits
        adjust = 1/self.visits
        return mean + adjust
