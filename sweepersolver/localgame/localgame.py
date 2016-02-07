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


XP_THRESHOLDS = {1: 0,
                 2: 10,
                 3: 20,
                 4: 40,
                 5: 82,
                 6: 100000}


class GameOverError(Exception):
    pass


class LocalGame(object):
    """ A local game to play against. """

    def __init__(self, width, height, enemy_counter):
        super(LocalGame, self).__init__()
        self._width = width
        self._height = height
        self._enemy_counter = enemy_counter

        self._tile_bank = TileBank(enemy_counter)
        self._board = GameBoard(self._width, self._height, self._tile_bank)

        self._place_enemies(list(enemy_counter.elements()))

        self._player = Player(XP_THRESHOLDS)

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
        return (sum(value for key, value in self._enemy_counter.items()
                    if key is not 0) == 0)

    def _new_board(self):
        return [[self._new_space() for i in range(self.width)]
                for j in range(self.height)]

    def _new_space(self):
        return {"revealed": False, "enemy": None}

    def _place_enemies(self, enemy_list):
        log.debug("Placing enemies: %r", enemy_list)
        board_spaces = [Point(x, y)
                        for y in range(self._height)
                        for x in range(self._width)]
        enemy_spaces = random.sample(board_spaces, len(enemy_list))

        spaces_to_enemies = {space: 0 for space in board_spaces}
        spaces_to_enemies.update({space: enemy
                                  for space, enemy in zip(enemy_spaces,
                                                          enemy_list)})
        log.debug("Decided enemy locations: %r", spaces_to_enemies)

        for space in board_spaces:
            log.debug("Placing tile in space: %r", space)
            neighbour_levels_sum = \
                sum(spaces_to_enemies.get(neighbour, 0)
                    for neighbour in space.all_chebyshev_neighbours())
            space_tile = self._tile_bank.take(spaces_to_enemies[space],
                                              neighbour_levels_sum)
            self._board.set_revealed_tile(space, space_tile)
