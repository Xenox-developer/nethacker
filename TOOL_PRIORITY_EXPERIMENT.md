# Reserve the usable digging tool before optional armor

Request `20260928T014749371663Z-2917a998324541ee94ab17faa1a40624`.
Implemented and fully evaluated; **no measured Public improvement, no promotion**.
The candidate is retained as requested.

## Change and source identity

The actual incoming `/refs/parent/autoascend/global_logic.py:70–89` selects the
known weapon, known armor, unknown-status weapon/armor, then the digging tool.
The candidate reserves the existing eligible tool after the known weapon and
before the first armor pass. The existing later tool call remains idempotent.
No eligibility, forced/cursed equipment, shield, XL, weight/slot, or dive gates
were changed. `keep_digging_tool()` still gates reservation; the current tour
flags remain disabled. All other incoming Python sources are byte-identical.

Source motivation/adapted priority block:
`github.com/daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b`,
available in `/refs/peers/peer1/autoascend/global_logic.py:79–86` and
`autoascend/jf_config.py:397` (`TOOL_KEEP_FIRST`). The pinned influence is added
to `nethackers.solution.json`. The existing root `LICENSE` exactly retains the
peer's complete MIT copyright/permission notice (Maciej Sypetkowski and Michał
Sypetkowski, 2022). No unrelated peer features were copied.

Exact patch: `tool_priority_evidence/candidate.patch`, SHA256
`6fa1d2fbce96e848e04cdeb06e99b934647f4bbfb1d79ea1eb021703c3dce177`.
`source-manifest.json` records SHA256 for every parent/candidate Python source
and solution manifest; `integrity.json` verifies them unchanged after scoring.
The only modified existing files are `global_logic.py` and the solution manifest;
`autoascend/tool_priority_observation.py` is the new optional diagnostic.

## Fixtures and integration repair

`tool_priority_evidence/fixtures.py` / `fixtures.json`: nine passing production
allocation fixtures plus a passing NumPy diagnostic-writer regression check.
Production Item, Inventory armor selection, and DiveLogic eligibility are used;
character damage estimates are fixed fixture inputs.

- Tight weight (capacity 500): parent keeps sword/mail/shield but drops pick;
  candidate keeps sword/pick/shield but drops mail.
- Tight slots (49 forced slots): tool replaces optional mail; known sword stays.
- Generous capacity (1000), no tool, and non-diving: identical selections.
- Forced cursed armor and forced overweight inventory: identical, forced
  weight remains charged; reservation cannot bypass forced equipment.
- Forced tool: identical selection, no double charge.
- Cursed shield plus mattock: tool remains ineligible; identical selection.

Every fixture checks candidate replay against actual candidate allocation,
old-order replay against the actual parent `_split`, unchanged item state,
and unchanged Python/NumPy RNG state. Initial fixture setup errors (empty
glyph list and a non-iterable fake inventory) were fixed before gameplay.
Compilation and imports passed.

The first opt-in seed-8 smoke run exposed a diagnostic integration defect:
NumPy capacity scalars were not JSON serializable. Its partial trace was
truncated at `capacity`; diagnostic exceptions disrupted play. The worker was
terminated deliberately, yielding a retained native `infrastructure_error`
at 32,557 steps / 879 turns. This is invalid evidence of policy performance.
The writer now serializes NumPy scalars and catches write errors; the regression
fixture exercises the real writer. This repair preceded both valid development
games and all Public scoring. No policy thresholds changed after outcomes.
Original diagnostic source, partial trace, arena log, and native error result
are retained in `tool_priority_evidence/integration-bug/`. One technical retry;
no ordinary deaths rerolled.

## Development mechanism evidence (separate from Public)

Opt in with `TOOL_PRIORITY_OBSERVE=/absolute/output/directory`. Diagnostics record
existing add-item calls and replay capacity accounting with the early reservation
omitted. They never rerun selectors, consume RNG, issue actions, mutate items,
or inspect seeds/evaluator internals/scores. Candidate replay is cross-checked
against actual allocation. Replay is bounded to 20,000 calls per process;
examples to 30 changed and 10 unchanged calls. Output is persisted during play.
Seed labels below belong only to the external run records, not the counters.

| Development game | Visits / compared | Retention gate | Eligible tool | Changed tool / armor allocations | Score |
|---|---:|---:|---:|---:|---:|
| 8 (repaired) | 9761 | 7137 | 7020 | 450 / 450 | 0.6015648510 |
| 11 | 2228 | 1001 | 0 | 0 / 0 | 0.4663763157 |

Neither run had replay mismatches or diagnostic write errors. Seed 8 traces
show capacity 950, forced weight 370 / five forced slots, a retained pick-axe,
and displaced optional crystal plate mail (weight 450); freed capacity also
admits supplies. Seed 11 is a negative example: gate visits without an eligible
tool or any changed allocation. Non-diving negatives are retained too.

Evidence paths (all under `tool_priority_evidence/`):
`dev8-fixed.json`, `dev8-fixed.log`, `dev8-fixed/observation-235.json`;
`dev11.json`, `dev11.log`, and `dev11/observation-*.json`.
These are candidate-only exploratory games, not a separate paired score claim.
Seed 8 died of starvation at depth 28; seed 11 died to an invisible stalker at 25.

## Full native Public15 comparison

Both arms used `python -m nethackers.arena.run --solution <arm> --batch
'[[0,"val-dwa-law-fem"],..., [14,"val-dwa-law-fem"]]' --evaluation-id local
--out <result>` with all native default limits and diagnostics disabled.
Each was one foreground command, awaited fully; no source tree was edited while
its evaluation ran. Exact batches and run provenance are in `runs.json`.

| Arm | Mean progression | Completed |
|---|---:|---:|
| Fresh incoming parent | 0.48754987757483376 | 15/15 |
| Final candidate | 0.4782335856935671 | 15/15 |
| Difference | -0.009316291881266647 | 0 gains / 14 ties / 1 loss |

Seed 1 falls from 0.6465049416 (depth 29, minotaur) to 0.5067605634
(depth 26, soldier ant). All other scores tie. Seeds 8/11 both tie their parent
scores; seed 8's death changes from captain to starvation. No scoring errors.
Full raw results/logs: `parent-public15.{json,log}` and
`candidate-public15.{json,log}`. `comparison.json` contains all paired rows.
There were 30 Public games, two valid development games, and one interrupted
technical smoke run; no additional controls or ordinary-death retries.

No Public improvement means no fresh-validation gate is triggered by this
comparison. The outer evolve harness retains authority over its own same-run
Public/fresh-validation decision; no hidden/fresh seeds or older champion mean
were used to claim improvement or promotion.

## Interpretation and limitations

Mechanism activation is demonstrated, but it did not raise full Public score.
Allocation counts include repeated proposed inventory decisions, not independent
retention events or confirmed equip/drop actions. Replaying a single allocation
does not predict later combat, hunger, or alternate game trajectories. Seed 1
has no diagnostic trace here, so its loss is not causally attributed to armor
loss. Seed 8 shows changed allocations and a score tie, not evidence of benefit.

The unchanged parent's fresh seed-9 score (0.5543572045) differs from the supplied
stored result (0.5067605634); other unchanged-parent death/turn details vary too.
This limits causal certainty and rules out treating an older stored mean as the
control. No extra control campaign or unrelated optimization was attempted.
