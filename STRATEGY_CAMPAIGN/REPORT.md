# Strategy campaign report

Request `20260927T215044431526Z-eab26a5f56264b9391f20dd5ac976a24`.

**Fixed-rule screening recommendation: A. Final publication candidate: A.**

Completed 80 primary games plus 6 separate diagnostic control games. All required combinations complete: True.

The diagnostic controls produced three paired score ties. A’s primary gains did not reproduce; confidence is **low**, and no robust strategy improvement is established. The fixed-rule selection above is retained without claiming success.

| Variant | Public n | Public mean | Development n | Development mean | Overall mean | Public G/T/L | Dev G/T/L | Errors |
|---|---:|---:|---:|---:|---:|---|---|---:|
| A | 15 | 0.484376768168 | 5 | 0.280343944118 | 0.433368562155 | 1/13/1 | 1/4/0 | 0 |
| B | 15 | 0.475060476286 | 5 | 0.280343944118 | 0.426381343244 | 0/14/1 | 1/4/0 | 0 |
| C | 15 | 0.475060476286 | 5 | 0.280343944118 | 0.426381343244 | 0/14/1 | 1/4/0 | 0 |
| baseline | 15 | 0.478233585694 | 5 | 0.249067255650 | 0.420942003183 | 0/15/0 | 0/5/0 | 0 |

Eligible singles: A. Required combinations: none. Missing combinations: none.

Eligibility requires strictly higher Public mean, nonregressing development mean and no errors. Every required combination is compared against the strongest eligible singleton; a combination must strictly improve Public and not regress development. Ties use development then alphabetic label.

## Integrity and implementation

Incoming digest: `sha256:825bbc5c9090edf91f7b7246296d72cbb34fc0d30a22b2f2177583c7e00efb69`.
Instrumented B0 digest: `sha256:9a36d7d83496db26e835f728b1847d2b3eb389a1cf1e0361da73871dce54d0c6`.

All completed helper batches verified unchanged sanitized runtime source; retained before/after manifests also match.

See [protocol](PROTOCOL.md), [focused fixtures](test_strategies.py), per-arm fixture logs, `incoming-manifest.json`, `common-preparation.patch`, instrumentation patches and `*-from-incoming.patch`. Complete copies remain outside the publication tree in `/tmp`. All flags begin off; independent singletons enable A, B or C only. B includes the documented pre-game nested-pickup refresh correction. Existing inherited changes, adapter, entrypoint and license are preserved.

## Diagnostics

Counters below are process aggregates and lower bounds. They include the selected technical attempt only. Raw counter files and bounded samples remain beside each native JSON. They have no invented per-seed attribution.

### A

```json
{
  "A.branch_nodes": 4445,
  "A.branching_evaluations": 1869,
  "A.evaluations": 9698,
  "A.score_changed": 154,
  "B.bail.location": 22,
  "B.bail.stock_hunger": 30,
  "B.considered": 82006,
  "C.observations": 304264,
  "C.qualified_loss": 12,
  "C.suppression_considered": 37
}
```

No selected-action change was recorded for A. Any endpoint score difference therefore lacks direct action-change attribution; score-calculation changes alone do not establish behavioral improvement.

### B

```json
{
  "A.branch_nodes": 4445,
  "A.branching_evaluations": 1869,
  "A.evaluations": 9698,
  "A.score_changed": 154,
  "B.bail.location": 22,
  "B.bail.stock_hunger": 30,
  "B.considered": 82916,
  "C.observations": 307492,
  "C.qualified_loss": 12,
  "C.suppression_considered": 37
}
```

B had no recorded started transaction: this sample does not establish usefulness or uselessness of purchases.

### C

```json
{
  "A.branch_nodes": 4455,
  "A.branching_evaluations": 1874,
  "A.evaluations": 9682,
  "A.score_changed": 154,
  "B.bail.location": 22,
  "B.bail.stock_hunger": 30,
  "B.considered": 82888,
  "C.observations": 307423,
  "C.qualified_loss": 14,
  "C.suppression_considered": 37
}
```

