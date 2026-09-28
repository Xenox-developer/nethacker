"""Optional action-neutral activation evidence; no-op outside campaign evals.

Call hit('A.considered') at a gate and hit('A.applied') only when behavior
changes. Counts are checkpointed at powers of two to bound diagnostic I/O.
Without an explicit flush() at normal shutdown they are LOWER BOUNDS, not exact
totals. Never use these counts or the environment setting to choose actions.
"""
import json
import os
from pathlib import Path

_directory = os.environ.get("NETHACKERS_CAMPAIGN_EVENTS_DIR")
_counts = {}
_writes = 0
_MAX_NAMES = 32
_MAX_WRITES = 512


def flush(*, exact=False):
    global _writes
    if not _directory or _writes >= _MAX_WRITES:
        return
    try:
        directory = Path(_directory)
        directory.mkdir(parents=True, exist_ok=True)
        destination = directory / f"events-{os.getpid()}.json"
        temporary = destination.with_suffix(".tmp")
        temporary.write_text(json.dumps({
            "pid": os.getpid(), "counts": _counts,
            "counts_are_lower_bounds": not exact, "writes": _writes + 1,
        }, sort_keys=True))
        os.replace(temporary, destination)
        _writes += 1
    except OSError:
        pass  # Diagnostics must never alter action selection or crash the bot.


def hit(name):
    if not _directory or not isinstance(name, str) or len(name) > 80:
        return
    if name not in _counts and len(_counts) >= _MAX_NAMES:
        return
    count = _counts[name] = _counts.get(name, 0) + 1
    if count & (count - 1) == 0:
        flush()
