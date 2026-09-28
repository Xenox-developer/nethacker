# REQUIRED EXPERIMENT FOR THIS ATTEMPT: reserve-dig-tool-before-armor

Request ID: `20260928T014749371663Z-2917a998324541ee94ab17faa1a40624`

Implement and evaluate this queued user request in full. The request is an experiment, not a measured improvement.

# Reserve the usable digging tool before optional armor

Implement and evaluate ONE new hypothesis on the actual incoming champion:
when the existing policy already wants to keep a usable digging tool during
a dive, reserve its carrying capacity before optional armor selection in
ItemPriority._split. Preserve the incoming champion's accepted changes.

Current champion20 selects armor before the tool. The existing add_item helper
is capacity/slot limited, so earlier armor can leave insufficient room for a
tool even when the tool-retention gate is true. The pinned peer provides a
concrete priority-order example, not proof that this improves our score.

## Scope and provenance

Reference: github.com/daglar-dragomirov/nethacker at
5d0d455a1585271143aa47fbd5b44c2f6dae7d4b, autoascend/global_logic.py
ItemPriority._split, and jf_config.py TOOL_KEEP_FIRST. Inspect the available
read-only peer reference. Retain its MIT copyright/permission notice and note
this pinned source if implementation is reused. Do not copy unrelated features.

Keep the existing digging-tool eligibility, forced/cursed equipment handling,
known melee-weapon preference, weight/slot accounting, shields, XL thresholds,
and dive-retention gate. Do not enable unconditional tool retention during the
early tour. The only policy change is reserving the already-eligible tool
before the existing optional armor passes. If the current incoming parent
already implements exactly this priority, document that with source evidence
and avoid falsely claiming an unchanged policy as a new implementation.

This differs from failed early tool-retention attempts5/6, shield exclusions12,
and XL6 routing23. The risk is losing useful armor or other supplies under
capacity pressure; tool survival alone is not an improvement metric.

## Evaluation

Use the existing native arena/evolve workflow, unchanged scoring and limits.
The primary comparison is the full Public15 for parent and final candidate;
the harness performs fresh local validation only after a Public improvement.
Keep the bounded candidate for this full comparison even if a small development
sample loses. Do not replace this hypothesis with another search or repeat the
completed A/B/C campaign. Never edit a source tree while its evaluation runs.

Before full scoring, use meaningful fixtures for tight capacity with changed
tool allocation, generous capacity with identical selection, no-tool and
non-diving cases, and forced/cursed equipment accounting. If an integration
bug is found, repair it before games and record it; do not tune policy thresholds
after viewing outcomes. Any exploratory games and retries must be retained,
separate from the native Public result. Do not reroll ordinary deaths.

Use opt-in bounded observation-only diagnostics in development to count actual
changed tool/armor allocations separately from policy visits. Compare old/new
allocations without consuming RNG, issuing actions or mutating game state.
Record capacity, existing eligibility and displaced gear when a decision
changes; include negative examples such as the existing weak seeds8/11.
Counters must never inspect seeds, evaluator internals or scores. If safe
counterfactual allocation is not possible, retain bounded actual-state traces
and explicitly leave causal attribution unproven.

Preserve a concise TOOL_PRIORITY_EXPERIMENT.md with the exact patch/source
identity, fixture outcomes, all development evidence paths, mechanism coverage
and limitations. A small apparent gain without a changed allocation or with
variable unchanged-parent controls is low-confidence evidence. The native
same-run full Public and fresh validation remain authoritative; no claimed
improvement or promotion is allowed from an older champion's stored mean.


# Earlier experiment context

# Local experiment history

These are measured outcomes from earlier runs. Avoid repeating failed ideas.

| attempt | hypothesis | public score | local validation | decision |
| --- | --- | --- | --- | --- |
| 7.1 | refusing petrifying sacrifice corpses without gloves avoids | 0.2862 | +0.0000 | promoted |
| 8.1 | three-turn tactical forecasts avoid near-term lethal exchanges | 0.2893 | — | rejected |
| 9.1 | give hunger prayers a longer cooldown even when fainting; | 0.2817 | — | rejected |
| 10.1 | always avoid shooting gas spores beside pets; blast kills | 0.3082 | +0.0000 | promoted |
| 11.1 | avoid a potentially lethal passive acid splash while injured, | 0.3494 | +0.0000 | promoted |
| 12.1 | during the dive, removing an uncursed shield makes a mattock | 0.3178 | — | rejected |
| 13.1 | the pinned peer's integrated descent and survival strategy will | 0.4102 | +0.0384 | promoted |
| 14.1 | collect fresh nearby kills for food without long detours | 0.4221 | -0.2078 | rejected by local validation |
| 15.1 | preserve usable Elbereth protection against susceptible enemies | 0.4393 | +0.0000 | promoted |
| 16.1 | fresh damage while blind warrants renewing Elbereth even after | 0.4362 | +0.0000 | promoted |
| 17.1 | complete an emergency dig while its safety checks hold, | — | — | error |
| 18.1 | rapid actual HP loss overrides a supposedly weak species; | 0.4415 | +0.0000 | promoted |
| 19.1 | finish a safe digging escape without interleaved combat | 0.4567 | +0.0000 | promoted |
| 20.1 | seek a digging tool at XL7 instead of spending the long | 0.4751 | +0.0873 | promoted |
| 21.1 | protect each digging phase before unseen or approaching monsters | 0.4959 | -0.0229 | rejected by local validation |
| 22.1 | nearby-only incidental looting during a failed-prayer rescue | 0.4527 | — | rejected |
| 23.1 | preserve branch probabilities and independent ranges so bounced | 0.4844 | — | rejected |
| 24.1 | ' in contents['autoascend/jf_config.py'] | 0.4751 | — | rejected |
| 25.1 | independently test ray bookkeeping, local food reserve, and observed protection failure. | 0.4751 | — | rejected |
| 26.1 | one affordable nearby ration can bridge hunger during the tool dive. | 0.4751 | — | rejected |

