"""Handles translation of input text to internal data and vice versa."""

import re
from enum import Enum, auto as enumAuto

from imago.data.enums import Player

VALID_WHITE_STRINGS = {
    "W",
    "WHITE"
}

VALID_BLACK_STRINGS = {
    "B",
    "BLACK"
}

class ParseCodes(Enum):
    """Return values of the move parser."""
    ERROR = enumAuto()
    QUIT = enumAuto()

def parseMove(args, boardsize):
    """Converts the textual representation of a move to a move instance."""
    if len(args) != 2:
        print("[ERROR] - Wrong n of args for move")
        return ParseCodes.ERROR
    color = parseColor(args[0])
    vertex = parseVertex(args[1], boardsize)
    return GtpMove(color, vertex)

def parseColor(text):
    """Returns color of a move given its input string."""
    text = text.upper()
    if text in VALID_WHITE_STRINGS:
        return Player.WHITE
    if text in VALID_BLACK_STRINGS:
        return Player.BLACK
    print("[ERROR] - Unknown color.")
    return ParseCodes.ERROR

def parseVertex(text, boardSize):
    """Returns row and column of a vertex given its input string. A vertex can also be the
    string "pass".

    GTP uses A1 style notation: columns are letters left to right, rows are number bottom
    to top.
    """
    text = text.upper()

    if not re.match("^[A-HJ-Z][1-9][0-9]*$", text):
        if text == "PASS":
            return "pass"
        return ParseCodes.ERROR

    vertexCol = ord(text[0])
    # Column 'I' does not exist
    if vertexCol > ord('I'):
        vertexCol -= 1
    vertexCol -= ord('A')

    vertexRow = boardSize - int(text[1:])

    if (vertexCol < 0 or vertexRow < 0
        or vertexCol >= boardSize or vertexRow >= boardSize):
        return ParseCodes.ERROR

    return [vertexRow, vertexCol]

def vertexToString(vertex, boardSize):
    """Returns a string representing the vertex.

    GTP uses A1 style notation: columns are letters left to right, rows are number bottom
    to top.
    """
    if vertex == "pass":
        return "pass"
    if len(vertex) != 2:
        return ParseCodes.ERROR
    if vertex[0] >= boardSize or vertex[1] >= boardSize or vertex[0] < 0 or vertex[1] < 0:
        return ParseCodes.ERROR

    vertexRow = boardSize - vertex[0]
    vertexCol = ord('A') + vertex[1]

    # Column 'I' does not exist
    if vertexCol >= ord('I'):
        vertexCol += 1

    return "%s%d" % (chr(vertexCol), vertexRow)

class GtpMove:
    """Stores the info of a move according to GTP specification: color and vertex."""
    def __init__(self, color, vertex):
        self.color = color
        self.vertex = vertex
