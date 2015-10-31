"""
Tests for the solver.
"""
import unittest

from point import Point
from tiles import TileBank
from board import GameBoard
import solver


# import logging
# logging.basicConfig(level=logging.DEBUG)


class TestFirstMove(unittest.TestCase):
    """ Test that a suitable first move is made. """

    def setUp(self):
        self.tile_bank = TileBank({0: 9})
        self.board = GameBoard(3, 3, self.tile_bank)
        self.board_center = Point(1, 1)

    def test_first_move(self):
        next_move = solver.make_move(1, self.board)
        self.assertEquals(next_move, self.board_center)


class TestRevealedAtLowerLevel(unittest.TestCase):
    """ Test that a tile is revealed next to one that is surrounded by a total
        level lower than the player level.
    """

    def setUp(self):
        self.tile_bank = TileBank({0: 100})
        self.board = GameBoard(10, 10, self.tile_bank)
        self.revealed_location = Point(1, 1)
        self.board.set_tile(self.revealed_location,
                            self.tile_bank.take(level=0, neighbour_lvls_sum=1))

    def test_single_revealed_at_same_level(self):
        next_move = solver.make_move(1, self.board)
        self.assertEqual(next_move.chebyshev_distance(self.revealed_location),
                         1)


class TestRemainingNeighboursAtLowerLevel(unittest.TestCase):
    """ Test that a tile is revealed next to one that is surrounded by a total
        level higher than the player level, but enough have already been
        revealed so the remaining total is lower.
    """

    def setUp(self):
        self.tile_bank = TileBank({0: 99, 8: 1})
        self.board = GameBoard(10, 10, self.tile_bank)
        self.revealed_location = Point(2, 2)
        self.revealed_neighbour = Point(1, 1)
        self.board.set_tile(self.revealed_location,
                            self.tile_bank.take(level=0, neighbour_lvls_sum=9))
        self.board.set_tile(self.revealed_neighbour,
                            self.tile_bank.take(level=8, neighbour_lvls_sum=19))

    def test_remaining_neighbours_at_same_level(self):
        next_move = solver.make_move(1, self.board)
        self.assertEqual(next_move.chebyshev_distance(self.revealed_location),
                         1)
        self.assertNotEqual(next_move, self.revealed_neighbour)


if __name__ == "__main__":
    unittest.main()
