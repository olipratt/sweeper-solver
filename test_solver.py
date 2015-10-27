"""
Tests for the solver.
"""
import unittest

from point import Point
from board import GameBoard, Tile
import solver


# import logging
# logging.basicConfig(level=logging.DEBUG)


class TestFirstMove(unittest.TestCase):
    """ Test that a suitable first move is made. """

    def setUp(self):
        self.board = GameBoard(3, 3)
        self.board_center = Point(1, 1)

    def test_first_move(self):
        next_move = solver.make_move(1, self.board)
        self.assertEquals(next_move, self.board_center)


class TestRevealedAtLowerLevel(unittest.TestCase):
    """ Test that a tile is revealed next to one that is surrounded by a total
        level lower than the player level.
    """

    def setUp(self):
        self.board = GameBoard(10, 10)
        self.revealed_location = Point(1, 1)
        self.board.set_tile(self.revealed_location,
                            Tile(enemy_lvl=0, neighbour_lvls_sum=1))

    def test_single_revealed_at_same_level(self):
        next_move = solver.make_move(1, self.board)
        self.assertEqual(next_move.chebyshev_distance(self.revealed_location),
                         1)

if __name__ == "__main__":
    unittest.main()
