"""Conservative AutoAscend adapter; install as combat/lookahead_adapter.py.

The arena exposes observations, not a clonable game state. Species attributes
are public facts; individual monster HP, hit chances and movement energy are
unknown. This adapter deliberately supports a small physical-combat subset.
"""

from collections import deque
from math import isfinite

from .lookahead import Action, Config, Monster, State, Topology, choose_action

# Mean damage dice for ordinary physical attackers (NetHack monst.c).
# These are unmodified species attacks, not a prediction of an actual hit.
PHYSICAL_DAMAGE = {
    "newt": 1.5, "jackal": 1.5, "fox": 2.0, "coyote": 2.5,
    "sewer rat": 2.0, "giant rat": 2.0,
    "little dog": 3.5, "kitten": 3.5, "dog": 3.5, "housecat": 3.5,
    "giant ant": 2.5, "rothe": 8.5,
}


def _terrain(agent, radius=5):
    from .. import utils
    from ..glyph import G

    level = agent.current_level()
    objects, glyphs = level.objects, agent.glyphs
    # Model only known, ordinary floor. Doors are omitted entirely: opening,
    # kicking and squeezing are additional actions this model does not cover.
    safe = (level.walkable & level.seen & (objects != -1)
            & ~level.forbidden & ~level.intact_doors
            & ~agent.monster_tracker.peaceful_monster_mask
            & ~utils.isin(glyphs, G.BOULDER, G.PETS)
            & ~utils.isin(objects, G.DOORS, G.TRAPS))
    if agent.inventory.items.gloves is None:
        safe &= level.petrify_until <= agent.blstats.time
    cy, cx = int(agent.blstats.y), int(agent.blstats.x)
    height, width = safe.shape
    cells = frozenset((y, x)
                      for y in range(max(0, cy-radius), min(height, cy+radius+1))
                      for x in range(max(0, cx-radius), min(width, cx+radius+1))
                      if safe[y, x])
    diagonals = frozenset(((y, x), (y+dy, x+dx))
                         for y, x in cells for dy in (-1, 1) for dx in (-1, 1)
                         if (y+dy, x+dx) in cells
                         and (y+dy, x) in cells and (y, x+dx) in cells)
    return Topology(cells, diagonals)


def select_action(agent, actions, selected, *, force_attack=False):
    """Return one original (priority, action) pair, or leave selection unchanged.

    The caller must first apply all existing emergency/forced-action filters.
    A model-based veto is only considered during the dive at reduced HP.
    """
    if force_attack or selected[1][0] not in ("move", "melee"):
        return selected
    try:
        return _select(agent, actions, selected)
    except (AttributeError, KeyError, IndexError, TypeError, ValueError, OverflowError):
        # Unsupported observations must not make a formerly valid bot crash.
        # AssertionError and programmer errors are intentionally not swallowed.
        agent.stats_logger.log_event("lookahead_unsupported")
        return selected


def _select(agent, actions, selected):
    bl = agent.blstats
    if not agent.global_logic.dive.diving:
        return selected
    if (bl.prop_mask or bl.carrying_capacity or bl.hunger_state >= 2
            or agent.character.prop.polymorph
            or bl.hitpoints <= 0 or bl.hitpoints > max(20, bl.max_hitpoints * .5)):
        return selected
    if agent.inventory.engraving_below_me.lower() == "elbereth":
        return selected
    # The existing melee handler may wield first. Never pretend that such an
    # action immediately damages an enemy, and do not model unarmed combat.
    weapon = agent.inventory.items.main_hand
    if weapon is None or weapon != agent.inventory.get_best_melee_weapon():
        return selected
    observed = agent.get_visible_monsters()
    if not 1 <= len(observed) <= 3:
        return selected
    py, px = int(bl.y), int(bl.x)
    if min(max(abs(int(y)-py), abs(int(x)-px)) for _, y, x, _, _ in observed) > 2:
        return selected
    if any(mon.mname not in PHYSICAL_DAMAGE for _, _, _, mon, _ in observed):
        return selected
    topology = _terrain(agent)
    if (py, px) not in topology.cells:
        return selected
    monsters = []
    for _, y, x, mon, _ in observed:
        pos = (int(y), int(x))
        if pos not in topology.cells or not 0 < mon.mmove <= 24:
            return selected
        # Do not use hidden individual HP or assume a wounded enemy will die.
        estimated_hp = max(8, 8 * (int(mon.mlevel) + 2))
        # AC affects only a bounded heuristic expectation; the planner also
        # evaluates a pessimistic damage/timing scenario.
        hit_chance = min(.95, max(.25, (10 + int(mon.mlevel) + int(bl.armor_class)) / 20))
        monsters.append(Monster(f"{y}:{x}", pos, estimated_hp,
                                PHYSICAL_DAMAGE[mon.mname] * hit_chance,
                                float(mon.mmove)))
    # A single damage value serves every modeled enemy. Use the lower estimate
    # for small/large targets rather than pretend that all use the small dice.
    enemy_ac = min(m.ac for _, _, _, m, _ in observed)
    damage = min(float(damage) * min(.95, max(.1, (float(to_hit) + enemy_ac) / 20))
                 for to_hit, damage in
                 (agent.character.get_melee_bonus(weapon, large_monster=large)
                  for large in (False, True)))
    if not isfinite(damage) or damage <= 0:
        return selected
    # The original move generator repeats NW. Keep one modeled action for
    # each command, retaining the selected pair's index if it is a duplicate.
    selected_key = next((i for i, pair in enumerate(actions) if pair is selected), None)
    if selected_key is None:
        selected_key = next((i for i, pair in enumerate(actions) if pair == selected), None)
    candidates_by_command = {}
    occupied = {monster.pos for monster in monsters}
    for index, pair in enumerate(actions):
        action = pair[1]
        if action[0] not in ("move", "melee") or len(action) != 3:
            continue
        target = (py + int(action[1]), px + int(action[2]))
        if (not topology.allows((py, px), target)
                or ((target in occupied) != (action[0] == "melee"))):
            continue
        command = (action[0], target)
        if command not in candidates_by_command or index == selected_key:
            candidates_by_command[command] = Action(index, action[0], target)
    candidates = tuple(candidates_by_command.values())
    if selected_key not in {action.key for action in candidates} or len(candidates) < 2:
        return selected
    level_key = (int(bl.dungeon_number), int(bl.level_number))
    memory = getattr(agent, "_lookahead_memory", None)
    if memory is None or memory[0] != level_key or int(bl.time) - memory[1] > 3:
        history = deque(maxlen=6)
    else:
        history = memory[2]
    if memory is None or memory[1] != int(bl.time) or not history or history[-1] != (py, px):
        history.append((py, px))
    agent._lookahead_memory = (level_key, int(bl.time), history)
    state = State(topology, (py, px), float(bl.hitpoints), damage,
                  tuple(monsters), speed=12, recent_positions=tuple(history))
    decision = choose_action(state, candidates, selected_key, Config(depth=3))
    agent._lookahead_last_decision = decision
    agent.stats_logger.log_event("lookahead_plan")
    if decision.override_key is None:
        return selected
    agent.stats_logger.log_event("lookahead_override")
    return actions[decision.override_key]
