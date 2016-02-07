"""
Solver for sweeper games.

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
import random

from ..point import Point


log = logging.getLogger(__name__)


def make_move(player, game_board):
    """ Make the next move.
    :return: The point to reveal next.
    """
    log.debug("Determining move for player: %s board:\n%s", player, game_board)

    # Handle the case where this is the first move.
    if game_board.in_start_state():
        log.info("Board is in initial state - return center point")
        next_point = Point(game_board.width // 2, game_board.height // 2)
        log.info("Determined starting move as: %s", next_point)
        return next_point

    # This isn't the first move - find a tile with an enemy of the given level
    # or lower if possible.
    safe_move = next(game_board.iter_unrevealed_below_level(player.level),
                     None)
    if safe_move is not None:
        log.info("There exists a safe move - find the best one")
        # The best move is one where we attack the highest level enemy.
        best_move = max(game_board.iter_unrevealed_below_level(player.level),
                        key=score_safe_move)
        log.info("Determined next move as: %s", best_move.location)
        return best_move.location

    # There are no safe moves - pick a move we at least know we can survive.
    survivable_level = player.highest_survivable_enemy
    survivable_move = \
        next(game_board.iter_unrevealed_below_level(survivable_level), None)
    if survivable_move is not None:
        log.info("There exists a survivable move - find the best")
        # The best move is one where we attack the lowest level enemy.
        best_move = \
            min(game_board.iter_unrevealed_below_level(survivable_level),
                key=score_survivable_move)
        log.info("Determined next move as: %s", best_move.location)
        return best_move.location

    # There's no known move we can survive. Pick a random one from all those
    # which are at least not certain to kill us.
    log.info("Forced to pick random non-guaranteed-death move")
    random_move = \
        random.choice(list(space
                           for space in game_board.iter_unrevealed_spaces()
                           if space.tile.enemy_lvl.min <= survivable_level))
    log.info("Determined next move as: %s", random_move.location)
    return random_move.location


def score_safe_move(space):
    """ Assign a score to a safe move, where the highest score is best.
        The best move is one where we attack the highest level enemy.
    """
    return space.tile.enemy_lvl.max + space.tile.enemy_lvl.min


def score_survivable_move(space):
    """ Assign a score to a survivable move, where the lowest score is safest.
        The safest move is one with the lowest possible maximum level, and
        of those with the lowest max, the one with the greatest possible
        level range.
    """
    return (space.tile.enemy_lvl.max -
            ((space.tile.enemy_lvl.max - space.tile.enemy_lvl.min) /
             (space.tile.enemy_lvl.max + 1)))
