# Local experiment history

These are measured outcomes from earlier runs. Avoid repeating failed ideas.

| attempt | hypothesis | public score | local validation | decision |
| --- | --- | --- | --- | --- |
| 32.1 | retreat from flooded Medusa islands to reduce drowning and exposure while digging. | 0.5023 | — | rejected |
| 33.1 | recover on a working Elbereth before digging destroys it, | — | — | error |
| 34.1 | preemptive protection on deep levels lets digging finish | 0.4949 | — | rejected |
| 35.1 | depth >= 20 pre-dig protection covers unseen arrivals. | 0.5098 | +0.0000 | promoted |
| 36.1 | scare approaching ravens before moving to a dig square; | 0.4992 | — | rejected |
| 37.1 | deep pre-dig protection helps against unseen arrivals. | 0.4296 | — | rejected |
| 38.1 | blind dust inscriptions often contain errors; allow more damage-triggered | 0.4920 | — | rejected |
| 39.1 | a tool-equipped XL6 character can descend under Elbereth sooner, | 0.5077 | -0.0135 | rejected by local validation |
| 40.1 | heal on a working Elbereth before digging erases it, | 0.4919 | +0.0000 | promoted |
| 41.1 | blind Elbereth retries should preserve earlier letters; | 0.4856 | — | rejected |
| 42.1 | use a safe, intact Elbereth to recover near full HP before | 0.4902 | — | rejected |
| 43.1 | a blind digger still needs to scare adjacent attackers before | 0.4843 | — | rejected |
| 44.1 | redundant words make a blind dust inscription more likely | 0.4978 | +0.0000 | promoted |
| 45.1 | spend offensive wands against high-level threats | 0.4815 | — | rejected |
| 46.1 | redundant blind words may retain one intact Elbereth. | 0.4206 | — | rejected |
| 47.1 | switching from a digging tool to a real weapon when swallowed | — | — | error |
| 48.1 | during the dive, estimate prayer success and imminent combat | 0.4888 | +0.0000 | promoted |
| 49.1 | an interrupted blind dig can expose a failed engraving | 0.4951 | +0.0000 | promoted |
| 50.1 | a digger can throw at point blank without spending a | 0.5084 | +0.0000 | promoted |
| 51.1 | a blind LOOK costs a turn and cannot read dust; | 0.4937 | +0.0000 | promoted |

## Whole-peer baselines

These exact peer commits were evaluated locally on the same 15 public games. A high Private score need not beat this bot on the public batch.

| source | public mean | compared champion | decision |
| --- | --- | --- | --- |
| `github.com/Komershan/nethacker@6073d88ea81f05d20c46c57b8fb9a38a54bfe75e` | 0.1351 | 0.1512 | not adopted: lower local public mean |
| `github.com/vkurenkov/nethacker@a5f72915d2a27db4c3835df61196dafe1ca31d7b` | 0.2692 | 0.1512 | promoted as local baseline |

## Reviewed experiment notes

Reviewed 28 September 2026, 14:08 UTC. Covers attempts through48;
the automatically generated history table is authoritative for newer decisions.
This is experiment context, not a required new mutation or a measured gain.

## Latest48: dive prayer model promoted; Private37 still our Valkyrie leader

Worker49 active, do not edit frozen input/runtime.48 final policy uses peer
kefirski/nethacker@454ae8df96e7ec68f0df2488b2b8a90368407cf1 MIT
prayer model for dive rescue decisions; parent tour policy/engraving retained.
See run48 PRAYER_MODEL_EXPERIMENT.md. Other trial changes reverted.
Internal15 .4861094613715122 ->.4919489209901017, but unchanged-parent
control also reached depth28 on gain11. Native fullPublic15 measured parent
.4861094613715122 -> candidate .48877581158301203:1gain11,12ties,
2loss3/14. Fresh1141–1143 three score ties, mean .4898134412088901
both arms;1141/1143 non-wall endpoints vary.48 promoted by same-run+fresh
gate, not historical absolutePublic record or causal proof. Published
prog_fd774136aa05c1987254d9e1749e602a@a678bde905c4ea84935393c13908804a8594b3e7;
champion digestcff5382be2c72a292ca38014f1b26b3a46ed8f852bc1c97e400cff35311f5579.
Keep unchanged-parent controls and variable endpoints in any prayer follow-up.

Hub14:07: valPrivate best own37 .41943976687370854 rank2 unchanged;
46 .4001094001805963 rank9 and45 .36222200149043293 rank10 newly complete.
48 Private absent. Full73 generalist best own29 .25419740108069006 rank5;
37 now full73 .2529299309992694 rank11,46 full73 .25138767925099187
rank13. Compare complete grids only; do not use Private to override local gate.
Exact own program/reference rows saved in reviews/hub-checks.jsonl.

## Latest45–46: tested31+44 combination, failed live diagnostics, new Private37

