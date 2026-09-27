# Local experiment history

These are measured outcomes from earlier runs. Avoid repeating failed ideas.

| attempt | hypothesis | public score | local validation | decision |
| --- | --- | --- | --- | --- |
| 1.1 | leave level-one farming at XL4 to find food and | 0.1086 | — | rejected |
| 2.1 | recovering HP before exploring prevents attrition deaths | 0.1512 | +0.0349 | promoted |
| 3.1 | keep distance from passive acid, paralysis, fire and stun attacks | 0.1080 | — | rejected |
| 5.1 | avoiding known petrifying corpses without gloves prevents | 0.2399 | — | rejected |
| 6.1 | starting descent at XL9 avoids attrition during the extended XL9-10 | 0.2670 | — | rejected |
| 7.1 | refusing petrifying sacrifice corpses without gloves avoids | 0.2862 | +0.0000 | promoted |

## Whole-peer baselines

These exact peer commits were evaluated locally on the same 15 public games. A high Private score need not beat this bot on the public batch.

| source | public mean | compared champion | decision |
| --- | --- | --- | --- |
| `github.com/Komershan/nethacker@6073d88ea81f05d20c46c57b8fb9a38a54bfe75e` | 0.1351 | 0.1512 | not adopted: lower local public mean |
| `github.com/vkurenkov/nethacker@a5f72915d2a27db4c3835df61196dafe1ca31d7b` | 0.2692 | 0.1512 | promoted as local baseline |

# REQUIRED EXPERIMENT FOR THIS ATTEMPT: tactical-lookahead

Request ID: `20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c`

Implement and evaluate this queued user request in this attempt. Use the history above to avoid repeating failed approaches. The request is an experiment, not a measured improvement.

# Implement and evaluate bounded tactical lookahead

The user explicitly requests an actual multi-turn planner in the playing bot.
This is the required mechanism for this attempt. Do not substitute an unrelated
heuristic, whole-peer replacement, or a one-step heatmap with a lookahead name.
The attached assets are our own reviewed implementation proposal. Inspect them,
integrate them in this evolve workspace, and repair any actual incompatibility.
Do not modify the read-only parent, scoring code, seeds, or arena environment.

## Concrete implementation

- `planner.py` is a pure Python, deterministic, bounded three-exchange search.
  It models player movement/melee and enemy movement/contact attacks under two
  approximate response hypotheses. It returns only a supplied existing root
  action, requires a safety margin, and exposes a forecast trace/node count.
- `adapter.py` builds the model solely from public observations and species
  constants. It starts narrowly: low-health ordinary physical fights while
  diving, already wielding the best melee weapon, no serious conditions, and
  known safe terrain. Urgent/special actions and forced-attack recovery retain
  their current priority. Unsupported states retain the existing policy.
- `install.py` copies the modules into `autoascend/combat/`, inserts the call
  immediately after fight2's existing argmax and before action execution, and
  enables `jf_config.TACTICAL_LOOKAHEAD`. Inspect the current parent's layout
  before running the installer; adapt manually if another validated attempt
  legitimately changed that code. Preserve the current parent's other fixes.

Run `python EXPERIMENT_ASSETS/<request-id>/install.py /workspace`, using the
actual frozen directory listed below this brief. The initial seed contains
inactive assets only; its baseline still runs the original policy.

## Verification and measurement

1. Run the bundled `selftest.py`, compile the changed bot, and import its real
   entrypoint inside the official container. Verify that a constructed combat
   fixture actually calls the adapter and can choose a different legal action.
   Test specials, forced attacks, weapon switching, unsupported enemies and
   conditions as fallbacks. Test geometry and occupancy against real NLE masks.
2. Check node budget, determinism and runtime at the maximum supported local
   geometry. A three-turn fixture must demonstrate an outcome that a one-turn
   planner misses. Intermediate death must remain terminal.
3. Use at most two small paired arena batches (e.g. three seeds each) to detect
   crashes or gross regressions before finishing. The outer evolve will perform
   the full 15-game Public evaluation and publication. Do not spend the entire
   attempt exploring unrelated changes or tuning to one rescued Public seed.
4. Keep a working, enabled implementation of this requested feature as the
   final candidate even when a small sample is inconclusive or regresses. The
   lab's full Public and fresh local validation gates decide whether it becomes
   champion. Never fake an improvement or disable all eligible cases to report
   unchanged behavior as a successful planner. If the model cannot be made safe
   to run, report the concrete blocker instead of claiming implementation.
5. Record exact changes, unit checks, sample results and limitations in
   `EXPERIMENTS.md`. Keep lineage/license files. Include a short `# hypothesis:`
   comment on the integration so the lab records this mechanism correctly.

This is an approximate observation-based model, not an exact clone of NetHack.
Individual enemy HP, future random rolls and movement energy are not observed.
Conservative estimates, fallback coverage and evaluation results must be stated
honestly. Do not add network/LLM calls to per-turn decisions.


