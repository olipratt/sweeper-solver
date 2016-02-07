"""
Tests for the Player character class.
"""
import unittest

from .player import Player, PlayerDiedError

# import logging
# logging.basicConfig(level=logging.DEBUG)


XP_THRESHOLDS = {1: 0,
                 2: 10,
                 3: 20,
                 4: 10000000}


class TestPlayerDeath(unittest.TestCase):
    """ Test that the player dies correctly. """

    def test_immediate_death(self):
        player = Player(10, XP_THRESHOLDS)

        self.assertRaises(PlayerDiedError, player.battle, 9)


class TestLevelUp(unittest.TestCase):
    """ Test that the player levels up correctly. """

    def test_single_level_up(self):
        player = Player(10, XP_THRESHOLDS)
        for iteration in range(10):
            player.battle(1)

        self.assertEqual(player.xp, 10)
        self.assertEqual(player.level, 2)
        self.assertEqual(player.hp, 10)


class TestTakeDamage(unittest.TestCase):
    """ Test that the player takes damage correctly. """

    def test_single_damage(self):
        player = Player(10, XP_THRESHOLDS)
        player.battle(2)

        self.assertEqual(player.xp, 2)
        self.assertEqual(player.level, 1)
        self.assertEqual(player.hp, 8)


class TestHighestSurvivable(unittest.TestCase):
    """ Test that the highest level the player can survive is correct. """

    def test_start_state(self):
        player = Player(10, XP_THRESHOLDS)

        self.assertEqual(player.highest_survivable_enemy, 3)

    def test_same_level(self):
        player = Player(1, XP_THRESHOLDS)

        self.assertEqual(player.highest_survivable_enemy, 1)
