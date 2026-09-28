# Three-strategy campaign — N=20

Request `20260927T215044431526Z-eab26a5f56264b9391f20dd5ac976a24`.

## Selection

Recommended: **C**. Final publication candidate: **C**.
This is a development selection, not promotion. Native outer Public scoring and fresh local validation remain authoritative.

**Confidence is low.** No selected-mechanism behavioral activation was recorded. The paired primary score differences did not fully reproduce in controls. A control reversed the sign of a primary paired difference. The numerical selection rule still selects the tested candidate; this is not proof of a causal improvement.

Primary games: **80**. Eligible singles: ['C']. Required combinations: []. Missing combinations: [].

| Variant | Games | Public mean | Development mean | Public gains/ties/losses | Development gains/ties/losses | Errors |
|---|---:|---:|---:|---|---|---:|
| A | 20 | 0.475060476286 | 0.280343944118 | 0/14/1 | 0/5/0 | 0 |
| B | 20 | 0.475060476286 | 0.280343944118 | 0/14/1 | 0/5/0 | 0 |
| C | 20 | 0.484376768168 | 0.280343944118 | 1/13/1 | 0/5/0 | 0 |
| baseline | 20 | 0.478233585694 | 0.280343944118 | 0/15/0 | 0/5/0 | 0 |

## Protocol and provenance

The actual incoming tree was frozen at `/tmp/campaign-incoming`; no champion20 replacement was used. `incoming-manifest.json` records sanitized source hashes and `incoming-full-file-hashes.json` also includes supplied assets. The common all-flags-off baseline and every independent singleton live outside the published tree in `/tmp/campaign-*`. All unrelated parent code, adapter, entrypoint, and license were retained.

Every primary variant received Public 0–14 and development 2000–2004 with secret `public`, namespace `local`, 1,000,000 steps, 10,000 no-progress limit, 120-second action timeout, and at most four concurrent episodes. Variant batches ran sequentially through the supplied `campaign.py`; both phases must finish before a variant counts. Development is selection data, not holdout.

Complete raw JSON, logs, diagnostics, per-file hashes, canonical membership, and baseline-relative patches are under `variants/<label>/`. The helper verifies the sanitized runtime snapshot after evaluation; separate before/after manifests also verify the frozen source trees. `incoming-to-baseline.patch`, `implementation-common.patch`, and `instrumentation-only.patch` preserve the common scaffold and separate action-neutral logging. Singletons enable only their named flag. Hypotheses, thresholds, and seed lists were fixed. Two contract-boundary corrections were made to unevaluated B/C while A ran; see `pre-evaluation-corrections.md` and retained initial/corrected manifests. No completed or running variant was changed or replaced.

## Mechanisms and focused validation

- **A:** cumulative branch probability and sibling-local remaining range in the existing range-13 wand simulation. Geometry, encounter costs, friendly/self penalties, and action priorities are unchanged.
- **B:** one affordable known-price food ration, unknown beatitude permitted and known cursed excluded, for a hungry/weak tool carrier with estimated nutrition below 400. Only known same-shop floor paths of at most two moves are considered; prerequisites are rechecked before each move and pickup. At elapsed eight turns no new move/pickup begins. Existing payment-or-drop cleanup always follows pickup, with overrun logging and a 100-turn failed-location cooldown.
- **C:** a separately scoped consecutive-turn same-level/tile intact-Elbereth HP-loss marker, excluding maximum-HP changes and polymorph, expires after three elapsed turns. Its flag only bypasses the existing LR_ELBERETH suppression. All outer emergency gates and action ordering remain unchanged; existing damage/rest/dig policies are retained.

`test_strategies.py` has 22 focused tests, including straight and deterministic rays, weighted descendants, branch order/mirror symmetry, self/friendly penalties, actual score-driven action ranking, tool/no-tool shopping, price/BUC/path/threat gates, timeout and debt cleanup, scoped HP evidence, and the actual source LR branch with its ordinary gates. Initial fixture setup errors (monster glyph zero used as empty floor and an unhashable fake monster) were corrected before any games; production strategy was not changed by those fixture fixes. `fixtures.log`, `fixtures-expanded.log`, and per-variant fixture logs retain outcomes. Additional pre-evaluation boundary suites passed for B (11 tests, including full cooldown from failure exit) and C (5 tests, including no deferred same-turn loss). All 23 supplied campaign-helper tests passed.

