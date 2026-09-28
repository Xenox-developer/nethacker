from pathlib import Path
import json,hashlib,collections,statistics,datetime
E=Path(__file__).resolve().parent;W=E.parent
load=lambda p:json.loads(p.read_text())
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results={a:load(E/(a+'-raw.json')) for a in ('baseline','hybrid')}
expected=list(range(15))+list(range(3100,3112))
for a,rs in results.items():
 assert [r['trajectory_id'] for r in rs]==expected
 for rel,digest in load(E/(a+'-manifest.json')).items():assert h(E/a/rel)==digest,(a,rel)
for rel,digest in load(E/'hybrid-manifest.json').items():assert h(W/rel)==digest,rel
stats={};coverage={}
for arm in results:
 files=sorted((E/'diagnostics'/arm).glob('*.jsonl'));c=collections.Counter();details=[]
 for p in files:
  rows=[json.loads(l) for l in p.read_text().splitlines()];pc=collections.Counter()
  for r in rows:
   pc[r['stage']]+=1
   if r.get('depth_alone'):pc[r['stage']+'_depth_alone']+=1
   if r['stage']=='engraving_call' and r.get('depth_alone') and r.get('visible_immune'):pc['new_engraving_visible_immune']+=1
  c.update(pc);details.append({'file':str(p.relative_to(E)),'counts':dict(pc)})
 stats[arm]=dict(c);coverage[arm]=details
(E/'diagnostic-summary.json').write_text(json.dumps({'counts':stats,'streams':coverage},indent=2)+'\n')
paired=[];groups={}
for name,seeds in [('Public',list(range(15))),('Development',list(range(3100,3112)))]:
 br={r['trajectory_id']:r for r in results['baseline']};hr={r['trajectory_id']:r for r in results['hybrid']}
 bm=statistics.mean(br[s]['progress'] for s in seeds);hm=statistics.mean(hr[s]['progress'] for s in seeds)
 gains=[s for s in seeds if hr[s]['progress']>br[s]['progress']];losses=[s for s in seeds if hr[s]['progress']<br[s]['progress']];ties=[s for s in seeds if hr[s]['progress']==br[s]['progress']]
 groups[name]={'baseline_mean':bm,'hybrid_mean':hm,'delta':hm-bm,'gains':gains,'ties':ties,'losses':losses}
 for s in seeds:paired.append({'group':name,'seed':s,'baseline':br[s],'hybrid':hr[s],'delta':hr[s]['progress']-br[s]['progress']})
