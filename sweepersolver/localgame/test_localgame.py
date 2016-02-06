"""
Tests for the local game.
"""
import unittest
from collections import Counter

from ..point import Point
from .localgame import LocalGame, GameOverError

# import logging
# logging.basicConfig(level=logging.DEBUG)


class TestSingleEnemyGame(unittest.TestCase):
    """ Test that a suitable first move is made. """

    def test_win(self):
        local_game = LocalGame(1, 1, Counter({1: 1}))

        local_game.reveal(Point(0, 0))

        self.assertTrue(local_game.is_complete)

    def test_loss(self):
        local_game = LocalGame(1, 1, Counter({9: 1}))

        self.assertRaises(GameOverError, local_game.reveal, Point(0, 0))


class TestInvalidReveals(unittest.TestCase):
    """ Test that attempts to reveal invalid locations are rejected. """

    def test_repeated_reveal(self):
        local_game = LocalGame(2, 2, Counter({1: 4}))

        local_game.reveal(Point(0, 0))
        self.assertRaises(ValueError, local_game.reveal, Point(0, 0))