Frozen implementation assets available in this input tree:

- `EXPERIMENT_ASSETS/20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c/README.md`
- `EXPERIMENT_ASSETS/20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c/REQUEST.md`
- `EXPERIMENT_ASSETS/20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c/adapter.py`
- `EXPERIMENT_ASSETS/20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c/install.py`
- `EXPERIMENT_ASSETS/20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c/planner.py`
- `EXPERIMENT_ASSETS/20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c/selftest.py`
- `EXPERIMENT_ASSETS/20260927T121610338875Z-852396f778594d1f89ea627ebc0c6e8c/verify_integration.py`


## Implemented tactical lookahead — 2026-09-27

Hypothesis: bounded three-exchange search avoids lethal tactical choices that
single-action priorities miss. This is one combat-selection mechanism; the
original policy remains responsible for unsupported situations.

Implementation:
- Installed the frozen request's planner and adapter as
  `autoascend/combat/lookahead.py` and `lookahead_adapter.py`.
- Hooked selection into `Agent.fight2` after the existing priority/forced-action
  filters, with the required hypothesis comment. Search returns an existing
  root move/melee action only, using two deterministic response estimates,
  depth 3, beam width 6, and at most 160 transitions per root.
- Enabled `TACTICAL_LOOKAHEAD`; placed the switch before existing development
  environment overrides so it follows the other configuration switches.
- Repaired an actual integration incompatibility: StatsLogger requires event
  names to be registered. Added plan, override and unsupported counters.
- Preserved bot/adapter contract, lineage manifest and licenses.

Reference review: inspected pinned peer3
`github.com/vkurenkov/nethacker@ef6acf87e265f74600b914060f620d06117070a3`,
its MIT license and fight2 implementation. Its trap-aware action filtering
reinforces the need to exclude unsupported movement geometry. No additional
peer mechanism or architecture was incorporated; implementation comes from the
frozen request assets already in this tree. Peer3 is already in the manifest.

Validation:
- Bundled selftest: 5 passed.
- Installed-module tests: `python -m unittest discover -s tests -p
  'test_lookahead.py' -v`: 6 passed. Includes three-turn dead end versus
  one-turn search, terminal intermediate death, deterministic bounded search,
  incomplete-horizon fallback, enemy corner movement and maximum geometry.
- Maximum adapter geometry: 121 cells, 3 enemies, 8 root actions, 456 searched
  transitions, about 0.065 seconds on this machine; identical repeated output.
- `python tests/verify_lookahead.py /workspace`: passed with real NLE species,
  glyph masks, production StatsLogger, real entrypoint import and actual fight2
  strategy executing a different legal action. Checks specials, forced attack,
  conditions, weapon switching, unsupported monsters/observations, doors,
  traps, boulders, pets, peaceful occupants, unknown terrain and corpse hazards.
- `python -m compileall -q autoascend`: passed.

Measurement (two small foreground arena runs, both using evaluation-id local):

```sh
python -m nethackers.arena.run --solution /workspace --batch '[[2,"val-dwa-law-fem"],[5,"val-dwa-law-fem"],[11,"val-dwa-law-fem"]]' --evaluation-id local --out /tmp/eval-fixed.json
```

The first run used `/tmp/eval.json`, before the logger registration repair.
It completed with the same scores below but is not relied on as planner
validation because an eligible planning call could hit an unregistered event.
The second run evaluated the corrected candidate. Parent pairing uses the
provided `/refs/parent-eval.json`; no new parent run was needed.

| Seed | Parent progress | Candidate progress | Parent depth | Candidate depth |
| --- | --- | --- | --- | --- |
| 2 | 0.445181409 | 0.445181409 | 24 | 24 |
| 5 | 0.206128548 | 0.206128548 | 12 | 12 |
| 11 | 0.366112631 | 0.366112631 | 17 | 19 |
| Mean | 0.339140863 | 0.339140863 | | |

All corrected episodes completed with null error fields. Seed 2 died to a
raven, seed 5 to a Grey-elf, seed 11 to a frost giant (parent: doppelganger).
Raw corrected results are saved in `lookahead-eval.json`. The arena output
does not expose the planner counters; changed trajectory details alone do not
establish which planner actions caused them. Existing cursor-overflow warnings
also appeared during evaluation.

Limitations: this sample demonstrates no BALROG score gain, and cannot establish
an overall improvement over the 0.289 parent mean. No full 15-seed run was made.
The planner uses approximate species HP, expected damage and speed credits;
actual hidden HP, movement energy, rolls, player speed intrinsics and enemy
movement decisions are not reconstructed. It is restricted to low-health,
unencumbered, condition-free ordinary physical fights while diving, with the
best weapon already wielded and known safe terrain. Unknown hazards remain
unknown. The enabled candidate is retained per the experiment brief for the
full evaluation gate; no claim of measured improvement is made.
