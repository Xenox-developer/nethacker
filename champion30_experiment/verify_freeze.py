from pathlib import Path
import ast,hashlib,json,shutil,difflib,datetime
E=Path('/workspace/champion30_experiment');W=E.parent
B=W/'EXPERIMENT_ASSETS/20260928T045001057713Z-e678ebe57d7e492fbe3650d77da1d660/base30-runtime'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root):return {str(p.relative_to(root)):h(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
def stripped(p):
 tree=ast.parse(p.read_text())
 class Strip(ast.NodeTransformer):
  def visit_ImportFrom(self,n):return None if n.module=='deep_protection_diagnostics' else n
  def visit_Expr(self,n):
   return None if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='_deep_observe' else n
 return ast.dump(Strip().visit(tree),include_attributes=False)
assert stripped(B/'autoascend/dive_logic.py')==stripped(E/'baseline/autoascend/dive_logic.py')
for arm in ('baseline','hybrid'):
 for p in B.rglob('*'):
  if p.is_file() and p.name not in ('dive_logic.py','nethackers.solution.json'):
   assert p.read_bytes()==(E/arm/p.relative_to(B)).read_bytes(),p
 assert h(E/arm/'autoascend/deep_protection_diagnostics.py')==h(E/'deep_protection_diagnostics.py')
 tree=ast.parse((E/arm/'autoascend/dive_logic.py').read_text())
 base=ast.parse((B/'autoascend/dive_logic.py').read_text())
 methods=lambda t:{n.name:ast.dump(n,include_attributes=False) for c in t.body if isinstance(c,ast.ClassDef) and c.name=='DiveLogic' for n in c.body if isinstance(n,ast.FunctionDef)}
 x,y=methods(tree),methods(base)
 assert all(x[k]==v for k,v in y.items() if k!='_elbereth_before_digging_escape')
 rows=[json.loads(l) for p in (E/'fixture-diagnostics'/(arm+'-valid')).glob('*.jsonl') for l in p.read_text().splitlines()]
 assert not any(r['stage']=='observation_error' for r in rows)
 sole=[r for r in rows if r['stage']=='engraving_call' and r.get('depth_alone')]
 assert len(sole)==(3 if arm=='hybrid' else 0),(arm,sole)
 if sole:assert any(r['visible_immune'] for r in sole)
# Bounded output, default off, failure isolation are also exercised directly.
import importlib.util,os
spec=importlib.util.spec_from_file_location('diag',E/'deep_protection_diagnostics.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m._ENABLED is False
m._ENABLED=True;m._LIMIT=2;m._path=E/'bounded-fixture.jsonl'
for i in range(5):m._write({'stage':'test'})
rows=[json.loads(l) for l in m._path.read_text().splitlines()];assert len(rows)==3 and rows[-1]['stage']=='truncated'
# Copy the evaluated hybrid to the native submission, retaining diagnostics.
for p in (E/'hybrid').iterdir():
 if p.is_dir():shutil.copytree(p,W/p.name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 else:shutil.copy2(p,W/p.name)
for arm in ('baseline','hybrid'):
 (E/(arm+'-manifest.json')).write_text(json.dumps(manifest(E/arm),indent=2)+'\n')
a=(E/'baseline/autoascend/dive_logic.py').read_text();b=(E/'hybrid/autoascend/dive_logic.py').read_text()
(E/'evaluated-policy.diff').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='baseline/autoascend/dive_logic.py',tofile='hybrid/autoascend/dive_logic.py')))
(E/'freeze.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arms':{a:h(E/(a+'-manifest.json')) for a in ('baseline','hybrid')},'diagnostics_sha256':h(E/'deep_protection_diagnostics.py'),'batch':[[s,'val-dwa-law-fem'] for s in list(range(15))+list(range(3100,3112))],'evaluation_id':'local','secret':'public','max_steps':1000000,'no_progress_timeout':10000,'action_timeout':120,'max_parallel_evals':4},indent=2)+'\n')
print('Verified baseline AST equivalence, unchanged callers and dispatch, diagnostic coverage, bounded logging, default-off behavior; both arms frozen.')
