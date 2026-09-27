"""Run in the pinned arena image after installing into an isolated workspace.

Exercises actual NLE glyphs/species and the real adapter without starting a game.
"""

import argparse
import ast
import sys
from contextlib import nullcontext
from unittest.mock import patch
from pathlib import Path
from types import SimpleNamespace as NS


def verify(solution):
    sys.path.insert(0, str(solution))
    import numpy as np
    from autoascend import jf_config
    from autoascend.combat import lookahead_adapter as adapter
    from autoascend.glyph import SS, G
    from autoascend.stats_logger import StatsLogger
    from autoascend.agent import Agent
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
    logger = StatsLogger()
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
        stats_logger=logger,
    )
    actions = [(10.0, ("move", -1, 0)), (9.0, ("move", 0, 1))]
    selected = adapter.select_action(agent, actions, actions[0])
    assert selected is actions[1], (
        selected, getattr(agent, "_lookahead_last_decision", None), logger._values)
    decision = agent._lookahead_last_decision
    assert all(root.depth_reached == 3 for root in decision.roots)
    assert logger._values["lookahead_override"] == 1
    # Drive the real fight2 strategy through selection and action execution.
    agent._last_turn, agent._allow_attack_all_turn = 100, -100
    agent.bfs = lambda: np.ones(shape, dtype=int)
    agent.character.parse_enhance_view = lambda: None
    agent.env = NS(debug_tiles=lambda *a, **kw: nullcontext(),
                   debug_log=lambda *a, **kw: nullcontext())
    performed = []
    def perform(action, wait):
        performed.append(action)
        raise StopFixture
    class StopFixture(Exception):
        pass
    agent._fight2_perform_action = perform
    with patch("autoascend.combat.fight_heur.get_priorities", return_value=(np.zeros(shape), actions.copy())), \
         patch("autoascend.combat.fight_heur.get_move_actions", return_value=[]), \
         patch("autoascend.combat.utils.action_str", return_value="fixture"):
        strategy = Agent.fight2.__wrapped__(agent)
        try:
            strategy.run()
        except StopFixture:
            pass
    assert performed == [actions[1][1]], performed
    assert adapter.select_action(agent, actions, actions[0], force_attack=True) is actions[0]
    urgent = (50, ("elbereth",))
    assert adapter.select_action(agent, [*actions, urgent], urgent) is urgent
    agent.blstats.prop_mask = 1
    assert adapter.select_action(agent, actions, actions[0]) is actions[0]
    agent.blstats.prop_mask = 0
    agent.inventory.get_best_melee_weapon = lambda: object()
    assert adapter.select_action(agent, actions, actions[0]) is actions[0]
    agent.inventory.get_best_melee_weapon = lambda: weapon
    original_monsters = agent.get_visible_monsters
    eye_id = next(i for i in range(nh.NUMMONS) if nh.permonst(i).mname == "floating eye")
    agent.get_visible_monsters = lambda: [(1, 6, 5, nh.permonst(eye_id), nh.GLYPH_MON_OFF + eye_id)]
    assert adapter.select_action(agent, actions, actions[0]) is actions[0]
    agent.get_visible_monsters = original_monsters
    # Real glyph masks exclude doors, traps, pets, boulders, unknown squares,
    # peaceful occupants and dangerous corpses; no diagonal corner squeezing.
    for glyph in (SS.S_vodoor, SS.S_pit):
        level.objects[5, 6] = glyph
        assert (5, 6) not in adapter._terrain(agent).cells
    level.objects[5, 6] = SS.S_room
    for glyph in (nh.GLYPH_PET_OFF + monster_id, next(iter(G.BOULDER))):
        glyphs[5, 6] = glyph
        assert (5, 6) not in adapter._terrain(agent).cells
    glyphs[5, 6] = SS.S_room
    agent.monster_tracker.peaceful_monster_mask[5, 6] = True
    assert (5, 6) not in adapter._terrain(agent).cells
    agent.monster_tracker.peaceful_monster_mask[5, 6] = False
    level.objects[5, 6] = -1
    assert (5, 6) not in adapter._terrain(agent).cells
    level.objects[5, 6] = SS.S_room
    agent.inventory.items.gloves = None
    level.petrify_until[5, 6] = 101
    assert (5, 6) not in adapter._terrain(agent).cells
    assert not adapter._terrain(agent).allows((4, 5), (5, 6))
    # Unsupported observation logging also uses the production registry.
    agent.get_visible_monsters = lambda: None
    assert adapter.select_action(agent, actions, actions[0]) is actions[0]
    assert logger._values["lookahead_unsupported"] == 1
    print(f"Real NLE adapter integration passed: {decision.reason}; nodes={decision.nodes}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("solution", type=Path)
    verify(parser.parse_args().solution.resolve())
