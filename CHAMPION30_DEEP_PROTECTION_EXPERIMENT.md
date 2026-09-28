# Champion30 depth-20 protection experiment

Request: `20260928T045001057713Z-e678ebe57d7e492fbe3650d77da1d660`.

Completed the fixed 54-game internal comparison: 27 freshly evaluated games per arm, without rerolls. This is an experiment, not a promotion decision. Public and development panels remain separate.

## Implementation and lineage

Baseline: accepted champion30 runtime from `github.com/Xenox-developer/nethacker@b01a1eef34751eb044a6971f1a2735e6007a7d3f`; peer2 package from `github.com/vkurenkov/nethacker@f15bb8c8e01d905d1946e32bfd2558e17394eab6` with the supplied adapter. All 47 supplied file hashes verified exactly (see `champion30_experiment/asset-verification.json`). The smaller runtime tree is not asserted to equal the historical whole-champion digest `sha256:c41a0a007ae3ee074a82632cee8c508e2384cb08db01e98946cb0ba73e9370a9`. MIT license and all existing attributions retained.

Only policy difference: current `blstats.depth >= 20` bypasses the no-nearby-susceptible-monster eligibility gate in `_elbereth_before_digging_escape`, adapted from `github.com/Xenox-developer/nethacker@7d546b6ab2b972c793489801f609aa691fc82b44`. No whole-helper transplant, peer1 hybrid, tool threshold or immune-enemy exception. `TOOL_RUN_XL=None`, `ELBERETH_ALWAYS=False`, `DROWN_GUARD=False`; sighted 4/blind 6 retry caps, intact engraving, polymorph/swallow/can-engrave guards, Medusa/Weak/pit-rewrite reasons and all callers/dispatch remain unchanged. Exact differences: `complete-hybrid.diff` (all runtime, diagnostic and attribution changes), `policy.diff`, `evaluated-policy.diff`, and the two instrumentation diffs under `champion30_experiment/`.

The incoming outer champion is preserved in `champion30_experiment/incoming-outer-champion.tar.gz`; `/refs/parent` and its results remain the native outer reference. The working submission is the evaluated hybrid, with retained opt-in diagnostics and source attribution. No manual champion replacement or publication API action was performed. Ordinary native same-run full Public plus fresh local validation remain the sole promotion gates; these development games are neither Private nor that fresh gate.

## Fixtures, repairs and freeze

Before gameplay, 33 checks per arm exercised actual imported helper methods: depth 19/20, original early reasons, intact text, sighted/blind cap boundaries, blind hurt retry, polymorph, swallowing, cannot engrave, immune-only and susceptible monsters, and actual normal/Gehennom dispatch. Structural checks prove all other DiveLogic methods unchanged and baseline policy AST identical after stripping passive diagnostic calls. Diagnostics tests cover actual-call-site observations, immune visibility, default-off mode, bounded output, logging failure isolation, and unchanged Python/NumPy RNG state. Fixtures are not gameplay evidence.

One pre-game technical repair: mock glyph arrays initially used NumPy default integer dtype; real `utils.isin` requires int16. Both failed fixture outputs and original fixture are retained under `repairs/01-fixture-dtype/`. Only the fixture dtype was corrected. No gameplay losses were erased and no policy repairs occurred.

Both arms frozen before the first game; `freeze.json` records time, hashes and fixed batch. Post-run checks verify every frozen runtime file and the working hybrid unchanged. No policy edits or additional hypotheses during comparison.

## Evaluation

Foreground sequential native `python -m nethackers.arena.run` batches, normal sandbox, public secret / `local` namespace, `val-dwa-law-fem`, max_steps=1,000,000, no_progress_timeout=10,000, action_timeout=120s, max_parallel_evals=4. Baseline all 27 first, hybrid all 27 second. Exact commands/environment, raw 27 rows, stdout/stderr and process exit records retained separately for each arm. No prior scores reused.