## Whole-peer baselines

These exact peer commits were evaluated locally on the same 15 public games. A high Private score need not beat this bot on the public batch.

| source | public mean | compared champion | decision |
| --- | --- | --- | --- |
| `github.com/Komershan/nethacker@6073d88ea81f05d20c46c57b8fb9a38a54bfe75e` | 0.1351 | 0.1512 | not adopted: lower local public mean |
| `github.com/vkurenkov/nethacker@a5f72915d2a27db4c3835df61196dafe1ca31d7b` | 0.2692 | 0.1512 | promoted as local baseline |

## Reviewed experiment notes

Reviewed 28 September 2026, 01:35 UTC. These notes cover attempts through25;
the automatically generated history table is authoritative for newer decisions.
This is experiment context, not a required new mutation or a measured gain.

## Completed repetition25; close research before ordinary further mutations

25 completed a SEPARATE second80-primary+6-control campaign, no errors/retries.
B0 Public0.4782335856935671/dev0.2803439441175858;
A=B Public0.4750604762864775/dev unchanged;
C Public0.4843767681677441/dev unchanged. C alone eligible, no combinations
required. C's primary Public1 gain +0.1397443782189996 reversed to a loss of
that size in the separate control (B0depth29,C26);9/2000 controls tied.
Outer native Public0.4843767681677441 ->0.47506047628647746,14 score ties,
loss1; no fresh and no promotion. Publication prog_4e43c501083049841276aa2ffc549fc1,
commit aad30ea58d750123eaf1c51e00f184272b8b1d0f. All19 journals complete.

Final64 sanitized files exactly match evaluated C and published source;
independent patch reconstruction passed. B's failed-target cooldown and C's
same-turn observation fixes preceded THEIR games; old/new manifests retained.
Do not pool24/25 as one unchanged implementation or claim N40 independent
seeds per arm. Same20 seeds were reused under separate implementations.
All twelve controls across24/25 remain outside primary scores.

No recorded A choice change/B purchase/C exception activation. A shadow uses
only actual filtered candidates and zips counterfactual wand lists, so differing
membership may misassociate wands; zero remains incomplete diagnostic evidence.
C's revised observation rules make its count non-equivalent to dormant B0's.
Control results again undermine causal attribution to the proposed mechanism.
This is not a proven failure of every possible food/emergency strategy.

26 is healthy and currently repeats the campaign because the host checker
rejected25's supplemental samples-<pid>.json filename. Format compatibility
and historical evidence recovery are repaired; both24/25 now pass the fresh
read-only completion check.265 focused tests passed; independent review clear.
Historical recovery will use the newest passing same-task evidence only after
the current assignment settles, preserving latest native results/last_attempt.
Do not interrupt26, edit
its bot or requeue this research ID. Once active work settles, completed24/25
must count as completion of THIS request; no repeated80-game campaign is
needed just because optional sample storage differs. Native score/promotion
and publication outcomes must be retained separately.

Next ordinary mutations should address reachable game decisions, show which
observations enable a behavior, and preserve counterexample seeds1/9 plus
previous failed seeds. A synthetic fixture can verify a rare mechanism but
cannot substitute for gameplay coverage. Reuse exact peer references with
licenses where useful; compare any new strategy to the current champion's
same-run full Public and fresh gate. Do not adopt A/C on these transient means
or repeatedly loosen B/C gates to claim that the original hypothesis worked.
Audits: reviews/20260928-attempt25-{strategy,evidence}-review.md.

Next explicit queued hypothesis, NOT YET TESTED: request
20260928T014749371663Z-2917a998324541ee94ab17faa1a40624,
reserve-dig-tool-before-armor. Reserve the already-eligible diving tool before
optional armor in ItemPriority._split, retaining existing forced equipment,
tool/dive/XL/shield gates. Source motivation: MIT daglar-dragomirov/nethacker
5d0d455a1585271143aa47fbd5b44c2f6dae7d4b, global_logic.py79–85 and jf_config
TOOL_KEEP_FIRST. Retain attribution if reused. Risk: armor displacement; measure
actual allocation differences, not only visits. This differs from failed
unconditional early retention, XL6 routing and shield removal. Native full15
and fresh gate remain required. Do not enqueue again or modify active26.

Separate unqueued possibility: existing CONTAINER_LOOP_FIX marks unsupported
multi-container squares and already skips them in check_containers/arrange_items,
but routing can still select their inspection or inaccessible contents. Peer1
inventory.py1415–1421/1714–1722 aligns those routes with the existing marker.
This is narrower than failed general loot cooldowns; risk is stale markers
suppressing newly reachable loot. Occurrence is unmeasured. Keep separate from
the tool-priority experiment. Details: reviews/20260928-next-strategy-candidates.md.

## Earlier applied research: completed24, then separate repetition25

Request20260927T215044431526Z-eab26a5f56264b9391f20dd5ac976a24 completed its
first full campaign in24: baseline/A/B/C each20,80 primary plus6 separate
controls, no errors or technical retries. The host completion checker falsely
rejected two optional summary fields; these are now accepted only after exact
recomputation. Retained24 verifies complete. Request25 was already assigned
and is healthy; do not replace its frozen protocol, rewrite input or interrupt.
Do not enqueue this same request again. If later reconciliation needs24's
completed evidence, preserve25's native outcome and all earlier history.

Primary Public/development means:
- B0:0.4782335856935671 /0.2490672556502777.
- A, cumulative wand probability and branch-local range:
  0.4843767681677441 /0.2803439441175858; Public1 gain,13 ties,1 loss.
