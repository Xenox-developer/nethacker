# Digger point-blank throwing

One strategy change: while diving with a pick-axe or mattock wielded, prefer an available hand-thrown projectile over a melee action that would first switch weapons. Keep existing trajectory, bystander, Watch, Elbereth, passive-monster and exploding-monster safeguards. No launcher swaps are introduced.

Inspired by the point-blank Ranger mechanism in `engines/dag/autoascend/combat/fight_heur.py` of github.com/eL1fe/nethacker@a9e63ae735fba55510cbdd83b1545d4ad9f04f94. The implementation adapts the idea to digging-tool holders. The peer's MIT license has the same copyright and terms as the retained root LICENSE; the pinned source is recorded in the solution manifest.

## Evaluation

All 15 training seeds, val-dwa-law-fem, evaluation-id `local`, run as three sequential foreground arena commands with batches:

- 0, 1, 3, 8, 14
- 2, 4, 5, 6, 7
- 9, 10, 11, 12, 13

Command shape: `python -m nethackers.arena.run --solution /workspace --batch '<batch JSON>' --evaluation-id local --out <output>`.

Reference mean: 0.4919489209901017. Candidate mean: 0.4937090366004345. One gain (14: depth 26 -> 27), one loss (13: depth 25 -> 24), thirteen score ties. All completed without reported evaluator errors. Raw rows are alongside this note.

The small improvement is **inconclusive**: an unchanged-parent control on seeds 13 and 14 reproduced the original depth 25 on 13 but reached depth 27 on 14. Thus the gain over the supplied reference is not evidence of a reliable causal improvement. A sighted-only variant preserved the first five tested scores but lost a further level on seed 3 in the next batch; it was removed. The retained source is exactly the variant evaluated on all 15 seeds above.

Earlier exploratory teleportation, pet separation, sleep/death-wand, digging-loop, Medusa-retreat, scare-priority and ranged-emergency changes were removed. No other strategy changes remain.

Validation: package compilation, imports, make_agent/reset/act contract smoke check, and six focused checks covering the priority boost, normal weapon behavior, non-diving behavior, peaceful overshoot rejection, exploding-monster exclusion and passive-monster exclusion.
