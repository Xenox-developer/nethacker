from pathlib import Path
import json,hashlib,statistics,collections,datetime
E=Path(__file__).resolve().parent
freeze=json.loads((E/'freeze.json').read_text())
def load(name):
 data=json.loads((E/(name+'-raw.json')).read_text())
 if isinstance(data,dict):
  for key in ['results','episodes','rows']:
   if key in data:return data[key]
 return data
runs={b['name']:load(b['name']) for b in freeze['batches']}
for b in freeze['batches']:
 rows=runs[b['name']];assert len(rows)==len(b['seeds']),(b['name'],len(rows))
 assert sorted(r['trajectory_id'] for r in rows)==b['seeds']
def paired(a,b):
 pairs=[{'seed':s,'baseline':a[s]['progress'],'candidate':b[s]['progress'],'delta':b[s]['progress']-a[s]['progress']} for s in sorted(a)]
 return {'n':len(pairs),'baseline_mean':statistics.mean(p['baseline'] for p in pairs),'candidate_mean':statistics.mean(p['candidate'] for p in pairs),'mean_delta':statistics.mean(p['delta'] for p in pairs),'gains':sum(p['delta']>0 for p in pairs),'ties':sum(p['delta']==0 for p in pairs),'losses':sum(p['delta']<0 for p in pairs),'pairs':pairs}
def select(name,extra=False):return {r['trajectory_id']:r for r in runs[name] if (r['trajectory_id']>=3200)==extra}
summary={name:paired(select('baseline-'+batch,extra),select('candidate-'+batch,extra)) for name,batch,extra in [('primary Public','primary',False),('extra development12','primary',True),('repeat Public','repeat',False)]}
repeat={arm:paired(select(arm+'-primary'),select(arm+'-repeat')) for arm in ['baseline','candidate']}
coverage={}
for name in runs:
 streams=list((E/'diagnostics'/name).glob('*.jsonl'));counts=collections.Counter()
 for p in streams:
  for line in p.read_text().splitlines():counts[json.loads(line)['stage']]+=1
 coverage[name]={'streams':len(streams),'events':dict(counts),'expected_episodes':len(runs[name])}
(E/'results-summary.json').write_text(json.dumps(summary,indent=2))
(E/'repeat-variability.json').write_text(json.dumps(repeat,indent=2))
(E/'diagnostic-summary.json').write_text(json.dumps(coverage,indent=2))
lines=['# Private31 trap-blocked armor cooldown experiment','', 'Request `20260928T054415304296Z-130a7ec3b8744f2fad4a17b97e75da07`. This is an experiment, not a demonstrated improvement.','',
'Implemented one mechanism: the five explicit reference refusal patterns return False and block only the affected armor slot until current game turn +20. Skips do not renew the expiry. The strategy respects blocked outer layers when changing shirts/suits, other slots remain usable, and arrange/drop retain blocked equipped armor. The original cursed and welded guards remain unchanged; no 1000-turn welded extension or escape actions were imported.','',
'Runtime baseline: `github.com/Xenox-developer/nethacker@56cd7f631d7a2400ec3366aa2d7f539524829572`, program `prog_64e10a9e6ae1e9aa93ffcdca5dc14e17`. Full historical digest `sha256:1e2f694943be0b87314c48f014bb290a26f836957193130ca90e319899552230` is provenance, not the hash of the reduced runtime asset. All 51 supplied runtime file hashes and both reference hashes were verified in `private31_experiment/asset-verification.json`. Attempt31 is daglar `5d0d455a1585271143aa47fbd5b44c2f6dae7d4b` plus attempt28 depth>=20 bypass, exact adapter and blind cap6. It is not the attempt30/35 vkurenkov runtime.','',
'Mechanism influence: `github.com/eL1fe/nethacker@a9e63ae735fba55510cbdd83b1545d4ad9f04f94`, `engines/dag/autoascend/item/inventory.py`. Only the bounded trap-refusal mechanism was adapted. The full MIT license (Copyright © 2022 Maciej Sypetkowski, Michał Sypetkowski) is retained in both arms and the candidate root LICENSE; the reference engine license is byte-identical. Native incoming parents are preserved in the candidate manifest separately from runtime authorship.','',
'## Freeze and validation','',
'`private31_experiment/freeze.json` records per-file baseline/candidate hashes and the pre-game timestamp. `policy.diff` is the exact uninstrumented policy change; `evaluated-policy.diff` compares evaluated inventory files; `baseline-diagnostic.diff` and `candidate-diagnostic.diff` record integration. `trap_diagnostics.py` is byte-identical across arms, default off. `incoming-outer-champion.tar.gz` preserves the incoming workspace runtime; supplied and historical trees were not edited.','',
'Production-path fixtures passed: baseline 13, candidate 17. They cover all five refusal patterns for wear/takeoff, same-turn and turn19 suppression without expiry extension, success at turn20, unrelated-message assertions, ordinary success, cursed items and welded guards, strategy termination, other-slot progress, arrange retention and direct drop rejection, blocked outer layers, and continuation into normal gameplay. These use production methods with controlled inventory/agent responses; they are not gameplay wins. Default-off and unwritable-log-path runs also passed. Raw fixture output and bounded fixture diagnostics are retained. Before evaluation, diagnostic accounting was repaired to distinguish a newly encountered refusal from an already-blocked entry; direct drop coverage was added. No gameplay ran before these repairs and freeze.','',
'## Fixed measurements','',
'All four batches ran sequentially: baseline27, candidate27, baseline-repeat15, candidate-repeat15. Public seeds 0–14, additional development 3200–3211. Native `nethackers.arena.run`, secret public, namespace local, val-dwa-law-fem, max_steps 1,000,000, no_progress 10,000, action_timeout 120 seconds, at most four episodes concurrently. Commands, start/finish times, exit codes, stdout/stderr and every raw row are retained. No ordinary death was rerolled, no rows omitted, and arms stayed frozen. This is 84 games with repeated Public seeds, not 42 independent trajectories per arm. The extra panel is development, not Private or native fresh validation.','',
'| Panel | n per arm | Baseline mean | Candidate mean | Paired delta | Gains / ties / losses |','|---|---:|---:|---:|---:|---|']
for name,s in summary.items():lines.append(f"| {name} | {s['n']} | {s['baseline_mean']:.12f} | {s['candidate_mean']:.12f} | {s['mean_delta']:+.12f} | {s['gains']} / {s['ties']} / {s['losses']} |")
lines+=['','## Repeat variability','', 'Each unchanged arm repeats the complete Public batch. Primary results remain primary; no favorable-row averaging or pooled selection score is used. In the following table gains/losses mean repeat relative to that arm’s primary.','', '| Arm | Primary mean | Repeat mean | Repeat minus primary | Gains / ties / losses |','|---|---:|---:|---:|---|']
for arm,s in repeat.items():lines.append(f"| {arm} | {s['baseline_mean']:.12f} | {s['candidate_mean']:.12f} | {s['mean_delta']:+.12f} | {s['gains']} / {s['ties']} / {s['losses']} |")
lines+=['','## Behavioral coverage and limitations','', 'Diagnostics write at most 2,000 event records plus one truncation marker per process. Streams are process-scoped and do not inspect seeds or evaluator internals. Refusals include the slot, turn, expiry and bounded message. Suppression records mark a true cooldown eligibility check that prevents an operation or keeps equipped armor forced; repeated checks are not unique game actions. Successful post-expiry records require a normal success message. Baseline only observes; its policy has no cooldown state. Logging consumes no RNG, issues no actions, and catches log failures.','', '```json',json.dumps(coverage,indent=2),'```','']
activations=sum(c['events'].get('refusal',0) for c in coverage.values())
if not activations:lines+=['No matching refusal was observed in any gameplay stream. Therefore these scores do not demonstrate a causal benefit from the mechanism. Fixture coverage establishes the intended behavior only. Any score differences despite zero observed activation must be interpreted as run variability, not evidence that this cooldown improved play.','']
else:lines+=['Matching refusals were observed; raw bounded streams retain exact evidence. Aggregate score differences alone do not establish that these events caused improvement; repeat variation and panel-specific paired rows must be considered.','']
lines+=['## Technical outcomes','']
for name,rows in runs.items():
 status=collections.Counter(r.get('status','missing') for r in rows)
 errors=[r for r in rows if r.get('error')]
 lines.append(f"- {name}: {len(rows)} rows; statuses {dict(status)}; {len(errors)} rows with errors; exit metadata `{name}-exit.json`. All losses and warnings are retained in the raw files.")
