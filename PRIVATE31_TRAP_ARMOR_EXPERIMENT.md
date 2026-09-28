# Private31 trap-blocked armor cooldown experiment

Request `20260928T054415304296Z-130a7ec3b8744f2fad4a17b97e75da07`. This is an experiment, not a demonstrated improvement.

Implemented one mechanism: the five explicit reference refusal patterns return False and block only the affected armor slot until current game turn +20. Skips do not renew the expiry. The strategy respects blocked outer layers when changing shirts/suits, other slots remain usable, and arrange/drop retain blocked equipped armor. The original cursed and welded guards remain unchanged; no 1000-turn welded extension or escape actions were imported.

Runtime baseline: `github.com/Xenox-developer/nethacker@56cd7f631d7a2400ec3366aa2d7f539524829572`, program `prog_64e10a9e6ae1e9aa93ffcdca5dc14e17`. Full historical digest `sha256:1e2f694943be0b87314c48f014bb290a26f836957193130ca90e319899552230` is provenance, not the hash of the reduced runtime asset. All 51 supplied runtime file hashes and both reference hashes were verified in `private31_experiment/asset-verification.json`. Attempt31 is daglar `5d0d455a1585271143aa47fbd5b44c2f6dae7d4b` plus attempt28 depth>=20 bypass, exact adapter and blind cap6. It is not the attempt30/35 vkurenkov runtime.

Mechanism influence: `github.com/eL1fe/nethacker@a9e63ae735fba55510cbdd83b1545d4ad9f04f94`, `engines/dag/autoascend/item/inventory.py`. Only the bounded trap-refusal mechanism was adapted. The full MIT license (Copyright © 2022 Maciej Sypetkowski, Michał Sypetkowski) is retained in both arms and the candidate root LICENSE; the reference engine license is byte-identical. Native incoming parents are preserved in the candidate manifest separately from runtime authorship.

## Freeze and validation

`private31_experiment/freeze.json` records per-file baseline/candidate hashes and the pre-game timestamp. `policy.diff` is the exact uninstrumented policy change; `evaluated-policy.diff` compares evaluated inventory files; `baseline-diagnostic.diff` and `candidate-diagnostic.diff` record integration. `trap_diagnostics.py` is byte-identical across arms, default off. `incoming-outer-champion.tar.gz` preserves the incoming workspace runtime; supplied and historical trees were not edited.

Production-path fixtures passed: baseline 13, candidate 17. They cover all five refusal patterns for wear/takeoff, same-turn and turn19 suppression without expiry extension, success at turn20, unrelated-message assertions, ordinary success, cursed items and welded guards, strategy termination, other-slot progress, arrange retention and direct drop rejection, blocked outer layers, and continuation into normal gameplay. These use production methods with controlled inventory/agent responses; they are not gameplay wins. Default-off and unwritable-log-path runs also passed. Raw fixture output and bounded fixture diagnostics are retained. Before evaluation, diagnostic accounting was repaired to distinguish a newly encountered refusal from an already-blocked entry; direct drop coverage was added. No gameplay ran before these repairs and freeze.

## Fixed measurements

All four batches ran sequentially: baseline27, candidate27, baseline-repeat15, candidate-repeat15. Public seeds 0–14, additional development 3200–3211. Native `nethackers.arena.run`, secret public, namespace local, val-dwa-law-fem, max_steps 1,000,000, no_progress 10,000, action_timeout 120 seconds, at most four episodes concurrently. Commands, start/finish times, exit codes, stdout/stderr and every raw row are retained. No ordinary death was rerolled, no rows omitted, and arms stayed frozen. This is 84 games with repeated Public seeds, not 42 independent trajectories per arm. The extra panel is development, not Private or native fresh validation.

| Panel | n per arm | Baseline mean | Candidate mean | Paired delta | Gains / ties / losses |
|---|---:|---:|---:|---:|---|
| primary Public | 15 | 0.423448730899 | 0.414410228903 | -0.009038501996 | 0 / 13 / 2 |
| extra development12 | 12 | 0.407260819321 | 0.407260819321 | +0.000000000000 | 0 / 12 / 0 |
| repeat Public | 15 | 0.429769016743 | 0.423422797929 | -0.006346218814 | 0 / 13 / 2 |

