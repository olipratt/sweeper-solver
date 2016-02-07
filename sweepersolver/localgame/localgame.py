"""
Run a local game to try and solve.
"""
import logging
import random

from ..board import GameBoard
from ..tiles import TileBank
from ..point import Point
from ..player import Player, PlayerDiedError

log = logging.getLogger(__name__)


class GameOverError(Exception):
    pass


class LocalGame(object):
    """ A local game to play against. """

    def __init__(self, difficulty):
        self._width = difficulty["width"]
        self._height = difficulty["height"]
        self._enemy_counter = difficulty["enemies"]

        self._tile_bank = TileBank(self._enemy_counter)
        self._board = GameBoard(self._width, self._height, self._tile_bank)

        self._place_enemies(list(self._enemy_counter.elements()))

        self._player = Player(difficulty["hp"], difficulty["xp thresholds"])

        self._revealed_locations = []

    def __str__(self):
        enemy_counts_str = ", ".join("%s: %s" % (enemy, count)
                                     for enemy, count in
                                     self._enemy_counter.items())
        return ("%s\nRevealed locations: %s\nEnemies:: %s\n%s" %
                (self._board,
                 self._revealed_locations,
                 enemy_counts_str,
                 self._player))

    @property
    def player(self):
        return self._player

    def reveal(self, location):
        """ Reveal and return a tile, forcing the player to battle any enemy
            on it. If the player dies, an error is raised.
        """
        if location in self._revealed_locations:
            raise ValueError("Can't reveal same location twice")
        self._revealed_locations.append(location)

        tile = self._board.get_tile(location)
        try:
            self._player.battle(tile.enemy_lvl.exact)
        except PlayerDiedError:
            raise GameOverError("Player Died! Killed by enemy: %s" %
                                tile.enemy_lvl.exact)

        self._enemy_counter.subtract({tile.enemy_lvl.exact: 1})
        return tile

    @property
    def is_complete(self):
        """ The game is complete when all (non-zero) enemies are defeated. """
        return (sum(value for key, value in self._enemy_counter.items()
                    if key is not 0) == 0)

    def _place_enemies(self, enemy_list):
        """ Randomly place the enemies on the board. """
        log.debug("Placing enemies: %r", enemy_list)

        if len(enemy_list) != (self._height * self._width):
            raise ValueError("Must have an enemy for every board space")

        board_spaces = [Point(x, y)
                        for y in range(self._height)
                        for x in range(self._width)]
        enemy_spaces = random.sample(board_spaces, len(enemy_list))

        spaces_to_enemies = {space: enemy
                             for space, enemy in zip(enemy_spaces, enemy_list)}
        log.debug("Decided enemy locations: %r", spaces_to_enemies)

        for space in board_spaces:
            log.debug("Placing tile in space: %r", space)
            neighbour_levels_sum = \
                sum(spaces_to_enemies.get(neighbour, 0)
                    for neighbour in space.all_chebyshev_neighbours())
            space_tile = self._tile_bank.take(spaces_to_enemies[space],
                                              neighbour_levels_sum)
            self._board.set_revealed_tile(space, space_tile)
