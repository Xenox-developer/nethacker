from pathlib import Path
import sys,shutil,subprocess,os
assets=next(Path('/workspace/EXPERIMENT_ASSETS').glob('20260927T215044*'))
sys.path.insert(0,str(assets));import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN');base=Path('/tmp/campaign-baseline')
flags={'A':'WAND_BRANCH_PROBABILITY','B':'TOOL_SHOP_RESERVE','C':'ELBERETH_FAILURE_OVERRIDE'}
def prepare(label):
    target=Path('/tmp/campaign-'+label.replace('+',''))
    shutil.copytree(base,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.nbc','*.nbi'))
    config=target/'autoascend/jf_config.py';text=config.read_text()
    for member in label.split('+'):text=text.replace(flags[member]+' = False',flags[member]+' = True')
    config.write_text(text)
    if "B" in label.split("+"):
        subprocess.run([sys.executable,str(out/"food-settlement-fix.py"),str(target)],check=True)
    with (out/f'fixtures-{label}.log').open('w') as log:
        subprocess.run([sys.executable,str(out/'test_strategies.py')],env={**os.environ,'CAMPAIGN_SOURCE':str(target)},stdout=log,stderr=log,check=True)
    (out/f'{label}-from-incoming.patch').write_text(campaign.patch(campaign.files('/tmp/campaign-incoming'),campaign.files(target)))
    campaign.atomic_json(out/f'{label}-before.json',campaign.manifest(campaign.files(target)))
    return target
if __name__=='__main__':
    campaign.atomic_json(out/'baseline-before.json',campaign.manifest(campaign.files(base)))
    (out/'common-preparation.patch').write_text(campaign.patch(campaign.files('/tmp/campaign-incoming'),campaign.files(base)))
    for label in sys.argv[1:] or ['A','B','C']:print(prepare(label))
