"""
Solver for mamono sweeper.

The main API function is 'next_move' - this returns the next location to
reveal.

The game board is simply represented as a 2d array of locations. Each location
is either:
- None, indicating that the location is still hidden.
- (enemy_lvl, sum_surrounding_lvls) - A 2-tuple defining an uncovered tile,
  where:
    - enemy_lvl - Either 0 indicating no enemy is present, or a level from 1-9.
    - sum_surrounding_lvls - The sum of the levels of surrounding enemies.

"""
import logging

from ..point import Point


log = logging.getLogger(__name__)


def make_move(level, game_board):
    """ Make the next move.
    :return: The point to reveal next.
    """
    log.debug("Determining move at level: %r on board:\n%s", level, game_board)
    assert level > 0, "Negative or zero level is invalid"

    # Handle the case where this is the first move.
    if game_board.in_start_state():
        log.debug("Board is in initial state - return center point: %r", level)
        next_point = Point(game_board.width // 2, game_board.height // 2)
        log.debug("Determined starting move as: %r", next_point)
        return next_point

    # This isn't the first move - find a tile with an enemy of the given level
    # or lower.
    target_space = next(game_board.iter_unrevealed_below_level(level), None)
    if target_space is not None:
        next_point = target_space.location
        log.debug("Determined next move as: %r", next_point)
        return next_point

    log.error("Failed to determine next move")
    raise Exception("Failed to determine next move")