C had no recorded emergency suppression bypass: no gameplay-effect coverage is established.

### baseline

```json
{
  "A.branch_nodes": 4426,
  "A.branching_evaluations": 1860,
  "A.evaluations": 9506,
  "A.score_changed": 154,
  "B.bail.location": 34,
  "B.bail.stock_hunger": 55,
  "B.bail.threat": 38,
  "B.considered": 81318,
  "C.observations": 301108,
  "C.qualified_loss": 11,
  "C.suppression_considered": 33
}
```

## Diagnostic controls

Seeds were preselected from primary paired deltas and written before either control run. Criteria and ties are fixed; repetitions do not enter primary means.

| Seed | Primary delta | Control delta | Baseline primary/control | Candidate primary/control | Reversal or lost gain |
|---:|---:|---:|---|---|---|
| 1 | +0.139744378219 | +0.000000000000 | 0.506760563380/0.506760563380 | 0.646504941599/0.506760563380 | True |
| 9 | -0.047596641106 | +0.000000000000 | 0.554357204487/0.506760563380 | 0.506760563380/0.506760563380 | False |
| 2001 | +0.156383442337 | +0.000000000000 | 0.445181408702/0.601564851038 | 0.601564851038/0.601564851038 | True |

Unexpected reversal or failure to reproduce a primary gain lowers confidence.

**Confidence: low.** Diagnostic repeats failed to reproduce primary gains; no robust endpoint improvement is established.

## All primary rows

Depth, turns, status, errors and death labels are retained verbatim in the machine-readable report and raw native JSON.

### A

| Seed | Score | Paired delta | Depth | Turns | Status | Death / error |
|---:|---:|---:|---:|---:|---|---|
| 0 | 0.425836074886 | +0.000000000000 | 23 | 22718 | completed | drowned in deep water |
| 1 | 0.646504941599 | +0.139744378219 | 29 | 27854 | completed | killed by a minotaur |
| 2 | 0.050758371235 | +0.000000000000 | 7 | 12491 | completed | killed by an owlbear |
| 3 | 0.506760563380 | +0.000000000000 | 26 | 19294 | completed | killed by a giant eel |
| 4 | 0.425836074886 | +0.000000000000 | 23 | 24057 | completed | killed by a raven |
| 5 | 0.646504941599 | +0.000000000000 | 29 | 17445 | completed | killed by a hallucinogen-distorted wolf |
| 6 | 0.554357204487 | +0.000000000000 | 27 | 27684 | completed | killed by an invisible arch-lich |
| 7 | 0.646504941599 | +0.000000000000 | 29 | 42222 | completed | killed by a troll |
| 8 | 0.601564851038 | +0.000000000000 | 28 | 60145 | completed | killed by a captain |
| 9 | 0.506760563380 | -0.047596641106 | 26 | 18909 | completed | killed by a raven |
| 10 | 0.601564851038 | +0.000000000000 | 28 | 23314 | completed | killed by a minotaur |
| 11 | 0.466376315653 | +0.000000000000 | 25 | 21375 | completed | killed by an invisible stalker |
| 12 | 0.425836074886 | +0.000000000000 | 23 | 18565 | completed | killed by a raven |
| 13 | 0.206128548363 | +0.000000000000 | 12 | 19766 | completed | killed by a warhorse |
| 14 | 0.554357204487 | +0.000000000000 | 27 | 23173 | completed | killed by a shark |
| 2000 | 0.117049964736 | +0.000000000000 | 8 | 22317 | completed | killed by a minotaur |
| 2001 | 0.601564851038 | +0.156383442337 | 28 | 15443 | completed | killed by an elf-lord |
| 2002 | 0.050758371235 | +0.000000000000 | 5 | 19769 | completed | killed by a manes |
| 2003 | 0.506760563380 | +0.000000000000 | 26 | 27382 | completed | killed by a minotaur |
| 2004 | 0.125585970199 | +0.000000000000 | 10 | 9692 | completed | killed by a snake |

