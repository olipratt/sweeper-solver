"""
Tests for the local game.
"""
import unittest
from collections import Counter

from ..point import Point
from .localgame import LocalGame, GameOverError

# import logging
# logging.basicConfig(level=logging.DEBUG)

XP_THRESHOLDS = {1: 0,
                 2: 10,
                 3: 20,
                 4: 10000000}


class TestSingleEnemyGame(unittest.TestCase):
    """ Test that a suitable first move is made. """

    def test_win(self):
        difficulty = {"width": 1,
                      "height": 1,
                      "hp": 10,
                      "enemies": Counter({1: 1}),
                      "xp thresholds": XP_THRESHOLDS}
        local_game = LocalGame(difficulty)

        local_game.reveal(Point(0, 0))

        self.assertTrue(local_game.is_complete)

    def test_loss(self):
        difficulty = {"width": 1,
                      "height": 1,
                      "hp": 10,
                      "enemies": Counter({9: 1}),
                      "xp thresholds": XP_THRESHOLDS}
        local_game = LocalGame(difficulty)

        self.assertRaises(GameOverError, local_game.reveal, Point(0, 0))


class TestInvalidReveals(unittest.TestCase):
    """ Test that attempts to reveal invalid locations are rejected. """

    def test_repeated_reveal(self):
        difficulty = {"width": 2,
                      "height": 2,
                      "hp": 10,
                      "enemies": Counter({1: 4}),
                      "xp thresholds": XP_THRESHOLDS}
        local_game = LocalGame(difficulty)

        local_game.reveal(Point(0, 0))
        self.assertRaises(ValueError, local_game.reveal, Point(0, 0))