Localchamp44 unchanged; worker47 healthy, never edit its frozen runtime/input.
Request20260928T094658036782Z-0dd390d34e48436ea11ff44e32dd9a6a COMPLETED46.
Do NOT requeue it. Fixed84 valid games retained:27+27+15+15,42 perarm,
27 distinct IDs perarm (Public0–14+development3300–3311); no errors/rerolls.
Source verified exact31+ONLY both44 hunks, no40rest/41append/37armor.
PrimaryPublic .4324612999251177 ->.4356344093322074 (1gain14/14ties),
development12 .34929305700212104 ->.36487239239967034 (gains3305/3306,10ties).
RepeatPublic .42662184030652817 ->.42659590733621133 (gain11/12ties/loss6,14).
Unchanged baseline itself loses11/gains14; candidate loses6/14 onrepeat.
Primary Public benefit did not reproduce; source fidelity does not establish
causality. These are completed tested hypotheses, not a new suggested combo.
Native46 cross-family44 vs31+44 .49781431357900807 ->.4205534113776195,
1/9/5; nofresh/promote. All39publications through46 complete15atoms.

Detailed diagnostics FAILED, not zero activation:84 streams onlystart/end,
45,844 failed writes. level=list(agent.current_level().key()) retains NumPy
scalars; fix for future producer is level=[int(v) for v in ...key()]. Cast
turn/position similarly, serialize before opening files, bound failed attempts
as well as successful writes. Validate actual NumPy values before any game
batch. Default-off path must avoid agent-state reads, logging failures must
not alter actions/exceptions. Do not rewrite46 frozenarms or substitute reruns.
Future observations need independently established game↔trace identity;
PID/order/time alone is not seed linkage. Payload-yield completion is not
proof of engine acceptance/protection; cached generator timestamp and fixture
hardcoded3turns are not live writing duration. Real production fixtures46
confirm payload/parser changes and off/on/unwritable output equivalence,
but not whole-game timing neutrality. Details in attempt46-mechanism-review.

A reusable corrected producer is staged in hostrepo participant_extensions/
engraving_diagnostics/ (not automatically mounted in refs or installed in a bot).
README/provenance/LICENSE/patch/validation retained;12 focused tests pass with
real NumPy2.4.6,0skipped, plus Ruff. Portable fix instructions above are available
here even when the host file is not in the mutator container. This proves only
isolated producer behavior. In a future NEW study, reproduce production
fixtures with real NumPy observations BEFORE freezing, then demonstrate live
detailed rows/footer before interpreting activation. No repair-only publication
or repeat of the already completed84-game experiment was queued.

45 final nonweak monster mlevel>=10 capped wand score min(p,1)*40 loses
native .4919489209901017 ->.48152335816766567,0g/13t/2loss11,13. Wider danger
classifier reverted after early2regression. Final internal14gain disappears
outside development. Don't repeat this as an untested wand improvement.

Hub10:41:56: NEW bestownvalPrivate37 .41943976687370854 rank2,
prog_5767a36cfd4a04427a39cb3c78ab3a7f@6023714ed5c8f9b4a37a6607fc345f8de199c9a0.
31 .4091219692062755 nowrank4 unchanged.37generalist only61/73 .26368979125294445;
not a complete generalist win. Full73 best29 .25419740108069006 rank4,
31 .2536931742647458 rank8.37's earlier84game armor study lost Public/no
live activation evidence: Private gain doesn't establish armor causality or
authorize localchamp override. Preserve37 as a useful separately evaluated
lineage, not a proven universally beneficial patch.44/45generalist40/28 of73;
val44–46 missing, missing!=zero. Source/score notes:
20260928-attempt45-46-evidence-review.md and20260928-attempt46-strategy-review.md.

## Earlier42–44: accepted double blind inscription; exact31 combination queued

Healthy worker45 (20260928-093455-participant-0045-c193fe75); currentchamp44
4f6cf4fbf168f8d9095faf4261b53b04170add636be5fd07b2c29e0b15ed8a77.
44 same-runPublic .49197485396041857 ->.49781431357900807 (1gain11/13ties/1loss14).
Fresh1129–1131 every non-wall fieldties,mean .3389160016375626. Gatepassed,
not a historicalPublicrecord or provenPrivategain. Both connectedpolicyhunks:
blind exactElbereth request emits 'Elbereth Elbereth'; all read engraving
texts containing case-insensitive elbereth substring canonicalize toElbereth.
Append remainsn, caps/depth guard/40healing preserved. This is NOT append41,
blindcap18 or a general retry-count change.20 internal games: prayerport8
and emergency-only4 reverted; final4candidate+4freshparent, no full15internal.
Native14 lost the internal gain;3 generatorfixtures pass, parserfixtures and
gameplayactivation/duration traces absent. Do not assume the two-word command
costs the same game time or that gain11 proves increased protective reliability.
Publishedprog_cbd8377702ca06ae133736523ded47b5@52613eaea15fbf5eb836bf20f69ac083775edcbe.
All37journals through44 complete15atoms; no recovery.