| Panel | N/arm | Baseline mean | Hybrid mean | Delta | Gains / ties / losses |
|---|---:|---:|---:|---:|---:|
| Public | 15 | 0.51271820816391056 | 0.48880174455332892 | -0.02391646361058164 | 0 / 11 / 4 |
| Development | 12 | 0.38648323392942419 | 0.38036333069140082 | -0.0061199032380233609 | 0 / 11 / 1 |

The hybrid regressed on both fixed panels, with no score gains. Public losses were seeds 6, 11, 12, 14; the development loss was 3106. The observed 129 depth-only engraving calls establish real activation, including 3 with a visible immune monster, but do not isolate which calls caused each endpoint difference. This experiment provides no measured improvement. The requested hybrid is nevertheless retained for ordinary native scoring/publication, without overriding promotion gates.

No pooled selection score is calculated.

## Every paired result and counterexample

| Panel/seed | Baseline | Hybrid | Delta | Depth B→H | Turns B→H | Baseline death | Hybrid death |
|---|---:|---:|---:|---|---|---|---|
| Public/0 | 0.46637631565303056 | 0.46637631565303056 | +0 | 25→25 | 11410→11414 | killed by a minotaur | killed by a minotaur |
| Public/1 | 0.1612677822768481 | 0.1612677822768481 | +0 | 11→11 | 8907→8907 | killed by a bolt of lightning | killed by a bolt of lightning |
| Public/2 | 0.44518140870167799 | 0.44518140870167799 | +0 | 24→24 | 16444→16458 | killed by a raven | killed by a raven |
| Public/3 | 0.5543572044866264 | 0.5543572044866264 | +0 | 27→27 | 13884→13928 | petrified by Medusa | drowned in a moat by a giant eel |
| Public/4 | 0.5543572044866264 | 0.5543572044866264 | +0 | 27→27 | 10249→14878 | killed by a baby silver dragon | killed by a purple worm |
| Public/5 | 0.5543572044866264 | 0.5543572044866264 | +0 | 27→27 | 15654→15735 | killed by a raven | killed by a raven |
| Public/6 | 0.5543572044866264 | 0.46637631565303056 | -0.087980888833595838 | 27→25 | 11116→11124 | killed by a fire elemental | killed by a pit viper |
| Public/7 | 0.46637631565303056 | 0.46637631565303056 | +0 | 25→25 | 17580→17589 | killed by a raven | killed by a raven |
| Public/8 | 0.60156485103821844 | 0.60156485103821844 | +0 | 28→28 | 10257→10496 | killed by a skeleton | killed by an iron golem |
| Public/9 | 0.5543572044866264 | 0.5543572044866264 | +0 | 27→27 | 15808→15660 | killed by an invisible lich | killed by a minotaur |
| Public/10 | 0.60156485103821844 | 0.60156485103821844 | +0 | 28→28 | 21417→21410 | killed by an umber hulk | killed by a minotaur |
| Public/11 | 0.60156485103821844 | 0.46637631565303056 | -0.13518853538518788 | 28→25 | 13568→13519 | killed by a minotaur | drowned in deep water |
| Public/12 | 0.5543572044866264 | 0.46637631565303056 | -0.087980888833595838 | 27→25 | 12109→11919 | killed by a xorn | killed by a minotaur |
| Public/13 | 0.46637631565303056 | 0.46637631565303056 | +0 | 25→25 | 11734→12690 | killed by a werewolf | drowned in a moat by a giant eel |
| Public/14 | 0.5543572044866264 | 0.50676056338028164 | -0.047596641106344761 | 27→26 | 12663→12675 | killed by a minotaur | killed by a cobra |
| Development/3100 | 0.46637631565303056 | 0.46637631565303056 | +0 | 25→25 | 16077→16076 | killed by a raven | killed by a raven |
| Development/3101 | 0.46637631565303056 | 0.46637631565303056 | +0 | 25→25 | 10341→10286 | killed by an elf-lord | killed by a captain |
| Development/3102 | 0.050758371234543298 | 0.050758371234543298 | +0 | 3→3 | 11377→11377 | killed by a magic missile | killed by a magic missile |
| Development/3103 | 0.036887590648350246 | 0.036887590648350246 | +0 | 1→1 | 9803→9803 | killed by a sewer rat | killed by a sewer rat |
| Development/3104 | 0.036887590648350246 | 0.036887590648350246 | +0 | 3→3 | 9181→9181 | killed by a wand | killed by a wand |
| Development/3105 | 0.37895667923256743 | 0.37895667923256743 | +0 | 20→20 | 10574→10574 | killed by a magic missile | killed by a magic missile |
| Development/3106 | 0.46637631565303056 | 0.39293747679675045 | -0.073438838856280109 | 25→21 | 10645→10602 | killed by a couatl | killed by a cobra |
| Development/3107 | 0.46637631565303056 | 0.46637631565303056 | +0 | 25→25 | 15875→15884 | killed by a wolf | killed by a forest centaur |
| Development/3108 | 0.46637631565303056 | 0.46637631565303056 | +0 | 25→25 | 10564→9955 | killed by a minotaur | killed by a minotaur |
| Development/3109 | 0.5543572044866264 | 0.5543572044866264 | +0 | 27→27 | 9953→10678 | killed by an invisible lich | killed by a stone giant |
| Development/3110 | 0.64650494159928118 | 0.64650494159928118 | +0 | 29→29 | 12867→12751 | killed by a leocrotta | killed by a green dragon |
| Development/3111 | 0.60156485103821844 | 0.60156485103821844 | +0 | 28→28 | 13841→13828 | killed by a hallucinogen-distorted baluchitherium | killed by a minotaur |

