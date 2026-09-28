# Peer depth-20 protection experiment

Request: `20260928T034110788586Z-a8629597f5574a028233d9f49b55a435`.

Complete pinned peer runtime: `github.com/daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b`, verified against read-only `/refs/peers/SOURCES.md`. The only runtime difference is the depth >= 20 bypass in `_elbereth_before_digging_escape`. Own influence: `github.com/Xenox-developer/nethacker@7d546b6ab2b972c793489801f609aa691fc82b44`, adapted from the supplied accepted28 diff. Peer license and metadata attribution are preserved. The peer adapter was copied unchanged because its prayer-state handling is part of the requested complete runtime. No incoming-champion policy changes were merged.

Hypothesis: pre-dig engraving at depth >=20 may protect against unseen arrivals. This is a new interaction experiment, not an established combined gain.

## Protocol

46 fresh games: 23 per arm, Public 0–14 and development 3000–3007. Baseline arm completed before hybrid began. Native arena, public secret, local namespace, val-dwa-law-fem, max_steps 1,000,000, no_progress 10,000, action_timeout 120 seconds, max concurrency 4. Exact commands, elapsed times, raw rows, stdout/stderr, patch and SHA-256 manifests are in `evaluation/peer-depth20/`. No death rerolls, omissions, threshold tuning, or policy changes during evaluation. Development 3000–3007 was already used in attempt29; it is not a holdout.

## Fixtures and implementation checks

Both actual helpers imported and passed depth19/20, early Medusa, Weak hunger, intact engraving, polymorph, can_engrave, swallowing, pit rewrite, nearby susceptible monster, sighted cap 4, blind cap 6 despite repeated damage, blind no-new-damage suppression, and unchanged DIG_ESCAPE/Gehennom dispatch fixtures. Only the hybrid depth20 case gained eligibility and called the mock engraving action. ELBERETH_ALWAYS=False and TOOL_RUN_XL=None verified. All other runtime source hashes match the pinned peer.

A pre-evaluation test-only repair replaced list dummy glyphs with an int16 ndarray. Original fixture and error details are retained in `technical-repair.txt` and `fixtures-before-repair.py`. No arena comparison had started; no policy repair was made.

## Paired results

| Group | Games/arm | Baseline mean | Hybrid mean | Delta | Gains / ties / losses |
| --- | ---: | ---: | ---: | ---: | --- |
| Public | 15 | 0.422035737103 | 0.420756447718 | -0.001279289385 | 2 / 12 / 1 |
| development | 8 | 0.388597114487 | 0.411423943817 | +0.022826829330 | 2 / 6 / 0 |

Public slightly regressed (-0.001279289385), while the reused development panel improved (+0.022826829330). This mixed result does not demonstrate a general improvement. Public gains were seeds 3 and 13; seed 12 was the loss. Development gains were 3005 and 3006, with the other six tied. Mean turns were Public 13,843.73 → 13,172.87 and development 12,523.38 → 13,125.88; these totals cannot isolate engraving costs.

All per-game outcomes, including counterexamples:

