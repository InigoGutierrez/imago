from imago.gameLogic.gameTree import GameTree
from imago.gameLogic.gameData import GameData
from imago.gameLogic.gameMove import GameMove
from imago.gameLogic.gameState import Player

class ASTNode:
    """Abstract Syntax Tree Node of SGF parser"""
    def __init__(self, children=None, leaf=None, props=None):
        if children:
            self.children = children
        else:
            self.children = []
        if props:
            self.props = props
        else:
            self.props = {}
        self.leaf = leaf

    def addToSequence(self, move):
        """Appends a move to the last of the sequence started by this move"""
        children = self.children
        while len(children) > 0:
            children = children[0].children
        children.append(move)

    def toGameTree(self):
        """Converts this node and its subtree into a GameTree"""
        gameData = GameData()
        for prop in self.props:
            if prop.name == "GM": # Type of game, 1 is Go
                if prop.value != 1:
                    print("ERROR") # TODO: Error handling
            if prop.name == "SZ": # Size of board. [19] for squared, [10:12] for rect.
                gameData.size = prop.value
            if prop.name == "AN": # Annotator
                gameData.annotator = prop.value
            if prop.name == "BR": # Rank of black player
                gameData.blackRank = prop.value
            if prop.name == "WR": # Rank of white player
                gameData.whiteRank = prop.value
            if prop.name == "PB": # Name of black player
                gameData.blackName = prop.value
            if prop.name == "PW": # Name of white player
                gameData.whiteName = prop.value
            if prop.name == "BT": # Name of black team
                gameData.blackTeam = prop.value
            if prop.name == "WT": # Name of white team
                gameData.whiteTeam = prop.value
            if prop.name == "CP": # Copyright information
                gameData.copyright = prop.value
            if prop.name == "DT": # Date
                gameData.date = prop.value
            if prop.name == "EV": # Event information
                gameData.event = prop.value
            if prop.name == "GN": # Game nae
                gameData.name = prop.value
            if prop.name == "GC": # Extra game comment
                gameData.gameComment = prop.value
            if prop.name == "ON": # Description of opening played
                gameData.openingInfo = prop.value
            if prop.name == "OT": # Overtime method
                gameData.overtimeInfo = prop.value
            if prop.name == "PC": # Place where the game took place
                gameData.place = prop.value
            if prop.name == "RE": # Result of the game
                gameData.result = prop.value
            if prop.name == "RO": # Round number and type
                gameData.roundInfo = prop.value
            if prop.name == "RU": # Rules used for the game
                gameData.rules = prop.value
            if prop.name == "SO": # Source of the gamw
                gameData.source = prop.source
            if prop.name == "TM": # Time limit in seconds
                gameData.timeInfo = prop.source
            if prop.name == "US": # User or program which entered the game
                gameData.user = prop.source

        firstMoves = []
        for child in self.children:
            firstMoves.append(child.toGameMoveTree)

        return GameTree(firstMoves, gameData)

    def toGameMoveTree(self):
        player = 0
        coords = []
        for prop in self.props:
            if prop.name == "B": # White move
                player = Player.BLACK
                coords = textToCoords(prop.value)
            if prop.name == "W": # White move
                player = Player.WHITE
                coords = textToCoords(prop.value)
        gameMove = GameMove(player, coords[0], coords[1])
        for child in self.children:
            newMove = child.toGameMoveTree()
            gameMove.nextMoves.append(newMove)
            newMove.previousMove = gameMove
        return gameMove

def textToCoords(text): # Poner en PropertyMove, subclase de Property
    col = ord(text[1]) - ord('a')
    row = ord(text[0]) - ord('a')
    return [row, col]


    def toString(self):
        """Returns a depth-first representation of the tree."""
        out = '(' + str(self.props) + ')'
        out += "in"
        for node in self.children:
            out = out + node.toString()
        out += "out"
        return out

class Property:
    """Property of a Node"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def addValue(self, value):
        """Adds a new value to this properties value, making it a list if necessary"""
        if type(self.value) == list:
            self.value.append(value)
        else:
            self.value = [self.value, value]
