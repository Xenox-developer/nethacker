from pathlib import Path
import hashlib,json,datetime,difflib
E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def hashes(root):return {str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.nbc','.nbi')}
b=E/'baseline';c=E/'candidate'
assert (b/'autoascend/trap_diagnostics.py').read_bytes()==(c/'autoascend/trap_diagnostics.py').read_bytes()
(E/'evaluated-policy.diff').write_text(''.join(difflib.unified_diff((b/'autoascend/item/inventory.py').read_text().splitlines(True),(c/'autoascend/item/inventory.py').read_text().splitlines(True),fromfile='baseline/inventory.py',tofile='candidate/inventory.py')))
(E/'freeze.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arms':{arm:hashes(E/arm) for arm in ('baseline','candidate')},'evidence':{p.name:sha(p) for p in E.glob('*.diff')},'diagnostic_module':sha(E/'trap_diagnostics.py'),'batches':[{'name':name,'arm':arm,'seeds':list(range(15))+(list(range(3200,3212)) if count==27 else [])} for name,arm,count in [('baseline-primary','baseline',27),('candidate-primary','candidate',27),('baseline-repeat','baseline',15),('candidate-repeat','candidate',15)] ]},indent=2))
