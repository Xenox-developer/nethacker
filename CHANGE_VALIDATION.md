# Blind Elbereth retries

The only retained strategy change is in `autoascend/agent.py`: when blind and
retrying Elbereth, answer yes to the engraving append prompt. Preserve existing
letters because blindness prevents verifying whether the previous inscription
already works. Sighted engraving and other text retain their old behavior.

Reference review: `/refs/peers/SOURCES.md`, the pinned peer2 `power.py` scroll
protection mechanism, and the existing blind engraving logic in `dive_logic.py`.
No peer code was copied. Scroll preservation and earlier minotaur emergency-item
use were tested without score improvements and reverted completely.

All games used `python -m nethackers.arena.run`, identity `val-dwa-law-fem`, and
`--evaluation-id local`, in sequential foreground batches of two to four games.

Latest results for the seven distinct tested seeds:

| Seed | Parent progress | Candidate progress |
| --- | --- | --- |
| 1 | 0.161268 | 0.161268 |
| 2 | 0.445181 | 0.445181 |
| 3 | 0.506761 | 0.506761 |
| 6 | 0.466376 | 0.554357 |
| 7 | 0.466376 | 0.466376 |
| 13 | 0.466376 | 0.466376 |
| 14 | 0.506761 | 0.506761 |

Matched sample mean: **0.431300 -> 0.443869**. This is a seven-seed sample,
not a new full-15 mean. Seed 6 reached depth 27 in both candidate runs; a fresh
parent control reproduced depth 25. Seed 14 initially reached depth 27 but
returned to depth 26 in both repeat runs; its initial gain is not counted above.
No episode errors were reported.

Results: `/tmp/eval-engrave.json`, `/tmp/eval-engrave-validation.json`,
`/tmp/eval-parent-control.json`, `/tmp/eval-engrave-repeat.json`.

Import/compile checks passed. A direct engraving-generator check verified the
append response for blind Elbereth, the replace response for sighted Elbereth,
and unchanged replacement for unrelated text while blind. The agent contract
and adapter are unchanged.
