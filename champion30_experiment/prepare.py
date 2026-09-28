from pathlib import Path
import hashlib,json,shutil,tarfile,difflib
W=Path('/workspace'); E=W/'champion30_experiment'; A=W/'EXPERIMENT_ASSETS/20260928T045001057713Z-e678ebe57d7e492fbe3650d77da1d660'; B=A/'base30-runtime'
def hashes(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
expected=json.loads((A/'base30-runtime-hashes.json').read_text()); actual=hashes(B)
assert actual==expected
(E/'asset-verification.json').write_text(json.dumps({'verified':len(actual),'hashes':actual},indent=2))
with tarfile.open(E/'incoming-outer-champion.tar.gz','w:gz') as t:
 for p in W.iterdir():
  if p!=E: t.add(p,arcname=p.name)
for arm in ('baseline','hybrid'):
 shutil.copytree(B,E/arm)
# Restore exact runtime package, including absence of extra outer-package files.
shutil.rmtree(W/'autoascend')
for p in B.iterdir():
 if p.is_dir(): shutil.copytree(p,W/p.name)
 else: shutil.copy2(p,W/p.name)
p=E/'hybrid/autoascend/dive_logic.py'; old=p.read_text()
s=old.replace('        if not near and not (ELBERETH_ALWAYS or self.on_medusa_level() or bl.hunger_state >= Hunger.WEAK or\n                             rewrite):', '''        # hypothesis: depth >= 20 pre-dig protection covers unseen arrivals.
        # Adapted from Xenox-developer/nethacker@7d546b6ab2b972c793489801f609aa691fc82b44.
        deep_dig = bl.depth >= 20
        if not near and not (ELBERETH_ALWAYS or deep_dig or self.on_medusa_level() or
                             bl.hunger_state >= Hunger.WEAK or rewrite):''')
assert s!=old;p.write_text(s)
(E/'policy.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='baseline/autoascend/dive_logic.py',tofile='hybrid/autoascend/dive_logic.py')))
p=E/'hybrid/nethackers.solution.json'; m=json.loads(p.read_text());m['parents'].append('github.com/Xenox-developer/nethacker@b01a1eef34751eb044a6971f1a2735e6007a7d3f');m['influences'].append('github.com/Xenox-developer/nethacker@7d546b6ab2b972c793489801f609aa691fc82b44');p.write_text(json.dumps(m,indent=2)+'\n')
print('Verified 47 runtime hashes; preserved incoming outer champion; prepared arms.')
