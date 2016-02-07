"""
Run the solver against an automated game locally.
"""
import logging
from collections import Counter

from sweepersolver import GameBoard, TileBank, make_move, LocalGame

log = logging.getLogger(__name__)


def run_automated():
    width = 16
    height = 16
    enemies = Counter({0: 226, 1: 10, 2: 8, 3: 6, 4: 4, 5: 2})
    local_game = LocalGame(width, height, enemies)

    tile_bank = TileBank(enemies)
    game_board = GameBoard(width, height, tile_bank)

    while not local_game.is_complete:
        print("Game state:\n%s" % local_game)
        next_location = make_move(local_game.player.level, game_board)

        print("Playing location: %s" % next_location)
        local_revealed_tile = local_game.reveal(next_location)
        bank_tile = tile_bank.take(local_revealed_tile.enemy_lvl.exact,
                                   local_revealed_tile.neighbour_lvls_sum)
        game_board.set_revealed_tile(next_location, bank_tile)

    print("Game won!")
