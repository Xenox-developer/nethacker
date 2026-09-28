# Blind digging movement protection

One retained strategy change: allow the existing capped Elbereth-before-moving defense while blind. The two-attempt limit per level/square and the polymorph, engraving availability, adjacent-hostile, and readable-inscription guards remain.

The peer2 snapshot `github.com/daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b` and the inherited strategy both protect movement to a digging square with Elbereth, but exclude blindness. This change extends that existing mechanism; no peer code was copied. Existing source attribution and licenses remain intact.

## Evidence

All runs used `python -m nethackers.arena.run --solution /workspace`, identity `val-dwa-law-fem`, and `--evaluation-id local`, in foreground batches. Retained candidate batches: `[2,3,7]` and `[0,1,5,6,13]`. Per-seed results are in `blind-walk-eval.json`.

| Seed | Parent progress | Candidate progress | Maximum depth |
| --- | ---: | ---: | --- |
| 0 | 0.466376 | 0.466376 | 25 → 25 |
| 1 | 0.161268 | 0.161268 | 11 → 11 |
| 2 | 0.445181 | 0.466376 | 24 → 25 |
| 3 | 0.554357 | 0.554357 | 27 → 27 |
| 5 | 0.466376 | 0.466376 | 25 → 25 |
| 6 | 0.466376 | 0.554357 | 25 → 27 |
| 7 | 0.466376 | 0.466376 | 25 → 25 |
| 13 | 0.466376 | 0.466376 | 25 → 25 |

Matched eight-seed mean: **0.436586 → 0.450233**. Two gains, six score ties, no errors. This is a sample result, not a new full-15 or all-identity score.

An unchanged-parent control for seed 2 reproduced its reference progress, depth, and turns (0.445181, depth 24, 16458 turns). Its decision log showed repeated exposed movement while blind among ravens on Medusa's level. The candidate log shows the new protection branch firing at turns 16438 and 16440, followed by reaching depth 25. Seed 6's gain was not repeated against a fresh parent control. Earlier probes showed variable seed-3 endpoints, so small differences need cautious interpretation.

Validation: package compilation, import of `make_agent`, callable `reset`/`act`, and six direct production decision cases (blind and sighted behavior, attempts zero/one/two, polymorph, engraving unavailable).

## Reverted probes

Before the retained change, Castle sea-route switching showed no improvement on seeds 3/8/13; tactile wand engraving and safe unicorn-horn blindness treatment tied on 2/3/7; fighting while blind regressed seed 7; raising eel escape to emergency priority changed seed 13's death without raising its score. All of those code changes were reverted. Only `autoascend/dive_logic.py` differs from the parent strategy package.
