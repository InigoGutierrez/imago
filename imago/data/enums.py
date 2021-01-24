"""Enums"""

from enum import Enum, auto as enumAuto

class Player(Enum):
    """Possibilities for players and the state of a cell."""
    EMPTY = enumAuto()
    BLACK = enumAuto()
    WHITE = enumAuto()

    @classmethod
    def otherPlayer(cls, player):
        """If argument is BLACK or WHITE returns the other, else it returns EMPTY."""
        if player == cls.BLACK:
            return cls.WHITE
        if player == cls.WHITE:
            return cls.BLACK
        return cls.EMPTY
