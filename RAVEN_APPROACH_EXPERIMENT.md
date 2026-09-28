# Protection before approaching ravens

The only strategy change is in `DiveLogic._dig_escape_action`: the existing
pre-movement Elbereth action also considers a raven within two squares.
Ravens move quickly and blind in melee. Waiting until one is adjacent can
leave the hero blind before the first engraving attempt. Existing blindness,
polymorph, engraving, immunity, and two-attempt guards remain in place.

The parent trace for seed 2 reached Medusa at turn 16437 with 68/68 HP. It
moved toward a digging square, became blind, and repeatedly failed to walk
through occupied squares. It died to a raven on depth 24. The candidate
engraved before that first relocation and reached depth 25, eventually dying
to a plains centaur. This is ordinary monster-state handling, with no seed,
identity, or evaluator-dependent policy.

Reviewed the pinned MIT peer snapshots, particularly the existing relocation
protection in `alexeyshmelev/nethacker@283f192d4ae6557722e5912082284798c70bd513`
(`autoascend/dive_logic.py`). The final change extends that mechanism already
present in the parent; no whole-peer replacement or new license is involved.

All games used the arena runner with `--evaluation-id local`, identity
`val-dwa-law-fem`, and foreground batches. Final batches were
`[2,3,5,6,14]`, `[0,1,4,7,8]`, and `[9,10,11,12,13]`.
Every final episode completed without a bot error.

Full 15-seed mean: **0.5036797062 -> 0.5053704898**, a gain of **0.0016907837**.
There were three gains, two losses, and ten score ties against the supplied
reference. Full rows are in `evaluation/raven-guard-eval.json`.

| Seed | Supplied parent | Candidate | Fresh parent control |
| --- | ---: | ---: | ---: |
| 2 | 0.445181 | 0.466376 | 0.445181 |
| 3 | 0.506761 | 0.554357 | 0.554357 |
| 5 | 0.554357 | 0.646505 | 0.554357 |
| 6 | 0.554357 | 0.466376 | 0.554357 |
| 14 | 0.554357 | 0.506761 | 0.506761 |

The fresh controls temporarily restored the pristine parent in `/workspace`,
then restored the final candidate. Their five-seed mean was 0.5230027171;
the candidate on those same seeds was 0.5280750682. Controls are preserved in
`evaluation/raven-guard-parent-controls.json`. The changing parent endpoints
on 3 and 14 mean their reference differences are not isolated effects of the
patch. Candidate traces showed the added engraving on seed 2; they do not
establish a causal explanation for the other score changes. This remains a
small training-set improvement, not held-out evidence.

Validation: compilation and `make_agent()` construction passed, with callable
`reset()` and `act()`. Six production escape-decision checks cover a nearby
raven, a distant raven, blindness, a cobra, a killer bee, and an immune
minotaur. Run them with
`PYTHONPATH=. python evaluation/check_raven_guard.py`.

Exploratory changes to scroll/potion retention, general monster speed/danger,
wand priority, blind retries, earlier tool search, emergency thresholds,
flood guards, prayer thresholds, and blind relocation were reverted after
ties or regressions. None is included in the final strategy. The adapter,
entrypoint, configuration, and all other strategy files match the parent.

An independent repeat of the final candidate on seed 2 reproduced depth 25,
score 0.4663763157, and 16,494 turns. See `evaluation/raven-guard-repeat.json`.
