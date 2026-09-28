"""Opt-in, bounded allocation replay; never queries policy, RNG, or evaluator."""
import atexit
import json
import os
from collections import Counter

_PATH = os.environ.get('TOOL_PRIORITY_OBSERVE')
_LIMIT = 20000
_counts = Counter()
_examples = []


def begin():
    if not _PATH:
        return False
    _counts['policy_visits'] += 1
    return _counts['policy_visits'] <= _LIMIT


def replay(forced, capacity, calls, skip, slots):
    inv = {i: i.count for i in forced}
    bag_inv = {}
    left = capacity - sum(i.weight() for i in forced)
    for index, (item, count, to_bag, bag) in enumerate(calls):
        if index == skip:
            continue
        target = bag_inv if to_bag and bag is not None and item is not bag else inv
        if left < 0 or (target is inv and len(target) >= slots):
            continue
        total = inv.get(item, 0) + bag_inv.get(item, 0)
        prior = target.get(item, 0)
        weight = item.unit_weight(with_content=False)
        extra = item.count if weight <= 0 else int(left // weight)
        if count is not None:
            extra = min(extra, count)
        target[item] = min(item.count, total + extra) - (total - prior)
        left -= weight * (target[item] - prior)
    return inv, bag_inv


def finish(items, forced, capacity, calls, reservation, tool, gate, inv, bag, slots):
    _counts['compared'] += 1
    current = replay(forced, capacity, calls, None, slots)
    if current != (inv, bag):
        _counts['replay_mismatch'] += 1
        return
    old_inv, old_bag = replay(forced, capacity, calls, reservation, slots)
    _counts['retention_gate'] += int(gate)
    _counts['eligible_tool'] += int(tool is not None)
    changes = []
    for item in dict.fromkeys(forced + items):
        old = old_inv.get(item, 0) + old_bag.get(item, 0)
        new = inv.get(item, 0) + bag.get(item, 0)
        if old != new:
            changes.append({'item': item.text or str(item.objs[0].name),
                            'category': item.category, 'weight': item.unit_weight(False),
                            'old': old, 'new': new, 'tool': item is tool})
    changed = bool(changes)
    _counts['changed_allocations'] += changed
    _counts['changed_tool'] += any(c['tool'] for c in changes)
    # Armor category is an item property, never an evaluator signal.
    import nle.nethack as nh
    _counts['changed_armor'] += any(c['category'] == nh.ARMOR_CLASS for c in changes)
    key = 'changed_examples' if changed else 'negative_examples'
    if _counts[key] < (30 if changed else 10):
        _counts[key] += 1
        _examples.append({'capacity': capacity, 'forced_weight': sum(i.weight() for i in forced),
                          'forced_slots': len(forced), 'gate': gate,
                          'eligible_tool': None if tool is None else tool.text or str(tool.objs[0].name),
                          'changed': changed, 'allocations': changes})

    # Persist within the episode too: process termination need not run atexit.
    try:
        flush()
    except (OSError, TypeError, ValueError):
        _counts['write_errors'] += 1


def flush():
    if _PATH:
        os.makedirs(_PATH, exist_ok=True)
        with open(os.path.join(_PATH, f'observation-{os.getpid()}.json'), 'w') as f:
            json.dump({'limit': _LIMIT, 'counts': dict(_counts), 'examples': _examples},
                      f, indent=2, default=lambda value: value.item())


atexit.register(flush)
