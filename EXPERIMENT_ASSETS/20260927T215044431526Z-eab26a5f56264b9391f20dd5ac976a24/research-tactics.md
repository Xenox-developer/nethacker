# Tactical research for the next controlled batch

Read-only research; no bot changes or evaluations performed. Inspected champion20, SHA256 `39c189656f92b62e57ea28399e2e8794c9446afe3f6dc21fec0afdf5002836aa`, Public `0.47506047628647746`. Source paths below are relative to that champion under `.nethackers-lab/val-dwa-law-fem/champions/`. Attempt21 was active during research; the campaign must use its actual next frozen input, preserving attempt21 if promoted. Do not replace that input with champion20 merely because these line numbers refer to it.

## What the primary literature supports

The original AutoAscend submission describes a hierarchy of explicit behaviors, combat damage estimates, avoiding dangerous passive/contact effects, avoiding rays through friendly creatures, and probability-weighted simulation of reflected wand trajectories. These are already part of this bot family, so importing them again is not a novel experiment. Its per-action diagnostics are useful here: a final death label cannot establish which tactical decision caused it. [NetHack Challenge appendix, AutoAscend section](https://proceedings.mlr.press/v176/hambro22a/hambro22a-supp.pdf).

The later HiHack paper describes AutoAscend as explicit strategies coordinated by predicates and records the active strategy on each action. That supports keeping changes inside a small existing controller decision and recording whether the new condition actually fired. It does not establish that either proposal below improves our score. [NetHack is Hard to Hack, section 3.2](https://papers.nips.cc/paper_files/paper/2023/file/764ba7236fb63743014fafbd87dd4f0e-Paper-Conference.pdf).

## A — repair branch bookkeeping in existing wand planning

**Recommended planning single.** Exact hook: `autoascend/combat/fight_heur.py:177–206`, `_simulate_wand_path`; called with range13 at lines209–218, then scored by `get_potential_wand_usages` at221–255 and included by `get_available_actions` at303 onward. Combat selection remains in `autoascend/agent.py:1820`, `fight2`.

Two concrete implementation errors occur together at a stochastic reflection:

1. A hit on the immediate successor receives `probability * next_prob`, but recursion passes `1.0`. Descendant hits forget the probability of their path. For a 5% branch followed by a deterministic step, a descendant is credited with mass1 instead of0.05.
2. The loop subtracts reflection and encounter costs directly from `range_left`. Each sibling outcome therefore inherits costs spent by earlier, mutually exclusive outcomes. Target weights can depend on branch enumeration order.

The same implementation is present in [upstream AutoAscend fight_heur.py](https://raw.githubusercontent.com/maciej-sypetkowski/autoascend/master/autoascend/combat/fight_heur.py). This is a mathematical consistency finding, not a claim about a measured game failure.

**Frozen change boundary:** calculate a fresh branch-local remaining range and branch probability for each successor; pass that probability into recursion. Preserve the existing initial range13, successor geometry/probabilities, encounter range costs, supported wand set, action candidates and all friendly/self/enemy priority constants. Preserve urgent preemptions and unknown-wand last-resort handling. Do not expand this into a new combat planner.

The engine has additional details beyond this approximation: `buzz` samples initial range and successful impacts affect remaining range. Those deserve separate hypotheses, not changes bundled with bookkeeping. [NLE zap.c](https://raw.githubusercontent.com/facebookresearch/nle/main/src/zap.c). NLE main is reference source, not proof of the exact pinned arena revision; verify version inside the official mutator before changing engine physics. The two bookkeeping errors do not depend on that version.

**Direct tests:** straight path unchanged; deterministic reflection unchanged; probability retained over at least two descendants after a5% split; sibling permutation produces identical weights; a range-consuming target on one branch does not shorten its sibling; mirrored fixture preserves mirrored weights; self/pet/peaceful labels and penalties retained; a complete action-ranking fixture changes the selected existing wand/direction for the intended reason. Do **not** assert sum of weights over all targets ≤1: rays can legitimately hit several targets or the same target repeatedly. Assert expected path mass at specified states/acyclic targets instead. Confirm bounded runtime with the existing horizon.

**Activation evidence:** count decisions with a stochastic branch, decisions whose target weights or wand scores differ, and actual selected-root differences. For a bounded sample of changed decisions, record wand, direction, old/new target weights and chosen action. No action override is demonstrated merely by a score change. Register any new `StatsLogger` event names (`stats_logger.py:43` validates them), or use a bounded diagnostic log. Avoid repeating attempt8's initial unregistered-counter error.

## C — an observed failure exception to Elbereth emergency suppression

**Recommended survival single if the batch needs this third family.** Narrow scope: change only eligibility of the existing last-resort block, not Elbereth rest, digging, melee, prayer thresholds or retreat ordering.

At `autoascend/agent.py:2387–2393`, `LR_ELBERETH` clears the adjacent-enemy list when nearby species appear susceptible and the engraving exists or can be written. This suppresses the entire emergency block, including available stairs and known digging escape. Species are insufficient to establish protection: the engine's `onscary` ignores Elbereth for an individually blind monster, information not supplied by the species object. [NLE monmove.c, onscary](https://raw.githubusercontent.com/facebookresearch/nle/main/src/monmove.c). Enemy ray effects are another reason observed damage need not respect a floor engraving; see `buzz` in the linked zap.c. Do not infer which mechanism occurred from HP loss alone.

**Frozen trigger and implementation:** record consecutive distinct game-turn observations in `DiveLogic.update` (`autoascend/dive_logic.py:555–567`). Mark an unsafe-protection observation only when:

- both observations have the same level key and player tile, and exact intact Elbereth text;
- the turn advanced by exactly1, max HP is unchanged, and neither observation is polymorphed;
- current HP is lower than previous HP.

Keep a marker scoped to that level/tile for at most3 game turns after the latest qualifying loss. Clear it when leaving the tile/level or when Elbereth is no longer intact. During this short window, skip only `LR_ELBERETH`'s `adjacent=[]` suppression. The original critically-low-HP, adjacent-hostile, burden and polymorph-buffer gates still decide whether emergency actions can run; retain their existing action ordering. At expiry the previous suppression resumes. Do not inhibit proactive engraving merely because it has not yet been tested by an attacker.

The existing `_hurt_on_elbereth` field (line545, updated564) lacks previous position/level/engraving attribution; it is used for unknown-monster melee policy at1179. Leave that existing behavior alone and add a separately scoped observation/helper for this hypothesis. The later `elbereth_futile` calculation in `agent.py:2440` already acknowledges recent damage, but occurs after suppression and controls a separate desperate-prayer feature; reusing it alone cannot fix this eligibility gap.

**Tests:** no marker from damage on arrival, level transition, newly written engraving, turn gap, max-HP change or polymorph; marker from same-tile consecutive protected HP loss; marker expires exactly at specified boundary and clears on leaving/erasure; marker changes only last-resort eligibility while retaining all ordinary gates/action order; unchanged no-damage Elbereth case still suppresses emergency gambles; repeated observations in the same game turn do not extend the marker. Log qualified observations, suppression bypasses and the actual emergency action selected.

**Risk and distinction:** HP loss can come from poison, hunger or another cause; the marker is evidence that remaining on this square did not prevent damage, not proof of an Elbereth-immune attacker. Re-enabling unknown-item gambles can regress games previously rescued by LR_ELBERETH. This remains a scored hypothesis. It differs from previous failed broad hold loops, HP-only rest repetition, early descent and additional species filters. It is compatible with attempt21 proactive engraving because it acts only after observed failure.

## Batch interpretation and prior evidence

Use the parent's fixed N20 protocol: Public seeds0–14 plus development2000–2004, one fresh common baseline, three isolated singles, then all combinations of singles eligible under the frozen selection rule, followed by native final scoring and the fresh3 promotion gate. Record activation before claiming tactical success. Zero activations mean the behavioral hypothesis was untested on this sample; do not broaden it or change seeds mid-comparison. Report paired gains/losses/ties as well as means.

Prior local reviews matter: attempt8's three-turn planner tied all Public results and lacked per-game activation proof; broad Elbereth hold/rest loops repeatedly caused major regressions; the accepted last-resort suppression and weak-monster burst-defense changes should be preserved outside C's explicit exception. Attempt20's apparent level-scoped engraving gain disappeared with a fresh parent control. Neither proposal repeats the already accepted `dig_first().repeat()` change. The completed history and `20260927-attempt19-20-strategy-review.md` are local evidence for these constraints, not evidence that A or C will win.
