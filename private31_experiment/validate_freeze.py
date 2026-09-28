from pathlib import Path
import subprocess,json,hashlib,ast,difflib,datetime
R=Path(__file__).resolve().parent; A=next((R.parent/'EXPERIMENT_ASSETS').glob('20260928T094*'))
for arm in ['baseline','candidate']:
 for mode in ['off','on','unwritable']:
  run=subprocess.run(['python',str(R/'fixtures.py'),arm,mode],capture_output=True,text=True)
  (R/f'fixture-{arm}-{mode}.json').write_text(run.stdout)
  (R/f'fixture-{arm}-{mode}.stderr').write_text(run.stderr)
  assert run.returncode==0,run.stderr
 assert len({(R/f'fixture-{arm}-{m}.json').read_text() for m in ['off','on','unwritable']})==1
# Verify untouched caller functions, retry caps, adapter and all unrelated source files.
original=A/'base31-runtime'
for arm in ['baseline','candidate']:
 for p in original.rglob('*.py'):
  rel=p.relative_to(original)
  if str(rel) in ['autoascend/agent.py','autoascend/item/inventory.py','bot.py']: continue
  assert p.read_bytes()==(R/arm/rel).read_bytes(),rel
 orig=ast.parse((original/'autoascend/agent.py').read_text()); new=ast.parse((R/arm/'autoascend/agent.py').read_text())
 oldcls=next(n for n in orig.body if isinstance(n,ast.ClassDef) and n.name=='Agent')
 newcls=next(n for n in new.body if isinstance(n,ast.ClassDef) and n.name=='Agent')
 for x,y in zip(oldcls.body,newcls.body):
  if isinstance(x,ast.FunctionDef) and x.name=='engrave': continue
  assert ast.dump(x)==ast.dump(y),getattr(x,'name','?')
 for p in (R/arm).rglob('*.py'): compile(p.read_text(),str(p),'exec')
assert (R/'baseline/autoascend/engraving_diagnostics.py').read_bytes()==(R/'candidate/autoascend/engraving_diagnostics.py').read_bytes()
# Controlled event assertions, including interrupted write.
for p in (R/'fixture-traces').glob('*.jsonl'):
 rows=[json.loads(l) for l in p.read_text().splitlines()]
 assert rows[0]['event']=='start' and rows[-1]['event']=='end'
 ends=[r for r in rows if r['event']=='emission_end']
 assert sum(r['completed'] for r in ends)==5
 assert sum(r['interrupted'] for r in ends)==1
 assert len([r for r in rows if r['event']=='reading'])==6
 assert all(r['turn']==13 for r in ends if r['completed'])
# Preserve native incoming manifest lineage while explicitly recording exact reused sources.
p=R/'candidate/nethackers.solution.json'; m=json.loads(p.read_text()); incoming=json.loads((R/'incoming/nethackers.solution.json').read_text())
m['parents']=incoming['parents']; m['influences']=list(dict.fromkeys(incoming['influences']+m.get('influences',[])+['github.com/Xenox-developer/nethacker@56cd7f631d7a2400ec3366aa2d7f539524829572','github.com/Xenox-developer/nethacker@52613eaea15fbf5eb836bf20f69ac083775edcbe']))
p.write_text(json.dumps(m,indent=2)+'\n')
(R/'candidate-manifest.diff').write_text(''.join(difflib.unified_diff((original/'nethackers.solution.json').read_text().splitlines(True),p.read_text().splitlines(True))))
def hashes(d): return {str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
for arm in ['incoming','baseline','candidate']: (R/(arm+'-manifest.json')).write_text(json.dumps(hashes(R/arm),indent=2)+'\n')
freeze={'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifacts':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in R.iterdir() if p.is_file() and p.name!='freeze.json'}}
(R/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
print('PASS: production generator and parser fixtures; on/off/unwritable action equality; interruption coverage; unchanged callers/caps/adapter; source compile; frozen manifests.')