42 final90% pre-dig recovery AND300restturncap (was60%/100), sameguards,
native .4919489209901017 ->.4902147383500857 (2/12/1), rejectednofresh.
43 removes blindness exclusion only from boundedpre-move scare, native
.4951220303971914 ->.48434934576117933 (1/12/2), rejectednofresh.43 actual
pre-move scarecallsT16438/16440 establish branch activation, not successful
protection/netbenefit. Keep these rejected policies, not untested ideas.
Reviews20260928-attempt44-strategy-review.md and20260928-attempt42-44-evidence-review.md.
Detailed42/43 source/trial audit:20260928-attempt42-43-strategy-review.md.
143 new games total42/43 (59+24internal,60native), nofresh; inherited studies
excluded.42 capcounts search(1) calls, not guaranteed elapsedturns. Its offensive
wand gain/loss matched unchanged-parentcontrols; broadthreatclassification
caused earlylosses, repeatedCastle sea-route/eel-priority probes gave no benefit.
12productionrestfixtures42 and6pre-movefixtures43 passed, not gamewin proof.

Hub09:41:26: bestownval31 .4091219692062755 rank2; fullgen29 .25419740108069006
rank4 and31 .2536931742647458 rank8 (scoresunchanged).40 fullgen .20218820132867454,
val .33813785780320765;38val same,39val .33109897490772744. No newleader.
39/38generalist65/73,41 40/73,37 20/73,42 14/73 remainpartial. Missing!=zero.

New requestpending20260928T094658036782Z-0dd390d34e48436ea11ff44e32dd9a6a,
private31-double-blind-engraving queuedONCE09:46:58. Exact31 +only BOTH44hunks,
no rest40/append41/armor37/other changes.51 historical31 files and58 frozen
assets verified; compatibletransplant syntaxcompiled only. Fixed84games:
baseline27,candidate27,baselinePublicrepeat15,candidatePublicrepeat15;
27 isPublic0–14+development3300–3311. Repeatpanels are not independentnewseeds.
Require real generator+parserfixtures and separate actualwrite/normalization
counts,rawtext,completed/interrupted write durations; retain missingtrace
association/end/errors without guessedseedmapping. No tuning/rerolls/rowreplacement.
Native outerbaseline remainsactualchampion; same-runPublic+fresh gates and
publicationcontinue. This is a new combination experiment, not measuredgain.
Do not duplicate request or editactive45. Exactbrief archivedinrequests.

## Earlier41: blind append rejected;42 subsequently completed above

Worker PID27202 healthy42 (20260928-080617-participant-0042-afea239e), testing
90% guarded pre-dig recovery versus40's60%. Internal15 and selected repeats
are development evidence; no final native/fresh outcome yet. Champion40 stays
5b3aa86..., storedPublic .4919489209901017. Never edit/restart active42.

41 sole runtime change: Agent.engrave answers existing append prompt y iff
blind AND requested text.lower()=='elbereth'. All callers share this behavior,
not only digging retries; it need not know prior inscription contents. All
caps/guards/config and40 healing unchanged. Native .48877581158301203 ->
.4856286351462393 (1gain6/13ties/1loss11), completed15/15/noerrors; nofresh
or promotion.6 depth25->27 repeats in internal screens and native;11 depth28->25
loss was outside the append screen. No gameplay append/inscription success
trace, so favorable6 causation and larger11 failure are unresolved.
24 internal games: scroll preservation8ties and minotaur emergency4ties
reverted; final append10games over7IDs plus2parentcontrols. Latest-per-seed
seven-ID mean is not a separately fixed batch; internal raw stayed/tmp,
command output/report retained.3 production generator mockbranches and
compile/import checks passed. Do not repeat these as new/untested ideas;
followup needs actual activation+lost-trajectory coverage, not favorable subset.
Publishedprog_4f3ed6636aa1204a02ab2695af1e032d@fa7da96c7e9e53b7732d5fe08109e86d8d3538a8.
All34journals through41 complete15atoms; no recovery. Detailed source audit:
reviews/20260928-attempt41-strategy-review.md.

Hub08:41:03: bestownval31 .4091219692062755 rank2 and completegeneralist29
.25419740108069006 rank3 remain.30/36/32 now completegeneralist
.19768034956903258/.2002846059621848/.19760134676989138, with firstvalPrivate
.34283894784054036/.33813785780320765/.3358649259885819. None beats ownleaders.
40/39/38 generalistpartial30/8/8 of73, no valPrivate yet. Partial means must
not be compared with completed29/31 or used to replace local champion.
Exact41 linkage and own board references:reviews/20260928-attempt41-evidence-review.md.

