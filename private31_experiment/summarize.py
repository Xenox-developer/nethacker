from pathlib import Path
import json,statistics,collections,hashlib
R=Path(__file__).resolve().parent
names=['baseline-primary','candidate-primary','baseline-repeat','candidate-repeat']
runs={n:json.loads((R/n/'results.json').read_text()) for n in names}
def indexed(rows): return {r['trajectory_id']:r for r in rows}
def compare(left,right,ids):
 a=indexed(left); b=indexed(right)
 pairs=[{'trajectory_id':i,'baseline':a[i]['progress'],'candidate':b[i]['progress'],'delta':b[i]['progress']-a[i]['progress'],'baseline_row':a[i],'candidate_row':b[i]} for i in ids]
 return dict(n=len(pairs),baseline_mean=statistics.mean(x['baseline'] for x in pairs),candidate_mean=statistics.mean(x['candidate'] for x in pairs),gains=sum(x['delta']>0 for x in pairs),ties=sum(x['delta']==0 for x in pairs),losses=sum(x['delta']<0 for x in pairs),pairs=pairs)
summary={
 'primary_public':compare(runs[names[0]],runs[names[1]],range(15)),
 'development':compare(runs[names[0]],runs[names[1]],range(3300,3312)),
 'repeat_public':compare(runs[names[2]],runs[names[3]],range(15)),
 'baseline_own_repeat':compare(runs[names[0]],runs[names[2]],range(15)),
 'candidate_own_repeat':compare(runs[names[1]],runs[names[3]],range(15))}
coverage={}
for name in names:
 files=list((R/name/'traces').glob('*.jsonl')); events=collections.Counter(); failures=0; dropped=0; missing=0; malformed=0
 for f in files:
  rows=[]
  for l in f.read_text().splitlines():
   try: rows.append(json.loads(l))
   except Exception: malformed+=1
  events.update(r['event'] for r in rows)
  ends=[r for r in rows if r['event']=='end']; missing+=not bool(ends)
  failures+=sum(r.get('write_failures',0) for r in ends); dropped+=sum(r.get('dropped',0) for r in ends)
 coverage[name]=dict(streams=len(files),events=dict(events),write_failures=failures,dropped_by_cap=dropped,missing_terminal=missing,malformed_rows=malformed,association='unmapped',statuses=dict(collections.Counter(r['status'] for r in runs[name])))