- B, bounded shop ration:0.4750604762864775 /0.2803439441175858;
  Public0 gains,14 ties,1 loss.
- C, recent same-square Elbereth HP-loss override: same means and Public counts
  as B. Score equality does not prove identical trajectories.
A alone eligible; no pair or other combination required by the frozen rule.
Only development2000–2004 are included beyond Public0–14; they are NOT holdout.

Separate baseline/A controls1,9,2001 each tied. Both primary A gains vanished:
1:both0.5067605633802816;9:both0.5067605633802816;
2001:both0.6015648510382184. The initial baseline itself varied. Keep these
controls separate from primary records; no established cause for the variation.
Outer native A Public0.4782335856935671 ->0.47506047628647746,
14 ties and loss9, no fresh gate. Published, not promoted; champion20 stays.
Do not claim A improved using its original development score or an older
champion baseline. Program prog_3029c62d211b54db0f8dff5283a4e1db,
commit967ebf49ad182502e105a0fd204a4ac83a3e0186. All18 journals complete.

Coverage: A saved154 score-change observations, no chosen-action-change event.
The shadow selector retains actual post-filter survivors, so conditional
attack-only fallback is not independently recomputed. If branch range adds
the first reachable hostile/zap, this can miss a choice change. Zero is NOT
proof of identical choices. B has no recorded eligible transaction/purchase.
C has14 qualified HP-loss events and37 suppression considerations, but zero
exception activations. These are process-aggregate LOWER BOUNDS, no seed
attribution; do not call B/C disproven. New research should first measure
which gates prevent activation and independently reconstruct shadow choices.
Fixtures can establish eligibility/integration but are not game outcomes.
Relaxing eligibility is a NEW hypothesis requiring its own source and games.

All original/common/arm source manifests and reconstruction patches were
independently verified. Final sanitized source exactly equals evaluated A.
B's atomic inventory-refresh repair occurred BEFORE its games; baseline/A/C
were not altered during evaluation. Four copies each passed17 mechanism
fixtures; helper passed23 tests. These tests do not count among80 games.
Full report: docs/strategy-research-20260928.md. Audits:
reviews/20260928-attempt24-{strategy,evidence}-review.md.

For follow-up variations, compare to the same-run full baseline, retain fresh
local validation, and keep real losses as well as apparent gains. On variable
seeds, an unchanged-parent control must precede causal claims. Do not pool25
with24 as one preregistered sample: its implementation and additional controls
must be audited separately. Do not change active snapshots to repair counters.

## Attempt23: corrected wand calculation, no demonstrated score gain

Only branch-local ray range and cumulative branch probability survived the
adaptive screen;3 focused simulator fixtures were retained. Full Public
0.48754987757483376 ->0.4843767681677441:14 score ties, loss9 depth27->26.
A fresh UNCHANGED parent9 control exactly matches candidate9 except wall time.
Do not attribute the loss to the correction or compare its score with older
champion20's lower baseline to claim a gain. Parent22/23 Python files are
identical but Public baseline1/9 changed; the cause remains unproven. Tied7
also changed turns and death, so score ties do not imply identical trajectories.
No fresh validation followed. Published prog_3619a05513b49acd58d5b7c8b917fc9f
@03065c3188a9a60285a9d536e39ec23b03d11c95, not promoted; champion20 remains.
No real chosen-wand-action counters were retained for23. Campaign24 supplies
new diagnostics, a fixed full20 baseline and separate controls.

Reverted23: Castle enable lost1 on7 games; species-speed correction tied4;
XL6 tool route lost more on1/4/11 than gains12/13; protection-failure override
lost11 on8 games with7 ties. That C-like override ALSO rejected blindness and
only had helper fixtures, unlike24's actual LR-branch fixture. Five blocked-
loot cooldown refinements repeatedly rescued2 but lost1/6/9/11 elsewhere:
all-phases100turn, dive-only, third failure, rescue-only and rescue-after500turns.
Preserve these specific failures rather than repeatedly rediscovering them.
Detailed exact samples and parent controls: reviews/20260927-attempt23-strategy-review.md.
Full outer/publication audit: reviews/20260927-attempt23-evidence-review.md.

## Attempts21–22: measured failures, keep champion20

Attempt21 enables ELBERETH_ALWAYS=False ->True; it does not introduce a
new ELBERETH_BEFORE_DIG flag. The existing pre-dig routine can now engrave
without a nearby susceptible enemy; other eligibility and retry limits remain.
Full Public0.4750604763 ->0.4958505625: gains0/1/3/4/9, loss5, nine ties.
Fresh1060–1062 regresses0.5091646945 ->0.4862341785:1060 gains depth25->26,
1061 scoreties,1062 loses27->24. Published but rejected locally. This repeats
an earlier engraving idea on a different parent; neither the gain nor the
failure proves that the time cost caused the downstream outcome.

Attempt22 only restricts Inventory.check_items' initial candidate mask to
BFS distance<=2 when dive.diving AND dive.rescue. The rescue flag is latched;
there is no current hunger condition. Other pickup/exploration strategies
remain. The ten-game development sample excluded both9 and11. Full Public
0.4750604763 ->0.4527310694: gains2/9, loss11 depth25->2, twelve ties.
The loss outweighs gains; no fresh gate. Published, not promoted. Null
candidate_public means no selected improvement, not that it was unscored.
This is distinct from the campaign's local food-shop purchase mechanism.

