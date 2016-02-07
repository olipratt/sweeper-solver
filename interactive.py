"""
Run the solver with a user interface.
"""
from queue import Queue
import logging

from cli import CLIInput
from sweepersolver import GameBoard, TileBank, Point, Player, make_move


log = logging.getLogger(__name__)


def _get_initial_parameters(to_user_q, from_user_q):
    log.debug("Retrieving initial parameters")
    to_user_q.put("We'll need some initial information.")
    to_user_q.put("1. Please enter the width of the board, in squares:")
    width = int(from_user_q.get())
    to_user_q.put("2. Please enter the height of the board, in squares:")
    height = int(from_user_q.get())
    to_user_q.put("3. Please provide the counts of enemies on the board. "
                  "Enter them in the format: '<enemy_level>: <count>', with "
                  "each entry on a new line. Once all have been entered, "
                  "enter 'q' on its own line.")

    enemies = {}
    response = from_user_q.get().strip()
    while response != 'q':
        level_str, count_str = response.split(':')
        level = int(level_str.strip())
        count = int(count_str.strip())
        enemies[level] = count
        response = from_user_q.get().strip()

    return width, height, enemies


def _output_game_state(to_user_q, board, level):
    to_user_q.put("Current board state:")
    to_user_q.put(str(board))
    to_user_q.put("Player level: %s" % level)


def _output_next_move(to_user_q, game_board, level):
    next_move = make_move(Player(level=level), game_board)
    to_user_q.put("Next move: %s" % next_move)


def _get_new_level(to_user_q, from_user_q):
    to_user_q.put("Please enter current level:")
    level = int(from_user_q.get().strip())
    return level


def _get_more_board_state(to_user_q, from_user_q, game_board, tile_bank):
    user_input = None

    while user_input != 'q':
        to_user_q.put("Please enter a revealed tile, in the format: \n"
                      "<x_coord>, <y_coord>, <monster_level>, "
                      "<neighbour_levels_sum>\n"
                      "Enter q to stop entering tiles.")
        user_input = from_user_q.get().strip()
        split_input = user_input.split(',')

        if len(split_input) == 4:
            x_coord = int(split_input[0].strip())
            y_coord = int(split_input[1].strip())
            monster_level = int(split_input[2].strip())
            neighbour_levels_sum = int(split_input[3].strip())
            game_board.set_revealed_tile(Point(x_coord, y_coord),
                                         tile_bank.take(monster_level,
                                                        neighbour_levels_sum))


def _main_loop(to_user_q, from_user_q, game_board, tile_bank):
    level = 1

    action = None
    while action != 'q':
        _output_game_state(to_user_q, game_board, level)
        to_user_q.put("Please select one of the following:\n"
                      "  i: input more data about the state of the board\n"
                      "  n: get next move\n"
                      "  l: update level\n"
                      "  q: quit")
        action = from_user_q.get().strip()

        if action == 'i':
            _get_more_board_state(to_user_q,
                                  from_user_q,
                                  game_board,
                                  tile_bank)
        elif action == 'l':
            level = _get_new_level(to_user_q, from_user_q)
        elif action == 'n':
            _output_next_move(to_user_q, game_board, level)


def run_interactive():
    to_user_q = Queue()
    from_user_q = Queue()
    interface = CLIInput(to_user_q, from_user_q)
    interface.start()

    to_user_q.put("Welcome to the sweepersolver!")

    width, height, enemies = _get_initial_parameters(to_user_q, from_user_q)
    tile_bank = TileBank(enemies)
    game_board = GameBoard(width, height, tile_bank)

    _main_loop(to_user_q, from_user_q, game_board, tile_bank)

    interface.stop()
