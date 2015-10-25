"""
Solver for mamono sweeper.

The main API function is 'next_move' - this takes a game board as an argument,
and returns the next location to reveal.

The game board is simply represented as a 2d array of locations. Each location
is either:
- None, indicating that the location is still hidden.
- (enemy_lvl, sum_surrounding_lvls) - A 2-tuple defining an uncovered tile,
  where:
    - enemy_lvl - Either 0 indicating no enemy is present, or a level from 1-9.
    - sum_surrounding_lvls - The sum of the levels of surrounding enemies.

"""
import logging

from logfmtadapter import StyleAdapter

log = StyleAdapter(logging.getLogger(__name__))


def _is_board_in_initial_state(board):
    """ Return True if no move has yet been made on the given board. """
    for row in board:
        for element in row:
            if element is not None:
                log.debug("Found non-empty board element: {}", element)
                return False

    log.debug("No none-empty board elements found")
    return True


def make_move(game_board):
    """ Make the next move.
    :return: A 2-tuple containing the point to reveal next.
    """
    log.debug("Determining move on board: {}", game_board)

    if _is_board_in_initial_state(game_board):
        log.debug("Board is in initial state - return center point")
        next_point = (len(game_board) / 2, len(game_board[0]) / 2)

    log.debug("Determined next move as: {}", next_point)
    return next_point