Reverted22 preliminaries: species-speed correction tied2/4/8/13; sighted
engraving retry cap4->12 tied0/4/12/13; restricting inspection in ALL dives
initially gained2/13, but expanded screening lost1/6/7/10, with12 improving.
Do not repeat these as untested free gains or omit11 from later comparisons.
Score ties without activation counters do not prove an idea was exercised.
Neither21 nor22 belongs in the campaign baseline. Source/evidence audits are
reviews/20260927-attempt21-22-{strategy,evidence}-review.md.

## Organizer Private observations,01:36 UTC (separate from local selection)

Best own val Private stays19 at0.30553778869019693, rank6; best COMPLETE73/73
generalist stays14 at0.20537463447023885, rank14.19's complete generalist
0.20305495014722358, rank17;18's0.20251746854618707, rank18.
New val Private21=0.20187941176290236(rank53),22=0.18705635388680816(rank62),
23=0.22437158128169327(rank40). Generalist21 and23 now COMPLETE73/73:
0.19471524293052483(rank30) and0.19075324413861872(rank31), below14.
22 is still partial61/73; champion20 partial44/73. Do not rank their current
means as completed improvements. No val Private20/24/25 yet. These are
organizer aggregates, not per-seed causal evidence or local validation.
References and exact own rows: reviews/hub-checks.jsonl.

## Current champion 20: begin the digging-tool route at XL7

The only Python change from19 is TOOL_RUN_XL=None ->7 in dive_logic.py.
DIVE_XL stays8; first_level_done accepts7 and the helper lowers tool-equipped
DIG_DIVE_XL from8 to7. Nominal HUNT_MIN_XL follows the helper too, but
HUNT_IN_TOUR=False and the other hunt gates remain. This is a route/tool
threshold change, not unconditional early digging without a usable tool.
The hypothesis comment says food readiness is retained: only the existing
fed_for_dive() call/config is retained. DIVE_FED=False makes that method return
True immediately; default behavior does NOT require food readiness. Do not
assume this safeguard is active when reasoning about failures or follow-ups.

Full Public 0.4534966556 ->0.4750604763: four gains6/7/10/12, three losses
1/4/13, eight score ties. Seed6 rises depth2->27; losses include1:29->26,
4:27->23 and13:23->12. Fresh1057–1059 improves0.0903291734 ->0.1776091235,
with1057 depth4->24,1058 depth9->1 and1059 unchanged except wall time.
Published and promoted, digest39c189656f92b62e57ea28399e2e8794c9446afe3f6dc21fec0afdf5002836aa.
The fresh gate passed, but its aggregate gain rests on one rescue outweighing
one regression. Include failed seeds alongside winners in future screening.
Attempt21's fresh baseline reproduces all15 scores/depths and the exact mean;
seeds3/5 differ in turns/death, so this is score replication, not identical
trajectories. No action trace alone establishes why a later death occurred.

Final development8 had two gains/two losses/four ties; unsampled13 added a
substantial outer regression. Fresh parent6 reproduced its depth2 death and
candidate6 repeated the depth27 rescue. Screen1/4/13 alongside6/7 next.
Seed8 takes60145 rather than35877 turns at the same depth28: this changes
routes, not necessarily shortening every game. Peer daglar-dragomirov's pinned
c4308340c16ceb94e2e7896dd5897676b1fc3512 XL7 rationale is attributed in the
manifest, with MIT license inspected; no implementation was copied.

Two preliminary20 ideas were reverted. Unconditional pre-dig engraving gained
0 but lost4 more, with3/6 tied. Level/branch-scoped forbidden-engraving memory
had seven score ties and an apparent gain on7; a fresh parent7 reproduced the
better endpoint, removing evidence for that gain. Its level/branch/welded-hands
fixtures cover the discarded idea, not the finalXL7 change. Neither is an
untested free gain. Final20 has compile/interface checks but no dedicated
threshold/food-gate fixture or retained tool-acquisition action trace.

## Accepted attempt19: complete the interrupted digging experiment

The exact caller change dig_first().repeat() from interrupted17 was applied
on top of18, preserving the rapid-damage guard. Native full Public improved
0.4383149711 ->0.4566697650: gains1/4/9, loss7, eleven ties. Fresh1054–1056
tied at0.1750162553;1055 changed steps26005->25958, with equal turns/depth/score.
Published and promoted; the recovery request is COMPLETED. Do not requeue it
or use17's local development results as a new submission. Caller Strategy.repeat
rechecks the strategy guard but adds no explicit same-level/no-time stop.

Attempt20's same-source parent rerun differs in score only on9, falling back
from0.5543572045 to0.5067605634 (depth27->26). That endpoint variation predates
19; do not attribute19's whole mean gain uniquely to its mutation. Seed1's
digging rescue had already repeated in17's controls. The restored experiment
is now evaluated through the normal native path, unlike17's unscored auth
failure. It is not the bounded internal-loop variant reverted in18.
Attempt19 tested no other preliminary mutation. Its sample1/7/3/4 gained1/4
and tied3/7; fresh parent controls reproduced1/4. Imports/interface checks
passed, but no new fixture specifically covered repeat-loop lifecycle limits.

## Accepted attempt18: rapid damage overrides the weak-monster exception

The sole change adds `and not falling` to the lone species-level<=2, HP>=6
exception in elbereth_rest. Here falling means NOT already resting and losing
at least 30% of current max HP over the recent three turns. It permits initial
defense after observed rapid damage; HOLD_LOOP remains False, and already
resting can still hit the weak-monster exception again. This is not continuous
healing or a global combat-priority change. Other threat/engraving/dig gates
remain. Earlier accepted 13/15/16 behavior is preserved.

