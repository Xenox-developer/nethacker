from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parent; W=R.parent
freeze=json.loads((R/'freeze.json').read_text())
checks={p:hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in freeze['artifacts'].items()}
assert all(v for p,v in checks.items() if p.endswith('.diff') or p in ['baseline-manifest.json','candidate-manifest.json','fixtures.py','diagnostics.py'])
manifest=json.loads((R/'candidate-manifest.json').read_text())
for arm in ['baseline','candidate']:
 for p,h in json.loads((R/(arm+'-manifest.json')).read_text()).items(): assert hashlib.sha256((R/arm/p).read_bytes()).hexdigest()==h
integrity={'frozen_artifact_checks':checks,'runtime_arms_unchanged':True,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(R/'final-integrity.json').write_text(json.dumps(integrity,indent=2)+'\n')
# Complete native incoming copy already retained; install only the frozen tested candidate.
assert (R/'incoming-full/autoascend/agent.py').read_bytes()==(W/'autoascend/agent.py').read_bytes()
shutil.rmtree(W/'autoascend')
shutil.copytree(R/'candidate/autoascend',W/'autoascend',ignore=shutil.ignore_patterns('__pycache__'))
for name in ['arena_adapter.py','bot.py','LICENSE','nethackers.solution.json']: shutil.copy2(R/'candidate'/name,W/name)
for p,h in manifest.items(): assert hashlib.sha256((W/p).read_bytes()).hexdigest()==h,p
(R/'staged-candidate-verification.json').write_text(json.dumps({'matches_frozen_candidate':True,'files':manifest},indent=2)+'\n')
report=W/'PRIVATE31_DOUBLE_BLIND_EXPERIMENT.md'
with report.open('a') as f:
 f.write('\n## Final integrity and handoff\n\nAll 84 rows have status completed; all four batch commands exited 0. Both runtime manifests and all frozen policy/diagnostic diffs still match their pre-game hashes. The staged workspace runtime matches the frozen candidate byte-for-byte. A complete incoming runtime copy is retained at `private31_experiment/incoming-full/`, in addition to `/refs/parent`.\n\n')
 mismatches=[p for p,v in checks.items() if not v]
 f.write('The freeze index also included the redirected `validation.stdout` before its final success line was flushed; that one non-runtime output therefore differs from its indexed empty-file hash. Its final output and the original index are both retained. No runtime, fixture, or policy/diagnostic diff changed. Final artifact hashes are recorded separately.\n\n' if mismatches==['validation.stdout'] else 'Freeze-index differences: '+repr(mismatches)+'\n\n')
 f.write('Observed primary Public gain was +0.003173109407090; repeat Public delta was -0.000025932970317. Baseline own-repeat delta was -0.005839459618590, and candidate own-repeat delta was -0.009038501995996. The primary gain did not reproduce cleanly. This experiment supports no reliable benefit claim. Detailed mechanism observation remains incomplete due to the retained serialization failure.\n')
(W/'LOCAL_CHANGE.md').write_text('# Published31 plus attempt44 blind inscription experiment\n\nThe workspace contains the exact frozen candidate tested in 84 fixed games (42 per arm, 27 distinct trajectory IDs). Both connected attempt44 policy hunks are applied to published31, preserving its adapter and unrelated policy. Diagnostics default off.\n\nSee [PRIVATE31_DOUBLE_BLIND_EXPERIMENT.md](PRIVATE31_DOUBLE_BLIND_EXPERIMENT.md) for all panels, controls, losses, provenance, and observation failures. Primary Public improved slightly; repeat Public did not confirm the gain. Native same-run Public and fresh local validation still gate promotion. Incoming runtime is preserved in private31_experiment/incoming-full and /refs/parent.\n')
# Raw repeat differences, not just score ties; exclude wall time only.
summary=json.loads((R/'summary.json').read_text()); differences={}
for arm in ['baseline','candidate']:
 a={x['trajectory_id']:x for x in json.loads((R/(arm+'-primary')/'results.json').read_text())}
 b=json.loads((R/(arm+'-repeat')/'results.json').read_text())
 differences[arm]={str(x['trajectory_id']):{k:{'primary':a[x['trajectory_id']].get(k),'repeat':x.get(k)} for k in set(x)|set(a[x['trajectory_id']]) if k!='wall_seconds' and x.get(k)!=a[x['trajectory_id']].get(k)} for x in b}
(R/'own-repeat-field-differences.json').write_text(json.dumps(differences,indent=2)+'\n')
files={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='evidence-hashes.json'}
files[report.name]=hashlib.sha256(report.read_bytes()).hexdigest()
(R/'evidence-hashes.json').write_text(json.dumps(files,indent=2)+'\n')
print('84 completed results retained; four exit statuses 0; frozen arms/diffs verified; workspace matches frozen candidate; evidence index saved.')
