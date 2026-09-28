# Repeating safe digging escapes

Hypothesis: repeat the existing digging escape strategy while its eligibility
checks pass, so lower-priority combat cannot interrupt hole completion between
actions. Higher-priority emergency strategies remain active.

Only gameplay change: `self.dive.dig_first().repeat()` in
`autoascend/global_logic.py`. No adapter or entrypoint changes.

Reviewed the pinned peer3 `_hold_loop` scheduling explanation and the existing
attempt-17 evidence in `/refs/parent/EXPERIMENTS.md`. This is a caller-level
`Strategy.repeat()` change, not a whole-peer replacement or broad hold loop.
Peer source: github.com/kefirski/nethacker@995d8f40b2d24ee09487b0e87e014ca2fcc10928
(already listed in the solution manifest; MIT license retained).

Evaluation used `python -m nethackers.arena.run`, identity `val-dwa-law-fem`,
`--evaluation-id local`, and seeds 1, 7, 3, 4. Each evaluation was one foreground
command, awaited to completion. Candidate results: `dig-repeat-eval.json`.

| Seed | Parent | Changed |
| --- | ---: | ---: |
| 1 | 0.466376 | 0.646505 |
| 7 | 0.506761 | 0.506761 |
| 3 | 0.506761 | 0.506761 |
| 4 | 0.466376 | 0.554357 |

Sample mean: 0.486568 -> 0.553596 (delta +0.067027).
Fresh parent controls on seeds 1 and 4 reproduced reference score, turn count,
maximum depth and cause of death; saved in `dig-repeat-parent-control.json`.
Two improvements, two score ties, no score regressions in this sample.
The full 15-seed mean has not been measured for this candidate.

Validation: `autoascend.global_logic` and `bot` import cleanly, and
`bot.make_agent` remains callable. All four candidate episodes completed
without reported errors.
