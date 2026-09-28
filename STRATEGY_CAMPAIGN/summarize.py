"""Complete evidence tables without modifying evaluation rows or choosing new seeds."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(next(Path('/workspace/EXPERIMENT_ASSETS').glob('*/campaign.py')).parent))
import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN')
report=campaign.report(out,['A','B','C'])
for label,comparison in report['comparisons'].items():
 record=json.loads((out/'variants'/label/'evaluation.json').read_text())
 comparison['game_count']=sum(len(campaign.selected_rows(record,phase)) for phase in campaign.BATCHES)
 comparison['rows']={phase:campaign.selected_rows(record,phase) for phase in campaign.BATCHES}
 for phase,pairs in comparison['paired'].items():
  comparison[phase+'_gains_ties_losses']={name:sum(test(p['delta']) for p in pairs) for name,test in [('gains',lambda x:x>0),('ties',lambda x:x==0),('losses',lambda x:x<0)]}
report['primary_game_count']=sum(c['game_count'] for c in report['comparisons'].values())
label=report['final_publication_candidate']
if label:
 pairs=report['comparisons'][label]['paired']
 seeds=[min(pairs['public'],key=lambda p:(-p['delta'],p['seed']))['seed'],
        min(pairs['public'],key=lambda p:(p['delta'],p['seed']))['seed'],
        min(pairs['development'],key=lambda p:(-abs(p['delta']),p['seed']))['seed']]
 report['diagnostic_seeds']=list(dict.fromkeys(seeds))
campaign.atomic_json(out/'report.json',report)
print(json.dumps({k:v for k,v in report.items() if k not in ('comparisons','activation')},indent=2))