## Diagnostics and limits

All diagnostics are disabled unless the campaign output environment variable is set. They read in-game state only and never seed, score, or evaluator internals. Counters are aggregate process lower bounds, not exact totals or per-seed counts. Branching counts include recursive calls in both actual and counterfactual projections, not distinct decisions. `A.considered` counts direction evaluations, including those with no usable wand. Score and root-action changes are recorded separately. Root comparisons rescore the existing filtered candidate list; they do not reconstruct a counterfactual combat policy with a different candidate set, and paired wand score comparisons use the existing enumeration. Thus they are diagnostic coverage, not a complete causal attribution of endpoint differences.

`B.eligible` is preliminary hunger/stock/location/status eligibility, before finding qualifying stock. No purchase activation means lack of coverage, not evidence that buying is useless. B bail categories and bounded transaction samples give stock before/after and elapsed turns. `C.qualified_loss` records observed HP loss, not an identified attacker. The dormant baseline/A/B observer predates the same-turn boundary correction in C; its qualified-loss count is not an equivalent control for C activation. Emergency class counters include all last-resort actions; bounded `emergency_action` samples separately mark whether the suppression exception was active. Samples are capped by kind, so their absence is not proof an event never happened.

### Coverage findings

- A: `A.applied` has 0 recorded events as an aggregate lower bound. No behavioral activation was recorded; these games do not establish the mechanism’s benefit.
- B: `B.purchased` has 0 recorded events as an aggregate lower bound. No behavioral activation was recorded; these games do not establish the mechanism’s benefit.
- C: `C.applied` has 0 recorded events as an aggregate lower bound. No behavioral activation was recorded; these games do not establish the mechanism’s benefit.

### A aggregate lower-bound counters

```json
{
  "A.branching": 4447,
  "A.considered": 204033,
  "A.score_changed": 124,
  "B.bail_location": 22,
  "B.bail_stock_hunger": 30,
  "B.considered": 52,
  "C.emergency_potion": 1,
  "C.emergency_wand": 8,
  "C.observations": 330346,
  "C.qualified_loss": 12,
  "C.suppression_gate": 37
}
```

### B aggregate lower-bound counters

```json
{
  "A.branching": 4455,
  "A.considered": 204889,
  "A.score_changed": 124,
  "B.bail_location": 22,
  "B.bail_stock_hunger": 30,
  "B.considered": 52,
  "C.emergency_potion": 1,
  "C.emergency_wand": 9,
  "C.observations": 333505,
  "C.qualified_loss": 15,
  "C.suppression_gate": 37
}
```

### C aggregate lower-bound counters

```json
{
  "A.branching": 4447,
  "A.considered": 204897,
  "A.score_changed": 124,
  "B.bail_location": 22,
  "B.bail_stock_hunger": 30,
  "B.considered": 52,
  "C.emergency_potion": 1,
  "C.emergency_wand": 7,
  "C.observations": 333574,
  "C.qualified_loss": 12,
  "C.suppression_gate": 37
}
```

### baseline aggregate lower-bound counters

```json
{
  "A.branching": 4447,
  "A.considered": 202777,
  "A.score_changed": 124,
  "B.bail_location": 34,
  "B.bail_stock_hunger": 55,
  "B.bail_threat": 38,
  "B.considered": 127,
  "C.emergency_potion": 1,
  "C.emergency_wand": 7,
  "C.observations": 324116,
  "C.qualified_loss": 11,
  "C.suppression_gate": 37
}
```

## Paired primary results

### A