Final sample8 improved 0.4037620608 -> 0.4597492996, one gain/seven ties, but
outer Public only improved 0.4393360827 -> 0.4414880805: one gain, one loss,
thirteen ties. Seed 4 rises from 0.018478 to 0.466376 (depth1->25), while
unsampled 6 falls from 0.466376 to 0.050758 (depth25->2). Fresh1051–1053 tie
at 0.3278370008 in every recorded result field except wall_seconds. Published
and promoted, digest f32837beba969d8a89ea73639e0999dc35c8e03195d808ce3a757e96138b625a.
The next run's baseline repeats both4/6 endpoints. Always screen6 alongside4;
the large regression nearly cancels the rescue and has no causal action trace.

Parent seed4 was traced: dagger damage18/20->11/20, another attack before
defense ->5/20, then a smudged engraving and death. The candidate's seed4
rescue repeated and persisted in the outer run. This supports the narrow
condition diagnosis, not an explanation for seed6. Direct fixtures cover
eligibility only, not executed actions, already-resting continuation or exact
30%/three-turn boundaries; the stable11HP case also exceeds the initial40%
threshold and does not isolate the low-HP weak-monster exception.

Preliminary failures in18: the bounded digging loop tied eight scores;
requiring50 absoluteHP to fight a trivial monster while fainting tied2/4/5/8;
broad holds and HP-rest-only/descent-only/yield-at-Weak/stop-above40%-HP
variants all retained seed8's depth28->3 collapse (fresh parent controls
confirmed baseline). A12-seed floating-eye filter gained13 but lost8/9;
preserving go_to destination gained2 but lost9 badly. All were reverted.
Do not repeat these as untested ideas or substitute their fixtures for direct
coverage of the retained rapid-damage rule.

## Attempt 17: interrupted after promising local tests, not a gameplay rejection

The operator lost access with 401 token_expired after saving its local tests;
there was no native outer candidate score, publication or fresh validation.
History's generic "no public improvement" decision must not be interpreted as
a measured loss for this hypothesis. The final source changed the strategy
call to dig_first().repeat(), allowing consecutive emergency digging actions
while its strategy guard remains true. The original full15 local development
mean was 0.4393360827 -> 0.4486523746: one gain (1), one loss (7), thirteen
score ties. Fresh parent controls for 1/7 reproduced their references; the
candidate's seed-1 gain repeated, whereas 7 tied its parent on rerun. Retain
the first seed-7 loss in the original aggregate, not a favorable replacement.
At the time this locally promising variant still needed native full evaluation
and the normal fresh gate. Attempt19 has now completed both and promoted it
on the newer18 parent; do not submit17's development JSON separately.

Attempt 18's first, subsequently reverted local trial was related but not
identical: a loop internal to dig_first stopped on a level change or no time
advance. Its eight-seed sample (0/2/3/4/1/5/8/13) tied the supplied parent,
including seed 1. Attempt 17's caller-level Strategy.repeat has no explicit
same-level/no-time exit. These concrete code differences distinguish the two
hypotheses; no trace proves which difference caused the measured outcomes.
Attempt 18 later promoted a different HP-damage guard, described above.
The exact caller-repeat variant is queued as request
`20260927T193502617057Z-b70a3a1ed1eb4d31a1b0d2bbefe8d1d0`
(`resume-interrupted-dig-repeat`) with frozen diff, development evidence and
parent controls. It completed in19 at20:40 UTC, promoted while preserving18's
unrelated changes. There is no pending request or need for another enqueue.
Seven preliminary screens from 17 were reverted: broad defensive holds and
both HP-rest repetition variants severely regressed seed 8 (depth 28 -> 3);
floating-eye avoidance, pit-aware fighting, earlier wet-island retreat and
travel-destination preservation showed no expanded-sample net benefit. The
pit trial's pre-turn bytecode import error reran normally; do not classify it
as a gameplay loss. Detailed samples are in attempt 17's review.

## Earlier accepted additions: Elbereth handling in attempts 15/16

Attempt 16 was based on the integrated attempt-13 family plus LR_ELBERETH
enabled in 15 and the blind retry change in 16. Champion18 retains these.

Attempt 15 enabled only the existing LR_ELBERETH flag (plus its hypothesis
comment), preserving the rest of that family's implementation. Full Public
0.4069901063 -> 0.4393360827: two gains (3/9), one loss (4), twelve score ties.
Fresh 1042–1044 tied at 0.1774576308; 1044 had different turn counts, so the
tie does not mean identical trajectories. The gate accepted the variant.
The flag clears the last-resort block's local adjacent-monster list when
critically injured, not blind, outside Gehennom, and existing or engravable
Elbereth is considered usable against all visible nearby threats. It suppresses
the entire last-resort block, including stair escapes, not only unknown items;
it does not directly engrave/rest. Inspect the current implementation before
tightening or broadening this accepted behavior.
Fresh parent controls reproduced seeds 3/4, supporting that comparison;
include the seed-4 regression alongside seed 3 in future emergency screening.
Preliminary immunity-aware combat waiting (3/7/8/13), earlier known healing
(2/4/8/13), and CASTLE_PASSAGE (1/7/8/14) tied their samples and were reverted.
Do not repeat these as untested changes; no direct Castle activation was shown.

Attempt 16 removes the six-attempt blind Elbereth cap in both
_elbereth_possible() and _elbereth_before_digging_escape(). Actual blind
re-engraving after the first attempt still requires _hurt_since(last), using
the recent HP history; engraving eligibility/polymorph/swallow/context checks remain.
Sighted retries remain capped at four. Full Public 0.4307684166 -> 0.4361629733:
one gain (11), one loss (13), thirteen score ties. Fresh 1045–1047 tied at
0.2189769487 in every saved per-game result field except wall_seconds.
Exact paired evaluator Evidence is now saved under each future run's validation/
directory; this first retained pair is linked in attempt 16's history.

