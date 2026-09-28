# Fixed-baseline three-strategy campaign

Request: `20260927T215044431526Z-eab26a5f56264b9391f20dd5ac976a24`.

**development recommendation only**. Recommended: `A`. Final publication candidate: `A`. These are separate decisions; native outer scoring and fresh validation remain authoritative.

**Confidence: low.** The sole primary Public gain reversed sign in the paired diagnostic repeat; no chosen-action-change diagnostic was recorded.

Primary games completed: **80**. Every listed arm has all 15 Public and 5 development games. Additional seeds are selection data, not holdout. No ordinary death was rerolled.

| Variant | Games | Public mean | Development mean | Pooled | Public G/T/L | Development G/T/L | Errors |
|---|---:|---:|---:|---:|---|---|---:|
| A | 20 | 0.4875498776 | 0.2803439441 | 0.4357483942 | 1/14/0 | 0/5/0 | 0 |
| B | 20 | 0.4843767682 | 0.2490672557 | 0.4255493900 | 1/13/1 | 0/4/1 | 0 |
| C | 20 | 0.4750604763 | 0.2803439441 | 0.4263813432 | 0/14/1 | 0/5/0 | 0 |
| baseline | 20 | 0.4782335857 | 0.2803439441 | 0.4287611753 | 0/15/0 | 0/5/0 | 0 |

Eligible singles: ['A']. Required combinations: none. Missing combinations: none.

Selection uses strict Public improvement and nonregressing development mean, with no errors. Combinations must beat the strongest eligible single on Public and not regress its development mean. No thresholds or seed lists were tuned after results.

## Implementation and fixtures

The actual incoming tree was frozen at `/tmp/campaign-incoming`, not replaced by the older research snapshot. `/tmp/campaign-baseline` is the action-equivalent flags-off baseline, with common dormant implementations and opt-in bounded diagnostics. Every singleton starts from it. `incoming-manifest.json`, `baseline-manifest.json`, `common-from-incoming.patch`, `dormant-implementation.patch` and `instrumentation-only.patch` preserve provenance. Singleton patches relative to both B0 and incoming source are retained. Variant `files.json` and `files-after.json` confirm unchanged source bytes. See `B-implementation-note.md` for the premeasurement nutrition correction.

A changes only cumulative branch probability and sibling range bookkeeping. B purchases at most one affordable noncursed food ration, using the total edible carried nutrition estimate, short known-shop paths, threat/hunger/location rechecks, an eight-turn start bound, mandatory settlement and 100-turn failed-target suppression. C scopes observed HP loss to consecutive protected observations on the same square and level, with unchanged maximum HP and no polymorph, and only bypasses the existing LR_ELBERETH suppression. Existing action ordering and unrelated parent improvements remain intact.

Focused tests exercise actual projection and wand ranking, wrapped food shopping, and the compiled actual LR suppression branch, plus the observation helper. Logs and the retained fixture source are under this directory. Campaign helper tests use fake rows and are separate from native games.

## Research basis

The frozen RESEARCH.md, research-resources.md and research-tactics.md motivate the mechanisms using the AutoAscend NetHack Challenge report (Hambro et al., 2022), NetHack is Hard to Hack (2023), and NetHack hunger, ray and Elbereth mechanics. These sources motivate the hypotheses; they do not establish a score improvement for this bot. No peer strategy code or older champion replaced the incoming parent.

## Coverage and limitations

- Aggregate process counters are lower bounds, without seed attribution.
- B0/A/C dormant B opportunity counters use the ordinary-food estimate; B uses total edible carried nutrition.
- Emergency action samples include all last-resort actions, not only exceptions.
- A branch counters include active and shadow projections. Score changes and retained-candidate shadow reranking are distinct counters; this is not a full counterfactual trajectory replay.
- Three-turn exception means trigger turn and the next two turns.
- Source manifests exclude assets, evidence and caches as documented by campaign.py.

**A aggregate counters:** `{"A.branch_nodes": 2871, "A.branching_projections": 1116, "A.evaluations": 754, "A.score_changed": 124, "A.zap_chosen": 11, "B.bail_location": 34, "B.bail_stock_or_hunger": 55, "B.bail_threat": 38, "C.emergency_action": 7, "C.observations": 234461, "C.qualified_loss": 11, "C.suppression_considered": 31}`.

**B aggregate counters:** `{"A.branch_nodes": 2501, "A.branching_projections": 1083, "A.evaluations": 693, "A.score_changed": 124, "A.zap_chosen": 11, "B.bail_location": 22, "B.bail_stock_or_hunger": 30, "C.emergency_action": 7, "C.observations": 241616, "C.qualified_loss": 12, "C.suppression_considered": 35}`.
B had zero observed starts: lack of game coverage, not evidence of uselessness. Any endpoint score differences without activation cannot be attributed to this reserve mechanism.

