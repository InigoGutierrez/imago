#!/usr/bin/python

"""Play Go!"""

from imago.engine.parseHelpers import ParseCodes, parseVertex
from imago.gameLogic.gameState import GameState

if __name__ == "__main__":

    #GAMESTATE = GameState(5)
    GAMESTATE = GameState(19)

    while 1:

        GAMESTATE.getBoard().printBoard()

        move = input("Move (" + GAMESTATE.getPlayerCode() + "): ")
        move = parseVertex(move, GAMESTATE.size)

        if move == ParseCodes.ERROR:
            print("Invalid move syntax. Example of move: A1")
            continue

        print()

        player = str(GAMESTATE.getPlayerCode())

        moveRow = move[0]
        moveCol = move[1]

        GAMESTATE.playMove(moveRow, moveCol)
