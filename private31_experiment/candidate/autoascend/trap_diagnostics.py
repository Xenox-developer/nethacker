"""Passive default-off, bounded observations. No policy state writes or RNG use."""
import os
import re
import json
import functools
import weakref
from pathlib import Path
_ENABLED = os.environ.get('PRIVATE31_DIAGNOSTICS') == '1'
_LIMIT = 2000
_count = 0
_seen = weakref.WeakKeyDictionary()
_PATTERN = r'Your foot is trapped!|Your feet are stuck in the |is attached to the buried ball!|bear trap prevents you from pulling your |and cannot pull your '

def emit(stage, **row):
    global _count
    try:
        if not _ENABLED or _count > _LIMIT:
            return
        if _count == _LIMIT:
            stage, row = 'truncated', {'limit': _LIMIT}
        directory = Path(os.environ.get('PRIVATE31_DIAGNOSTICS_DIR', '/tmp/private31-diagnostics'))
        directory.mkdir(parents=True, exist_ok=True)
        with (directory / ('process-%s.jsonl' % os.getpid())).open('a') as f:
            f.write(json.dumps(dict(stage=stage, **row), sort_keys=True) + '\n')
        _count += 1
    except Exception:
        pass

def operation(fn):
    @functools.wraps(fn)
    def wrapped(self, item, *args, **kwargs):
        if not _ENABLED:
            return fn(self, item, *args, **kwargs)
        # Observe the actual prompt response, even if the original method asserts.
        before = self.agent.message
        already_blocked = self.agent.blstats.time < getattr(self, '_trap_armor_until', {}).get(item.object.sub, 0)
        result = None
        try:
            result = fn(self, item, *args, **kwargs)
            return result
        finally:
            try:
                message = self.agent.message
                slot = item.object.sub
                turn = int(self.agent.blstats.time)
                seen = _seen.setdefault(self, {})
                # Suppressed entry has unchanged message and a live policy deadline.
                suppressed = (result is False and already_blocked and before == message and
                              turn < getattr(self, '_trap_armor_until', {}).get(slot, 0))
                if not suppressed and re.search(_PATTERN, message):
                    seen[slot] = turn + 20
                    emit('refusal', operation=fn.__name__, slot=int(slot), turn=turn, expiry=turn+20, message=message[:500])
                elif result is True and slot in seen and turn >= seen[slot] and (
                    'You finish your dressing maneuver.' in message or 'You are now wearing ' in message or
                    'You finish taking off ' in message or 'You were wearing ' in message or
                    'You feel that monsters no longer have difficulty pinpointing your location.' in message):
                    emit('post_expiry_success', operation=fn.__name__, slot=int(slot), turn=turn, expiry=seen.pop(slot))
            except Exception:
                pass
    return wrapped

def slot_check(fn):
    @functools.wraps(fn)
    def wrapped(self, slot):
        result = fn(self, slot)
        if result and _ENABLED:
            try:
                emit('suppressed', slot=int(slot), turn=int(self.agent.blstats.time), expiry=int(self._trap_armor_until[slot]))
            except Exception:
                pass
        return result
    return wrapped

emit('enabled', limit=_LIMIT)