**C aggregate counters:** `{"A.branch_nodes": 2507, "A.branching_projections": 1086, "A.evaluations": 724, "A.score_changed": 124, "A.zap_chosen": 11, "B.bail_location": 22, "B.bail_stock_or_hunger": 30, "C.emergency_action": 8, "C.observations": 241706, "C.qualified_loss": 12, "C.suppression_considered": 35}`.
C had zero observed exception activations: lack of game coverage.

**baseline aggregate counters:** `{"A.branch_nodes": 2507, "A.branching_projections": 1086, "A.evaluations": 724, "A.score_changed": 124, "A.zap_chosen": 11, "B.bail_location": 34, "B.bail_stock_or_hunger": 55, "B.bail_threat": 38, "C.emergency_action": 7, "C.observations": 234461, "C.qualified_loss": 11, "C.suppression_considered": 31}`.

Changed wand scores alone do not demonstrate changed selected actions. In particular, absence of a chosen_action_changed counter is not positive evidence that the scoring change caused an endpoint gain.

HP loss is evidence of damage during apparent protection, not proof of attacker identity. Death causes and endpoint differences do not establish mechanism-level causality. Samples are bounded per process and category, and are not attributed to seeds.

## Diagnostic repeats

Control games: 6; excluded from every primary mean. Preselection is saved separately.

| Seed | Primary delta | Repeat delta | Reversal |
|---:|---:|---:|---|
| 1 | 0.1397443782 | -0.1397443782 | True |
| 0 | 0.0000000000 | 0.0000000000 | False |
| 2000 | 0.0000000000 | 0.0000000000 | False |

Unexpected reversal lowers confidence.
Repeat deltas changed; trajectory variability limits confidence.

## Full paired rows

Each arm retains exact raw JSON and native logs in `variants/<label>/`; controls are separate. The machine-readable report includes all original row fields, errors, depths, turns and death causes.

### A

| Phase | Seed | B0 score | Score | Delta | Status | Depth | Turns | Death |
|---|---:|---:|---:|---:|---|---:|---:|---|
| public | 0 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 22718 | drowned in deep water |
| public | 1 | 0.5067605634 | 0.6465049416 | +0.1397443782 | completed | 29 | 27854 | killed by a minotaur |
| public | 2 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 7 | 12491 | killed by an owlbear |
| public | 3 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 19294 | killed by a giant eel |
| public | 4 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 24057 | killed by a raven |
| public | 5 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 25955 | died of starvation |
| public | 6 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 27684 | killed by an invisible arch-lich |
| public | 7 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 20145 | killed by a minotaur |
| public | 8 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 60145 | killed by a captain |
| public | 9 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 31015 | died of starvation |
| public | 10 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 23314 | killed by a minotaur |
| public | 11 | 0.4663763157 | 0.4663763157 | +0.0000000000 | completed | 25 | 21375 | killed by an invisible stalker |
| public | 12 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 18565 | killed by a raven |
| public | 13 | 0.2061285484 | 0.2061285484 | +0.0000000000 | completed | 12 | 19766 | killed by a warhorse |
| public | 14 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 23173 | killed by a shark |
| development | 2000 | 0.1170499647 | 0.1170499647 | +0.0000000000 | completed | 8 | 22317 | killed by a minotaur |
| development | 2001 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 15443 | killed by an elf-lord |
| development | 2002 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 5 | 19769 | killed by a manes |
| development | 2003 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 27382 | killed by a minotaur |
| development | 2004 | 0.1255859702 | 0.1255859702 | +0.0000000000 | completed | 10 | 9692 | killed by a snake |

### B

| Phase | Seed | B0 score | Score | Delta | Status | Depth | Turns | Death |
|---|---:|---:|---:|---:|---|---:|---:|---|
| public | 0 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 22718 | drowned in deep water |
| public | 1 | 0.5067605634 | 0.6465049416 | +0.1397443782 | completed | 29 | 27854 | killed by a minotaur |
| public | 2 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 7 | 12491 | killed by an owlbear |
| public | 3 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 19294 | killed by a giant eel |
| public | 4 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 24057 | killed by a raven |
| public | 5 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 24039 | killed by a shark |
| public | 6 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 27684 | killed by an invisible arch-lich |
| public | 7 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 42222 | killed by a troll |
| public | 8 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 60145 | killed by a captain |
| public | 9 | 0.5543572045 | 0.5067605634 | -0.0475966411 | completed | 26 | 18909 | killed by a raven |
| public | 10 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 23314 | killed by a minotaur |
| public | 11 | 0.4663763157 | 0.4663763157 | +0.0000000000 | completed | 25 | 21375 | killed by an invisible stalker |
| public | 12 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 18565 | killed by a raven |
| public | 13 | 0.2061285484 | 0.2061285484 | +0.0000000000 | completed | 12 | 19766 | killed by a warhorse |
| public | 14 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 23173 | killed by a shark |
| development | 2000 | 0.1170499647 | 0.1170499647 | +0.0000000000 | completed | 8 | 22317 | killed by a minotaur |
| development | 2001 | 0.6015648510 | 0.4451814087 | -0.1563834423 | completed | 24 | 15341 | killed by a raven |
| development | 2002 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 5 | 19769 | killed by a manes |
| development | 2003 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 27382 | killed by a minotaur |
| development | 2004 | 0.1255859702 | 0.1255859702 | +0.0000000000 | completed | 10 | 9692 | killed by a snake |