### B

| Seed | Score | Paired delta | Depth | Turns | Status | Death / error |
|---:|---:|---:|---:|---:|---|---|
| 0 | 0.425836074886 | +0.000000000000 | 23 | 22718 | completed | drowned in deep water |
| 1 | 0.506760563380 | +0.000000000000 | 26 | 27675 | completed | killed by a soldier ant |
| 2 | 0.050758371235 | +0.000000000000 | 7 | 12491 | completed | killed by an owlbear |
| 3 | 0.506760563380 | +0.000000000000 | 26 | 19274 | completed | killed by a pit viper |
| 4 | 0.425836074886 | +0.000000000000 | 23 | 24057 | completed | killed by a raven |
| 5 | 0.646504941599 | +0.000000000000 | 29 | 24039 | completed | killed by a shark |
| 6 | 0.554357204487 | +0.000000000000 | 27 | 27684 | completed | killed by an invisible arch-lich |
| 7 | 0.646504941599 | +0.000000000000 | 29 | 42222 | completed | killed by a troll |
| 8 | 0.601564851038 | +0.000000000000 | 28 | 60145 | completed | killed by a captain |
| 9 | 0.506760563380 | -0.047596641106 | 26 | 18909 | completed | killed by a raven |
| 10 | 0.601564851038 | +0.000000000000 | 28 | 23314 | completed | killed by a minotaur |
| 11 | 0.466376315653 | +0.000000000000 | 25 | 21375 | completed | killed by an invisible stalker |
| 12 | 0.425836074886 | +0.000000000000 | 23 | 18565 | completed | killed by a raven |
| 13 | 0.206128548363 | +0.000000000000 | 12 | 19766 | completed | killed by a warhorse |
| 14 | 0.554357204487 | +0.000000000000 | 27 | 23173 | completed | killed by a shark |
| 2000 | 0.117049964736 | +0.000000000000 | 8 | 22317 | completed | killed by a minotaur |
| 2001 | 0.601564851038 | +0.156383442337 | 28 | 15443 | completed | killed by an elf-lord |
| 2002 | 0.050758371235 | +0.000000000000 | 5 | 19769 | completed | killed by a manes |
| 2003 | 0.506760563380 | +0.000000000000 | 26 | 27382 | completed | killed by a minotaur |
| 2004 | 0.125585970199 | +0.000000000000 | 10 | 9692 | completed | killed by a snake |

### C

| Seed | Score | Paired delta | Depth | Turns | Status | Death / error |
|---:|---:|---:|---:|---:|---|---|
| 0 | 0.425836074886 | +0.000000000000 | 23 | 22718 | completed | drowned in deep water |
| 1 | 0.506760563380 | +0.000000000000 | 26 | 27675 | completed | killed by a soldier ant |
| 2 | 0.050758371235 | +0.000000000000 | 7 | 12491 | completed | killed by an owlbear |
| 3 | 0.506760563380 | +0.000000000000 | 26 | 19294 | completed | killed by a giant eel |
| 4 | 0.425836074886 | +0.000000000000 | 23 | 24057 | completed | killed by a raven |
| 5 | 0.646504941599 | +0.000000000000 | 29 | 24039 | completed | killed by a shark |
| 6 | 0.554357204487 | +0.000000000000 | 27 | 27684 | completed | killed by an invisible arch-lich |
| 7 | 0.646504941599 | +0.000000000000 | 29 | 42222 | completed | killed by a troll |
| 8 | 0.601564851038 | +0.000000000000 | 28 | 60145 | completed | killed by a captain |
| 9 | 0.506760563380 | -0.047596641106 | 26 | 18909 | completed | killed by a raven |
| 10 | 0.601564851038 | +0.000000000000 | 28 | 23314 | completed | killed by a minotaur |
| 11 | 0.466376315653 | +0.000000000000 | 25 | 21375 | completed | killed by an invisible stalker |
| 12 | 0.425836074886 | +0.000000000000 | 23 | 18565 | completed | killed by a raven |
| 13 | 0.206128548363 | +0.000000000000 | 12 | 19766 | completed | killed by a warhorse |
| 14 | 0.554357204487 | +0.000000000000 | 27 | 23173 | completed | killed by a shark |
| 2000 | 0.117049964736 | +0.000000000000 | 8 | 22317 | completed | killed by a minotaur |
| 2001 | 0.601564851038 | +0.156383442337 | 28 | 15364 | completed | killed by a nurse |
| 2002 | 0.050758371235 | +0.000000000000 | 5 | 19769 | completed | killed by a manes |
| 2003 | 0.506760563380 | +0.000000000000 | 26 | 27382 | completed | killed by a minotaur |
| 2004 | 0.125585970199 | +0.000000000000 | 10 | 9692 | completed | killed by a snake |

