"""Install only the completed, frozen candidate; keep native incoming archive intact."""
from pathlib import Path
import json,hashlib,shutil,datetime
E=Path(__file__).resolve().parent;W=E.parent
freeze=json.loads((E/'freeze.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for arm,files in freeze['arms'].items():
 for p,h in files.items():assert sha(E/arm/p)==h,(arm,p)
for b in freeze['batches']:
 rows=json.loads((E/(b['name']+'-raw.json')).read_text())
 assert len(rows)==len(b['seeds'])
 assert sorted(r['trajectory_id'] for r in rows)==b['seeds']
 assert json.loads((E/(b['name']+'-exit.json')).read_text())['exit_code']==0
# The root is the candidate submission workspace, not the native champion store.
shutil.rmtree(W/'autoascend')
shutil.copytree(E/'candidate/autoascend',W/'autoascend',ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.nbc','*.nbi'))
for p in ['bot.py','arena_adapter.py','LICENSE','nethackers.solution.json']:shutil.copyfile(E/'candidate'/p,W/p)
assert all(sha(W/p)==h for p,h in freeze['arms']['candidate'].items())
(E/'final-audit.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arms_unchanged':True,'installed_candidate_matches_freeze':True,'games':84,'native_champion_replaced':False,'outer_scoring_publication':'pending enclosing native workflow','incoming_preserved_sha256':sha(E/'incoming-outer-champion.tar.gz')},indent=2))