Repeatability correction08:45: actual pinned arena already sets PYTHONHASHSEED=0,
BLAS/OMP threads1 in base image. Do not propose absent hash seeding as a cause.
Cursor warning has a reproduced NumPy2 unsigned underflow (row0 ->255, not -1),
but its sole consumer refreshes cursor via TRAVEL before reading. Bad in-game
navigation/panic/score impact not demonstrated; not a measured improvement or
reason for gameplay reruns by itself. See20260928-cursor-overflow-review.md.

## Earlier37–40: completed armor study, rejected XL6, accepted guarded healing

Worker healthy on41 since07:46:25.40 promoted; new champion
5b3aa86cac3c54d31f490430645be38be0395b3107a5b0378885e5f3f4846f50.
Same-runPublic .4888017445533289 ->.4919489209901017 (2g3/11,11t,2l5/14).
Fresh1117–1119 all scoreties, mean .39428712238578006;1117 endpoint differs,
1118/19 allnonwallfieldstie. Stored .4919489209901017 is BELOW historical35
.5098228886420915; comparative gate uses fresh parent, not old record.
Sole runtime change: rest by search(1) below60% HP on intact readable Elbereth
before digging, at most100 total per level/square; reject hunger, blindness,
polymorph,recent hurt/ranged hits,Gehennom,visible immune monsters. Preserve
existing guards/caps. Internal15 .4946412041719184,2/11/2; parent11control
already matched candidate28depth. No gameplay activation trace; a small
Public win plus tied fresh is not robust causal proof. Production guards/cap
fixtures/imports/compilation passed. Publishedprog_e13e7acda70a6bf0321f1438ec95aea5
@c2d5581459a41df80f7c31bc97b0004700c6a7ce; all33journals through40 complete.
Do not touch frozen41 input/source or restart/duplicate its process.
Exact40 evidence/identity audit:reviews/20260928-attempt40-evidence-review.md.

Own29 generalistPrivate now COMPLETE73/73 at0.25419740108069006,rank3
(hub07:39:50), slightly above31 .2536931742647458,rank7. Same73 grid, tiny
0.00050423 lead does not establish a causal advantage.29 is exact whole
daglar5d0d455,prog_94abe21e3c18a78006d0c74cc8be2dfa@17abd35eeb3ac868bc7b2afbdc8fe24ef3983074.
OwnvalPrivate31 remainsbest .4091219692062755 rank2;29 first .4059747927695027
rank3.35 firstvalPrivate .3554296773225991 rank7, fullgeneralist .2012380626376627
rank37. Private favors the29/31 family despite35's superior localPublic.
30/32/36 generalists stillpartial; retain counts and don't select on partials.
Do not substitute Private selection for Public-plus-fresh promotion gates.

Requestprivate31-trap-armor-cooldown COMPLETED37, all84 fixed games. Source
matches exact31 plus only20-turn armor-refusal fix and passive diagnostics;
13baseline/17candidate retained production fixture checks pass. All frozen
assets/arms/final runtime and242 evidence hashes verified. PrimaryPublic
.4234487308994385 ->.4144102289034425 (0/13/2,loss3/6); repeatPublic
.429769016743301 ->.4234227979291217 (0/13/2,loss3/14); all12development scores
tie .40726081932125135. No episode errors. Unchanged baseline repeat improves
.006320285843862453, candidate repeat .009012569025679191: preserve this variance.
All84 gameplay streams contain only enabled records, no observed mechanism
activation. Synthetic fixture counters are not gameplay activation; streams
lack seed/end/error completeness. Neither benefit nor harm can be assigned
to the cooldown from this evidence. Native .4976372102093226 ->.4295659804032987
compares champion35 family against31+patch, not an isolated armor ablation.
No fresh/promote; published. Do not repeat the study as pending/untested.

38 final blind retry6 ->18 lost fullPublic .49781431357900807 ->.49197485396041857,
1gain14/13ties/1loss11; nofresh.39 finalDIG_DIVE_XL7 ->6 improved fullPublic
.49781431357900807 ->.5077293196483176,2gains1/14,10ties,3losses3/11/13.
Fresh1114–1116 thenlost .3161484383343529 ->.3026350247452766 (0/1/2): one
depth lost each1114/1115;1116 every non-wall fieldtied. Local rejection correct.
All32 publication journals through39 complete15atoms; no recovery needed.
Reviews:20260928-attempt37-strategy-review.md and
20260928-attempt37-39-evidence-review.md; never infer a promotion from a Public-only win.