All score regressions (counterexamples to a uniformly beneficial effect):

- Public: 6, 11, 12, 14. Gains: none. Ties: 0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 13.
- Development: 3106. Gains: none. Ties: 3100, 3101, 3102, 3103, 3104, 3105, 3107, 3108, 3109, 3110, 3111.

Score ties can still have different actions, turns or deaths. Endpoint differences do not by themselves establish the causal chain. All rows, including unfavorable results and all fields omitted from this display, are in `paired-results.json` and the raw files.

## Errors and diagnostics

- baseline: arena exit 0; 0 error/non-completed rows; statuses {'completed': 27}.
- hybrid: arena exit 0; 0 error/non-completed rows; statuses {'completed': 27}.

Runtime warnings and any other output are retained verbatim in each arm’s stderr/stdout, not discarded as reroll candidates.

Diagnostics are byte-identical across arms, enabled only with `CHAMPION30_DIAGNOSTICS=1`; default disabled. Each sandbox emits a process-local header and at most 20,000 event records plus a truncation marker. No RNG, seeds, evaluator state, actions or policy state writes; logging failures are swallowed. Observations use the helper’s actual locals and read-only visible-monster/species checks.

`eligibility_depth_alone` counts visits reaching the gate where depth would be the only new eligibility reason, in both arms. `engraving_call_depth_alone` records the immediate, unconditional `agent.engrave("Elbereth")` call site solely enabled by depth. It measures calls/attempts, not successful intact engravings, NLE keystrokes, turns saved or prevented deaths. Safety/intact rejections occur before full eligibility locals exist, so their depth-only counterfactual is not computed. Blind guard combines cap and no-damage-since-last rejection, faithfully retaining the original compound guard.

| Observation | Baseline | Hybrid |
|---|---:|---:|
| enabled | 27 | 27 |
| visit | 1605 | 1869 |
| eligibility | 1212 | 1281 |
| eligibility_depth_alone | 212 | 129 |
| engraving_call | 456 | 735 |
| engraving_call_depth_alone | 0 | 129 |
| new_engraving_visible_immune | 0 | 3 |
| safety_reject | 57 | 57 |
| intact_reject | 336 | 531 |
| eligibility_reject | 747 | 533 |
| sighted_cap_reject | 0 | 5 |
| sighted_cap_reject_depth_alone | 0 | 0 |
| blind_guard_reject | 9 | 8 |
| blind_guard_reject_depth_alone | 0 | 0 |
| observation_error | 0 | 0 |
| truncated | 0 | 0 |