(E/'paired-results.json').write_text(json.dumps({'groups':groups,'pairs':paired},indent=2)+'\n')
lines=['# Champion30 depth-20 protection experiment','', 'Request: `20260928T045001057713Z-e678ebe57d7e492fbe3650d77da1d660`.','',
'Completed the fixed 54-game internal comparison: 27 freshly evaluated games per arm, without rerolls. This is an experiment, not a promotion decision. Public and development panels remain separate.','',
'## Implementation and lineage','',
'Baseline: accepted champion30 runtime from `github.com/Xenox-developer/nethacker@b01a1eef34751eb044a6971f1a2735e6007a7d3f`; peer2 package from `github.com/vkurenkov/nethacker@f15bb8c8e01d905d1946e32bfd2558e17394eab6` with the supplied adapter. All 47 supplied file hashes verified exactly (see `champion30_experiment/asset-verification.json`). The smaller runtime tree is not asserted to equal the historical whole-champion digest `sha256:c41a0a007ae3ee074a82632cee8c508e2384cb08db01e98946cb0ba73e9370a9`. MIT license and all existing attributions retained.','',
'Only policy difference: current `blstats.depth >= 20` bypasses the no-nearby-susceptible-monster eligibility gate in `_elbereth_before_digging_escape`, adapted from `github.com/Xenox-developer/nethacker@7d546b6ab2b972c793489801f609aa691fc82b44`. No whole-helper transplant, peer1 hybrid, tool threshold or immune-enemy exception. `TOOL_RUN_XL=None`, `ELBERETH_ALWAYS=False`, `DROWN_GUARD=False`; sighted 4/blind 6 retry caps, intact engraving, polymorph/swallow/can-engrave guards, Medusa/Weak/pit-rewrite reasons and all callers/dispatch remain unchanged. Exact differences: `complete-hybrid.diff` (all runtime, diagnostic and attribution changes), `policy.diff`, `evaluated-policy.diff`, and the two instrumentation diffs under `champion30_experiment/`.','',
'The incoming outer champion is preserved in `champion30_experiment/incoming-outer-champion.tar.gz`; `/refs/parent` and its results remain the native outer reference. The working submission is the evaluated hybrid, with retained opt-in diagnostics and source attribution. No manual champion replacement or publication API action was performed. Ordinary native same-run full Public plus fresh local validation remain the sole promotion gates; these development games are neither Private nor that fresh gate.','',
'## Fixtures, repairs and freeze','',
'Before gameplay, 33 checks per arm exercised actual imported helper methods: depth 19/20, original early reasons, intact text, sighted/blind cap boundaries, blind hurt retry, polymorph, swallowing, cannot engrave, immune-only and susceptible monsters, and actual normal/Gehennom dispatch. Structural checks prove all other DiveLogic methods unchanged and baseline policy AST identical after stripping passive diagnostic calls. Diagnostics tests cover actual-call-site observations, immune visibility, default-off mode, bounded output, logging failure isolation, and unchanged Python/NumPy RNG state. Fixtures are not gameplay evidence.','',
'One pre-game technical repair: mock glyph arrays initially used NumPy default integer dtype; real `utils.isin` requires int16. Both failed fixture outputs and original fixture are retained under `repairs/01-fixture-dtype/`. Only the fixture dtype was corrected. No gameplay losses were erased and no policy repairs occurred.','',
'Both arms frozen before the first game; `freeze.json` records time, hashes and fixed batch. Post-run checks verify every frozen runtime file and the working hybrid unchanged. No policy edits or additional hypotheses during comparison.','',
'## Evaluation','',
'Foreground sequential native `python -m nethackers.arena.run` batches, normal sandbox, public secret / `local` namespace, `val-dwa-law-fem`, max_steps=1,000,000, no_progress_timeout=10,000, action_timeout=120s, max_parallel_evals=4. Baseline all 27 first, hybrid all 27 second. Exact commands/environment, raw 27 rows, stdout/stderr and process exit records retained separately for each arm. No prior scores reused.','',
'| Panel | N/arm | Baseline mean | Hybrid mean | Delta | Gains / ties / losses |','|---|---:|---:|---:|---:|---:|']
for name,g in groups.items():lines.append(f"| {name} | {15 if name=='Public' else 12} | {g['baseline_mean']:.17g} | {g['hybrid_mean']:.17g} | {g['delta']:+.17g} | {len(g['gains'])} / {len(g['ties'])} / {len(g['losses'])} |")
lines+=['','The hybrid regressed on both fixed panels, with no score gains. Public losses were seeds 6, 11, 12, 14; the development loss was 3106. The observed 129 depth-only engraving calls establish real activation, including 3 with a visible immune monster, but do not isolate which calls caused each endpoint difference. This experiment provides no measured improvement. The requested hybrid is nevertheless retained for ordinary native scoring/publication, without overriding promotion gates.','', 'No pooled selection score is calculated.','', '## Every paired result and counterexample','', '| Panel/seed | Baseline | Hybrid | Delta | Depth B→H | Turns B→H | Baseline death | Hybrid death |','|---|---:|---:|---:|---|---|---|---|']
for p in paired:
 b=p['baseline'];a=p['hybrid'];esc=lambda v:str(v or '—').replace('|','\\|').replace('\n',' ')
 lines.append(f"| {p['group']}/{p['seed']} | {b['progress']:.17g} | {a['progress']:.17g} | {p['delta']:+.17g} | {b['max_depth']}→{a['max_depth']} | {b['turns']}→{a['turns']} | {esc(b.get('cause_of_death'))} | {esc(a.get('cause_of_death'))} |")
lines+=['','All score regressions (counterexamples to a uniformly beneficial effect):', '']
for name,g in groups.items():lines.append(f"- {name}: {', '.join(map(str,g['losses'])) or 'none'}. Gains: {', '.join(map(str,g['gains'])) or 'none'}. Ties: {', '.join(map(str,g['ties'])) or 'none'}.")
lines+=['','Score ties can still have different actions, turns or deaths. Endpoint differences do not by themselves establish the causal chain. All rows, including unfavorable results and all fields omitted from this display, are in `paired-results.json` and the raw files.','', '## Errors and diagnostics','']
for arm,rs in results.items():
 errors=[r for r in rs if r.get('error') or r['status']!='completed']
 lines.append(f"- {arm}: arena exit {load(E/(arm+'-exit.json'))['exit_code']}; {len(errors)} error/non-completed rows; statuses {dict(collections.Counter(r['status'] for r in rs))}.")
 for r in errors:lines.append(f"  - {r['trajectory_id']}: {r['status']}: {r.get('error')}")
