# Deep-level pre-dig protection

One retained hypothesis: engrave Elbereth before digging at depth >=20 even
when no susceptible monster is visible, so arriving or unseen monsters cannot
interrupt the digging occupation. Existing engraving eligibility, retry caps,
blindness handling, and Gehennom exclusion remain in force. Early travel is
unchanged. Only autoascend/dive_logic.py changes strategy behavior.

All evaluations used evaluation-id `local`, identity `val-dwa-law-fem`, and
foreground arena commands. Candidate seeds were evaluated in batches
[0,1,4,5], [3,6,8,9,11,12], [2,7,10,13,14]. All completed without errors.

Full candidate mean: 0.4809840848; supplied parent mean: 0.4750604763.
Against supplied results: gains 0,4,9; loss 1; eleven ties.

A fresh pristine-parent control on [0,1,4,9] reproduced supplied scores on
0,1,4, but seed9 reached depth27 (0.5543572045), tying the candidate. Thus the
seed9 gain is not established. Substituting these four fresh controls into
the supplied baseline gives mean 0.4782335857, for a smaller +0.0027504991
candidate improvement. This is a mixed-time baseline, not a fresh full run.
No held-out evaluation was performed; the measured gain is small.

| Seed | Parent control | Candidate |
|---|---:|---:|
|0|0.4258360749|0.4663763157|
|1|0.5067605634|0.3789566792|
|4|0.4258360749|0.5543572045|
|9|0.5543572045|0.5543572045|

Validation: compileall passed; bot.py, arena_adapter.py, manifest, and license
match the parent. The complete 15 candidate rows and four parent controls are
saved alongside this report.

Rejected screens (all reverted):
- Peer1 container routing exclusions: seeds2,1,9,13 all tied supplied parent.
- Peer2 recognition of wished items: seeds4,2,1,9 all tied supplied parent.
- Peer2-inspired combat against Elbereth-immune enemies: seeds8,10,1,13 all
  score-tied; seed8's turns changed.
- Whole Peer3 strategy package with original workspace adapter: seeds0,2,4,8,13
  mean0.1548992655 versus parent0.3420247841; rejected. Source:
  github.com/vlomshakov/nethacker@94016e19ff133adc0d1b321bc14a7beb74d4f366 (MIT).

Pinned peer sources inspected for mechanisms:
- github.com/daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b
- github.com/vkurenkov/nethacker@f15bb8c8e01d905d1946e32bfd2558e17394eab6

No newly copied peer code remains. The final change uses the parent's existing
pre-dig protection mechanism with a depth condition; it is distinct from the
previous rejected all-depth ELBERETH_ALWAYS attempt.
