# Local experiment history

These are measured outcomes from earlier runs. Avoid repeating failed ideas.

| attempt | hypothesis | public score | local validation | decision |
| --- | --- | --- | --- | --- |
| 1.1 | leave level-one farming at XL4 to find food and | 0.1086 | — | rejected |
| 2.1 | recovering HP before exploring prevents attrition deaths | 0.1512 | +0.0349 | promoted |
| 3.1 | keep distance from passive acid, paralysis, fire and stun attacks | 0.1080 | — | rejected |
| 5.1 | avoiding known petrifying corpses without gloves prevents | 0.2399 | — | rejected |
| 6.1 | starting descent at XL9 avoids attrition during the extended XL9-10 | 0.2670 | — | rejected |

## Whole-peer baselines

These exact peer commits were evaluated locally on the same 15 public games. A high Private score need not beat this bot on the public batch.

| source | public mean | compared champion | decision |
| --- | --- | --- | --- |
| `github.com/Komershan/nethacker@6073d88ea81f05d20c46c57b8fb9a38a54bfe75e` | 0.1351 | 0.1512 | not adopted: lower local public mean |
| `github.com/vkurenkov/nethacker@a5f72915d2a27db4c3835df61196dafe1ca31d7b` | 0.2692 | 0.1512 | promoted as local baseline |

## Petrifying sacrifice pickup guard (2026-09-27)

One retained strategy change: `GlobalLogic.can_sacrify` rejects cockatrice and
chickatrice corpses when no gloves are worn. The sacrifice selector also drives
item collection, so this prevents deliberate bare-handed pickup without changing
pathfinding, floor inspection, combat, or the leveling route.

Peer inspection: `github.com/vkurenkov/nethacker@ef6acf87e265f74600b914060f620d06117070a3`
contains corpse-hazard tracking and avoidance. This fix instead targets the
sacrifice selector. Existing MIT license preserved; source recorded in manifest.

Validation used foreground arena runs with `--evaluation-id local`, identity
`val-dwa-law-fem`, and two batches: `[7,2,12]` and `[4,8,9]`.

Six-seed mean: **0.379314 → 0.475424** (+0.096110).
The full 15-seed mean was not remeasured. Per-seed output: `local-eval.json`.

| Seed | Parent | Change |
| --- | ---: | ---: |
| 2 | 0.445181 | 0.445181 |
| 4 | 0.425836 | 0.425836 |
| 7 | 0.117050 | 0.646505 |
| 8 | 0.554357 | 0.601565 |
| 9 | 0.179100 | 0.179100 |
| 12 | 0.554357 | 0.554357 |

Package compilation, entrypoint import, and focused checks for both petrifying
corpse types with and without gloves, plus an ordinary corpse, passed.

Discarded experiments (all reverted): cold-resistant melee, exact critical-HP
prayer threshold, first-level farming limit, difficulty-based danger classification,
early Elbereth recovery, a bounded leveling tour, broad corpse inspection avoidance,
blind-only inspection avoidance, and a pickup-inspection fallback guard. They
either lowered sampled results or did not improve them. Broad corpse inspection
avoidance rescued seed 7 but regressed seeds 2 and 12; rejecting unsafe sacrifice
corpses preserved those two games and improved seed 7 further.
