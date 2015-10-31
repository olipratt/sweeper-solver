"""
Object to represent a game board.
"""
import logging

from boundedint import BoundedInt

log = logging.getLogger(__name__)


class Tile:
    """ Represents a single tile on a game board. """

    def __init__(self, enemy_lvl, neighbour_lvls_sum=None, placeholder=False):
        self._enemy_lvl = enemy_lvl
        self._neighbour_lvls_sum = neighbour_lvls_sum
        self._placeholder = placeholder

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,
                               self.enemy_lvl,
                               self.neighbour_lvls_sum)

    def __str__(self):
        return "%d/%02d" % (self.enemy_lvl, self.neighbour_lvls_sum)

    @property
    def enemy_lvl(self):
        return self._enemy_lvl

    @property
    def neighbour_lvls_sum(self):
        return self._neighbour_lvls_sum

    @neighbour_lvls_sum.setter
    def neighbour_lvls_sum(self, neighbour_lvls_sum):
        assert self._neighbour_lvls_sum is None, \
            "Can't set neighbour_lvls_sum twice"
        self._neighbour_lvls_sum = neighbour_lvls_sum

    @property
    def placeholder(self):
        return self._placeholder


class TileBank:
    """ A collection of tiles with limits, which can be drawn from. """

    def __init__(self, enemy_lvls_and_counts):
        self._bank = {lvl: count
                      for lvl, count in enemy_lvls_and_counts.items()}
        self._max_level = max(key for key in self._bank)
        self._placeholders = []

    @property
    def max_level(self):
        return self._max_level

    def new_placeholder(self):
        new_placeholder = Tile(BoundedInt(0, self._max_level),
                               placeholder=True)
        self._placeholders.append(new_placeholder)
        return new_placeholder

    def return_placeholder(self, placeholder):
        assert placeholder.placeholder, "Returned placeholder not placeholder"
        assert placeholder in self._placeholders, "Not from this tile bank"
        self._placeholders.remove(placeholder)

    def take(self, level, neighbour_lvls_sum):
        assert level in self._bank
        assert self._bank[level] > 0
        self._bank[level] -= 1

        return Tile(BoundedInt(level, level),
                    neighbour_lvls_sum=neighbour_lvls_sum,
                    placeholder=False)