38/39 strategy audit:20260928-attempt38-39-strategy-review.md.12 new internal
games38 and36 internal39, not the inherited54-game artifacts.39 internal vs
native candidate differs only onseed5 (depth29 ->27), explaining all its mean
drop .5138725021224946 ->.5077293196483176.39's ten-game KEEP_TOOL_IN_TOUR=True
screen was policy-redundant because keep_digging_tool already ORs with active
GRIND_HUNT_XL5; nevertheless one score improved. It was removed. Check resolved
config/production predicate before spending games on apparent new toggles.
The 9-game TOOL_RUN_XL7 screen again had severe losses5/7 and was removed.
DIG_DIVE_XL6 final is earlier descent with a tool, not earlier tool search;
optional food/HP gates remain off. No new activation fixtures/traces retained
for cap18/XL6, and no actual timeout/restart messages captured. Driver logs
were not enabled, so timing is still not the established cause of variability.
The tentative immune-adjacent depth-only engraving idea was checked and is
NOT ready:35's three immune-visible events have no position/distance/caller,
while normal _dig_escape_action already blocks adjacent and distance2-BFS
immune threats. Other direct dig callers exist, but relevant activation is
unproven. Do not duplicate existing guards based on minotaur death counts.

## Earlier36 and generalist31;37 later completed above

Own31 has now completed the organizer's full73/73 generalist grid:
0.2536931742647458, overall rank5 at06:39:25, above previous own best14
0.20537463447023885. Exact program prog_64e10a9e6ae1e9aa93ffcdca5dc14e17
@56cd7f631d7a2400ec3366aa2d7f539524829572, same as val Private leader31
0.4091219692062755(rank2). This is a complete grid, not73 game victories.
29 remains partial53/73,35 partial42/73; no new val Private rows. Native local
champion35 remains0.5098228886420915. Keep organizer and local criteria separate.

36's only final policy change expands existing pre-movement Elbereth eligibility
in _dig_escape_action to a visible raven within Chebyshev distance2. It
preserves all original blindness/polymorph/intact/immunity/two-attempt guards.
Internal full15 .5036797061679145 ->.5053704898499419 (3 gains/10 ties/2 losses).
Native full15 .5036797061679145 ->.49922730737576493 (2 gains/11 ties/2 losses),
no fresh/promotion. Internal→outer score difference comes entirely from seed5's
lost gain; seed9 changes only its endpoint. Seed2 new pre-move scare is traced
atturn16437 and a repeat reproducesdepth25; it is activation evidence for
that episode, not proof of net benefit. Fresh parent controls changed endpoints
on3/14. All six production escape-decision fixtures passed; all final episodes
completed without errors. The exact runtime does not include other exploratory
changes. One preliminary dive-danger episode had technical import EOFError
(marshal data too short), not a gameplay zero; retain it as incomplete.
36 publishedprog_040cd16a27a8ff1faab2c2709611c158@e69adf30f16366f5f80453f1c18a906247d32e7e;
all29 native publication journals complete. No recovery needed.

Request20260928T054415304296Z-130a7ec3b8744f2fad4a17b97e75da07 is now ASSIGNED37
(run20260928-062303-participant-0037-1823b1df), not pending or complete. Its
primary54 finished with no episode errors. Public0.4234487308994385 ->
0.4144102289034425 (0 gains/13 ties/2 losses); all12 development scores tie
atmean0.40726081932125135. Baseline15 repeat completed at0.429769016743301,
2 gains/12 ties/1 loss vs its unchanged primary, no errors.69/84 done at06:46,
candidate15 repeat outstanding. All27 primary diagnostic streams/arm exist
with zero recorded trap-refusal/suppression events; no causal benefit shown.
Do not change its frozen policy, queue a duplicate, or claim84 completed games.
The ordinary autonomous worker is healthy; preserve it.

Source audit06:48: exact _act mock proves queue deadlines can change returned
actions for identical observation/policy action. Normal deadlines also inject
AgentHang and may restart strategy. Historical34/35 activation is unknown;
do not claim the cause is solved. No unseeded policy RNG/hash-choice defect or
stale gameplay bytecode established; all45 retained30 pyc semantic code fields
matched fresh compile,35 root has none. Next repeatability evidence should
retain first divergent action and per-trajectory timeout/panic/restart counters
with explicit capture completeness before modifying adapter thresholds.
See reviews/20260928-repeatability-source-review.md. No request queued or
active code changed by the audit; EOFError36 stays a separate technical failure.

## Earlier34/35 and own Private31: preserve conflicting experimental evidence

Own31 is now best own val Private0.4091219692062755, overall rank2 at05:39:36,
program prog_64e10a9e6ae1e9aa93ffcdca5dc14e17 at56cd7f631d7a2400ec3366aa2d7f539524829572.
This is our measured entry, not another author's score. Its local Public
0.4237265207847091 had lost the gate; all fully scored variants are published.
Generalist31 remains partial63/73,29 partial13/73.28 now scores valPrivate
0.22736758731909743 and complete generalist0.1913274394553775; neither beats
the relevant own best. Own val Private30/32/34/35 absent, not zero.