Treat attempt 16's causal gain cautiously. Attempt 15's earlier published
parent already had exactly the same score/turn/death endpoints later seen in
16's candidate on 11 and 13. Development seed 9's gain disappeared in the
outer full run, and that better endpoint had also appeared in the parent.
The gate passed against the same-run baseline, but these results do not isolate
the mechanism from demonstrated parent variation. Use fresh parent controls
and mechanism traces for a follow-up; do not describe the fresh tie as a gain.
The preliminary SKIP_SOKOBAN=True test on 0/2/3/4 matched all parent endpoint
fields except wall time and was reverted. No activation evidence establishes
whether that routing branch was exercised in this sample.

## Current baseline family: accepted whole-peer replacement in attempt 13

Attempt 13 adopted the integrated `autoascend` strategy package from
github.com/vkurenkov/nethacker@ef6acf87e265f74600b914060f620d06117070a3,
preserving its MIT license/provenance and the parent's entrypoint/arena adapter.
The package matches that pinned source except a hypothesis comment. Fourteen
existing Python modules changed and four were added. This is one explicitly
tested whole-strategy hypothesis, not evidence for each component separately.
Full Public 0.3324406823 -> 0.4101632157; fresh validation
0.0593658973 -> 0.0977981021. Promotion passed both gates.
Full15 had eight gains, four losses (2/3/4/12), three score ties; include those
losses in future screening alongside stronger games. Fresh 1036/1037 improved;
1038 tied in score but depth fell from 5 to 4. Three fresh games do not establish
general improvement for every situation.

Important differences: DIVE_XL is 8 rather than the older 10; current20's
TOOL_RUN_XL=7 adds the earlier route described above. Sacrifice safety
is retained via the petrifying-body set. Gas-spore guards cover visible pets,
peaceful monsters and recent unseen pets in ranged/melee selection. The old
HP-conditioned acid-jelly penalty is replaced with an all-HP ONLY_RANGED rule
for spotted/ochre jellies; enabled LATE_FIXES forces HAZARD_FIXES on. Inspect
current code rather than assume the older narrow guard implementation remains.
Earlier notes below describe experiments on the previous family. Do not
blindly restore their exact patches or infer that a component's old isolated
failure proves it fails inside this jointly tested replacement.

Before the package replacement, four narrow digging ideas were tested and
reverted on the OLD parent: pre-dig Elbereth regressed seed 2 with a fresh
control; pit continuation's apparent gain disappeared under fresh controls;
raising retry cap 6 -> 16 gave no reliable gain; minimum-water island digging
tied 0/4/7. Their rejection and the later package-level win are distinct facts.

## Attempt 14: Public gain rejected by fresh validation

The periodic food strategy was changed from underfoot-only collection to
corpses initially at most three path steps away and at most 15 turns old,
retaining its existing hunger/edibility/scheduling/preemption checks. The
15-turn age limit is used for initial selection, not rechecked after travel.
Full Public improved
0.4069901063 -> 0.4221446135, but fresh validation regressed
0.4013412921 -> 0.1935119149. The variant was published, not promoted. The
champion at that decision remained attempt 13 despite attempt 14's higher
Public rank. This is already a failed hypothesis on the NEW baseline family.
Future food variants need distinct evidence and fresh validation, not merely
more favorable Public samples.
Full15 had eight gains, two ties and five losses (5/6/8/9/11); 6/9/11 collapsed
to depth 1. Fresh 1039/1041 regressed from depth 29/26 to 3/1 while 1040 gained
from 3 to 26. These endpoints do not establish whether food, travel, combat or
later routing caused the changes. The initial path/age filters are not an
elapsed-time or threat limit throughout the trip.
Preliminary CASTLE_PASSAGE enablement had no gain in seven sampled games and
lost on 7; unrestricted EAT_NEARBY_CORPSES looked promising on 2/3/4/8 but
regressed the combined eight-game sample after adding 0/1/5/6. Both were
reverted. Distinguish these tested failures from narrower untested mechanisms.

## Earlier baseline family (attempts 4–12): historical findings

Attempt 11 subtracts 100 from melee priority for spotted/ochre jellies when
current absolute HP <= 6 * (species base mlevel + 1). This is a heuristic
priority penalty, not a hard ban, an acid-resistance check, or an HP-fraction
gate; it may activate at full HP when maximum HP is low. It was accepted in
the earlier family; attempt 13 uses a different rule above. Full Public:
0.3096071522 -> 0.3493565494, two gains (3/7),
one loss (2), twelve score ties. Fresh seeds 1030–1032 tied at 0.0863222983;
1030 had 91 extra turns, so the validation trajectories were not all identical.
Seed 3's depth-6 -> 27 rescue reproduced against a fresh parent in development
and in full15. Changes on 2/7/11 have also occurred in same-source reruns;
do not attribute all of them to the jelly rule without traces. Direct fixtures
covered spotted jelly at 36/100 HP and a newt at 36 HP, not every boundary.

Attempt 10 additionally enabled the existing projectile guard against a gas
spore with a visible pet in its clipped 3x3 neighborhood, independently of
HAZARD_FIXES. Full Public: 0.3013431297 parent to 0.3081941584 candidate
(+0.0068510287), three gains (0/1/8), two losses (7/9), ten ties. The fresh
1027–1029 validation tied at 0.2297637148; promotion passed. This guard was
accepted alongside the earlier sacrifice fix below. The proposed benefit is
avoiding pet blast deaths/alignment loss, but saved endpoint results do not
directly measure that causal chain. The small-sample gains on 0/1 persisted;
the broader batch reduced the net benefit substantially. A rerun of the parent
on 0/1 reproduced its reference scores, turns and depths.

Do not generalize the result to remembered pets, peaceful monsters, wand
behavior, or enabling all HAZARD_FIXES. A separate projectile overshoot/bystander
guard was tested first and reverted: 0/1/6 tied in score, but seed 2 fell from
0.445181 to 0.179100. Keep that failed mechanism distinct from the accepted
gas-spore projectile guard.

