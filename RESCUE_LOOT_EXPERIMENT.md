# Rescue looting experiment

Hypothesis: during a failed-prayer rescue dive, limiting incidental inspection of unknown ground items to two BFS steps avoids long detours while hunger makes descent urgent. Normal dives retain the original behavior. This changes only Inventory.check_items; other food, pickup, tool-search and exploration strategies remain available.

The parent seed-2 trace reproduced the reference death and showed repeated check_items trips, blocked movement, and prolonged residence on depth 7 before death. This motivates reducing incidental detours; it does not establish that every later death is caused by looting.

Peer review: inspected pinned peer1 combat threat heuristics, peer2 descent/exploration logic, and peer3 dive_logic.py (especially bounded exploration and rescue routing). The retained change is original; no peer code was copied. Existing source attributions and licenses remain intact.

## Local validation

Ran two foreground arena commands with --evaluation-id local, identity val-dwa-law-fem, batches [1,2,6,7,10] and [0,4,8,12,13]. Results are in rescue-loot-eval.json. Compared with /refs/parent-eval.json.

| Seed | Parent | Candidate |
| --- | ---: | ---: |
| 0 | 0.425836075 | 0.425836075 |
| 1 | 0.506760563 | 0.506760563 |
| 2 | 0.050758371 | 0.097709352 |
| 4 | 0.425836075 | 0.425836075 |
| 6 | 0.554357204 | 0.554357204 |
| 7 | 0.646504942 | 0.646504942 |
| 8 | 0.601564851 | 0.601564851 |
| 10 | 0.601564851 | 0.601564851 |
| 12 | 0.425836075 | 0.425836075 |
| 13 | 0.206128548 | 0.206128548 |
| Mean | 0.444514756 | 0.449209854 |

One gain, nine score ties. Seed 2 improves from depth 7 to depth 9. This is a ten-seed training comparison, not a full-15 or held-out measurement. The parent seed-2 endpoint was reproduced in a fresh diagnostic run; the retained candidate endpoint also matches the preliminary broader-looting candidate on that rescue game.

Python compileall and make_agent/reset/act interface import checks passed. arena_adapter.py and bot.py are unchanged.

## Reverted trials

- Species movement speed instead of name-based combat speed: four score ties on 2/4/8/13.
- Increase sighted digging-engraving retry allowance: four score ties on 0/4/12/13.
- Nearby-only item inspection for all dives: gains on 2/13 but substantial regressions on 1/6/7/10. Rejected; the final condition is restricted to the existing failed-prayer rescue state.