### C

| Phase | Seed | B0 score | Score | Delta | Status | Depth | Turns | Death |
|---|---:|---:|---:|---:|---|---:|---:|---|
| public | 0 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 22718 | drowned in deep water |
| public | 1 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 27675 | killed by a soldier ant |
| public | 2 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 7 | 12491 | killed by an owlbear |
| public | 3 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 19294 | killed by a giant eel |
| public | 4 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 24057 | killed by a raven |
| public | 5 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 24039 | killed by a shark |
| public | 6 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 27684 | killed by an invisible arch-lich |
| public | 7 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 42222 | killed by a troll |
| public | 8 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 60145 | killed by a captain |
| public | 9 | 0.5543572045 | 0.5067605634 | -0.0475966411 | completed | 26 | 18909 | killed by a raven |
| public | 10 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 23314 | killed by a minotaur |
| public | 11 | 0.4663763157 | 0.4663763157 | +0.0000000000 | completed | 25 | 21375 | killed by an invisible stalker |
| public | 12 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 18565 | killed by a raven |
| public | 13 | 0.2061285484 | 0.2061285484 | +0.0000000000 | completed | 12 | 19766 | killed by a warhorse |
| public | 14 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 23173 | killed by a shark |
| development | 2000 | 0.1170499647 | 0.1170499647 | +0.0000000000 | completed | 8 | 22317 | killed by a minotaur |
| development | 2001 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 15443 | killed by an elf-lord |
| development | 2002 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 5 | 19769 | killed by a manes |
| development | 2003 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 27382 | killed by a minotaur |
| development | 2004 | 0.1255859702 | 0.1255859702 | +0.0000000000 | completed | 10 | 9692 | killed by a snake |

### baseline

| Phase | Seed | B0 score | Score | Delta | Status | Depth | Turns | Death |
|---|---:|---:|---:|---:|---|---:|---:|---|
| public | 0 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 22718 | drowned in deep water |
| public | 1 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 27675 | killed by a soldier ant |
| public | 2 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 7 | 12491 | killed by an owlbear |
| public | 3 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 19274 | killed by a pit viper |
| public | 4 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 24057 | killed by a raven |
| public | 5 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 25955 | died of starvation |
| public | 6 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 27684 | killed by an invisible arch-lich |
| public | 7 | 0.6465049416 | 0.6465049416 | +0.0000000000 | completed | 29 | 20145 | killed by a minotaur |
| public | 8 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 60145 | killed by a captain |
| public | 9 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 31015 | died of starvation |
| public | 10 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 23314 | killed by a minotaur |
| public | 11 | 0.4663763157 | 0.4663763157 | +0.0000000000 | completed | 25 | 21375 | killed by an invisible stalker |
| public | 12 | 0.4258360749 | 0.4258360749 | +0.0000000000 | completed | 23 | 18565 | killed by a raven |
| public | 13 | 0.2061285484 | 0.2061285484 | +0.0000000000 | completed | 12 | 19766 | killed by a warhorse |
| public | 14 | 0.5543572045 | 0.5543572045 | +0.0000000000 | completed | 27 | 23173 | killed by a shark |
| development | 2000 | 0.1170499647 | 0.1170499647 | +0.0000000000 | completed | 8 | 22317 | killed by a minotaur |
| development | 2001 | 0.6015648510 | 0.6015648510 | +0.0000000000 | completed | 28 | 15443 | killed by an elf-lord |
| development | 2002 | 0.0507583712 | 0.0507583712 | +0.0000000000 | completed | 5 | 19769 | killed by a manes |
| development | 2003 | 0.5067605634 | 0.5067605634 | +0.0000000000 | completed | 26 | 27382 | killed by a minotaur |
| development | 2004 | 0.1255859702 | 0.1255859702 | +0.0000000000 | completed | 10 | 9692 | killed by a snake |

