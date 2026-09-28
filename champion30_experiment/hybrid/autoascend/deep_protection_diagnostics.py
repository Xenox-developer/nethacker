"""Opt-in passive helper observations; no RNG, evaluator data or policy writes.

One bounded JSONL stream per sandbox process. The filename is only a process
identifier, not a game identifier. `engraving_call` records entry at the actual
call site, not successful text completion or lasting protection.
"""
import json
import os
from pathlib import Path

_ENABLED = os.environ.get('CHAMPION30_DIAGNOSTICS') == '1'
_LIMIT = 20000
_count = 0
_path = None

def _write(row):
    global _count, _path
    try:
        if not _ENABLED or _count > _LIMIT:
            return
        if _path is None:
            directory = Path(os.environ.get('CHAMPION30_DIAGNOSTICS_DIR', '/tmp/champion30-diagnostics'))
            directory.mkdir(parents=True, exist_ok=True)
            _path = directory / ('process-%s.jsonl' % os.getpid())
        if _count == _LIMIT:
            row = {'stage': 'truncated', 'limit': _LIMIT}
        with _path.open('a') as f:
            f.write(json.dumps(row, sort_keys=True) + '\n')
        _count += 1
    except Exception:
        # Diagnostic failures cannot prevent or change the helper action.
        pass

def observe(stage, state):
    if not _ENABLED:
        return
    try:
        self = state['self']
        agent = self.agent
        bl = agent.blstats
        row = dict(stage=stage, turn=int(bl.time), depth=int(bl.depth))
        if 'near' in state and 'rewrite' in state:
            from .glyph import Hunger
            from . import dive_logic
            original = bool(state['near'] or dive_logic.ELBERETH_ALWAYS or
                            (self.medusa_level is not None and state['spot'][0] == self.medusa_level) or
                            bl.hunger_state >= Hunger.WEAK or state['rewrite'])
            row['depth_alone'] = bool(bl.depth >= 20 and not original)
        if stage == 'engraving_call':
            monsters = agent.get_visible_monsters()
            row['visible_immune'] = any(self._melee_ignores_elbereth(m[3]) for m in monsters)
            row['immune_names'] = sorted({m[3].mname for m in monsters if self._melee_ignores_elbereth(m[3])})
        _write(row)
    except Exception:
        _write({'stage': 'observation_error', 'at': stage})

_write({'stage': 'enabled', 'limit': _LIMIT})
