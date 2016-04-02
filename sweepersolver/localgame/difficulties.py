"""
Define some standard game difficulties that set game parameters.
"""
import logging
from collections import Counter

log = logging.getLogger(__name__)


WIDTH_EASY = 16
HEIGHT_EASY = 16
HP_EASY = 10
ENEMIES_EASY = Counter({0: 226, 1: 10, 2: 8, 3: 6, 4: 4, 5: 2})
XP_THRESHOLDS_EASY = {1: 0,
                      2: 10,
                      3: 20,
                      4: 40,
                      5: 82,
                      6: 100000}

WIDTH_HUGE_EX = 50
HEIGHT_HUGE_EX = 25
HP_HUGE_EX = 20
ENEMIES_HUGE_EX = Counter({0: 926,
                           1: 36,
                           2: 36,
                           3: 36,
                           4: 36,
                           5: 36,
                           6: 36,
                           7: 36,
                           8: 36,
                           9: 36})
XP_THRESHOLDS_HUGE_EX = {1: 0,
                         2: 2,
                         3: 10,
                         4: 150,
                         5: 540,
                         6: 1116,
                         7: 2268,
                         8: 4572,
                         9: 9180,
                         10: 100000}

DIFFICULTY_EASY = {"width": WIDTH_EASY,
                   "height": HEIGHT_EASY,
                   "hp": HP_EASY,
                   "enemies": ENEMIES_EASY,
                   "xp thresholds": XP_THRESHOLDS_EASY}
DIFFICULTY_HUGE_EX = {"width": WIDTH_HUGE_EX,
                      "height": HEIGHT_HUGE_EX,
                      "hp": HP_HUGE_EX,
                      "enemies": ENEMIES_HUGE_EX,
                      "xp thresholds": XP_THRESHOLDS_HUGE_EX}
