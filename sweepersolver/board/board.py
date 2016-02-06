"""
Object to represent a game board.
"""
import logging

from ..point import Point
from ..boundedint import BoundedInt


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
        """ The Tile in this space on the board. """
        return self._tile

    def replace_placeholder(self, new_tile):
        """ Replace a placeholder tile with an actual tile, returning the
            placeholder.
        """
        if not self.tile.placeholder:
            raise ValueError("Can replace placeholder tile only")
        if new_tile.placeholder:
            raise ValueError("Must replace placeholder with non-placeholder")

        old_tile = self._tile
        self._tile = new_tile

        return old_tile

    @property
    def location(self):
        """ The coordinates of this tile on the game board. """
        return self._location

    @property
    def revealed(self):
        """ Whether this space is revealed, and so if the tile in this space is
            a placeholder or not.
        """
        return not self.tile.placeholder

    def is_neighbour(self, neighbour):
        """ Returns True if this space neighbours the given space. """
        return self.location.chebyshev_distance(neighbour.location) == 1


class GameBoard:
    """ Object to represent a game board made up of a 2D array of tiles. """

    def __init__(self, width, height, tile_bank):
        if width <= 0:
            raise ValueError("Width must be strictly positive")
        if height <= 0:
            raise ValueError("Height must be strictly positive")

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
        """ The read only width of the board. """
        return self._width

    @property
    def height(self):
        """ The read only height of the board. """
        return self._height

    def _get_space(self, location):
        """ Get the space at the given location on the board. """
        if not self._point_inside_board(location):
            raise ValueError("Tried to get tile outside board")

        return self._board[location.y][location.x]

    def get_tile(self, location):
        """ Get the tile at the given location on the board. """
        return self._get_space(location).tile

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

    def iter_unrevealed_neighbours(self, space):
        """ Return an iterator over all unrevealed spaces in the board
            neighbouring the given space.
        """
        return (neighbour for neighbour in self.iter_neighbours(space)
                if not neighbour.revealed)

    def in_start_state(self):
        """ Whether the board still has all tiles unrevealed. """
        return next(self.iter_revealed_spaces(), None) is None

    def iter_unrevealed_below_level(self, level):
        """ Iterator over all unrevealed tiles known to contain an enemy with
            a level no greater than the provided level.
        """
        return (space for space in self.iter_unrevealed_spaces()
                if space.tile.enemy_lvl <= level)

    def unrevealed_neighbour_levels_sum(self, space):
        """ The sum of the levels of the unrevealed neighbours of a space. """
        if not space.revealed:
            raise ValueError("Cannot calculate for unrevealed space")

        result = space.tile.neighbour_lvls_sum
        result -= sum(neighbour.tile.enemy_lvl.exact
                      for neighbour in self.iter_revealed_neighbours(space))

        log.debug("Found remaining unrevealed neighbours as: %r", result)
        return result

    def _point_inside_board(self, point):
        """ Check that the given point is that of a space on the board. """
        return (0 <= point.x < self.width) and (0 <= point.y < self.height)

    def set_revealed_tile(self, location, tile):
        """ Set the tile at the given coordinates to the given tile. """
        log.debug("Setting revealed tile %r at location: %r", tile, location)
        space = self._get_space(location)
        placeholder = space.replace_placeholder(tile)
        self._tile_bank.return_placeholder(placeholder)

        self._update_board_after_reveal(space)

    def space_level_bounds_from_neighbour(self, space, neighbour):
        """ Given a space and one of its neighbours, examine all other
            neighbours of the neighbour space to give a maximum and minumum
            possible level for the space.
        """
        if not neighbour.revealed:
            raise ValueError("Cannot calculate for unrevealed neighbour")
        if not space.is_neighbour(neighbour):
            raise ValueError("Spaces given must be neighbours")

        result_min = neighbour.tile.neighbour_lvls_sum
        result_max = neighbour.tile.neighbour_lvls_sum
        result_max -= sum(iter_neighbour.tile.enemy_lvl.min
                          for iter_neighbour in self.iter_neighbours(neighbour)
                          if iter_neighbour != space)
        result_min -= sum(iter_neighbour.tile.enemy_lvl.max
                          for iter_neighbour in self.iter_neighbours(neighbour)
                          if iter_neighbour != space)

        bounds = BoundedInt(result_min, result_max)

        log.debug("Found possible level limits as: %r", bounds)
        return bounds

    def _update_unrevealed_space(self, space):
        """ Given an unrevealed space, update its possible state from its
            neighbours.

        This means looping through all its revealed neighbours, and seeing if
        base on them we can further restrict the bounds on this space.

        :return: Returns True if the space was actually modified in any way.
        """
        log.debug("Updating bounds on unrevealed space: %r", space)
        if space.revealed:
            raise ValueError("Require unrevealed space")

        any_updates = False

        for neighbour in self.iter_revealed_neighbours(space):
            log.debug("Updating bounds based on neighbour: %r", neighbour)
            new_bounds = self.space_level_bounds_from_neighbour(space,
                                                                neighbour)
            updated = space.tile.restrict_enemy_level(new_bounds)
            any_updates = any_updates or updated

        return any_updates

    def _update_unrevealed_neighbours_of_revealed(self, space):
        """ Update all the unrevealed neighbours of the given revealed space on
            the board.

        :return: A set of any modified unrevealed spaces.
        """
        if not space.revealed:
            raise ValueError("Require revealed space")

        updated_spaces = set()

        for neighbour in self.iter_unrevealed_neighbours(space):
            log.debug("Checking unrevealed neighbour space: %r", neighbour)
            updated = self._update_unrevealed_space(neighbour)
            if updated:
                updated_spaces.add(neighbour)

        return updated_spaces

    def _propagate_unrevealed_space_update(self, unrevealed_space):
        """ An unrevealed space on the board has been updated - propagate that
            update to all affected spaces.

        In practice, this means that all revealed neighbours of the unrevealed
        space must have their unrevealed neighbours updated too.

        :return: Set of any modified unrevealed spaces.
        """
        modified_spaces = set()

        for neighbour in self.iter_revealed_neighbours(unrevealed_space):
            updates = self._update_unrevealed_neighbours_of_revealed(neighbour)
            modified_spaces.update(updates)

        log.debug("Modified spaces: %r", modified_spaces)
        return modified_spaces

    def _update_set_of_unrevealed_spaces(self, space_set):
        """ Given a set of updated unrevealed spaces, propagate those updates
            to the rest of the board. If any further updates are made,
            propagate those too, and so on until all updates are complete.
        """
        while len(space_set) > 0:
            space = space_set.pop()
            modified_spaces = self._propagate_unrevealed_space_update(space)
            space_set.update(modified_spaces)

    def _update_board_after_reveal(self, space):
        """ A space on the board has just been revealed. Update all affected
            spaces on the board to reflect this new information.

        When a space is revealed:
        - Each revealed neighbour needs to update all its unrevealed neighbours
          since their values are more closely constrained, but revealed
          neighbours of that revealed neighbour are unaffected.
        - Each unrevealed neighbour needs to update its possible values.

        Following on from and including those updates, any time that an
        unrevealed space is actually altered, all revealed neighbours of that
        space must have their unrevealed neighbours updated too. This cascade
        then continues until no more modifications take place.
        """
        updated_spaces = set()

        for neighbour in self.iter_unrevealed_neighbours(space):
            log.debug("Checking unrevealed neighbour space: %r", neighbour)
            updated = self._update_unrevealed_space(neighbour)
            if updated:
                log.debug("Space was updated")
                updated_spaces.add(neighbour)

        for neighbour in self.iter_revealed_neighbours(space):
            log.debug("Checking revealed neighbour space: %r", neighbour)
            updates = self._update_unrevealed_neighbours_of_revealed(neighbour)
            updated_spaces.update(updates)

        log.debug("Set of spaces to propagate updates to: %r", updated_spaces)
        self._update_set_of_unrevealed_spaces(updated_spaces)
