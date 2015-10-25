"""
Tests for the solver.
"""
import unittest

import solver


INITIAL_BOARD = [[None, None, None],
                 [None, None, None],
                 [None, None, None]]
INITIAL_BOARD_CENTER = (1, 1)


class TestFirstMove(unittest.TestCase):
    """ Test that a suitable first move is made. """

    def test_first_move(self):
        next_move = solver.make_move(INITIAL_BOARD)
        self.assertEquals = (next_move, INITIAL_BOARD_CENTER)


if __name__ == "__main__":
    unittest.main()