| Group / seed | Baseline | Hybrid | Delta | Baseline turns / hybrid | Baseline death | Hybrid death |
| --- | ---: | ---: | ---: | --- | --- | --- |
| Public 0 | 0.466376315653 | 0.466376315653 | +0.000000000000 | 11410 / 11414 | killed by a minotaur | killed by a minotaur |
| Public 1 | 0.161267782277 | 0.161267782277 | +0.000000000000 | 8907 / 8907 | killed by a bolt of lightning | killed by a bolt of lightning |
| Public 2 | 0.445181408702 | 0.445181408702 | +0.000000000000 | 16444 / 16458 | killed by a raven | killed by a raven |
| Public 3 | 0.506760563380 | 0.554357204487 | +0.047596641106 | 13816 / 13928 | killed by a giant eel | drowned in a moat by a giant eel |
| Public 4 | 0.036887590648 | 0.036887590648 | +0.000000000000 | 6965 / 6965 | killed by a hill orc | killed by a hill orc |
| Public 5 | 0.554357204487 | 0.554357204487 | +0.000000000000 | 15654 / 15706 | killed by a raven | killed by a chameleon imitating a minotaur |
| Public 6 | 0.466376315653 | 0.466376315653 | +0.000000000000 | 11147 / 11124 | drowned in deep water | killed by a pit viper |
| Public 7 | 0.466376315653 | 0.466376315653 | +0.000000000000 | 15762 / 15904 | killed by a raven | killed by a raven |
| Public 8 | 0.050758371235 | 0.050758371235 | +0.000000000000 | 13177 / 13177 | killed by a giant bat | killed by a giant bat |
| Public 9 | 0.554357204487 | 0.554357204487 | +0.000000000000 | 15683 / 15660 | killed by a minotaur | killed by a minotaur |
| Public 10 | 0.601564851038 | 0.601564851038 | +0.000000000000 | 21417 / 21410 | killed by an umber hulk | killed by a minotaur |
| Public 11 | 0.466376315653 | 0.466376315653 | +0.000000000000 | 13510 / 13519 | killed by a cobra | drowned in deep water |
| Public 12 | 0.554357204487 | 0.466376315653 | -0.087980888834 | 12109 / 11919 | killed by a xorn | killed by a minotaur |
| Public 13 | 0.445181408702 | 0.466376315653 | +0.021194906951 | 10243 / 11202 | killed by a raven | killed by a minotaur |
| Public 14 | 0.554357204487 | 0.554357204487 | +0.000000000000 | 21412 / 10300 | drowned in a moat by a giant eel | killed by a shark |
| development 3000 | 0.117049964736 | 0.117049964736 | +0.000000000000 | 23624 / 23624 | killed by a soldier ant | killed by a soldier ant |
| development 3001 | 0.554357204487 | 0.554357204487 | +0.000000000000 | 9280 / 9303 | killed by a minotaur | killed by a minotaur |
| development 3002 | 0.554357204487 | 0.554357204487 | +0.000000000000 | 10730 / 10918 | killed by a kobold mummy | killed by a minotaur |
| development 3003 | 0.466376315653 | 0.466376315653 | +0.000000000000 | 10852 / 16032 | killed by a shark | killed by a fire elemental |
| development 3004 | 0.554357204487 | 0.554357204487 | +0.000000000000 | 11671 / 11684 | killed by a minotaur | killed by a minotaur |
| development 3005 | 0.445181408702 | 0.554357204487 | +0.109175795785 | 10934 / 10504 | killed by a winter wolf cub | killed by a leocrotta |
| development 3006 | 0.392937476797 | 0.466376315653 | +0.073438838856 | 11751 / 11597 | killed by a frost giant | killed by a bolt of fire |
| development 3007 | 0.024160136551 | 0.024160136551 | +0.000000000000 | 11345 / 11345 | killed by a bolt of lightning | killed by a bolt of lightning |

## Activation, uncertainty, and disposition

Arena error/non-completed rows: 0; preserved in `errors.json` and the full raw rows. Runtime warnings are preserved in arm logs. No optional counters were added. Real-game helper visits, depth-only eligibility, and resulting engraving actions were not measured. Fixture calls are not evidence of real-game activation. Any apparent gain is low-confidence without actual action evidence; outcome differences alone cannot attribute the mechanism.

Extra engraving can consume turns and nutrition, delay escape, and fail against Elbereth-immune enemies. Caps remain intact but do not remove these costs. Whole-game turn differences are descriptive, not measurements of engraving overhead. Repeated Public outcomes have varied historically; this is one paired run, not proof of deterministic replication or generalization.

Attempt28 improved its own Public comparison but tied fresh1081–1083 and did not retest failed21’s1060–1062. The depth restriction is not proven to repair those failures. Attempt29’s prior Public loss and development gain are context only, not reused measurements. The peer author’s Private score is not our result.

The fully tested hybrid remains in `/workspace` for native outer full Public/publication regardless of this internal comparison. The actual incoming local champion remains the outer parent, preserved read-only in `/refs/parent`; its supplied evaluation is copied separately for provenance. Internal pinned-peer results do not establish improvement over that champion. Native same-run Public and fresh validation remain the only local promotion gates. Outer evaluation, fresh validation, and organizer Private results for this candidate are not yet available; no promotion or publication result is claimed.