summary['diagnostics']=coverage
(R/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
# Reverify every frozen file; Python-generated cache files are not runtime source.
for arm in ['baseline','candidate']:
 for p,h in json.loads((R/(arm+'-manifest.json')).read_text()).items(): assert hashlib.sha256((R/arm/p).read_bytes()).hexdigest()==h,p
lines=['# Private31 double blind engraving experiment','', 'Completed the fixed 84-game experiment: 54 primary games and 30 repeat controls, 27 distinct trajectory IDs per arm. No primary row was replaced by a repeat. No score-driven edits or rerolls were made.','', '## Results','', '| Panel | Baseline mean | Candidate mean | Gains / ties / losses |','|---|---:|---:|---:|']
for key in ['primary_public','development','repeat_public','baseline_own_repeat','candidate_own_repeat']:
 s=summary[key]; lines.append(f"| {key} | {s['baseline_mean']:.15f} | {s['candidate_mean']:.15f} | {s['gains']} / {s['ties']} / {s['losses']} |")
lines+=['','Own-repeat rows compare the primary arm to its unchanged repeat; gains refer to the repeat. Development3300–3311 is development, not Private or a native fresh promotion gate. Panels are not pooled into a selection metric.','', '## All paired differences','']
for key,s in summary.items():
 if key=='diagnostics': continue
 lines += [f'### {key}','','| Trajectory | Baseline | Candidate | Delta |','|---|---:|---:|---:|']
 for p in s['pairs']: lines.append(f"| {p['trajectory_id']} | {p['baseline']:.12f} | {p['candidate']:.12f} | {p['delta']:+.12f} |")
 lines.append('')
lines += ['## Observation coverage','', 'Detailed live observation failed serialization, while episode start/end records survived. A separate post-freeze fixture reproduced the cause: NumPy integers in level keys passed to JSON without conversion. That fixture also confirmed identical actions with diagnostics on/off/unwritable; it did not repair or edit either frozen runtime. The production fixtures used ordinary Python integers and did not expose this. Log exceptions were swallowed by the diagnostic support, as required; terminal records explicitly count failed event writes. Frozen arms were not repaired after scored gameplay began. Consequently zero retained detailed events does NOT mean zero mechanism activations. Double-write activation, normalization activation, and game duration cannot be measured from these failed observations. No seed association is inferred from PID, filename, or order.','', '| Batch | Streams | Events | Failed writes | Cap drops | Missing end |','|---|---:|---|---:|---:|---:|']
for n,c in coverage.items(): lines.append(f"| {n} | {c['streams']} | {c['events']} | {c['write_failures']} | {c['dropped_by_cap']} | {c['missing_terminal']} |")
lines+=['','The generator-resumption emission timestamp also uses cached Agent.blstats before update_state completes. It must not be interpreted as an exact live write duration. The post-operation attempt-return record would supply a later timestamp, but those records also failed. Fixture completion and synthetic three-turn duration are not NetHack protection or wins.','', '## Frozen implementation and provenance','', 'All 51 supplied runtime/license/manifest hashes verified before editing (`source-verification.json`). Baseline: github.com/Xenox-developer/nethacker@56cd7f631d7a2400ec3366aa2d7f539524829572, prog_64e10a9e6ae1e9aa93ffcdca5dc14e17; historical full-tree SHA256 1e2f694943be0b87314c48f014bb290a26f836957193130ca90e319899552230. Runtime manifests are separate and do not claim that historical full-tree digest.','', 'Mechanism: github.com/Xenox-developer/nethacker@52613eaea15fbf5eb836bf20f69ac083775edcbe, prog_cbd8377702ca06ae133736523ded47b5; full digest 4f6cf4fbf168f8d9095faf4261b53b04170add636be5fd07b2c29e0b15ed8a77. Only the two connected policy hunks were transplanted. Existing MIT license and attribution remain. The incoming agent.py and inventory.py hashes match the supplied reference44 files; its vkurenkov-family lineage remains recorded in the candidate manifest, alongside exact31/44 influences. `/refs/parent` preserves the complete incoming native outer baseline.','', 'Candidate sends exactly Elbereth Elbereth plus carriage return only for blind, case-insensitive exact Elbereth requests; otherwise requested text is preserved. Existing append response stays n. Actual engraving readings containing an intact case-insensitive elbereth substring normalize to Elbereth. Every unrelated31 policy, caller, depth guard, cap, action budget and the exact31 adapter remain unchanged. Diagnostic support is byte-identical in both arms and defaults off.','', '## Validation and reproducibility','', 'Executable fixtures: `private31_experiment/fixtures.py`; outputs retained for both arms in off/on/unwritable modes. Tests call real Agent.engrave and Inventory.get_items_below_me, cover case variants, doubled and damaged strings, no intact substring, unrelated/no message, append n, denial ESC, interruption, and can_engrave eligibility. Action outputs were identical across diagnostic modes. AST equality verifies all Agent methods outside engrave; all other policy modules and adapter are byte-identical to31. Both arms compile and ran native gameplay.','', 'Freeze timestamp, artifact hashes, separate policy/diagnostic/manifest diffs, and both runtime manifests are retained in `private31_experiment/`. Four batches ran sequentially: baseline-primary27, candidate-primary27, baseline-repeat15, candidate-repeat15. Each batch directory retains exact argv, environment subset, timestamps, exit status, raw result rows, stdout, stderr, and traces. Settings: public secret, local namespace, val-dwa-law-fem, max_steps1,000,000, no_progress10,000, action_timeout120s, max parallel4. No evaluator internals or hidden trajectories inspected.','', '## Selection and limitations','', 'This is an experiment, not proof of improvement or causality. Repeat variability must be considered alongside primary differences. Live diagnostic failures prevent an activation/protection claim. The fully tested combined candidate is left at `/workspace` for ordinary native full Public scoring/publication, even if these internal panels lose or tie. The native outer baseline remains the actual incoming champion in `/refs/parent`; that cross-family comparison does not isolate these two hunks. Champion promotion still requires native same-run Public improvement and fresh local validation. No host evolve cycle, champion promotion, or external publication was performed here; existing recovery and pinned-commit behavior were not changed.','']
(R.parent/'PRIVATE31_DOUBLE_BLIND_EXPERIMENT.md').write_text('\n'.join(lines))
print(json.dumps({k:{a:b for a,b in v.items() if a!='pairs'} for k,v in summary.items()},indent=2))
