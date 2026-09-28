# High-level threat wand priority

One policy change: value an offensive wand hit on a monster of level 10 or
higher at 40 (capped at one expected hit), so a safe zap can beat routine
melee. Existing collateral penalties and Elbereth rules still apply.

Reviewed the pinned peer2 combat scorer and monster data at
`github.com/daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b`.
Its minotaur data lists two 3d10 claws and a 2d8 butt, supporting urgent
resource use. No peer code was copied.

Validation used the prescribed arena command, identity `val-dwa-law-fem`,
evaluation ID `local`, in foreground batches [0,1,2,3], [4,8,10,12], and
[5,6,7,9,11,13,14]. All 15 episodes completed without errors.

| Version | Mean progress |
| --- | ---: |
| Supplied parent results | 0.491948921 |
| Final candidate | 0.493709037 |

Seed 14 improved from depth 26 to 27; seed 13 regressed from depth 25 to
24. The other 13 scores tied. This is a small training-batch gain, not
evidence of an improvement on unseen seeds.

An initial broader change to the shared danger classifier was rejected:
seeds 0,1,3 tied and seed 2 regressed to 0.050758371. That change was fully
reverted before testing the final wand-only policy.

Imports and targeted checks passed: a safe minotaur zap outranks routine
melee, while predicted self-hits and peaceful collateral retain negative
priority.
