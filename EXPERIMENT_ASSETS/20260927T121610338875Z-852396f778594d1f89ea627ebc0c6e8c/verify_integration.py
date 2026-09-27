"""Run in the pinned arena image after installing into an isolated workspace.

Exercises actual NLE glyphs/species and the real adapter without starting a game.
"""

import argparse
import ast
import sys
from pathlib import Path
from types import SimpleNamespace as NS


def verify(solution):
    sys.path.insert(0, str(solution))
    import numpy as np
    from autoascend import jf_config
    from autoascend.combat import lookahead_adapter as adapter
    from autoascend.glyph import SS
    from bot import make_agent
    from nle import nethack as nh

    assert callable(make_agent) and jf_config.TACTICAL_LOOKAHEAD
    source = ast.parse((solution / "autoascend/agent.py").read_text())
    fight = next(n for n in ast.walk(source)
                 if isinstance(n, ast.FunctionDef) and n.name == "fight2")
    assert any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
               and n.func.id == "select_action" for n in ast.walk(fight))
    cells = {(4, 5), (5, 5), (6, 5), (5, 6), (5, 7), (5, 8)}
    shape = (21, 79)
    walkable = np.zeros(shape, dtype=bool)
    objects = np.full(shape, -1, dtype=np.int16)
    glyphs = np.full(shape, SS.S_stone, dtype=np.int16)
    for pos in cells:
        walkable[pos] = True
        objects[pos] = SS.S_room
        glyphs[pos] = objects[pos]
    monster_id = next(i for i in range(nh.NUMMONS) if nh.permonst(i).mname == "jackal")
    monster = nh.permonst(monster_id)
    glyphs[6, 5] = nh.GLYPH_MON_OFF + monster_id
    empty = np.zeros(shape, dtype=bool)
    level = NS(walkable=walkable, seen=walkable.copy(), objects=objects,
               forbidden=empty.copy(), intact_doors=empty.copy(),
               petrify_until=np.zeros(shape, dtype=np.int32))
    weapon = object()
    events = []
    agent = NS(
        blstats=NS(y=5, x=5, hitpoints=3, max_hitpoints=30, time=100,
                   prop_mask=0, carrying_capacity=0, hunger_state=0,
                   armor_class=10, dungeon_number=0, level_number=5),
        glyphs=glyphs,
        current_level=lambda: level,
        monster_tracker=NS(peaceful_monster_mask=empty.copy()),
        global_logic=NS(dive=NS(diving=True)),
        character=NS(prop=NS(polymorph=False), get_melee_bonus=lambda *a, **kw: (20, 1)),
        inventory=NS(items=NS(main_hand=weapon, gloves=object()),
                     get_best_melee_weapon=lambda: weapon, engraving_below_me=""),
        get_visible_monsters=lambda: [(1, 6, 5, monster, int(glyphs[6, 5]))],
        stats_logger=NS(log_event=events.append),
    )
    actions = [(10.0, ("move", -1, 0)), (9.0, ("move", 0, 1))]
    selected = adapter.select_action(agent, actions, actions[0])
    assert selected is actions[1], (
        selected, getattr(agent, "_lookahead_last_decision", None), events)
    decision = agent._lookahead_last_decision
    assert all(root.depth_reached == 3 for root in decision.roots)
    assert "lookahead_override" in events
    assert adapter.select_action(agent, actions, actions[0], force_attack=True) is actions[0]
    urgent = (50, ("elbereth",))
    assert adapter.select_action(agent, [*actions, urgent], urgent) is urgent
    agent.blstats.prop_mask = 1
    assert adapter.select_action(agent, actions, actions[0]) is actions[0]
    print(f"Real NLE adapter integration passed: {decision.reason}; nodes={decision.nodes}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solution", type=Path)
    verify(parser.parse_args().solution.resolve())
