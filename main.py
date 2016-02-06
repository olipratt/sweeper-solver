"""
Run the solver with a user interface.
"""
import sys
import logging

from interactive import run_interactive


log = logging.getLogger(__name__)


if __name__ == "__main__":
    if sys.argv[1] == "-i":
        run_interactive()
