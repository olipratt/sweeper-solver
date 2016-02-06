"""
Representation of a bank of available tiles.
"""
import logging

from .tile import Tile
from ..boundedint import BoundedInt

log = logging.getLogger(__name__)


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
