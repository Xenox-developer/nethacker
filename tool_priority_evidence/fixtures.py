import importlib.util
import json
import random
from pathlib import Path
from types import SimpleNamespace as NS
import numpy as np
from autoascend import objects as O, tool_priority_observation as obs
from autoascend.global_logic import ItemPriority
from autoascend.item import Item
from autoascend.item.inventory import Inventory
from autoascend.dive_logic import DiveLogic
from autoascend.character import Character

spec = importlib.util.spec_from_file_location('autoascend.parent_global_logic', '/refs/parent/autoascend/global_logic.py')
parent = importlib.util.module_from_spec(spec); spec.loader.exec_module(parent)

def item(name, status=Item.UNCURSED, equipped=False):
    return Item([O.from_name(name)], O.possible_glyphs_from_object(O.from_name(name)), status=status, equipped=equipped, modifier=0, text=name)

sword, pick, mail, shield = [item(n) for n in ['long sword', 'pick-axe', 'splint mail', 'small shield']]

class Items(list):
    pass

def run(name, items, forced, cap, diving=True, offhand=None, change=False):
    agent = NS(blstats=NS(time=1), RESERVE_CORPSE_IDS=set())
    agent.character = NS(role=Character.VALKYRIE, alignment=Character.NEUTRAL,
        get_melee_bonus=lambda i, **kw: (10, 10 if i is sword else 1),
        get_ranged_bonus=lambda *a: (1,1))
    inventory = object.__new__(Inventory); inventory.agent = agent; inventory.items = Items(forced + items); inventory.items.off_hand = offhand
    agent.inventory = inventory
    dive = object.__new__(DiveLogic); dive.agent = agent; dive.diving = diving
    agent.global_logic = NS(dive=dive)
    old = parent.ItemPriority(agent)._split(items, forced, cap)
    state = random.getstate(); npstate = np.random.get_state()
    before = [dict(i.__dict__) for i in items + forced]
    captured = {}
    original_begin, original_finish = obs.begin, obs.finish
    obs.begin = lambda: True
    def capture(its, fs, capacity, calls, reservation, tool, gate, inv, bag, slots):
        assert obs.replay(fs, capacity, calls, None, slots) == (inv, bag)
        oi, ob = obs.replay(fs, capacity, calls, reservation, slots)
        assert [oi.get(i,0) for i in its] == old[None], 'shadow differs from actual parent'
        captured.update(gate=gate, eligible=None if tool is None else tool.text,
                        old=old[None], new=[inv.get(i,0) for i in its])
    obs.finish = capture
    try:
        new = ItemPriority(agent)._split(items, forced, cap)
    finally:
        obs.begin, obs.finish = original_begin, original_finish
    assert (new != old) == change, name
    assert random.getstate() == state
    assert all(np.array_equal(a,b) for a,b in zip(npstate,np.random.get_state()))
    assert before == [dict(i.__dict__) for i in items + forced]
    return dict(name=name, capacity=cap, items=[i.text for i in items], passed=True, **captured)

rows = []
rows.append(run('tight_weight', [sword,pick,mail,shield], [], 500, change=True))
assert rows[-1]['old'][1] == 0 and rows[-1]['new'][1] == 1
rows.append(run('generous', [sword,pick,mail,shield], [], 1000))
rows.append(run('no_tool', [sword,mail,shield], [], 500))
rows.append(run('non_diving', [sword,pick,mail,shield], [], 500, diving=False))
cursed = item('splint mail', Item.CURSED, True)
rows.append(run('forced_cursed_armor', [sword,pick,shield], [cursed], 500))
rows.append(run('forced_overweight', [sword,pick,shield], [cursed], 300))
rows.append(run('forced_tool_not_double_charged', [sword,pick,mail,shield], [pick], 600))
forced_slots = [item('leather gloves', Item.CURSED, True) for _ in range(49)]
rows.append(run('tight_slots', [sword,pick,mail], forced_slots, 5000, change=True))
cursed_shield = item('small shield', Item.CURSED, True)
mattock = item('dwarvish mattock')
rows.append(run('cursed_shield_mattock_ineligible', [sword,mattock,mail], [cursed_shield], 500, offhand=cursed_shield))
assert rows[-1]['eligible'] is None
print(json.dumps(rows, indent=2))
# Live blstats/capacity often use NumPy scalars; exercise the real diagnostic writer.
import tempfile
with tempfile.TemporaryDirectory() as directory:
    obs._PATH = directory
    obs.finish([pick], [], np.int64(100), [(pick,None,False,None)], 0,
               pick, True, {pick:1}, {}, 51)
    saved = json.loads(next(Path(directory).glob('*.json')).read_text())
    assert saved['counts']['changed_tool'] == 1
    assert saved['examples'][-1]['capacity'] == 100
    assert saved['counts'].get('write_errors',0) == 0
    obs._PATH = None
