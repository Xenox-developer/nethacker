# Protected recovery before digging

One focused strategy change: when an intact, readable Elbereth is already
protecting the bot before it digs, recover toward 90% HP instead of 60%, with
a 300-turn per-square budget instead of 100. Existing hunger, damage, ranged
attack, blindness, polymorph, Gehennom, and immune-monster guards remain.
Digging removes shelter; the extra HP buffer helps survive the next exposure.
Only `autoascend/dive_logic.py` changes gameplay. The hypothesis is marked
there. Adapter, entrypoint, and all configuration defaults match the parent.

Read pinned peers listed in `/refs/peers/SOURCES.md`, including peer2's combat,
prayer threat model, and digging/engraving behavior. The final change adjusts
the inherited recovery mechanism, with no copied peer code or new dependency.
The peer2 source is already credited in the solution manifest.

## Evaluation

All runs used the prescribed arena runner, identity `val-dwa-law-fem`, and
`--evaluation-id local`, as foreground commands with batches of 2–4 seeds.
Final full coverage: [1,2,5,6], [0,3,8,12], [4,7,9,10], [11,13,14].

Supplied parent mean: **0.4919489210**.
Candidate mean: **0.4960541980** (+0.0041052770, about 0.83% relative).
Three gains, two losses, ten ties; all episodes completed without errors.

| Seed | Parent depth | Candidate depth |
| --- | ---: | ---: |
| 2 | 24 | 25 |
| 3 | 27 | 26 |
| 5 | 25 | 27 |
| 9 | 27 | 26 |
| 14 | 26 | 27 |

Raw full results: `recovery-eval.json`.
Fresh unchanged-parent controls on [2,5,9] reproduced all three stored parent
scores (`recovery-parent-control.json`). Candidate repeats of [2,5] reproduced
both gains, including exact turns and scores (`recovery-repeat.json`).
Earlier unchanged-parent controls on [3,14] matched the candidate scores,
rather than the supplied baseline (`wand-parent-control.json`), demonstrating
run variability. Do not attribute those two apparent changes to this patch.
This is a modest training-seed improvement, not held-out evidence.

## Checks

Bot and strategy imports passed. Twelve direct calls of the production
recovery decision verified the new HP threshold and budget boundary, plus
all retained safety guards. Source comparison confirmed only dive_logic.py
changed and bot.py/arena_adapter.py remained byte-identical.

## Discarded experiments

All other gameplay edits were reverted. Their raw outputs are retained in
`recovery-discarded-experiments.json`:

- Scare-scroll retention: no demonstrated improvement.
- Broad difficulty-based threat classification (10, then 15): early regression.
- Offensive-wand-only threat classification: tied the supplied full mean;
  parent controls matched the apparent score changes.
- Minotaur-only dangerous classification: three sampled ties.
- Eel rescue through the emergency handler: prevented drowning in two sampled
  games, but both scores tied because the bot later died at the same depths.
- Castle sea-monster route switch: no demonstrated improvement.