## Repeat variability

Each unchanged arm repeats the complete Public batch. Primary results remain primary; no favorable-row averaging or pooled selection score is used. In the following table gains/losses mean repeat relative to that arm’s primary.

| Arm | Primary mean | Repeat mean | Repeat minus primary | Gains / ties / losses |
|---|---:|---:|---:|---|
| baseline | 0.423448730899 | 0.429769016743 | +0.006320285844 | 2 / 12 / 1 |
| candidate | 0.414410228903 | 0.423422797929 | +0.009012569026 | 1 / 14 / 0 |

## Behavioral coverage and limitations

Diagnostics write at most 2,000 event records plus one truncation marker per process. Streams are process-scoped and do not inspect seeds or evaluator internals. Refusals include the slot, turn, expiry and bounded message. Suppression records mark a true cooldown eligibility check that prevents an operation or keeps equipped armor forced; repeated checks are not unique game actions. Successful post-expiry records require a normal success message. Baseline only observes; its policy has no cooldown state. Logging consumes no RNG, issues no actions, and catches log failures.

```json
{
  "baseline-primary": {
    "streams": 27,
    "events": {
      "enabled": 27
    },
    "expected_episodes": 27
  },
  "candidate-primary": {
    "streams": 27,
    "events": {
      "enabled": 27
    },
    "expected_episodes": 27
  },
  "baseline-repeat": {
    "streams": 15,
    "events": {
      "enabled": 15
    },
    "expected_episodes": 15
  },
  "candidate-repeat": {
    "streams": 15,
    "events": {
      "enabled": 15
    },
    "expected_episodes": 15
  }
}
```

No matching refusal was observed in any gameplay stream. Therefore these scores do not demonstrate a causal benefit from the mechanism. Fixture coverage establishes the intended behavior only. Any score differences despite zero observed activation must be interpreted as run variability, not evidence that this cooldown improved play.

## Technical outcomes

- baseline-primary: 27 rows; statuses {'completed': 27}; 0 rows with errors; exit metadata `baseline-primary-exit.json`. All losses and warnings are retained in the raw files.
- candidate-primary: 27 rows; statuses {'completed': 27}; 0 rows with errors; exit metadata `candidate-primary-exit.json`. All losses and warnings are retained in the raw files.
- baseline-repeat: 15 rows; statuses {'completed': 15}; 0 rows with errors; exit metadata `baseline-repeat-exit.json`. All losses and warnings are retained in the raw files.
- candidate-repeat: 15 rows; statuses {'completed': 15}; 0 rows with errors; exit metadata `candidate-repeat-exit.json`. All losses and warnings are retained in the raw files.

## Native disposition

The tested candidate is left in `/workspace` for ordinary native Public scoring and publication regardless of internal results. This experiment does not manually promote it or replace the incoming champion. Promotion still requires native same-run Public improvement and fresh validation against the actual incoming champion. No new Private result is inferred; the historical 0.4091219692062755 Private result belongs only to attempt31, and its historical generalist grid was partial (63/73). Native outer scoring/publication are pending the enclosing workflow.

## Raw paired rows

### primary Public

| Seed | Baseline | Candidate | Delta |
|---:|---:|---:|---:|
| 0 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 1 | 0.161267782276848 | 0.161267782276848 | +0.000000000000000 |
| 2 | 0.445181408701678 | 0.445181408701678 | +0.000000000000000 |
| 3 | 0.554357204486626 | 0.506760563380282 | -0.047596641106345 |
| 4 | 0.036887590648350 | 0.036887590648350 | +0.000000000000000 |
| 5 | 0.554357204486626 | 0.554357204486626 | +0.000000000000000 |
| 6 | 0.554357204486626 | 0.466376315653031 | -0.087980888833596 |
| 7 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 8 | 0.050758371234543 | 0.050758371234543 | +0.000000000000000 |
| 9 | 0.554357204486626 | 0.554357204486626 | +0.000000000000000 |
| 10 | 0.601564851038218 | 0.601564851038218 | +0.000000000000000 |
| 11 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 12 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 13 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 14 | 0.506760563380282 | 0.506760563380282 | +0.000000000000000 |

