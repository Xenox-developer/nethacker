"""Separate same-configuration controls; never substitute into campaign means."""
import sys,os,json,subprocess,tempfile,datetime
from pathlib import Path
sys.path.insert(0,str(next(Path('/workspace/EXPERIMENT_ASSETS').glob('*/campaign.py')).parent))
import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN'); report=json.loads((out/'report.json').read_text())
label=sys.argv[1]
assert report['complete'] and label in ('baseline',report['final_publication_candidate'])
seeds=report['diagnostic_seeds']
source=Path('/tmp/campaign-'+label.replace('+',''))
contents=campaign.files(source); before=campaign.manifest(contents)
dest=out/'controls'/label;dest.mkdir(parents=True,exist_ok=False)
record={'label':label,'seeds':seeds,'config':campaign.CONFIG,'before':before,'attempts':[],'complete':False}
campaign.atomic_json(dest/'control.json',record)
with tempfile.TemporaryDirectory(prefix='campaign-control-') as temporary:
 snapshot=Path(temporary)
 for name,data in contents.items():
  p=snapshot/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 for retry in range(2):
  results=dest/f'results-{retry}.json';events=dest/f'events-{retry}';events.mkdir()
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',NETHACKERS_CAMPAIGN_EVENTS_DIR=str(events));env.pop('NETHACK_ARENA_SECRET',None)
  attempt={'results_file':results.name,'technical_failure':False};record['attempts'].append(attempt)
  try:
   with (dest/f'run-{retry}.log').open('w') as log:
    subprocess.run(campaign.arena_command(snapshot,seeds,results),check=True,timeout=1200,stdout=log,stderr=log,env=env)
   rows=campaign.validate_rows(json.loads(results.read_text()),seeds);attempt['results']=rows
   attempt['technical_failure']=any(r.get('status')=='infrastructure_error' for r in rows)
  except (subprocess.SubprocessError,OSError,ValueError) as e:
   attempt.update(technical_failure=True,failure=f'{type(e).__name__}: {e}')
  campaign.atomic_json(dest/'control.json',record)
  if not attempt['technical_failure']:break
 if attempt['technical_failure']:raise RuntimeError('Control technical retry exhausted')
 record['after']=campaign.manifest(campaign.files(snapshot));assert record['after']==before
record['complete']=True;campaign.atomic_json(dest/'control.json',record)
print(label,'control complete',[(r['trajectory_id'],r['progress']) for r in rows])
