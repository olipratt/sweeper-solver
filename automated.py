"""
Run the solver against an automated game locally.
"""
import logging
from collections import Counter

from sweepersolver import GameBoard, TileBank, make_move, LocalGame

log = logging.getLogger(__name__)


def run_automated(difficulty):
    enemies = Counter(difficulty["enemies"])
    local_game = LocalGame(difficulty)

    tile_bank = TileBank(enemies)
    game_board = GameBoard(difficulty["width"],
                           difficulty["height"],
                           tile_bank)

    while not local_game.is_complete:
        print("Game state:\n%s" % local_game)
        print("Player knowledge:\n%s" % game_board)
        next_location = make_move(local_game.player, game_board)

        print("Playing location: %s" % next_location)
        local_revealed_tile = local_game.reveal(next_location)
        print("Location contained: %s" % local_revealed_tile)
        bank_tile = tile_bank.take(local_revealed_tile.enemy_lvl.exact,
                                   local_revealed_tile.neighbour_lvls_sum)
        game_board.set_revealed_tile(next_location, bank_tile)

    print("Game won!")
