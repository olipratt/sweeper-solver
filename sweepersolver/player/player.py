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
XP_THRESHOLDS = [0, 10, 40, 10000000]


class PlayerDiedError(Exception):
    pass


class Player:
    """ The player character in the game. """

    def __init__(self):
        self.level = 1
        self.hp = 10
        self.xp = 0

    def __str__(self):
        return ("Player:: Level: %s, HP: %s, XP: %s" %
                (self.level, self.hp, self.xp))

    def battle(self, enemy_level):
        self.hp -= self._damage_taken(enemy_level)
        if self.hp <= 0:
            raise PlayerDiedError("Player died!")

        self.xp += self._calc_xp(enemy_level)
        self._check_for_level_up()

    def _calc_damage(self, enemy_level):
        """ Damage is dealt by the player and the enemy both equal to their
            level. The player strikes first, then the enemy counter-attacks.
            This calculation works out how much damage the player would take
            in killing the enemy (which may far exceed their HP!).
        """
        return ((((enemy_level + self.level - 1) // self.level) - 1) *
                enemy_level)

    def _damage_taken(self, enemy_level):
        level_diff = self.level - enemy_level
        if level_diff < 0:
            damage_taken = self._calc_damage(enemy_level)
        else:
            damage_taken = 0

        log.debug("Player took damage: %r", damage_taken)
        return damage_taken

    def _calc_xp(self, enemy_level):
        return LEVEL_TO_XP[enemy_level]

    def _check_for_level_up(self):
        while (self.xp > XP_THRESHOLDS[self.level + 1]):
            log.debug("Level up to level: %r", self.level + 1)
            self.level += 1
