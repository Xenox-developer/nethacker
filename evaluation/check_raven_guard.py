"""Exercise the production escape decision without running a full game.

Run from the solution root: PYTHONPATH=. python evaluation/check_raven_guard.py
"""
from types import SimpleNamespace as NS

import numpy as np

from autoascend.dive_logic import DiveLogic
from autoascend.glyph import MON, SS
from autoascend.level import Level


def escape_action(name, distance, blind=False):
    mon = MON.permonst(MON.from_name(name))
    level = NS(dungeon_number=Level.DUNGEONS_OF_DOOM, key=lambda: (0, 24),
               stair_destination={}, objects=np.full((21, 79), SS.S_room))
    agent = NS(
        current_level=lambda: level, blstats=NS(y=10, x=10, time=100),
        glyphs=np.zeros((21, 79), dtype=np.int16),
        get_visible_monsters=lambda: [(distance, 10, 10 + distance, mon, None)],
        inventory=NS(items=[], engraving_below_me=''),
        character=NS(prop=NS(blind=blind, polymorph=False)),
        can_engrave=lambda: True, _hurt_recently=lambda n: False,
    )
    dive = DiveLogic.__new__(DiveLogic)
    dive.agent = agent
    dive.diving = True
    dive.undiggable = set()
    dive._dig_blocked_until = dive._dig_walk_blocked_until = 0
    dive.digging_tool = lambda: object()
    dive._dig_max_wet = lambda: 0
    dive._medusa_reroll_stairs = lambda wet: None
    dive._in_own_pit = lambda: False
    dive._diggable_spot = lambda *args: False
    dive._dig_walk_target = lambda wet: (11, 10)
    result = dive._dig_escape_action()
    return result[0] if result else None


if __name__ == '__main__':
    cases = [
        ('raven', 2, False, 'scare'),
        ('raven', 3, False, 'step'),
        ('raven', 2, True, 'step'),
        ('cobra', 2, False, 'step'),
        ('killer bee', 2, False, 'step'),
        ('minotaur', 2, False, None),
    ]
    for name, distance, blind, expected in cases:
        actual = escape_action(name, distance, blind)
        assert actual == expected, (name, distance, blind, actual, expected)
    print('6 escape-decision checks passed')
