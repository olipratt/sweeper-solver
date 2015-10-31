"""
Object to represent a game board.
"""
import logging

from point import Point


log = logging.getLogger(__name__)


class BoardSpace:
    """ Represents a space on a game board, with coordinates and an optional
        tile.
    """

    def __init__(self, location, tile):
        self._location = location
        self._tile = tile

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,
                               self.location,
                               self.tile)

    def __str__(self):
        return "%s" % self.tile

    @property
    def tile(self):
        return self._tile

    def replace_placeholder(self, new_tile):
        assert self.tile.placeholder, "Must replace placeholder tile"
        assert not new_tile.placeholder, "Must replace with non-placeholder"
        old_tile = self._tile
        self._tile = new_tile

        return old_tile

    @property
    def location(self):
        return self._location

    @property
    def revealed(self):
        return not self.tile.placeholder

    def is_neighbour(self, neighbour):
        """ Returns True if this space neighbours the given space. """
        return self.location.chebyshev_distance(neighbour.location) == 1


class GameBoard:
    """ Object to represent a game board made up of a 2D array of tiles. """

    def __init__(self, width, height, tile_bank):
        assert width > 0, "Width must be strictly positive"
        assert height > 0, "Height must be strictly positive"
        self._width = width
        self._height = height
        self._tile_bank = tile_bank

        self._board = [[BoardSpace(Point(x, y),
                                   self._tile_bank.new_placeholder())
                        for x in range(self.width)]
                       for y in range(self.height)]

    def __repr__(self):
        row_strs = ["[%s]" % ", ".join(repr(space) for space in row)
                    for row in self._board]
        return "%s([%s])" % (self.__class__.__name__, ", ".join(row_strs))

    def __str__(self):
        row_strs = ["|%s|" % "|".join(str(space) for space in row)
                    for row in self._board]
        border = '-' * len(row_strs[0])
        inner_border = "\n%s\n" % border
        return "%s\n%s\n%s" % (border, inner_border.join(row_strs), border)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def iter_spaces(self):
        """ Return an iterator over all spaces in the board. """
        return (space for row in self._board for space in row)

    def iter_revealed_spaces(self):
        """ Return an iterator over all revealed spaces in the board. """
        return (space for space in self.iter_spaces() if space.revealed)

    def iter_unrevealed_spaces(self):
        """ Return an iterator over all unrevealed spaces in the board. """
        return (space for space in self.iter_spaces() if not space.revealed)

    def iter_neighbours(self, space):
        """ Return an iterator over all spaces in the board neighbouring the
            given space.
        """
        return (neighbour for neighbour in self.iter_spaces()
                if neighbour.is_neighbour(space))

    def iter_revealed_neighbours(self, space):
        """ Return an iterator over all revealed spaces in the board
            neighbouring the given space.
        """
        return (neighbour for neighbour in self.iter_neighbours(space)
                if neighbour.revealed)

    def in_start_state(self):
        """ Whether the board still has all tiles unrevealed. """
        return next(self.iter_revealed_spaces(), None) is None

    def unrevealed_neighbour_levels_sum(self, space):
        """ The sum of the levels of the unrevealed neighbours of a space. """
        assert space.revealed, "Cannot calculate for unrevealed space"
        result = space.tile.neighbour_lvls_sum
        result -= sum(neighbour.tile.enemy_lvl.exact
                      for neighbour in self.iter_revealed_neighbours(space))
        log.debug("Found remaining unrevealed neighbours as: %r", result)
        return result

    def set_tile(self, location, tile):
        """ Set the tile at the given coordinates to the given tile. """
        space = self._board[location.y][location.x]
        placeholder = space.replace_placeholder(tile)
        self._tile_bank.return_placeholder(placeholder)
