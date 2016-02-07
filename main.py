"""
Run the solver in the requested mode.
"""
import logging
import argparse

from interactive import run_interactive
from automated import run_automated
from sweepersolver import DIFFICULTY_EASY, DIFFICULTY_HUGE_EX


log = logging.getLogger(__name__)


# Mapping of user facing difficulty names to internal difficulties.
DIFFICULTY_MAP = {"easy": DIFFICULTY_EASY,
                  "huge-extreme": DIFFICULTY_HUGE_EX}


def _set_up_arg_parser():
    """ Create a parser for the allowed command line arguments. """
    parser = argparse.ArgumentParser("Run the sweeper solver.")
    main_group = parser.add_mutually_exclusive_group(required=True)
    main_group.add_argument('-i',
                            dest="interactive",
                            action="store_true",
                            help="Run interactively")
    main_group.add_argument('-a',
                            dest="automated",
                            action="store_true",
                            help="Run automated")
    parser.add_argument('-d',
                        dest="difficulty",
                        type=str,
                        choices=DIFFICULTY_MAP.keys(),
                        default=DIFFICULTY_EASY,
                        help="Select difficulty")
    parser.add_argument('-p',
                        dest="pause",
                        type=float,
                        default=0,
                        help="Time to pause between moves")
    return parser


if __name__ == "__main__":
    parser = _set_up_arg_parser()
    args = parser.parse_args()

    if args.interactive:
        run_interactive()
    if args.automated:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)-15s %(message)s')
        run_automated(DIFFICULTY_MAP[args.difficulty], args.pause)
