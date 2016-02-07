"""
The player playing a game.
"""
import logging

log = logging.getLogger(__name__)


LEVEL_TO_XP = {0: 0,
               1: 1,
               2: 2,
               3: 4,
               4: 8,
               5: 16,
               6: 32,
               7: 64,
               8: 128,
               9: 256}
XP_THRESHOLDS_DEFAULT = {1: 0,
                         2: 2,
                         3: 10,
                         4: 150,
                         5: 540,
                         6: 1116,
                         7: 2268,
                         8: 4572,
                         9: 9180,
                         10: 100000}


class PlayerDiedError(Exception):
    pass


class Player:
    """ The player character in the game. """

    def __init__(self, hp=10, xp_thresholds=XP_THRESHOLDS_DEFAULT, level=1):
        self._level = level
        self._hp = hp
        self._xp = xp_thresholds[level]
        self._xp_thresholds = xp_thresholds

    @property
    def level(self):
        return self._level

    @property
    def hp(self):
        return self._hp

    @property
    def xp(self):
        return self._xp

    @property
    def highest_survivable_enemy(self):
        """ Get the highest level enemy the player can face without dying. """
        survivable_level = self.level
        while (self._calc_damage(survivable_level + 1) < self.hp):
            survivable_level += 1
        return survivable_level

    def __str__(self):
        return ("Player:: Level: %s, HP: %s, XP: %s" %
                (self.level, self.hp, self.xp))

    def battle(self, enemy_level):
        self._take_danage(enemy_level)
        self._gain_xp(enemy_level)

    def _calc_damage(self, enemy_level):
        """ Damage is dealt by the player and the enemy both equal to their
            level. The player strikes first, then the enemy counter-attacks.
            This calculation works out how much damage the player would take
            in killing the enemy (which may far exceed their HP!).
        """
        return ((((enemy_level + self.level - 1) // self.level) - 1) *
                enemy_level)

    def _take_danage(self, enemy_level):
        """ Update the player's HP based on battling an enemy of the given
            level, and raise an error if they die.
        """
        level_diff = self.level - enemy_level
        if level_diff < 0:
            damage_taken = self._calc_damage(enemy_level)
        else:
            damage_taken = 0

        log.debug("Player took damage: %r", damage_taken)
        self._hp -= damage_taken

        if self.hp <= 0:
            raise PlayerDiedError("Player died!")

    def _gain_xp(self, enemy_level):
        """ Increment the player's XP after killing an enemy. """
        self._xp += LEVEL_TO_XP[enemy_level]
        self._perform_any_level_ups()

    def _perform_any_level_ups(self):
        """ Perform any level ups after the player's XP changes. """
        while (self.xp >= self._xp_thresholds[self.level + 1]):
            log.debug("Level up to level: %r", self.level + 1)
            self._level += 1
