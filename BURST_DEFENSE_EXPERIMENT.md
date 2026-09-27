# Damage-aware Elbereth defense

Hypothesis: observed rapid HP loss should override the assumption that a lone
low-level monster is safe to fight. The existing three-turn damage detector
already triggers at a loss of 30% of maximum HP, but `elbereth_rest` then
unconditionally rejects a species of level <= 2 while the hero has >= 6 HP.
The change exempts the rapid-loss case from that rejection. All other rest,
engraving, immunity, and emergency checks remain unchanged.

Observed parent failure: on local seed 4, a dagger-wielding goblin reduced HP
from 18/20 to 11/20. The hero fought again, fell to 5/20, and subsequently died
while retrying a smudged Elbereth. A diagnostic copy of the unmodified parent
reproduced the reference endpoint exactly: 1,649 turns, depth 1, score
0.0184784046. The diagnostic wrapper was outside the submitted solution.

Reviewed source: `github.com/kefirski/nethacker@995d8f40b2d24ee09487b0e87e014ca2fcc10928`,
`autoascend/dive_logic.py`, especially the rapid-loss trigger and weak-monster
exception. This peer is already recorded in the solution manifest. The final
change is an original one-condition correction; existing license is retained.

## Local validation

Run with `python -m nethackers.arena.run --solution /workspace --batch ...
--evaluation-id local --out ...`, in two foreground batches:

- `[2, 4, 8, 9]`, all `val-dwa-law-fem`.
- `[0, 3, 5, 13]`, all `val-dwa-law-fem`.

Per-seed candidate results are in `burst-defense-eval.json`; parent comparison
uses `/refs/parent-eval.json` on the same eight seeds.

| Seed | Parent | Candidate |
| --- | ---: | ---: |
| 0 | 0.425836 | 0.425836 |
| 2 | 0.050758 | 0.050758 |
| 3 | 0.506761 | 0.506761 |
| 4 | 0.018478 | 0.466376 |
| 5 | 0.646505 | 0.646505 |
| 8 | 0.601565 | 0.601565 |
| 9 | 0.554357 | 0.554357 |
| 13 | 0.425836 | 0.425836 |
| Mean | 0.403762 | 0.459749 |

Seed 4 reached depth 25 rather than depth 1. Seven other scores tied; some
trajectories changed. This is an eight-seed result, not a measured full-15 or
held-out improvement.

Direct checks of the actual strategy passed for rapid damage, stable HP,
critical HP, and Elbereth-immune threats. `bot.make_agent` imports cleanly.
`bot.py`, `arena_adapter.py`, and all configuration defaults match the parent.

## Discarded exploration

All these experimental edits were reverted before the final change:

- Continuing emergency digs: eight sampled score ties.
- Requiring 50 HP before fighting a trivial monster while fainting: four ties.
- Continuous protective/healing holds, including narrower descent, hunger,
  and critical-HP variants: seed 2 improved, but seed 8 regressed substantially;
  fresh parent controls confirmed the regression.
- Hard filtering visible floating-eye melee: seed 13 gained, seed 8 lost,
  and seed 9 regressed sharply in the wider sample.
- Preserving `go_to`'s target during replanning: seed 2 gained, seed 9 regressed.

An independent repeat of candidate seed 4 reproduced score 0.4663763157,
23,690 turns, and depth 25; see `burst-defense-repeat.json`.