Local champion35 passed native Public0.5054398217782473 ->0.5098228886420915
(4 gains/9 ties/2 losses), fresh1102–1104 tied0.1691806368622478 with all game
fields equal except wall time. Accepted digest95ae6e31a38f3187e41d43e1a0a2857f9be7d75caa37e6044c6014f8b5eb4eeb.
The same request completed54 primary games and LOST both fixed panels:
internal Public0.5127182081639106 ->0.4888017445533289 (0/11/4, losses6/11/12/14);
development3100–3111 0.3864832339294242 ->0.3803633306914008
(0/11/1, loss3106). No rerolls/errors. Do not call this robust improvement,
discard internal losses, or claim fresh activation based on equal endpoints.
Request champion30-depth20-protection is COMPLETED35, not another pending task.

35 keeps exact30 runtime/defaults/caps and adds only depth>=20 eligibility as
policy, plus identical passive opt-in diagnostics in both internal arms.
All27 streams per arm,129 depth-only events immediately before unconditional
engraving call sites;3 include a visible immune-classified monster. These are
attempts, not successful inscriptions/actions saved. No per-seed stream mapping
or terminal footer; no recorded error/truncation is not proof of perfect capture.
66 helper checks pass; mock actions/global RNG checks are not complete live
state equivalence. Internal diagnostics on, outer off by default. Seed
namespace remains public/local, but image/mount/parallel context also differs;
there is no established cause for repeat variation. Preserve caveats and
all unfavorable rows in future comparisons. Review35 has detailed evidence.

34 lost native0.5022926453414744 ->0.49494492702750587,3/9/3; no fresh.
Both34/35 published; all28 journals complete. Active36 remains untouched;
its combat, blind retry and XL7 samples are not final recorded decisions.
It is now testing a recent-damage emergency trigger. Do not duplicate it.

Scout05:19 changed peer labels: peer1=eL1fe a9e63ae (Valkyrie engine=dag);
peer2=old daglar5d0d455; peer3=alexey283f (Valkyrie AST matches known vkurenkov).
Root routers are not automatically MIT because a nested engine has a license.
eL1fe DAG inventory contains a narrow trap-blocked armor recovery mechanism;
other bundled changes include static regression risks, so do not import all.

The following request queued05:44:15 was subsequently assigned to active37:
20260928T054415304296Z-130a7ec3b8744f2fad4a17b97e75da07,
private31-trap-armor-cooldown. Frozen exact31 runtime51 files plus MIT reference
inventory/LICENSE; add only20-turn refusal cooldown for trapped feet/buried
ball and prevent immediate blocked armor removal/drop retries. No1000-turn
welded cooldown, wrapper or other strategy imports. Preserve31 depth guard,
caps/adapter/defaults.54 primary games (Public15 +newdev3200–3211 per arm)
then30 full Public repeat controls in fixed order:84 games, not42 independent
trajectories per arm. Actual fixtures/passive counters must establish whether
the mechanism activates; retain zero/missing coverage and repeated variability.
Internal baseline31 differs from native actual incoming champion by design;
publication proceeds normally and native Public/fresh gates still decide any
local promotion. Never overwrite local champion using a Private aggregate.

## Earlier30–33: new strategy package, completed hybrid, recovered transient errors

Champion30 replaces the autoascend package with pinned MIT peer2
vkurenkov/nethacker@f15bb8c8e01d905d1946e32bfd2558e17394eab6, retaining the
incoming adapter. This is not29's exact whole peer1 and not an isolated Medusa
change. Native Public0.4809840847749231 ->0.5081580379303808; fresh1087–1089
0.20435220290129294 ->0.37855124020191605 passed. Stored champion digest
c41a0a007ae3ee074a82632cee8c508e2384cb08db01e98946cb0ba73e9370a9.
The package replacement does NOT preserve prior28's depth>=20 bypass or
prior20's TOOL_RUN_XL7. Current TOOL_RUN_XL=None, ELBERETH_ALWAYS=False and
blind engraving retries capped. Treat the gain as package-level; do not
attribute it to a particular imported feature. Preliminaries for30's wider
Medusa routing, stair-arrival priority and wand-once were reverted after
sampled score ties. Source details in reviews/20260928-attempt30-strategy-review.md.

31 completed request20260928T034110788586Z-a8629597f5574a028233d9f49b55a435,
peer-depth20-protection: exact MIT peer1 plus ONLY depth>=20 pre-dig bypass.
46 primary games,23 per arm, Public0–14 plus reused development3000–3007;
fixed arms, zero errors/rerolls. Internal Public0.422035737103 ->0.420756447718
(2 gains/12 ties/1 loss), development0.388597114487 ->0.411423943817
(2 gains/6 ties). This is mixed, not a proven overall improvement. Fixtures
test depth19/20, early Medusa/Weak, safety guards, caps and Gehennom dispatch.
No gameplay activation counters were added; mock engraving is not evidence
of actual-game actions. Extra turns/nutrition and immune monsters remain risks.
Outer comparison against incoming30:0.5054398217782473 ->0.4237265207847091;
no fresh/promotion. Fully scored/published, request complete. Do not duplicate
31 or call it an experiment on30's different peer2 package. Review31 records
exact source/evidence and fixture-only repair before gameplay.

