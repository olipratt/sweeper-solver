"""
Representations of a tile for a game board, and a bank of available tiles.
"""
import logging

from .boundedint import BoundedInt

log = logging.getLogger(__name__)


class Tile:
    """ Represents a single tile on a game board. """

    def __init__(self, enemy_lvl, neighbour_lvls_sum=None, placeholder=False):
        if not isinstance(enemy_lvl, BoundedInt):
            raise TypeError("Enemy level must be bounded integer")
        self._enemy_lvl = enemy_lvl
        self._neighbour_lvls_sum = neighbour_lvls_sum
        self._placeholder = placeholder

    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__.__name__,
                                   self.enemy_lvl,
                                   self.neighbour_lvls_sum,
                                   self.placeholder)

    def __str__(self):
        placeholder_str = "?" if self.placeholder else "/"
        if self.neighbour_lvls_sum is None:
            neighbour_str = "--"
        else:
            neighbour_str = "%02d" % self.neighbour_lvls_sum
        return "%s%s%s" % (self.enemy_lvl, placeholder_str, neighbour_str)

    @property
    def enemy_lvl(self):
        """ Get the level of the enemy on this tile as a bounded integer. """
        return self._enemy_lvl

    @property
    def neighbour_lvls_sum(self):
        """ The sum of levels of enemies on all neighbouring tiles.

        Is None on a placeholder, and a fixed value on a non-placeholder.
        """
        return self._neighbour_lvls_sum

    @property
    def placeholder(self):
        """ Whether this is a placeholder tile or not. """
        return self._placeholder

    def restrict_enemy_level(self, new_bounds):
        """ Tighten the bounds on the enemy level if at all possible using the
            new bounds provided - hence this must be a placeholder tile.

        :return: True if the bounds on this tile were updated at all.
        """
        if not self.placeholder:
            raise ValueError("Can't update bounds on non-placeholder tile")

        intersection = self.enemy_lvl.intersection(new_bounds)
        if intersection is None:
            raise ValueError("New bounds don't intersect existing bounds")

        if intersection == self.enemy_lvl:
            return False
        else:
            self._enemy_lvl = intersection
            return True


class TileBank:
    """ A collection of tiles with limits, which can be drawn from. """

    def __init__(self, enemy_lvls_and_counts):
        if len(enemy_lvls_and_counts) == 0:
            raise ValueError("Tile bank must contain some tiles")

        self._bank = {lvl: count
                      for lvl, count in enemy_lvls_and_counts.items()}
        self._min_level = min(key for key in self._bank)
        self._max_level = max(key for key in self._bank)
        self._placeholders = []

    @property
    def min_level(self):
        """ The read-only minimum tile level in the bank. """
        return self._min_level

    @property
    def max_level(self):
        """ The read-only maximum tile level in the bank. """
        return self._max_level

    def new_placeholder(self):
        """ Create a new placeholder tile associated with this bank. """
        new_placeholder = Tile(BoundedInt(self.min_level, self.max_level),
                               placeholder=True)
        self._placeholders.append(new_placeholder)
        return new_placeholder

    def return_placeholder(self, placeholder):
        """ Return a placeholder tile to the bank. """
        if not placeholder.placeholder:
            raise ValueError("Tried to return non-placeholder tile")
        if placeholder not in self._placeholders:
            raise ValueError("Tried to return placeholder not from this bank")

        self._placeholders.remove(placeholder)

    def take(self, level, neighbour_lvls_sum):
        """ Take a tile from the bank's pool - one must be available. """
        if level not in self._bank:
            raise ValueError("Tried to take tile not present in bank")
        if self._bank[level] <= 0:
            raise ValueError("No tiles of this level left in bank")

        new_tile = Tile(BoundedInt(level, level),
                        neighbour_lvls_sum=neighbour_lvls_sum,
                        placeholder=False)

        self._bank[level] -= 1

        return new_tile
