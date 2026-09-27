# Wand projection experiment

Final change: preserve cumulative probability through wand-ray bounces and give each sibling branch its own remaining range. Geometry, range penalties, horizon and action priorities are unchanged. All other screened gameplay changes were reverted.

## Validation

- All 15 training seeds, val-dwa-law-fem, namespace `local`: **0.484376768**, supplied parent **0.487549878**.
- Four sequential foreground batches of 4, 4, 4 and 3 episodes. All completed without result errors.
- 14 score ties and one decline against the supplied reference. Seed 9: reference 0.554357204, candidate 0.506760563. A separate unchanged-parent control reproduced 0.506760563 and the candidate's 18909 turns exactly. This control is retained separately and does not replace the reference row.
- Three regression tests pass: downstream branch probability, sibling-order/range independence, and unchanged straight-ray weight. Package compilation and make_agent/reset/act interface checks pass.
- **No demonstrated score gain.** The final change fixes a calculation defect, but the score objective remains unproven. There is no held-out validation or evidence of better selected wand actions.

## Reference review

Read /refs/CONTEXT.md, parent per-seed deaths, EXPERIMENTS.md, and pinned peer snapshots. The retained defect is present in the shared wand simulator inspected in the peers. No peer implementation was copied; the existing MIT license and manifest attribution remain intact. Other mechanisms, including Castle passage and earlier tool acquisition, did not produce a convincing improvement. A diagnostic replay of parent seed 2 exposed repeated monster-blocked item inspection trips; multiple cooldown variants were tested and rejected.

## Screened experiments

Each row compares its original evaluated sample with the same seeds from the supplied parent reference. Samples differ, so these means are not a ranking across variants. All raw results are retained. Tests were adaptive development, not independent validation.

| Variant | Games | Parent mean | Candidate mean | Gains | Losses |
|---|---:|---:|---:|---:|---:|
| Enable existing Castle passage | 7 | 0.607337 | 0.587374 | 0 | 1 |
| Independent probability-weighted wand branches (final) | 15 | 0.487550 | 0.484377 | 0 | 1 |
| Use species movement speed | 4 | 0.309270 | 0.309270 | 0 | 0 |
| Begin digging-tool trip at XL6 | 8 | 0.400204 | 0.275985 | 2 | 3 |
| Emergency exception after damage through intact Elbereth | 8 | 0.426385 | 0.413852 | 0 | 1 |
| Cooldown all monster-blocked item inspection trips | 8 | 0.405252 | 0.277802 | 2 | 4 |
| Cooldown during any descent | 15 | 0.487550 | 0.473542 | 1 | 4 |
| Cooldown after three failures during descent | 4 | 0.429499 | 0.244692 | 0 | 2 |
| Cooldown during failed-prayer rescue | 8 | 0.453848 | 0.453512 | 1 | 3 |
| Cooldown during rescue after 500 turns on level | 4 | 0.429499 | 0.401371 | 1 | 2 |

## Final per-seed scores

| Seed | Parent | Final |
|---|---:|---:|
| 0 | 0.425836075 | 0.425836075 |
| 1 | 0.646504942 | 0.646504942 |
| 2 | 0.050758371 | 0.050758371 |
| 3 | 0.506760563 | 0.506760563 |
| 4 | 0.425836075 | 0.425836075 |
| 5 | 0.646504942 | 0.646504942 |
| 6 | 0.554357204 | 0.554357204 |
| 7 | 0.646504942 | 0.646504942 |
| 8 | 0.601564851 | 0.601564851 |
| 9 | 0.554357204 | 0.506760563 |
| 10 | 0.601564851 | 0.601564851 |
| 11 | 0.466376316 | 0.466376316 |
| 12 | 0.425836075 | 0.425836075 |
| 13 | 0.206128548 | 0.206128548 |
| 14 | 0.554357204 | 0.554357204 |

Final fight_heur.py SHA-256: `95bab12c6b21aac71edbd345cd724ba33f024905d854302e89ae78c4ec58c91d`.

Reproduce regression checks: `python -m unittest discover -s tests -p test_wand_projection.py`.

Arena command pattern: `python -m nethackers.arena.run --solution /workspace --batch '[[0,"val-dwa-law-fem"], ...]' --evaluation-id local --out /tmp/eval.json`.
