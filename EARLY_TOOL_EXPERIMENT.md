# Tool-equipped descent at XL6

Only strategy change: DIG_DIVE_XL 7 -> 6 in autoascend/dive_logic.py.
The existing tool requirement, food checks, prayer readiness and protected digging remain in use.
Hypothesis: avoid further grind encounters once a tool is available and reduce generated monster difficulty by descending at lower XL.

Peer reference: github.com/daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b,
autoascend/dive_logic.py ARC_DIG_DIVE_XL / ROG_DIG_DIVE_XL early tool-equipped descent.
Peer LICENSE is MIT; no peer implementation was copied.

Evaluated all seeds 0–14 for val-dwa-law-fem, evaluation-id local, in three foreground batches of five.
Stored parent mean: 0.49781431357900807. Candidate: 0.5138725021224945.
Three gains, three losses, nine ties; all episodes completed without errors.
Fresh parent controls on seeds 1 and 5 reproduced their stored progress scores.
This is training-batch evidence, not a held-out improvement guarantee.

| Seed | Parent | Candidate | Difference |
| --- | --- | --- | --- |
| 0 | 0.466376 | 0.466376 | +0.000000 |
| 1 | 0.161268 | 0.466376 | +0.305109 |
| 2 | 0.445181 | 0.445181 | +0.000000 |
| 3 | 0.554357 | 0.506761 | -0.047597 |
| 4 | 0.554357 | 0.554357 | +0.000000 |
| 5 | 0.554357 | 0.646505 | +0.092148 |
| 6 | 0.466376 | 0.466376 | +0.000000 |
| 7 | 0.466376 | 0.466376 | +0.000000 |
| 8 | 0.601565 | 0.601565 | +0.000000 |
| 9 | 0.554357 | 0.554357 | +0.000000 |
| 10 | 0.601565 | 0.601565 | +0.000000 |
| 11 | 0.601565 | 0.466376 | -0.135189 |
| 12 | 0.466376 | 0.466376 | +0.000000 |
| 13 | 0.466376 | 0.445181 | -0.021195 |
| 14 | 0.506761 | 0.554357 | +0.047597 |

Discarded exploratory changes: TOOL_RUN_XL=7 regressed seeds 5 and 7 severely;
KEEP_TOOL_IN_TOUR=True was redundant because GRIND_HUNT_XL already enables retention.
Neither remains in the final strategy.
