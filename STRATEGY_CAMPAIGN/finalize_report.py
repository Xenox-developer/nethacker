"""Augment the supplied helper report with complete rows, counts and controls."""
import json,sys,collections
from pathlib import Path
assets=next(Path('/workspace/EXPERIMENT_ASSETS').glob('20260927T215044*'))
sys.path.insert(0,str(assets));import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN')
r=campaign.report(out,['A','B','C'])
records={label:json.loads((out/'variants'/label/'evaluation.json').read_text()) for label in r['comparisons']}
r['incoming_manifest']=json.loads((out/'incoming-manifest.json').read_text())
r['all_rows']={label:{phase:campaign.selected_rows(record,phase) for phase in campaign.BATCHES} for label,record in records.items()}
r['counts']={label:{phase:len(rows) for phase,rows in phases.items()} for label,phases in r['all_rows'].items()}
for label, phases in r['all_rows'].items():
    rows = [row for values in phases.values() for row in values]
    r['comparisons'][label]['means']['overall'] = sum(row['progress'] for row in rows) / len(rows)
    pairs = [pair for values in r['comparisons'][label]['paired'].values() for pair in values]
    r['comparisons'][label]['overall_paired'] = {'mean_delta': sum(p['delta'] for p in pairs)/len(pairs), 'gains': sum(p['delta']>0 for p in pairs), 'ties': sum(p['delta']==0 for p in pairs), 'losses': sum(p['delta']<0 for p in pairs)}
r['primary_games']=sum(sum(phases.values()) for phases in r['counts'].values())
r['attempted_result_rows_including_technical_failures']=sum(len(a.get('results',[])) for rec in records.values() for attempts in rec['phases'].values() for a in attempts)
r['outcomes']={}
for label,phases in r['all_rows'].items():
    r['outcomes'][label]={}
    source=Path('/tmp/campaign-'+label.replace('+',''))
    after=campaign.manifest(campaign.files(source));campaign.atomic_json(out/f'{label}-after.json',after)
    assert after['digest']==records[label]['solution_digest']
    for phase,rows in phases.items():
        deltas=r['comparisons'][label]['paired'][phase]
        r['outcomes'][label][phase]={
          'gains':sum(p['delta']>0 for p in deltas),'ties':sum(p['delta']==0 for p in deltas),'losses':sum(p['delta']<0 for p in deltas),
          'errors':[row for row in rows if row.get('error') is not None or row.get('status')!='completed'],
          'deaths':dict(collections.Counter(row.get('cause_of_death') for row in rows)),
          'mean_depth':sum(row.get('max_depth',0) for row in rows)/len(rows),
          'mean_turns':sum(row.get('turns',0) for row in rows)/len(rows)}
r['food_samples']={}
for label,record in records.items():
    samples=[]
    for phase,attempts in record['phases'].items():
        directory=out/'variants'/label/attempts[-1]['events_directory']
        for p in directory.glob('samples-*.jsonl'):
            for line in p.read_text().splitlines():
                value=json.loads(line)
                if value.get('kind')=='food_transaction':samples.append(value)
    r['food_samples'][label]={'bounded_samples':samples,'complete_transaction_totals':False,'per_seed_attribution':False}
controls=out/'controls'
r['controls']=None
if (controls/'selection.json').exists():
    selection=json.loads((controls/'selection.json').read_text())
    candidate=selection['candidate'];control_rows={}
    for label in ['baseline',candidate]:
        if not json.loads((controls/label/'complete.json').read_text())['complete']:raise RuntimeError('Incomplete controls')
        control_rows[label]=campaign.validate_rows(json.loads((controls/label/'results.json').read_text()),selection['seeds'])
    original={p['seed']:p for pairs in r['comparisons'][candidate]['paired'].values() for p in pairs}
    comparisons=[]
    for a,b in zip(control_rows['baseline'],control_rows[candidate],strict=True):
        old=original[a['trajectory_id']];delta=b['progress']-a['progress']
        comparisons.append({'seed':a['trajectory_id'],'primary_delta':old['delta'],'control_delta':delta,
          'baseline_primary':old['old'],'baseline_control':a['progress'],'candidate_primary':old['new'],'candidate_control':b['progress'],
          'unexpected_reversal':old['delta']*delta<0,
          'primary_gain_not_reproduced':old['delta']>0 and delta<=0,
          'baseline_progress_changed':old['old']!=a['progress'],'candidate_progress_changed':old['new']!=b['progress']})
    r['controls']={'selection':selection,'rows':control_rows,'paired':comparisons,'game_count':2*len(selection['seeds']),
                   'unexpected_reversal':any(p['unexpected_reversal'] for p in comparisons),
                   'primary_gain_not_reproduced':any(p['primary_gain_not_reproduced'] for p in comparisons),
                   'confidence_lowered':any(p['unexpected_reversal'] or p['primary_gain_not_reproduced'] for p in comparisons)}
