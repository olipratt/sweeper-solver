"""
Object to represent a game board.
"""
import logging


log = logging.getLogger(__name__)


class Tile:
    """ Represents a single tile on a game board. """

    def __init__(self, enemy_lvl=None, neighbour_lvls_sum=None):
        self._enemy_lvl = enemy_lvl
        self._neighbour_lvls_sum = neighbour_lvls_sum

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,
                               self.enemy_lvl,
                               self.neighbour_lvls_sum)

    def __str__(self):
        return "%d/%02d" % (self.enemy_lvl, self.neighbour_lvls_sum)

    @property
    def enemy_lvl(self):
        return self._enemy_lvl

    @enemy_lvl.setter
    def enemy_lvl(self, enemy_lvl):
        assert self._enemy_lvl is None, "Can't set enemy_lvl twice"
        self._enemy_lvl = enemy_lvl

    @property
    def neighbour_lvls_sum(self):
        return self._neighbour_lvls_sum

    @neighbour_lvls_sum.setter
    def neighbour_lvls_sum(self, neighbour_lvls_sum):
        assert self._neighbour_lvls_sum is None, \
            "Can't set neighbour_lvls_sum twice"
        self._neighbour_lvls_sum = neighbour_lvls_sum


class TileBank:
    """ A collection of tiles with limits, which can be drawn from. """

    def __init__(self, enemy_lvl_count_pairs):
        self._bank = {lvl: count for lvl, count in enemy_lvl_count_pairs}

    @property
    def max_level(self):
        return max(key for key in self._bank)
