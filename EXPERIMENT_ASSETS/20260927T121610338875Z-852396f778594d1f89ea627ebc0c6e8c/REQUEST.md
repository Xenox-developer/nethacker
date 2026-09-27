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
