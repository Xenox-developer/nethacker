from pathlib import Path
import hashlib,json,shutil,subprocess,difflib
R=Path('/workspace/private31_experiment'); A=next(Path('/workspace/EXPERIMENT_ASSETS').glob('20260928T094*')); B=A/'base31-runtime'
h=json.loads((A/'base31-runtime-hashes.json').read_text())
assert len(h)==51
for p,v in h.items(): assert hashlib.sha256((B/p).read_bytes()).hexdigest()==v,p
(R/'source-verification.json').write_text(json.dumps({'verified':h},indent=2))
for arm in ['incoming','baseline','candidate']:
 d=R/arm; d.mkdir(exist_ok=True)
 for p in h:
  src=(Path('/workspace') if arm=='incoming' else B)/p
  if not src.exists(): continue
  (d/p).parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,d/p)
subprocess.run(['patch','-p1','-i',str(A/'base31-with44-policy.diff')],cwd=R/'candidate',check=True)
p=R/'candidate/autoascend/agent.py'; p.write_text(p.read_text().replace('# Preserve attempt44 redundant blind inscription behavior.','# hypothesis: redundant blind words may retain one intact Elbereth.'))
(R/'policy.diff').write_text(''.join(''.join(difflib.unified_diff((R/'baseline'/p).read_text().splitlines(True),(R/'candidate'/p).read_text().splitlines(True),fromfile='a/'+p,tofile='b/'+p)) for p in h))