### baseline

| Seed | Score | Paired delta | Depth | Turns | Status | Death / error |
|---:|---:|---:|---:|---:|---|---|
| 0 | 0.425836074886 | +0.000000000000 | 23 | 22718 | completed | drowned in deep water |
| 1 | 0.506760563380 | +0.000000000000 | 26 | 27675 | completed | killed by a soldier ant |
| 2 | 0.050758371235 | +0.000000000000 | 7 | 12491 | completed | killed by an owlbear |
| 3 | 0.506760563380 | +0.000000000000 | 26 | 19274 | completed | killed by a pit viper |
| 4 | 0.425836074886 | +0.000000000000 | 23 | 24057 | completed | killed by a raven |
| 5 | 0.646504941599 | +0.000000000000 | 29 | 25955 | completed | died of starvation |
| 6 | 0.554357204487 | +0.000000000000 | 27 | 27684 | completed | killed by an invisible arch-lich |
| 7 | 0.646504941599 | +0.000000000000 | 29 | 20145 | completed | killed by a minotaur |
| 8 | 0.601564851038 | +0.000000000000 | 28 | 60145 | completed | killed by a captain |
| 9 | 0.554357204487 | +0.000000000000 | 27 | 31015 | completed | died of starvation |
| 10 | 0.601564851038 | +0.000000000000 | 28 | 23314 | completed | killed by a minotaur |
| 11 | 0.466376315653 | +0.000000000000 | 25 | 21375 | completed | killed by an invisible stalker |
| 12 | 0.425836074886 | +0.000000000000 | 23 | 18565 | completed | killed by a raven |
| 13 | 0.206128548363 | +0.000000000000 | 12 | 19766 | completed | killed by a warhorse |
| 14 | 0.554357204487 | +0.000000000000 | 27 | 23173 | completed | killed by a shark |
| 2000 | 0.117049964736 | +0.000000000000 | 8 | 22317 | completed | killed by a minotaur |
| 2001 | 0.445181408702 | +0.000000000000 | 24 | 15341 | completed | killed by a raven |
| 2002 | 0.050758371235 | +0.000000000000 | 5 | 19769 | completed | killed by a manes |
| 2003 | 0.506760563380 | +0.000000000000 | 26 | 27382 | completed | killed by a minotaur |
| 2004 | 0.125585970199 | +0.000000000000 | 10 | 9692 | completed | killed by a snake |

## Limits and provenance

- Twenty shared selection/development trajectories per arm; development2000–2004 are not an untouched holdout.
- Diagnostics are bounded aggregate lower bounds, not per-seed attribution. Missing counters do not demonstrate absence; zero activation is lack of coverage.
- Branching/wand evaluation counters include actual and opposite-calculation diagnostic projections; changed scoring is distinguished from a changed selected action.
- Observed protected HP loss does not establish an attacker identity or damage cause.
- Native outer Public scoring and fresh local validation remain the authority for promotion.

The frozen research notes cite AutoAscend/NetHack Challenge, HiHack and NetHack hunger/ray mechanics as motivation. They do not establish measured gains. No peer strategy source was copied; the incoming license is preserved. No judge, arena adapter, secret derivation, seed list, limits, local champion state or publication machinery was changed.
