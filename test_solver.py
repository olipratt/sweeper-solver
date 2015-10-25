"""
Tests for the solver.
"""
import unittest

import solver


INITIAL_BOARD = [[[None, None], [None, None], [None, None]],
                 [[None, None], [None, None], [None, None]],
                 [[None, None], [None, None], [None, None]]]


class TestFirstMove(unittest.TestCase):
    """ Test that a suitable first move is made. """

    def test_first_move(self):
        next_move = solver.make_move(INITIAL_BOARD)
        self.assertEquals = (next_move, (1, 1))


if __name__ == "__main__":
    unittest.main()
