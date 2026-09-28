"""Install only the exact fully evaluated candidate after all required evidence."""
from pathlib import Path
import json,shutil,sys
assets=next(Path('/workspace/EXPERIMENT_ASSETS').glob('20260927T215044*'))
sys.path.insert(0,str(assets));import campaign
workspace=Path('/workspace');out=workspace/'STRATEGY_CAMPAIGN'
r=json.loads((out/'report.json').read_text())
assert r['complete'] and not r['missing_combinations']
assert r['controls'] and r['controls']['game_count']>0
label=r['final_publication_candidate'];assert label and label!='baseline'
for name in ['baseline','A','B','C',*r['required_combinations']]:
    record=json.loads((out/'variants'/name/'evaluation.json').read_text())
    assert record['complete']
    assert sum(len(campaign.selected_rows(record,phase)) for phase in campaign.BATCHES)==20
source=Path('/tmp/campaign-'+label.replace('+',''))
contents=campaign.files(source);expected=campaign.manifest(contents)
record=json.loads((out/'variants'/label/'evaluation.json').read_text())
assert expected['digest']==record['solution_digest']
assert b'# hypothesis:' in contents['autoascend/jf_config.py']
for name,content in contents.items():
    target=workspace/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)
for path in sorted(workspace.rglob('__pycache__'),reverse=True):
    if path.is_dir():shutil.rmtree(path)
for path in sorted(workspace.rglob('.pytest_cache'),reverse=True):
    if path.is_dir():shutil.rmtree(path)
actual=campaign.manifest(campaign.files(workspace));assert actual==expected
campaign.atomic_json(out/'final-install.json',{'candidate':label,'recommended':r['recommended'],
  'source':str(source),'exact_evaluated_source_installed':True,'sanitized_manifest':actual,
  'publication_performed':False,'note':'Native outer smoke/scoring/fresh gate/publication remain untouched.'})
print('Installed exact evaluated candidate',label,actual['digest'])