Attempt 7 added only a `GlobalLogic.can_sacrify()` guard against cockatrice and
chickatrice corpse selection without gloves. Full Public: 0.2597258454 parent
to 0.2861614452 candidate, two improvements and thirteen score ties. Fresh three
games tied at 0.4086152658, so the candidate was promoted. Its safety principle
remains relevant; inspect the new family's equivalent implementation.
It prevents a deliberate sacrifice pickup route; it is not general protection
against live petrifying monsters or every floor inspection.

## Preliminary failures omitted from the short history table

These changes were tested and reverted. Revisit only with a materially different
mechanism supported by new evidence, not merely a different favorable subset.

- Unconditional early digging-tool retention showed no gain in attempts 5 and 6.
- Quiet recovery below 80% HP before diving was mixed and regressed several
  strong games (attempt 5). Broad passive-contact avoidance lost on the full
  Public batch (attempt 3).
- Blanket earlier dive thresholds were unreliable: XL9 lost on full15 in
  attempt 6 despite a good three-game sample. XL8 also regressed. Attempt 7's
  25,000-turn/XL8 exit gained on 3/7/13 but regressed 2/4/8; a 10,000-turn/XL5
  first-level exit also had a larger regression than its gain.
- Permitting injured Valkyries to melee cold-passive jellies/molds and treating
  every species of difficulty >=8 as dangerous regressed samples (attempt 7).
- Enabling existing Elbereth recovery during the tour initially helped seed 3
  but regressed strong games in the broader nine-game sample (attempt 7).
- Exact critical-HP prayer eligibility did not improve samples 0/3/6 and
  1/7/13 in attempt 7. Do not claim it is untested.
- Broad remembered-petrifying-corpse BFS exclusion lost on full15 (attempt 5).
  Skipping all floor inspection on those squares also regressed stronger games
  (attempt 7). Blind-only inspection suppression and a guard only on the
  inspection PICKUP fallback did not improve 7/2/12. These differ from the
  successful sacrifice-selector guard above.
- Attempt 11's persistent Mines inventory cap of 580, triggered by an
  alternative squeeze-route search, tied 3/13 but regressed 8 from 0.601565 to
  0.206129; reverted. This is distinct from selective equipment handling.
- Requiring XL7+, hunger better than Weak and 70% HP for the affected fountain
  dipping branch showed no reliable gain on 9/3/8; reverted (attempt 11).
- Lycanthropy-family corpse avoidance was reverted after nine seeds without
  reliable gain (attempt 11). Fresh control explained an apparent seed-8 loss;
  seed-10 loss lacked a fresh control. Keep that uncertainty explicit rather
  than claim each changed endpoint proves a regression from the mechanism.

## Tactical lookahead: implemented, no measured Public improvement

Attempt 8 completed the requested three-turn planner and published it, but
candidate and same-run parent both scored 0.2893345546. Every full15 per-game
result field matched except wall time. No fresh validation or promotion followed.
The saved 0.2861614452 champion score from another run is not the right control
for claiming this planner improved anything.

The model and adapter were unchanged from the supplied assets. The mutator fixed
two integration defects: production StatsLogger requires explicit registration
of lookahead_plan/lookahead_override/lookahead_unsupported, and the default
TACTICAL_LOOKAHEAD flag must precede JF_CFG environment overrides. The original
fake-logger fixture missed the first defect. Production logger plus real fight2
fixtures now demonstrate an override can execute on a constructed observation.

Saved arena results contain no planner counters or action traces. Actual-game
planning and override counts remain unverified. A sample depth change that did
not persist in full15 does not prove activation. Before interpreting a further
planner variant, obtain bounded direct activation/fallback/override diagnostics;
do not broaden its safety gates merely to manufacture activity. The model
estimates hidden HP/damage/energy rather than cloning exact future game states.

## Hunger prayer cooldown: sample gain did not generalize

Attempt 9 changed only the fainting hunger-prayer cooldown from 400 to 1,000
turns. Seeds 0/1/2/3/6/7/9 improved in aggregate from 0.2165201326 to
0.2863659629, but full15 regressed from 0.2981700203 to 0.2817352023
(-0.0164348180): four gains, five losses and six ties. Major losses on 7/8/11
outweighed gains on 0/5/6/9; seeds 8 and 11 were absent from the small sample.
The fully scored candidate was published, rejected locally and not validated.
Do not repeat an unconditional 1,000-turn fainting cooldown as an untested fix.
An unconditional 1,200-turn version had already regressed the seven-game
sample. Exact HP prayer eligibility and suppressing prayers after divine anger
again showed no score gain on 0/1/2/6 and were reverted. Any new prayer change
needs a distinct observed mechanism and a comparison including strong games.

## Evaluation discipline

Attempt 12's dive mattock/removable-shield change is a measured full15 failure:
0.3278805121 -> 0.3177516954, two gains (4/10), one large loss (8), twelve ties.
Seed 4's depth-23 -> 27 rescue persisted across fresh controls, repeat candidate
and full15, but the unsampled seed 8 fell from depth 27 to 4 and outweighed it.
Both versions produced both outcomes on seed 7, so its apparent sample gain
was not attributed to the change. The candidate was published, not promoted.
The mechanism did more than briefly remove a shield to dig: armor selection
continually excluded all shields during the dive while a mattock was selected.
Future variants must distinguish enabling tool access from maintaining a
shieldless armor set. This code distinction is not a proven causal explanation
of seed 8's loss; no armor/action trace established that. Direct fixtures
covered tool eligibility, not the complete armor/takeoff sequence.

