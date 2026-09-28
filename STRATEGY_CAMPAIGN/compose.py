"""Compose eligible members exclusively from frozen B0 and singleton deltas."""
from pathlib import Path
import json,sys
root=Path('/workspace');out=root/'STRATEGY_CAMPAIGN'
sys.path.insert(0,str(next((root/'EXPERIMENT_ASSETS').iterdir())))
import campaign as c
r=c.report(out,['A','B','C'])
label=sys.argv[1];assert label in r['required_combinations']
contents=c.files('/tmp/campaign-baseline');target=Path('/tmp/campaign-'+label.replace('+',''));target.mkdir()
if 'B' in label:contents['autoascend/item/inventory.py']=c.files('/tmp/campaign-B')['autoascend/item/inventory.py']
for member in label.split('+'):
    contents['autoascend/jf_config.py']=contents['autoascend/jf_config.py'].replace(f'CAMPAIGN_{member} = False'.encode(),f'CAMPAIGN_{member} = True'.encode())
for name,data in contents.items():
    p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
c.atomic_json(out/f'{label}-pre-evaluation-manifest.json',c.manifest(contents))
(out/f'{label}-from-incoming.patch').write_text(c.patch(c.files('/tmp/campaign-incoming'),contents))
print(target)