baseline: 27/27 diagnostic process streams, 27 enabled headers; 24 streams with helper visits. 0 observation errors; 0 truncation markers.

hybrid: 27/27 diagnostic process streams, 27 enabled headers; 24 streams with helper visits. 0 observation errors; 0 truncation markers.

Process IDs are not game seeds; no per-seed or per-panel attribution of the diagnostic streams is claimed. Counts cover the arm as a whole where streams are present. Process termination or filesystem failure could omit a trailing event without a marker; no durable end-of-game diagnostic footer exists. Do not interpret absent/missing streams as zero activity. The full per-process counts and every bounded raw event are retained in `diagnostic-summary.json` and `diagnostics/`.

Visible immune means a visible monster that the existing `_melee_ignores_elbereth` predicate classifies immune (including its existing unknown-monster logic), anywhere in the visible list. This is not a full guarantee of hostile behavior, peaceful/blind individual state, ranged immunity, or imminent attack. Immune names at each engraving are retained. No immunity observation changes policy.

Extra turns/nutrition and early retry-budget consumption remain possible costs. Outcomes are reported without tuning the guard. Real activation supports that the mechanism ran, but does not prove which score differences it caused; absence of activation would provide no causal evidence for this mechanism.

## Evidence hashes

Paths below are relative to `champion30_experiment/`. `evidence-sha256.json` lists SHA-256 for all artifacts (excluding generated caches and itself); per-arm manifests separately pin every runtime source file.

| Artifact | SHA-256 |
|---|---|
| `complete-hybrid.diff` | `96128d96a4ac6e2d1d8aa4386a806103c25fdf090fc2305f7bd173120136b26d` |
| `source-evidence.json` | `f8ecf1112aef4ea55c8b9b9bce4f4e805d5c37929233adcb3cc499b832ef4835` |
| `asset-verification.json` | `239a122bb71687b19a79ca8fadbae6f0c34d315f55fbd03d49449a413a14cedd` |
| `incoming-outer-champion.tar.gz` | `02cf9e8ced33c0f9d00f66e19b1f1cd903143e38829b0f8d84e13d4bf5c5ccaa` |
| `baseline-manifest.json` | `92da5cfbb1206cdfe7ad6379e7846e094d100df434eb8b783592d89a74f7a6e1` |
| `hybrid-manifest.json` | `d6e8c76b73e8c9ba499e7079d905382092a46d53468a90dd3da5a1172c8f6d5c` |
| `policy.diff` | `abbf38a7babed7ce9c88f88ba8c3f803b8b1e44cedcbaae15cc6503df46ec942` |
| `evaluated-policy.diff` | `467f6601565b82008bdaace1a755efd13ff2c3416027c0735ecfdda1b660f91c` |
| `deep_protection_diagnostics.py` | `43f173b333c622e5ba92ea1c7f8fa23d65453fa2f2d0aa2914fcca6c3ec876bc` |
| `freeze.json` | `78c528eba1ee757c76c045213208046e8740c98c20f31760885adc9ff7a86041` |
| `baseline-raw.json` | `cc0e5325f9a0e924a9f38db44908dc9a736217dbe0db14393800ff74d7c10ab2` |
| `hybrid-raw.json` | `5678684b7d176ee1888cd80d592925be9c0ac3661cf46364c9582945ad6f8a28` |
| `diagnostic-summary.json` | `1d69239d99bd102fc5059a7fc6eeec5b8f5ee523b9af1858bf4c1ba3b02ec661` |
| `paired-results.json` | `5b92ae8828acbe13a1b0d7e6c708331ca455ad5db40d78786bce8bfcff1303d6` |