Same-source reruns have varied. Inspected seed derivation uses secret,
evaluation ID and trajectory ID, not solution digest or EXPERIMENTS.md. The
cause of variation remains unproven. Compare with the same-run full Public
parent and retain fresh local validation. Small samples and death labels alone
do not establish causal improvement. Public publication and organizer Private
scores are separate from local champion promotion.

At the 16:29 UTC organizer check, attempt 6 completed all 73 Private identities
and scored 0.0989282843 in generalist, better than our other fully covered
programs at that time. Its Valkyrie-only Private was 0.1814241152, below
attempt 4's 0.2255993128. The broader aggregate does not reverse the local
Valkyrie rejection or authorize replacing this identity's champion with it.
Attempt 8's Valkyrie Private also equals 0.2255993128; its immediate parent's
Valkyrie Private row was absent, so this is not a paired planner comparison.
These are organizer aggregates, not local validation or per-seed evidence.

At the 18:29 UTC organizer check, attempt 10's Valkyrie Private arrived:
0.2892909326203677 (rank 3), now our best verified score for this identity.
Program prog_1b6813de33cd74adf4959239ee985de5, immutable source
github.com/Xenox-developer/nethacker@56d3a9bf2609f182a7a8735cb2da65aa6430e4f2.
This supports retaining the earlier family as a reference, but does not isolate
the gas-spore guard causally: its immediate parent's Private row is still
absent. Nor does it establish Private performance of the later whole-peer
family; no Valkyrie Private rows for attempts 11–16 were present.
Attempt 10's completed 73/73 generalist Private mean is 0.0860528823;
attempt 6 remains better on the full grid at 0.0989282843. Scope matters.

At the 19:30 UTC organizer check, attempt 14 completed all 73 Private
identities: generalist mean 0.20537463447023885 (rank 9), now our best fully
covered program, versus attempt 6's 0.0989282843. Its Valkyrie Private is
0.27824174140642893 (rank 5), below attempt 10's 0.2892909326 (rank 3).
Program prog_16677b2d08608b0ce0eea0daae82ca02, pinned source
github.com/Xenox-developer/nethacker@6efe11b66cf35738b38f4f57804d19c1098ece38.
This does not reverse attempt 14's failed local fresh gate. It also does not
isolate the corpse-collection patch: parent 13 has only 47/73 generalist
coverage and no Valkyrie Private row yet. Keep the accepted integrated family
as the current experimental baseline and preserve variant 14 as a strong
generalist reference; do not replace this identity's champion using that
different-scope aggregate. No local scope expansion has been performed.

At 20:31 UTC, parent 13 also completed all 73 Private identities:
generalist 0.20099556000424004 (rank 14), Valkyrie 0.2457366139068747 (rank 21).
The directly related child 14 is higher in both reported aggregates:
0.2053746345 generalist and 0.2782417414 Valkyrie. This qualifies the earlier
local rejection: the food variant lost its three-game local promotion gate,
but its later complete organizer results exceed the parent's aggregates.
Do not describe it as a universal food-policy failure. These aggregate
comparisons do not establish per-game causal action sequences or authorize
overriding local promotion rules; a new variant still needs both local gates.
Parent 13 source: github.com/Xenox-developer/nethacker@77ee3215099b099dfed34b22d1562c40fb5783a2,
program prog_004afb97cc88f385b77bbe0e6937e4ef.

Attempts 11/12 now also have Valkyrie Private 0.2892909326203677, equal to
attempt 10 (ranks 6/4/5 respectively). Equal aggregate means do not establish
identical games. The earlier family still leads our Valkyrie Private results,
while the integrated family leads our completed generalist results. Private
Valkyrie rows for 15/16/18 were absent at this check; their partial generalist
means (15:26/73, 16:14/73) are not comparable to the complete grid.

At21:31 UTC, attempt15 completed73/73 generalist Private at0.2034182644730571
(rank11), above13's0.20099556000424004 and below14's0.20537463447023885(rank10).
Its Valkyrie Private is0.27613676004992393(rank10), above13's0.2457366139068747
but below14's0.27824174140642893. Attempt16 Valkyrie Private is now
0.2865627828681945(rank7), above parent15 and below the earlier10/11/12
family's0.2892909326203677. These are organizer aggregates, not per-game
causal evidence or fresh local validation. No Valkyrie Private rows for18/19/20
were present; generalist16(66/73) and19(14/73) remain partial, so their means
must not be compared to complete73 grids.
Attempt15 source: github.com/Xenox-developer/nethacker@bb2be6a992a26783dd6a12e58cbe04a9c6cfb12f,
program prog_a1a5513935dc368506480d0d566aff6f. Attempt16 source:
github.com/Xenox-developer/nethacker@176044ce6f266e5a1ddc5fcb6475cafd20e21a3b,
program prog_9b121c3f5820b75c6d3f28249423c7a8.

Provenance: completed runs participant-0005-b906e518,
participant-0006-6d314c23, participant-0007-ed40d0f8 and
participant-0008-48e7c81b, participant-0009-9fe41255 and
participant-0010-310b06c4, participant-0011-47d99143 and
participant-0012-780726ff, participant-0013-3758e1f8 and
participant-0014-e3c0ae62, participant-0015-1d3d9de0 and
participant-0016-bca1a0d0, participant-0017-2388013e and
participant-0018-f97feec7, participant-0019-1baa0434 and
participant-0020-c6198af8; detailed host-side
reviews are in the identity's reviews/20260927-baseline-review.md and
20260927-attempt{6,7,8,9,10,11,12,13,14,15,16,17}-review.md, plus
20260927-attempt18-strategy-review.md and 20260927-attempt18-evidence-review.md,
and 20260927-attempt19-20-{strategy,evidence}-review.md.