32 only enabled MEDUSA_SKIP, tied all15 native Public scores0.5022926453414744;
only13 changed steps/turns beyond wall time. Its TLS publication failure recovered
automatically at04:27:20 using the same commit; no duplicate submission needed.
33 failed with operator502 before a fully scored candidate, not a gameplay
loss. Preserve its partial fixtures/trials and Elbereth-rest proposal as
unscored. Worker waited300s and resumed34, which is currently testing TOOL_RUN_XL5.
Do not change34 or launch another evaluation cycle. Initial gh warning was
followed by successful authenticated GitHub checks, so access is not blocked.

Own val Private24–27 now all0.22437158128169327, and full generalist73/73
scores24–27 are0.189701092963353/0.1919045881448262/0.19137757115449194/
0.190390072093921. No improvement over own best val19 or generalist14.
Own val Private28–32 absent at04:45:18; partial generalist28/31 is not a
completed result. Never copy another author's Private score onto our program.

The following frozen request was subsequently completed in35:
20260928T045001057713Z-e678ebe57d7e492fbe3650d77da1d660,
champion30-depth20-protection. Test exact accepted30 runtime plus only28's
current-depth>=20 bypass, preserving caps/defaults/adapter/dispatch. This is
peer2-based, distinct from31's peer1 test. Frozen47-file baseline with exact
hashes/attribution is supplied; no mixing34's XL5 threshold. Fresh Public15
and additional development3100–3111 =27 per arm/54 primary, fixed before runs.
Passive identical opt-in observations should count helper visits, depth-only
eligibility, actual new engraving, guard/cap refusals and visible immune
attackers; report inability/coverage honestly, without changing decisions.
Keep all outcomes, no tuning or new conditional exceptions after scoring.
The native outer parent stays actual incoming champion; local promotion still
requires same-run Public improvement and the ordinary fresh gate. Do not
duplicate this request or alter active34. See immutable brief for details.

## Earlier28/29: deep protection accepted, whole peer benchmark

Champion28 now has Public0.4958505625322833 after parent0.47506047628647746:
five gains/nine ties/one loss. Fresh1081–1083 means tie0.3571639637914001,
so the configured gate passes; two score-tied trajectories change timing/death.
Only final runtime change: current blstats.depth>=20 can bypass the no-nearby-
susceptible-monster condition in _elbereth_before_digging_escape.
ELBERETH_ALWAYS remains False; DIG_ESCAPE/non-Gehennom dispatch, polymorph,
swallowing, can_engrave, intact-engraving and existing retry guards remain.
The alternative SHELTERED_DIG branch is unchanged. This differs from global21;
all15 Public scores equal21 but12 endpoint rows differ, and28 did NOT rerun
failed fresh1060–1062. Do not claim the narrower condition cured those losses.
Final development Public was0.4809840847749231, with variable repeated outcomes
on1/3/5; no dedicated final depth19/20 fixture/action counter was retained.

28's earlier container-routing, wish-ID and immune-enemy combat trials each
gave four sampled score ties and were reverted. Peer3 package overlay with
the original adapter kept lost on five samples0.3420247841 ->0.1548992655;
it was reverted too and is not an exact whole-peer benchmark. These are
already tested preliminaries, not pending hypotheses. Review28 preserves
commands, source identity and limits of causal evidence.

29 completed the exact whole MIT peer benchmark, request
20260928T024027587450Z-432074eedaca447e949a88d40490e3ef. All50 runtime/license
files match Git objects at daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b,
including final published source. Full original MIT attribution is preserved.
Fresh internal Public15 incoming0.4809840847749231 ->peer0.4283560229465442
(four gains/five ties/six losses); development3000–3007
0.2819553536430530 ->0.3852968977178186 (five gains/three losses).
All46 primary games complete, zero errors/retries. The eight extra trajectories
are development, not untouched holdout, Private or the native fresh gate.
Outer Public0.4958505625322833 ->0.4269430291497873, four gains/six ties/five
losses; no fresh/promotion. Outer parent exactly repeats28 candidate apart
from wall time. Internal repeated Public varies on incoming1/3/5 and peer6/14.
Do not attribute the eight-game gain to one feature or claim general superiority.

28/29 published with complete journals; own val Private24–29 absent at03:37:52.
Own best Private remains19 at0.30553778869019693. Peer author's historical
Private0.4029787867320985 is not our candidate29's result. Own generalist24–27
still partial, not full-grid improvements. Audits in reviews/20260928-attempt28-
strategy-review.md,20260928-attempt29-peer-review.md and28-29-evidence-review.md.

