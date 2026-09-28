"""Post-freeze diagnosis only; does not edit either runtime or rerun scored games."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parent
s=(R/'fixtures.py').read_text().replace('import sys,os,json,contextlib','import sys,os,json,contextlib\nimport numpy as np').replace('key=lambda:(0,1)','key=lambda:(np.int64(0),np.int64(1))').replace("out=root/'fixture-traces'","out=root/'numpy-fixture-traces'")
p=R/'fixtures_numpy.py'; p.write_text(s)
for arm in ['baseline','candidate']:
 outputs=[]
 for mode in ['off','on','unwritable']:
  r=subprocess.run(['python',str(p),arm,mode],capture_output=True,text=True)
  (R/f'numpy-{arm}-{mode}.stdout').write_text(r.stdout); (R/f'numpy-{arm}-{mode}.stderr').write_text(r.stderr)
  assert r.returncode==0,r.stderr
  outputs.append(r.stdout)
 assert len(set(outputs))==1
for f in (R/'numpy-fixture-traces').glob('*.jsonl'):
 rows=[json.loads(l) for l in f.read_text().splitlines()]
 assert [r['event'] for r in rows]==['start','end']
 assert rows[-1]['write_failures']>0
print('Reproduced: NumPy level keys suppress detailed events; terminal failure count is retained. Real generator/parser action outputs remain identical across off/on/unwritable modes. Runtime arms untouched.')