r['recommendation_text']='NO recommended improvement' if r['recommended']=='baseline' else r['recommended']
r['technical_retry_count'] = sum(len(attempts)-1 for rec in records.values() for attempts in rec['phases'].values())
r['confidence'] = {'level': 'limited', 'reason': 'Small development-selected sample; endpoint differences lack recorded selected-action attribution for A. Native fresh validation remains required.'}
if r['controls'] and r['controls']['confidence_lowered']:
    r['confidence'] = {'level': 'low', 'reason': 'Diagnostic repeats failed to reproduce primary gains; no robust endpoint improvement is established.'}
r['source_integrity']='All completed helper batches verified unchanged sanitized runtime source; retained before/after manifests also match.'
r['limitations']=[
  'Twenty shared selection/development trajectories per arm; development2000–2004 are not an untouched holdout.',
  'Diagnostics are bounded aggregate lower bounds, not per-seed attribution. Missing counters do not demonstrate absence; zero activation is lack of coverage.',
  'Branching/wand evaluation counters include actual and opposite-calculation diagnostic projections; changed scoring is distinguished from a changed selected action.',
  'Observed protected HP loss does not establish an attacker identity or damage cause.',
  'Native outer Public scoring and fresh local validation remain the authority for promotion.'
]
campaign.atomic_json(out/'report.json',r)
lines=['# Strategy campaign report','',f"Request `{assets.name}`.",'',
       f"**Fixed-rule screening recommendation: {r['recommendation_text']}. Final publication candidate: {r['final_publication_candidate']}.**",'',
       f"Completed {r['primary_games']} primary games plus {r['controls']['game_count'] if r['controls'] else 0} separate diagnostic control games. All required combinations complete: {r['complete']}.",
       '', '| Variant | Public n | Public mean | Development n | Development mean | Overall mean | Public G/T/L | Dev G/T/L | Errors |',
       '|---|---:|---:|---:|---:|---:|---|---|---:|']
if r['controls'] and all(p['control_delta']==0 for p in r['controls']['paired']):
    lines[8:8] = ['The diagnostic controls produced three paired score ties. A’s primary gains did not reproduce; confidence is **low**, and no robust strategy improvement is established. The fixed-rule selection above is retained without claiming success.', '']
for label,comp in r['comparisons'].items():
    p=r['outcomes'][label]['public'];d=r['outcomes'][label]['development'];counts=r['counts'][label]
    lines.append(f"| {label} | {counts['public']} | {comp['means']['public']:.12f} | {counts['development']} | {comp['means']['development']:.12f} | {comp['means']['overall']:.12f} | {p['gains']}/{p['ties']}/{p['losses']} | {d['gains']}/{d['ties']}/{d['losses']} | {len(p['errors'])+len(d['errors'])} |")
lines+=['',f"Eligible singles: {', '.join(r['eligible_singles']) or 'none'}. Required combinations: {', '.join(r['required_combinations']) or 'none'}. Missing combinations: {', '.join(r['missing_combinations']) or 'none'}.",
        '', 'Eligibility requires strictly higher Public mean, nonregressing development mean and no errors. Every required combination is compared against the strongest eligible singleton; a combination must strictly improve Public and not regress development. Ties use development then alphabetic label.']
