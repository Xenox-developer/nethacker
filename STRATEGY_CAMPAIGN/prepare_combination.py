"""Compose only eligible members independently from the frozen common baseline."""
import sys,json,subprocess,os
from pathlib import Path
sys.path.insert(0,str(next(Path('/workspace/EXPERIMENT_ASSETS').glob('*/campaign.py')).parent))
import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN');r=campaign.report(out,['A','B','C']);label=sys.argv[1]
assert label in r['required_combinations'] and label in r['missing_combinations']
members=label.split('+');base=campaign.files('/tmp/campaign-baseline');contents=dict(base)
flags={'A':'CAMPAIGN_WAND','B':'TOOL_SHOP_RESERVE','C':'PROTECTION_FAILURE'}
for member in members:
 contents['autoascend/jf_config.py']=contents['autoascend/jf_config.py'].replace((flags[member]+' = False').encode(),(flags[member]+' = True').encode())
 # Capture only the member's pre-evaluation contract corrections, not another singleton's flag.
 if member=='B':contents['autoascend/item/inventory.py']=Path('/tmp/campaign-B/autoascend/item/inventory.py').read_bytes()
 if member=='C':contents['autoascend/protection_failure.py']=Path('/tmp/campaign-C/autoascend/protection_failure.py').read_bytes()
dest=Path('/tmp/campaign-'+''.join(members));dest.mkdir(exist_ok=False)
for name,data in contents.items():
 p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
campaign.atomic_json(out/(label+'-before.json'),campaign.manifest(campaign.files(dest)))
env=dict(os.environ,PYTHONPATH=str(dest))
with (out/(label+'-fixtures.log')).open('w') as log:
 subprocess.run(['python',str(out/'test_strategies.py')],cwd='/tmp',env=env,stdout=log,stderr=log,check=True)
 for member in members:
  if member in ('B','C'):subprocess.run(['python',str(out/'test_boundary_regressions.py'),member],cwd='/tmp',env=env,stdout=log,stderr=log,check=True)
print('Prepared',label,'from B0; focused fixtures passed')