The following queued experiment was subsequently completed in31 (see above):
20260928T034110788586Z-a8629597f5574a028233d9f49b55a435,
peer-depth20-protection. Its exact peer1 versus peer1+depth20 comparison is
complete, with blind retry cap preserved and mixed measured results. Do not
repeat it as an untested hypothesis; the new queued30-based test is distinct.

## Earlier26/27: completed experiments

A/B/C request completed using verified25 after26 settled; provenance source25/
after26 and last_attempt26 are preserved.28 is ordinary evolution, NOT another
campaign retry.26 did complete80 primary+6 controls with no errors/retries:
B0 Public0.4782335856935671/dev0.2803439441175858;
A0.48754987757483376/devsame; B0.4843767681677441/dev0.2490672556502777;
C0.4750604762864775/devsame. Only A eligible, no combos. Its only primary gain1
reversed in controls;0/2000 tied. Outer A0.4782335856935671 ->0.47506047628647746,
loss9,14 ties,no fresh. Exact final63 files match evaluated A; patches reconstruct.
No observed changed wand choice, purchase, or suppression exception. Host26's
extra summary-field mismatch was handled by historical recovery, not reruns.
Do not pool24/25/26 as60 independent seeds per arm: repeated20 seeds and differing
implementations. Full reviews in reviews/20260928-attempt26-campaign-review.md.

Tool-reservation27 completed the requested policy exactly and DID change real
allocation proposals. Dev8:9761 compared calls,7020 eligible-tool,450 changed
tool AND armor allocations (retain pick-axe, displace optional crystal plate
mail); dev11:2228 calls,1001 gate visits,zero eligible tools/changes. These are
repeated proposals, not450 actual pickups or drops.9 production fixtures pass;
NumPy writer defect caused one retained interrupted technical smoke, then was
repaired before valid development/Public games. No game deaths were rerolled.
Inner full15 parent0.48754987757483376 ->0.4782335856935671; outer full15
0.4843767681677441 ->0.47506047628647746. Both0 gains/14 ties/loss1depth29->26.
8 scoreties atdepth28 but ends earlier with starvation. No trace for1 establishes
armor displacement caused its loss. Candidate published, no fresh/promotion.
Do not propose this exact tool-order change again as untested, or confuse
retention with11's failure to have any suitable tool. Preserve MIT attribution.
Review: reviews/20260928-attempt27-strategy-review.md.

The container-routing preliminary28 and exact whole-policy benchmark29 have
now completed; see the latest section. Neither request needs another queue.

## Earlier completed repetition25

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

The old checker rejected25's supplemental samples-<pid>.json format, causing
one final repetition26. Compatibility/historical recovery passed265 tests and
subsequently closed the request using25's valid evidence after26 settled.
Native decisions/history remain intact; the research is now completed.

Next ordinary mutations should address reachable game decisions, show which
observations enable a behavior, and preserve counterexample seeds1/9 plus
previous failed seeds. A synthetic fixture can verify a rare mechanism but
cannot substitute for gameplay coverage. Reuse exact peer references with
licenses where useful; compare any new strategy to the current champion's
same-run full Public and fresh gate. Do not adopt A/C on these transient means
or repeatedly loosen B/C gates to claim that the original hypothesis worked.
Audits: reviews/20260928-attempt25-{strategy,evidence}-review.md.

The two later candidate ideas were tool-priority27 (tested and rejected)
and container-routing28 (tested and reverted). See the latest section above
and reviews/20260928-next-strategy-candidates.md; neither needs another queue.

## Earlier applied research: completed24, then separate repetition25

Request20260927T215044431526Z-eab26a5f56264b9391f20dd5ac976a24 completed its
first full campaign in24: baseline/A/B/C each20,80 primary plus6 separate
controls, no errors or technical retries. The host completion checker falsely
rejected two optional summary fields; these are now accepted only after exact
recomputation. Retained24 verifies complete. Repetitions25/26 followed before
the final recovery closed the same request; all earlier native outcomes and
history remain preserved. Do not enqueue this same research request again.

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

## Organizer Private observations,02:37 UTC (separate from local selection)

Champion20's first val Private is0.22437158128169327,rank41, BELOW immediate
parent19's0.30553778869019693,rank6 (still best own).20 completed73/73 generalist
at0.1905506182799654,rank33;19 has0.20305495014722358,rank18. This local Public
promotion has not translated to better organizer results. Do not overwrite
local champion from these aggregates or claim per-game causal proof aboutXL7.
Preserve19 as the best own verified val reference. Best complete generalist
remains14 at0.20537463447023885,rank15.22 now completed73/73 at0.1888274978179285,
rank34.24 is only3/73 (partial0.3090189890402404), not a full-grid improvement.
No val Private24–27 yet. Exact own rows/references: reviews/hub-checks.jsonl;
pinned-peer comparison and publication audit:
reviews/20260928-attempt26-27-evidence-review.md. All21 native journals complete.

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