### extra development12

| Seed | Baseline | Candidate | Delta |
|---:|---:|---:|---:|
| 3200 | 0.554357204486626 | 0.554357204486626 | +0.000000000000000 |
| 3201 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 3202 | 0.036887590648350 | 0.036887590648350 | +0.000000000000000 |
| 3203 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 3204 | 0.445181408701678 | 0.445181408701678 | +0.000000000000000 |
| 3205 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 3206 | 0.024160136550547 | 0.024160136550547 | +0.000000000000000 |
| 3207 | 0.646504941599281 | 0.646504941599281 | +0.000000000000000 |
| 3208 | 0.646504941599281 | 0.646504941599281 | +0.000000000000000 |
| 3209 | 0.161267782276848 | 0.161267782276848 | +0.000000000000000 |
| 3210 | 0.506760563380282 | 0.506760563380282 | +0.000000000000000 |
| 3211 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |

### repeat Public

| Seed | Baseline | Candidate | Delta |
|---:|---:|---:|---:|
| 0 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 1 | 0.161267782276848 | 0.161267782276848 | +0.000000000000000 |
| 2 | 0.445181408701678 | 0.445181408701678 | +0.000000000000000 |
| 3 | 0.554357204486626 | 0.506760563380282 | -0.047596641106345 |
| 4 | 0.036887590648350 | 0.036887590648350 | +0.000000000000000 |
| 5 | 0.554357204486626 | 0.554357204486626 | +0.000000000000000 |
| 6 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 7 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 8 | 0.050758371234543 | 0.050758371234543 | +0.000000000000000 |
| 9 | 0.554357204486626 | 0.554357204486626 | +0.000000000000000 |
| 10 | 0.601564851038218 | 0.601564851038218 | +0.000000000000000 |
| 11 | 0.601564851038218 | 0.601564851038218 | +0.000000000000000 |
| 12 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 13 | 0.466376315653031 | 0.466376315653031 | +0.000000000000000 |
| 14 | 0.554357204486626 | 0.506760563380282 | -0.047596641106345 |

## Artifact index

All paths below are relative to `private31_experiment/`. Full raw arena rows include deaths, steps, turns, errors, and wall times; no row is replaced by its repeat.

- `baseline-primary-raw.json`, `baseline-primary.stdout`, `baseline-primary.stderr`, `baseline-primary-command.json`, `baseline-primary-exit.json`, and `diagnostics/baseline-primary/`.
- `candidate-primary-raw.json`, `candidate-primary.stdout`, `candidate-primary.stderr`, `candidate-primary-command.json`, `candidate-primary-exit.json`, and `diagnostics/candidate-primary/`.
- `baseline-repeat-raw.json`, `baseline-repeat.stdout`, `baseline-repeat.stderr`, `baseline-repeat-command.json`, `baseline-repeat-exit.json`, and `diagnostics/baseline-repeat/`.
- `candidate-repeat-raw.json`, `candidate-repeat.stdout`, `candidate-repeat.stderr`, `candidate-repeat-command.json`, `candidate-repeat-exit.json`, and `diagnostics/candidate-repeat/`.
- `results-summary.json`, `repeat-variability.json`, `diagnostic-summary.json`: machine-readable panel comparisons and coverage.
- `asset-verification.json`, `freeze.json`, `final-audit.json`, `evidence-sha256.json`: source verification, frozen arms, installation audit, artifact hashes.
- `fixtures.py`, `fixtures-*.stdout`, `fixtures-*.stderr`, `fixture-diagnostics/`: executable fixtures and raw outcomes.
- `baseline/`, `candidate/`, `policy.diff`, `evaluated-policy.diff`, `*-diagnostic.diff`, `trap_diagnostics.py`: complete evaluated sources and exact changes.
- `prepare.py`, `instrument.py`, `freeze.py`, `run_comparison.py`, `report.py`: preparation and evaluation scripts.