lines+=['','## Native disposition','', 'The tested candidate is left in `/workspace` for ordinary native Public scoring and publication regardless of internal results. This experiment does not manually promote it or replace the incoming champion. Promotion still requires native same-run Public improvement and fresh validation against the actual incoming champion. No new Private result is inferred; the historical 0.4091219692062755 Private result belongs only to attempt31, and its historical generalist grid was partial (63/73). Native outer scoring/publication are pending the enclosing workflow.','',
'## Raw paired rows','']
for name,s in summary.items():
 lines+=['### '+name,'','| Seed | Baseline | Candidate | Delta |','|---:|---:|---:|---:|']
 for p in s['pairs']:lines.append(f"| {p['seed']} | {p['baseline']:.15f} | {p['candidate']:.15f} | {p['delta']:+.15f} |")
 lines.append('')
lines+=['## Artifact index','', 'All paths below are relative to `private31_experiment/`. Full raw arena rows include deaths, steps, turns, errors, and wall times; no row is replaced by its repeat.','']
for name in runs:
 lines.append(f'- `{name}-raw.json`, `{name}.stdout`, `{name}.stderr`, `{name}-command.json`, `{name}-exit.json`, and `diagnostics/{name}/`.')
lines+=['- `results-summary.json`, `repeat-variability.json`, `diagnostic-summary.json`: machine-readable panel comparisons and coverage.', '- `asset-verification.json`, `freeze.json`, `final-audit.json`, `evidence-sha256.json`: source verification, frozen arms, installation audit, artifact hashes.', '- `fixtures.py`, `fixtures-*.stdout`, `fixtures-*.stderr`, `fixture-diagnostics/`: executable fixtures and raw outcomes.', '- `baseline/`, `candidate/`, `policy.diff`, `evaluated-policy.diff`, `*-diagnostic.diff`, `trap_diagnostics.py`: complete evaluated sources and exact changes.', '- `prepare.py`, `instrument.py`, `freeze.py`, `run_comparison.py`, `report.py`: preparation and evaluation scripts.','']
(E.parent/'PRIVATE31_TRAP_ARMOR_EXPERIMENT.md').write_text('\n'.join(lines))
print(json.dumps(summary,indent=2))