if r['recommended']=='baseline':lines+=['','The final singleton is a fully tested negative/mixed experiment, **not a recommended improvement**. Its publication does not imply promotion.']
lines+=['','## Integrity and implementation','',f"Incoming digest: `{r['incoming_manifest']['digest']}`.",f"Instrumented B0 digest: `{r['baseline_digest']}`.",'',r['source_integrity'],
        '', 'See [protocol](PROTOCOL.md), [focused fixtures](test_strategies.py), per-arm fixture logs, `incoming-manifest.json`, `common-preparation.patch`, instrumentation patches and `*-from-incoming.patch`. Complete copies remain outside the publication tree in `/tmp`. All flags begin off; independent singletons enable A, B or C only. B includes the documented pre-game nested-pickup refresh correction. Existing inherited changes, adapter, entrypoint and license are preserved.',
        '', '## Diagnostics','', 'Counters below are process aggregates and lower bounds. They include the selected technical attempt only. Raw counter files and bounded samples remain beside each native JSON. They have no invented per-seed attribution.']
for label,data in r['activation'].items():
    counts=data['selected_attempt_counts'];lines+=['',f'### {label}','', '```json',json.dumps(counts,indent=2,sort_keys=True),'```']
    if 'A' in label and not counts.get('A.chosen_action_changed'):
        lines+=['','No selected-action change was recorded for A. Any endpoint score difference therefore lacks direct action-change attribution; score-calculation changes alone do not establish behavioral improvement.']
    if 'B' in label and not counts.get('B.started'):lines+=['','B had no recorded started transaction: this sample does not establish usefulness or uselessness of purchases.']
    if 'C' in label and not counts.get('C.exception_activated'):lines+=['','C had no recorded emergency suppression bypass: no gameplay-effect coverage is established.']
    samples=r['food_samples'][label]['bounded_samples']
    if samples:lines+=['','Bounded food stock/elapsed-turn samples:', '', '```json',json.dumps(samples,indent=2),'```']
lines+=['','## Diagnostic controls','']
if r['controls']:
    lines += ['Seeds were preselected from primary paired deltas and written before either control run. Criteria and ties are fixed; repetitions do not enter primary means.', '',
              '| Seed | Primary delta | Control delta | Baseline primary/control | Candidate primary/control | Reversal or lost gain |','|---:|---:|---:|---|---|---|']
    for p in r['controls']['paired']:
        lines.append(f"| {p['seed']} | {p['primary_delta']:+.12f} | {p['control_delta']:+.12f} | {p['baseline_primary']:.12f}/{p['baseline_control']:.12f} | {p['candidate_primary']:.12f}/{p['candidate_control']:.12f} | {p['unexpected_reversal'] or p['primary_gain_not_reproduced']} |")
    lines+=['', 'Unexpected reversal or failure to reproduce a primary gain lowers confidence.' if r['controls']['confidence_lowered'] else 'No unexpected score reversal or lost primary gain was observed in these controls.']
else:lines+=['Controls are not complete.']
lines+=['', '**Confidence: ' + r['confidence']['level'] + '.** ' + r['confidence']['reason']]
lines+=['','## All primary rows','', 'Depth, turns, status, errors and death labels are retained verbatim in the machine-readable report and raw native JSON.']
for label,phases in r['all_rows'].items():
    lines+=['',f'### {label}','', '| Seed | Score | Paired delta | Depth | Turns | Status | Death / error |','|---:|---:|---:|---:|---:|---|---|']
    for phase,rows in phases.items():
        deltas={p['seed']:p['delta'] for p in r['comparisons'][label]['paired'][phase]}
        for row in rows:
            detail=str(row.get('error') or row.get('cause_of_death') or '').replace('|','/').replace('\n',' ')
            lines.append(f"| {row['trajectory_id']} | {row['progress']:.12f} | {deltas[row['trajectory_id']]:+.12f} | {row.get('max_depth')} | {row.get('turns')} | {row['status']} | {detail} |")
lines+=['','## Limits and provenance','']+[f'- {s}' for s in r['limitations']]
lines+=['','The frozen research notes cite AutoAscend/NetHack Challenge, HiHack and NetHack hunger/ray mechanics as motivation. They do not establish measured gains. No peer strategy source was copied; the incoming license is preserved. No judge, arena adapter, secret derivation, seed list, limits, local champion state or publication machinery was changed.']
(out/'REPORT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({key:r[key] for key in ['complete','primary_games','eligible_singles','required_combinations','recommended','final_publication_candidate']},indent=2))