| Group | Seed | B0 score | Score | Delta | Status | Turns | Depth | Death / ending |
|---|---:|---:|---:|---:|---|---:|---:|---|
| development | 2000 | 0.117049964736 | 0.117049964736 | +0.000000000000 | completed | 22317 | 8 | killed by a minotaur |
| development | 2001 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 15443 | 28 | killed by an elf-lord |
| development | 2002 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 19769 | 5 | killed by a manes |
| development | 2003 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 27382 | 26 | killed by a minotaur |
| development | 2004 | 0.125585970199 | 0.125585970199 | +0.000000000000 | completed | 9692 | 10 | killed by a snake |
| public | 0 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 22718 | 23 | drowned in deep water |
| public | 1 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 27675 | 26 | killed by a soldier ant |
| public | 2 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 12491 | 7 | killed by an owlbear |
| public | 3 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 19294 | 26 | killed by a giant eel |
| public | 4 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 24057 | 23 | killed by a raven |
| public | 5 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 17445 | 29 | killed by a hallucinogen-distorted wolf |
| public | 6 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 27684 | 27 | killed by an invisible arch-lich |
| public | 7 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 42222 | 29 | killed by a troll |
| public | 8 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 60145 | 28 | killed by a captain |
| public | 9 | 0.554357204487 | 0.506760563380 | -0.047596641106 | completed | 18909 | 26 | killed by a raven |
| public | 10 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 23314 | 28 | killed by a minotaur |
| public | 11 | 0.466376315653 | 0.466376315653 | +0.000000000000 | completed | 21375 | 25 | killed by an invisible stalker |
| public | 12 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 18565 | 23 | killed by a raven |
| public | 13 | 0.206128548363 | 0.206128548363 | +0.000000000000 | completed | 19766 | 12 | killed by a warhorse |
| public | 14 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 23173 | 27 | killed by a shark |

### B

| Group | Seed | B0 score | Score | Delta | Status | Turns | Depth | Death / ending |
|---|---:|---:|---:|---:|---|---:|---:|---|
| development | 2000 | 0.117049964736 | 0.117049964736 | +0.000000000000 | completed | 22317 | 8 | killed by a minotaur |
| development | 2001 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 15364 | 28 | killed by a nurse |
| development | 2002 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 19769 | 5 | killed by a manes |
| development | 2003 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 27382 | 26 | killed by a minotaur |
| development | 2004 | 0.125585970199 | 0.125585970199 | +0.000000000000 | completed | 9692 | 10 | killed by a snake |
| public | 0 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 22718 | 23 | drowned in deep water |
| public | 1 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 27675 | 26 | killed by a soldier ant |
| public | 2 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 12491 | 7 | killed by an owlbear |
| public | 3 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 19294 | 26 | killed by a giant eel |
| public | 4 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 24057 | 23 | killed by a raven |
| public | 5 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 24039 | 29 | killed by a shark |
| public | 6 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 27684 | 27 | killed by an invisible arch-lich |
| public | 7 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 42222 | 29 | killed by a troll |
| public | 8 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 60145 | 28 | killed by a captain |
| public | 9 | 0.554357204487 | 0.506760563380 | -0.047596641106 | completed | 18909 | 26 | killed by a raven |
| public | 10 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 23314 | 28 | killed by a minotaur |
| public | 11 | 0.466376315653 | 0.466376315653 | +0.000000000000 | completed | 21375 | 25 | killed by an invisible stalker |
| public | 12 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 18565 | 23 | killed by a raven |
| public | 13 | 0.206128548363 | 0.206128548363 | +0.000000000000 | completed | 19766 | 12 | killed by a warhorse |
| public | 14 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 23173 | 27 | killed by a shark |

### C

| Group | Seed | B0 score | Score | Delta | Status | Turns | Depth | Death / ending |
|---|---:|---:|---:|---:|---|---:|---:|---|
| development | 2000 | 0.117049964736 | 0.117049964736 | +0.000000000000 | completed | 22317 | 8 | killed by a minotaur |
| development | 2001 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 15443 | 28 | killed by an elf-lord |
| development | 2002 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 19769 | 5 | killed by a manes |
| development | 2003 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 27382 | 26 | killed by a minotaur |
| development | 2004 | 0.125585970199 | 0.125585970199 | +0.000000000000 | completed | 9692 | 10 | killed by a snake |
| public | 0 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 22718 | 23 | drowned in deep water |
| public | 1 | 0.506760563380 | 0.646504941599 | +0.139744378219 | completed | 27854 | 29 | killed by a minotaur |
| public | 2 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 12491 | 7 | killed by an owlbear |
| public | 3 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 19294 | 26 | killed by a giant eel |
| public | 4 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 24057 | 23 | killed by a raven |
| public | 5 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 24039 | 29 | killed by a shark |
| public | 6 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 27684 | 27 | killed by an invisible arch-lich |
| public | 7 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 42222 | 29 | killed by a troll |
| public | 8 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 60145 | 28 | killed by a captain |
| public | 9 | 0.554357204487 | 0.506760563380 | -0.047596641106 | completed | 18909 | 26 | killed by a raven |
| public | 10 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 23314 | 28 | killed by a minotaur |
| public | 11 | 0.466376315653 | 0.466376315653 | +0.000000000000 | completed | 21375 | 25 | killed by an invisible stalker |
| public | 12 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 18565 | 23 | killed by a raven |
| public | 13 | 0.206128548363 | 0.206128548363 | +0.000000000000 | completed | 19766 | 12 | killed by a warhorse |
| public | 14 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 23173 | 27 | killed by a shark |

