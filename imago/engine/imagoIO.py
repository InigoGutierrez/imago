#!/usr/bin/python

"""Imago GTP engine input output"""

import sys

from imago.engine import parseHelpers
from imago.engine.core import GameEngine

def protocol_version(_):
    """Version of the GTP Protocol"""
    print("2")

def name(_):
    """Name of the engine"""
    print("Imago")

def version(_):
    """Version of the engine"""
    print("0.0.0")

def getCoordsText(row, col):
    """Returns a string representation of row and col.
        In GTP A1 is bottom left corner.
    """
    return "%s%d" % (chr(65+row), col+1)

class ImagoIO:
    """Recieves and handles commands."""

    def __init__(self):
        self.commands_set = {
            protocol_version,
            name,
            version,
            self.known_command,
            self.list_commands,
            self.boardsize,
            self.clear_board,
            self.komi,
            self.fixed_handicap,
            self.place_free_handicap,
            self.set_free_handicap,
            self.play,
            self.genmove,
            self.undo
        }
        self.gameEngine = GameEngine()

    def start(self):
        """Starts reading commands interactively."""
        while True:
            input_tokens = input().split()

            if input_tokens[0] == "quit":
                sys.exit(0)

            command = None
            for comm in self.commands_set:
                if comm.__name__ == input_tokens[0]:
                    command = comm

            if command is not None:
                arguments = input_tokens[1:]
                #print("[DEBUG]:Selected command: %s; args: %s" % (command, arguments))
                command(arguments)
            else:
                print("unknown command")

    def known_command(self, args):
        """True if command is known, false otherwise"""
        if len(args) != 1:
            print ("Wrong number of args.")
            print ("Usage: known_command COMMAND_NAME")
            sys.exit(0)
        out = "false"
        for c in self.commands_set:
            if c.__name__ == args[0]:
                out = "true"
        print(out)

    def list_commands(self, _):
        """List of commands, one per row"""
        for c in self.commands_set:
            print("%s - %s" % (c.__name__, c.__doc__))

    def boardsize(self, args):
        """Changes the size of the board.
        Board state, number of stones and move history become arbitrary.
        It is wise to call clear_board after this command.
        """
        if len(args) != 1:
            print("Error - Wrong n of args")
            sys.exit(1)
        size = int(args[0])
        self.gameEngine.setBoardsize(size)

    def clear_board(self, _):
        """The board is cleared, the number of captured stones reset to zero and the move
        history reset to empty.
        """
        self.gameEngine.clearBoard()

    def komi(self, args):
        """Sets a new value of komi."""
        if len(args) != 1:
            print("Error - Wrong n of args")
            sys.exit(1)
        komi = float(args[0])
        self.gameEngine.setKomi(komi)

    def fixed_handicap(self, args):
        """Handicap stones are placed on the board on standard vertices.
            These vertices follow the GTP specification.
        """
        if len(args) != 1:
            print("Error - Wrong n of args")
            sys.exit(1)
        stones = float(args[0])
        vertices = self.gameEngine.setFixedHandicap(stones)
        out = getCoordsText(vertices[0][0], vertices[0][1])
        for vertex in vertices[1:]:
            out += " " + getCoordsText(vertex[0], vertex[1])
        print(out)

    def place_free_handicap(self, args):
        """Handicap stones are placed on the board by the AI criteria."""
        #TODO

    def set_free_handicap(self, args):
        """Handicap stones are placed on the board as requested."""
        #TODO

    def play(self, args):
        """A stone of the requested color is played at the requested vertex."""
        if len(args) != 2:
            print("Error - Wrong n of args")
            sys.exit(1)
        move = parseHelpers.parseMove(args, self.gameEngine.gameState.size)
        self.gameEngine.play(move.color, move.vertex)

    def genmove(self, args):
        """A stone of the requested color is played where the engine chooses."""
        if len(args) != 1:
            print("Error - Wrong n of args")
            sys.exit(1)
        color = parseHelpers.parseColor(args[0])
        output = parseHelpers.vertexToString(self.gameEngine.genmove(color),
                self.gameEngine.gameState.size)
        print(output)
        self.gameEngine.gameState.getBoard().printBoard()

    def undo(self, _):
        """The board configuration and number of captured stones are reset to the state
            before the last move, which is removed from the move history.
        """
        self.gameEngine.undo()
