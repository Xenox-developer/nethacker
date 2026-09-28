# Heal before erasing shelter

One strategy change in `autoascend/dive_logic.py`: before applying a digging
tool, spend single search turns recovering to the existing 60% HP threshold
on an intact, readable Elbereth. Stop after 100 rest turns per level/square.
Do not rest while hungry, blind, polymorphed, recently hurt or shot, in
Gehennom, or with a visible monster classified as ignoring Elbereth.

Reference inspected: pinned MIT peer
`daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b`,
particularly `autoascend/dive_logic.py`'s engraving/dig phases. Its comments
identify the pit erasing the protective inscription. This change is an
independent implementation of a short recovery window before that exposure;
it does not replace the bot or import a bundle of peer policies.

Evaluation: `python -m nethackers.arena.run --solution /workspace --batch
'[[SEED,"val-dwa-law-fem"], ...]' --evaluation-id local --out OUTPUT`.
Ran foreground batches [0,2,3,11], [1,5,8,13], and [4,6,7,9,10,12,14].
All 15 episodes completed without errors. Combined results are in
`pre-dig-rest-eval.json`.

Mean progression: supplied parent 0.4888017446; candidate 0.4946412042
(+0.0058394596). Two gains, two losses, eleven ties:

| Seed | Parent depth | Candidate depth |
| --- | --- | --- |
| 5 | 27 | 25 |
| 6 | 25 | 27 |
| 11 | 25 | 28 |
| 14 | 27 | 26 |

Validation: package compilation and bot import passed. Direct execution of
the production pre-dig decision verified the 100-turn cap and guards for
HP, hunger, blindness, polymorph, recent damage, ranged hits, Gehennom,
and a missing engraving. Adapter and entrypoint are unchanged.

This is a modest training-batch improvement, not evidence of a held-out gain.
An additional unchanged-parent control on [6,11] reproduced seed 6's depth 25,
but seed 11 reached depth 28, matching the candidate rather than the supplied
parent result. Thus seed 11's apparent gain is not reliably attributable to
this change. Retained in `pre-dig-rest-parent-control.json`; the reported
15-seed mean comparison uses the supplied baseline, not a fresh full control.
