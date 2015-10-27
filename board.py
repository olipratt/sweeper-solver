"""
Object to represent a game board.
"""
import logging

from point import Point


log = logging.getLogger(__name__)


class Tile:
    """ Represents a single tile on a game board. """

    def __init__(self, enemy_lvl, neighbour_lvls_sum):
        self._enemy_lvl = enemy_lvl
        self._neighbour_lvls_sum = neighbour_lvls_sum

    @property
    def enemy_lvl(self):
        return self._enemy_lvl

    @property
    def neighbour_lvls_sum(self):
        return self._neighbour_lvls_sum


class BoardSpace:
    """ Represents a space on a game board, with coordinates and an optional
        tile.
    """

    def __init__(self, location, tile=None):
        self._location = location
        self._tile = tile

    @property
    def tile(self):
        return self._tile

    @property
    def location(self):
        return self._location

    @property
    def revealed(self):
        return self.tile is not None

    @tile.setter
    def tile(self, tile):
        assert self._tile is None
        self._tile = tile

    def is_neighbour(self, neighbour):
        """ Returns True if this space neighbours the given space. """
        return self.location.chebyshev_distance(neighbour.location)


class GameBoard:
    """ Object to represent a game board made up of a 2D array of tiles. """

    def __init__(self, width, height):
        self._width = width
        self._height = height

        self._board = [[BoardSpace(Point(x, y)) for x in range(self.width)]
                       for y in range(self.height)]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def iter_spaces(self):
        """ Return an iterator over all spaces in the board. """
        return (space for row in self._board for space in row)

    def iter_neighbours(self, space):
        """ Return an iterator over all spaces in the board neighbouring the
            given space.
        """
        return (neighbour for neighbour in self.iter_spaces()
                if neighbour.is_neighbour(space))

    def in_start_state(self):
        """ Whether the board still has all tiles unrevealed. """
        for board_space in self.iter_spaces():
            if board_space.revealed:
                log.debug("Found revealed board space: %r", board_space)
                return False

        log.debug("No revealed spaces found")
        return True

    def set_tile(self, location, tile):
        """ Set the tile at the given coordinates to the given tile. """
        self._board[location.y][location.x].tile = tile