### baseline

| Group | Seed | B0 score | Score | Delta | Status | Turns | Depth | Death / ending |
|---|---:|---:|---:|---:|---|---:|---:|---|
| development | 2000 | 0.117049964736 | 0.117049964736 | +0.000000000000 | completed | 22317 | 8 | killed by a minotaur |
| development | 2001 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 15443 | 28 | killed by an elf-lord |
| development | 2002 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 19769 | 5 | killed by a manes |
| development | 2003 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 27382 | 26 | killed by a minotaur |
| development | 2004 | 0.125585970199 | 0.125585970199 | +0.000000000000 | completed | 9692 | 10 | killed by a snake |
| public | 0 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 22718 | 23 | drowned in deep water |
| public | 1 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 27675 | 26 | killed by a soldier ant |
| public | 2 | 0.050758371235 | 0.050758371235 | +0.000000000000 | completed | 12491 | 7 | killed by an owlbear |
| public | 3 | 0.506760563380 | 0.506760563380 | +0.000000000000 | completed | 19294 | 26 | killed by a giant eel |
| public | 4 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 24057 | 23 | killed by a raven |
| public | 5 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 17445 | 29 | killed by a hallucinogen-distorted wolf |
| public | 6 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 27684 | 27 | killed by an invisible arch-lich |
| public | 7 | 0.646504941599 | 0.646504941599 | +0.000000000000 | completed | 20145 | 29 | killed by a minotaur |
| public | 8 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 60145 | 28 | killed by a captain |
| public | 9 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 31015 | 27 | died of starvation |
| public | 10 | 0.601564851038 | 0.601564851038 | +0.000000000000 | completed | 23314 | 28 | killed by a minotaur |
| public | 11 | 0.466376315653 | 0.466376315653 | +0.000000000000 | completed | 21375 | 25 | killed by an invisible stalker |
| public | 12 | 0.425836074886 | 0.425836074886 | +0.000000000000 | completed | 18565 | 23 | killed by a raven |
| public | 13 | 0.206128548363 | 0.206128548363 | +0.000000000000 | completed | 19766 | 12 | killed by a warhorse |
| public | 14 | 0.554357204487 | 0.554357204487 | +0.000000000000 | completed | 23173 | 27 | killed by a shark |

## Separate diagnostic repeats

The repeat seeds were selected before repeating: largest Public gain, largest Public loss, and largest absolute development difference, with lower seed ID breaking ties and duplicates removed. They are controls only and never replace primary outcomes.

Preselected seeds: [1, 9, 2000]. See `controls/` for full original results, logs, configuration, and before/after hashes.

| Seed | Primary delta | Repeat B0 | Repeat candidate | Repeat delta |
|---|---:|---:|---:|---:|
| 1 | +0.139744378219 | 0.646504941599 | 0.506760563380 | -0.139744378219 |
| 9 | -0.047596641106 | 0.506760563380 | 0.506760563380 | +0.000000000000 |
| 2000 | +0.000000000000 | 0.117049964736 | 0.117049964736 | +0.000000000000 |

**A sign reversal occurred in the controls; confidence is lower.**
Some paired deltas changed on repetition. Endpoint gains are therefore not fully reproducible and should not be treated as established causal improvements.

Completed primary plus control games: **86**. All completed without result errors; there were **zero technical retries**. Primary results were never replaced by controls.

