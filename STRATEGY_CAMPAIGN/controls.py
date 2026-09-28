"""Separate deterministic diagnostic reruns, never included in primary means."""
import json,os,sys,subprocess
from pathlib import Path
assets=next(Path('/workspace/EXPERIMENT_ASSETS').glob('20260927T215044*'))
sys.path.insert(0,str(assets));import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN')
def select():
    report=json.loads((out/'report.json').read_text())
    label=report['final_publication_candidate']
    if not report['complete'] or label is None:raise RuntimeError('No fully tested final candidate')
    paired=report['comparisons'][label]['paired']
    choices={
      'largest_public_gain':min(paired['public'],key=lambda r:(-r['delta'],r['seed']))['seed'],
      'largest_public_loss':min(paired['public'],key=lambda r:(r['delta'],r['seed']))['seed'],
      'largest_development_absolute_difference':min(paired['development'],key=lambda r:(-abs(r['delta']),r['seed']))['seed']}
    result={'candidate':label,'criteria':choices,'seeds':sorted(set(choices.values())),
            'warning':'Diagnostic repeats only; never substituted into primary means.'}
    controls=out/'controls';controls.mkdir(exist_ok=False)
    campaign.atomic_json(controls/'selection.json',result)
    return result

def run(label):
    controls=out/'controls'
    selection=json.loads((controls/'selection.json').read_text())
    if label not in ['baseline',selection['candidate']]:raise ValueError(label)
    solution=Path('/tmp/campaign-'+label.replace('+',''))
    before=campaign.manifest(campaign.files(solution))
    directory=controls/label;directory.mkdir(exist_ok=False)
    campaign.atomic_json(directory/'before.json',before)
    events=directory/'events';events.mkdir()
    output=directory/'results.json'
    command=campaign.arena_command(solution,selection['seeds'],output)
    campaign.atomic_json(directory/'command.json',command)
    environment=dict(os.environ);environment.pop('NETHACK_ARENA_SECRET',None)
    environment.update(PYTHONDONTWRITEBYTECODE='1',NETHACKERS_CAMPAIGN_EVENTS_DIR=str(events))
    with (directory/'arena.log').open('w') as log:
        subprocess.run(command,check=True,timeout=1200,stdout=log,stderr=log,env=environment)
    rows=campaign.validate_rows(json.loads(output.read_text()),selection['seeds'])
    after=campaign.manifest(campaign.files(solution));campaign.atomic_json(directory/'after.json',after)
    if before != after:raise RuntimeError('Control source changed')
    campaign.atomic_json(directory/'complete.json',{'complete':True,'games':len(rows),'digest':after['digest']})

if __name__=='__main__':
    if sys.argv[1]=='select':print(json.dumps(select(),indent=2))
    else:run(sys.argv[1])
