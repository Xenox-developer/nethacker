# XL7 tool-seeking experiment

One strategy change: `TOOL_RUN_XL = 7`. End level-one training at XL7,
retaining the existing food-readiness check, and use the existing tool-run
thresholds for digging and dwarf tool acquisition. No identity or seed checks.

Peer inspiration: `github.com/daglar-dragomirov/nethacker@c4308340c16ceb94e2e7896dd5897676b1fc3512`,
`autoascend/global_logic.py` describes an XL7 Valkyrie training threshold.
The peer's MIT license was inspected. No peer implementation was copied;
this enables the existing tool-run mechanism.

Evaluation used `python -m nethackers.arena.run --solution /workspace`
with `--evaluation-id local`, in two foreground batches of four games.
Identity: `val-dwa-law-fem`. Results: `tool-run-eval.json`.

| Seed | Parent score | Candidate score | Parent depth | Candidate depth |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0.425836 | 0.425836 | 23 | 23 |
| 1 | 0.646505 | 0.506761 | 29 | 26 |
| 2 | 0.050758 | 0.050758 | 7 | 7 |
| 3 | 0.506761 | 0.506761 | 26 | 26 |
| 4 | 0.554357 | 0.425836 | 27 | 23 |
| 6 | 0.050758 | 0.554357 | 2 | 27 |
| 7 | 0.466376 | 0.646505 | 25 | 29 |
| 8 | 0.601565 | 0.601565 | 28 | 28 |

Eight-seed mean: 0.412864587 -> 0.464797331 (+0.051932744).
Two gains, two losses, four score ties. This is not a full 15-seed result.
A fresh parent control on seed 6 reproduced score 0.050758 and depth 2.
The candidate repeat reproduced score 0.554357, depth 27 and 27,684 turns.
A fresh parent control on seed 7 during the preceding trial reached depth 26
(score 0.506761), above its supplied depth-25 reference; the candidate's
0.646505 still exceeds both parent outcomes. No action trace proves causation.

Earlier trials, fully reverted: unconditional pre-dig engraving regressed
four-seed mean; level-specific engraving-failure memory tied seven scores,
and its apparent eighth-seed gain was reproduced by a fresh parent control.

Validation: Python compilation and entrypoint import passed. The adapter,
make_agent/reset/act contract, and all other strategy settings are unchanged.
