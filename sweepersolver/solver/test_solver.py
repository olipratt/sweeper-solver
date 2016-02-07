"""
Tests for the solver.
"""
import unittest

from ..point import Point
from ..tiles import TileBank
from ..board import GameBoard
from ..player import Player
from . import solver


# import logging
# logging.basicConfig(level=logging.DEBUG)


class TestFirstMove(unittest.TestCase):
    """ Test that a suitable first move is made. """

    def setUp(self):
        self.tile_bank = TileBank({0: 9})
        self.board = GameBoard(3, 3, self.tile_bank)
        self.board_center = Point(1, 1)
        self.test_player = Player(10, {})

    def test_first_move(self):
        next_move = solver.make_move(self.test_player, self.board)
        self.assertEqual(next_move, self.board_center)


class TestRevealedAtLowerLevel(unittest.TestCase):
    """ Test that a tile is revealed next to one that is surrounded by a total
        level lower than the player level.
    """

    def setUp(self):
        self.tile_bank = TileBank({0: 98, 1: 1, 5: 1})
        self.board = GameBoard(10, 10, self.tile_bank)
        self.revealed_location = Point(1, 1)
        self.board.set_revealed_tile(self.revealed_location,
                                     self.tile_bank.take(level=0,
                                                         neighbour_lvls_sum=1))
        self.test_player = Player(10, {})

    def test_single_revealed_at_same_level(self):
        next_move = solver.make_move(self.test_player, self.board)
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
        self.board.set_revealed_tile(self.revealed_location,
                                     self.tile_bank.take(level=0,
                                                         neighbour_lvls_sum=9))
        self.board.set_revealed_tile(self.revealed_neighbour,
                                     self.tile_bank.take(
                                         level=8,
                                         neighbour_lvls_sum=19))
        self.test_player = Player(10, {})

    def test_remaining_neighbours_at_same_level(self):
        next_move = solver.make_move(self.test_player, self.board)
        self.assertEqual(next_move.chebyshev_distance(self.revealed_location),
                         1)
        self.assertNotEqual(next_move, self.revealed_neighbour)


class TestMultistageBoardStatePropagation(unittest.TestCase):
    """ Test that board state can be determined and bounds on spaces propagated
        through multiple stages to determine a valid move.

    My original plan was as follows, but it's harder to implement than I hoped,
    since it makes other spaces low level too - so instead I just check that
    one of the goal spaces below is indeed known to be level 1 or lower.

    - Start with a set of three spaces containing at most level 5 enemies.
    - These border a space with a neighbour total of 16, but only one other
      non-zero neighbour.
    - This neighbour borders a revealed space with a neighbour total of 2,
      and only one other non-revealed space.
    - Hence that other non-revealed space can contain at most a level 1 enemy.
    """

    def setUp(self):
        self.tile_bank = TileBank({0: 10, 1: 10, 2: 10, 3: 10, 4: 10,
                                   5: 10, 6: 10, 7: 10, 8: 10, 9: 10})
        self.board = GameBoard(10, 10, self.tile_bank)
        self.start_location_1 = Point(2, 0)
        self.start_location_2 = Point(2, 4)
        self.second_location = Point(4, 2)
        self.third_location = Point(6, 4)
        self.zero_neighbours_1 = Point(5, 0)
        self.zero_neighbours_2 = Point(6, 1)
        self.lvl_zero_high_neighbours = Point(4, 3)
        self.a_goal_space = Point(7, 5)
        self.board.set_revealed_tile(self.start_location_1,
                                     self.tile_bank.take(level=0,
                                                         neighbour_lvls_sum=5))
        self.board.set_revealed_tile(self.start_location_2,
                                     self.tile_bank.take(level=0,
                                                         neighbour_lvls_sum=5))
        self.board.set_revealed_tile(self.second_location,
                                     self.tile_bank.take(
                                         level=0,
                                         neighbour_lvls_sum=20))
        self.board.set_revealed_tile(self.third_location,
                                     self.tile_bank.take(
                                         level=0,
                                         neighbour_lvls_sum=2))
        self.board.set_revealed_tile(self.zero_neighbours_1,
                                     self.tile_bank.take(
                                         level=0,
                                         neighbour_lvls_sum=0))
        self.board.set_revealed_tile(self.zero_neighbours_2,
                                     self.tile_bank.take(
                                         level=0,
                                         neighbour_lvls_sum=0))
        self.board.set_revealed_tile(self.lvl_zero_high_neighbours,
                                     self.tile_bank.take(
                                         level=0,
                                         neighbour_lvls_sum=20))
        self.test_player = Player(10, {})

    def test_propagation(self):
        # Useful for debugging:
        # print(self.board)
        next_move = solver.make_move(self.test_player, self.board)
        self.assertEqual(next_move.chebyshev_distance(self.start_location_1),
                         1)
        self.assertLessEqual(self.board.get_tile(self.a_goal_space).enemy_lvl,
                             1)


if __name__ == "__main__":
    unittest.main()
