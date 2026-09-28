# Skip blind inspection after engraving

The only strategy change is in `autoascend/agent.py`, `Agent.engrave`.
After writing, a blind character now clears the cached engraving instead of
calling `get_items_below_me()`. Sighted inspection is unchanged. No inscription
is assumed successful, and existing retry limits and digging policy remain.

Hypothesis: eliminate a wasted vulnerable turn before the next digging action
or protective retry. NetHack 3.6.6 `invent.c:look_here` returns `!!Blind`, so
manual blind inspection consumes a turn. Dust cannot be read by touch. The
parent's seed-2 trace showed repeated blind engraving immediately before death.

Peer reference inspected:
`github.com/kefirski/nethacker@454ae8df96e7ec68f0df2488b2b8a90368407cf1`,
`autoascend/dive_logic.py`, especially its explanation of raven blindness and
interrupted digging. This source is already recorded in the solution manifest.
No peer code was copied for this change.

## Results

All commands used `python -m nethackers.arena.run`, identity
`val-dwa-law-fem`, and `--evaluation-id local`, running each batch in the
foreground to completion. The final implementation was evaluated in batches
`[2,3,4,13]`, `[0,1,6,7,8,11]`, and `[5,9,10,12,14]`.

| Comparison | Mean progression |
| --- | ---: |
| Supplied parent, seeds 0–14 | 0.4873887508 |
| Final implementation, seeds 0–14 | 0.4905618602 |

All 15 completed without evaluation errors. Relative to the supplied parent,
seed 3 improved from depth 26 to 27; fourteen scores tied. Raw final results:
`evaluation/blind-look-local.json`.

**The score improvement is not established as causal.** A fresh unchanged-parent
seed-3 control also reached depth 27 with the same endpoint as the candidate.
That control is retained in `evaluation/blind-look-parent-control.json`.
The mechanism removes an unnecessary action, but these runs do not demonstrate
a reliable progression advantage over a freshly evaluated parent.

Compilation and entrypoint import passed. Direct method checks verified that
sighted engraving still inspects the floor, blind engraving skips inspection
and invalidates the engraving cache, and becoming blind during writing also
skips inspection. Missing floor-item caches receive the existing empty fallback.

Exploratory changes were reverted: blindness treatment using carried cures
tied four games exactly; suppressing all blind floor inspection during dives
added runtime without additional score gains. Neither is in the final code.
