"""Tests for parseHelpers module."""

import unittest

from imago.data.enums import Player
from imago.engine import parseHelpers

TEST_BOARD_SIZE = 19

class TestParseHelpers(unittest.TestCase):
    """Test parseHelpers module."""

    def testParseMove(self):
        """Test parsing of GtpMove"""

        self.assertEqual(parseHelpers.parseMove(["B"], TEST_BOARD_SIZE),
            parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.parseMove(["A1"], TEST_BOARD_SIZE),
            parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.parseMove(["B", "A1", "W"], TEST_BOARD_SIZE),
            parseHelpers.ParseCodes.ERROR)

        parsedMove = parseHelpers.parseMove(["B", "t1"], TEST_BOARD_SIZE)

        targetMove = parseHelpers.GtpMove(Player.BLACK, [18, 18])
        self.assertEqual(parsedMove.color, targetMove.color)
        self.assertEqual(parsedMove.vertex, targetMove.vertex)

    def testParseColor(self):
        """Test parsing of color"""
        self.assertEqual(parseHelpers.parseColor("b"), Player.BLACK)
        self.assertEqual(parseHelpers.parseColor("B"), Player.BLACK)
        self.assertEqual(parseHelpers.parseColor("w"), Player.WHITE)
        self.assertEqual(parseHelpers.parseColor("W"), Player.WHITE)
        self.assertEqual(parseHelpers.parseColor("bw"), parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.parseColor("wb"), parseHelpers.ParseCodes.ERROR)

    def testParseVertexWrongInputs(self):
        """Test wrong inputs for parseVertex."""
        inputs = ( "a", "1", "1a", "aa1", "a0", "u1", "a"+str(TEST_BOARD_SIZE+1) )
        for text in inputs:
            self.assertEqual(parseHelpers.parseVertex(text, TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)

    def testParseVertexCorrectInputs(self):
        """Test correct inputs and their resulting coordinates for parseVertex."""
        self.assertEqual(parseHelpers.parseVertex(
            "a1", TEST_BOARD_SIZE),
            [18,0])
        self.assertEqual(parseHelpers.parseVertex(
            "b1", TEST_BOARD_SIZE),
            [18,1])
        self.assertEqual(parseHelpers.parseVertex(
            "a2", TEST_BOARD_SIZE),
            [17,0])
        self.assertEqual(parseHelpers.parseVertex(
            "b2", TEST_BOARD_SIZE),
            [17,1])

        self.assertEqual(parseHelpers.parseVertex(
            "T1", TEST_BOARD_SIZE),
            [18,18])
        self.assertEqual(parseHelpers.parseVertex(
            "T19", TEST_BOARD_SIZE),
            [0,18])
        self.assertEqual(parseHelpers.parseVertex(
            "A19", TEST_BOARD_SIZE),
            [0,0])

    def testVertexToString(self):
        """Test converting vertices to strings."""
        self.assertEqual(parseHelpers.vertexToString([0,0], TEST_BOARD_SIZE), "A19")
        self.assertEqual(parseHelpers.vertexToString([1,0], TEST_BOARD_SIZE), "A18")
        self.assertEqual(parseHelpers.vertexToString([2,0], TEST_BOARD_SIZE), "A17")
        self.assertEqual(parseHelpers.vertexToString([0,1], TEST_BOARD_SIZE), "B19")
        self.assertEqual(parseHelpers.vertexToString([0,2], TEST_BOARD_SIZE), "C19")
        self.assertEqual(parseHelpers.vertexToString([0,18], TEST_BOARD_SIZE), "T19")
        self.assertEqual(parseHelpers.vertexToString([18,0], TEST_BOARD_SIZE), "A1")
        self.assertEqual(parseHelpers.vertexToString([18,18], TEST_BOARD_SIZE), "T1")

        self.assertEqual(parseHelpers.vertexToString([-1,0], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.vertexToString([0,-1], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.vertexToString([-1,-1], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.vertexToString([19,0], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.vertexToString([0,19], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.vertexToString([19,19], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.vertexToString([0], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)
        self.assertEqual(parseHelpers.vertexToString([0,0,0], TEST_BOARD_SIZE),
                parseHelpers.ParseCodes.ERROR)

if __name__ == '__main__':
    unittest.main()