lines+=['','Runtime warnings and any other output are retained verbatim in each arm’s stderr/stdout, not discarded as reroll candidates.','',
'Diagnostics are byte-identical across arms, enabled only with `CHAMPION30_DIAGNOSTICS=1`; default disabled. Each sandbox emits a process-local header and at most 20,000 event records plus a truncation marker. No RNG, seeds, evaluator state, actions or policy state writes; logging failures are swallowed. Observations use the helper’s actual locals and read-only visible-monster/species checks.','',
'`eligibility_depth_alone` counts visits reaching the gate where depth would be the only new eligibility reason, in both arms. `engraving_call_depth_alone` records the immediate, unconditional `agent.engrave("Elbereth")` call site solely enabled by depth. It measures calls/attempts, not successful intact engravings, NLE keystrokes, turns saved or prevented deaths. Safety/intact rejections occur before full eligibility locals exist, so their depth-only counterfactual is not computed. Blind guard combines cap and no-damage-since-last rejection, faithfully retaining the original compound guard.','',
'| Observation | Baseline | Hybrid |','|---|---:|---:|']
keys=['enabled','visit','eligibility','eligibility_depth_alone','engraving_call','engraving_call_depth_alone','new_engraving_visible_immune','safety_reject','intact_reject','eligibility_reject','sighted_cap_reject','sighted_cap_reject_depth_alone','blind_guard_reject','blind_guard_reject_depth_alone','observation_error','truncated']
for k in keys:lines.append(f"| {k} | {stats['baseline'].get(k,0)} | {stats['hybrid'].get(k,0)} |")
for arm in results:
 c=stats[arm];files=coverage[arm];active=sum(bool(f['counts'].get('visit')) for f in files)
 lines.append(f"\n{arm}: {len(files)}/27 diagnostic process streams, {c.get('enabled',0)} enabled headers; {active} streams with helper visits. {c.get('observation_error',0)} observation errors; {c.get('truncated',0)} truncation markers.")
lines+=['',
'Process IDs are not game seeds; no per-seed or per-panel attribution of the diagnostic streams is claimed. Counts cover the arm as a whole where streams are present. Process termination or filesystem failure could omit a trailing event without a marker; no durable end-of-game diagnostic footer exists. Do not interpret absent/missing streams as zero activity. The full per-process counts and every bounded raw event are retained in `diagnostic-summary.json` and `diagnostics/`.','',
'Visible immune means a visible monster that the existing `_melee_ignores_elbereth` predicate classifies immune (including its existing unknown-monster logic), anywhere in the visible list. This is not a full guarantee of hostile behavior, peaceful/blind individual state, ranged immunity, or imminent attack. Immune names at each engraving are retained. No immunity observation changes policy.','',
'Extra turns/nutrition and early retry-budget consumption remain possible costs. Outcomes are reported without tuning the guard. Real activation supports that the mechanism ran, but does not prove which score differences it caused; absence of activation would provide no causal evidence for this mechanism.','',
'## Evidence hashes','',
'Paths below are relative to `champion30_experiment/`. `evidence-sha256.json` lists SHA-256 for all artifacts (excluding generated caches and itself); per-arm manifests separately pin every runtime source file.','', '| Artifact | SHA-256 |','|---|---|']
for name in ['complete-hybrid.diff','source-evidence.json','asset-verification.json','incoming-outer-champion.tar.gz','baseline-manifest.json','hybrid-manifest.json','policy.diff','evaluated-policy.diff','deep_protection_diagnostics.py','freeze.json','baseline-raw.json','hybrid-raw.json','diagnostic-summary.json','paired-results.json']:
 lines.append(f'| `{name}` | `{h(E/name)}` |')
(W/'CHAMPION30_DEEP_PROTECTION_EXPERIMENT.md').write_text('\n'.join(lines)+'\n')
index={str(p.relative_to(E)):h(p) for p in sorted(E.rglob('*')) if p.is_file() and '__pycache__' not in str(p) and p.name!='evidence-sha256.json'}
(E/'evidence-sha256.json').write_text(json.dumps(index,indent=2)+'\n')
print(json.dumps({'groups':groups,'diagnostics':stats},indent=2))
