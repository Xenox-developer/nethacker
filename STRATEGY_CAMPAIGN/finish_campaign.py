"""Development evidence only: use the frozen campaign helper, never publish."""
from pathlib import Path
import json,sys,subprocess,os,tempfile
ROOT=Path('/workspace'); OUT=ROOT/'STRATEGY_CAMPAIGN'
sys.path.insert(0,str(next((ROOT/'EXPERIMENT_ASSETS').iterdir())))
import campaign as c

def report():
    r=c.report(OUT,['A','B','C'])
    for label,comp in r['comparisons'].items():
        path=OUT/'variants'/label
        record=json.loads((path/'evaluation.json').read_text())
        tree='/tmp/campaign-baseline' if label=='baseline' else '/tmp/campaign-'+label.replace('+','')
        after=c.manifest(c.files(tree)); before=json.loads((path/'files.json').read_text())
        assert after==before,(label,'source changed')
        c.atomic_json(path/'files-after.json',after)
        comp['rows']={phase:c.selected_rows(record,phase) for phase in c.BATCHES}
        comp['game_count']=sum(len(v) for v in comp['rows'].values())
        comp['pooled_mean']=sum(row['progress'] for rows in comp['rows'].values() for row in rows)/comp['game_count']
        comp['outcomes']={phase:{'gains':sum(p['delta']>0 for p in pairs),'ties':sum(p['delta']==0 for p in pairs),'losses':sum(p['delta']<0 for p in pairs)} for phase,pairs in comp['paired'].items()}
        comp['errors']=[row for rows in comp['rows'].values() for row in rows if row.get('error') or row['status']!='completed']
    r['primary_game_count']=sum(v['game_count'] for v in r['comparisons'].values())
    r['recommendation_status']='NO recommended improvement' if r['recommended']=='baseline' else 'development recommendation only'
    r['instrumentation_limitations']=['Aggregate process counters are lower bounds, without seed attribution.','B0/A/C dormant B opportunity counters use the ordinary-food estimate; B uses total edible carried nutrition.','Emergency action samples include all last-resort actions, not only exceptions.','A branch counters include active and shadow projections. Score changes and retained-candidate shadow reranking are distinct counters; this is not a full counterfactual trajectory replay.','Three-turn exception means trigger turn and the next two turns.','Source manifests exclude assets, evidence and caches as documented by campaign.py.']
    c.atomic_json(OUT/'report.json',r)
    return r

def controls():
    r=report(); assert r['complete'] and r['final_publication_candidate']
    label=r['final_publication_candidate']; comp=r['comparisons'][label]
    pub=comp['paired']['public']; dev=comp['paired']['development']
    choices=[('largest Public gain',min(pub,key=lambda p:(-p['delta'],p['seed']))),('largest Public loss',min(pub,key=lambda p:(p['delta'],p['seed']))),('largest development absolute difference',min(dev,key=lambda p:(-abs(p['delta']),p['seed'])))]
    seeds=list(dict.fromkeys(p['seed'] for _,p in choices))
    out=OUT/'controls';out.mkdir(exist_ok=False)
    c.atomic_json(out/'preselection.json',{'candidate':label,'seeds':seeds,'rules':[{'rule':rule,**p} for rule,p in choices],'config':c.CONFIG,'not_primary_data':True})
    for name,source in [('baseline',Path('/tmp/campaign-baseline')),(label,Path('/tmp/campaign-'+label.replace('+','')))]:
        d=out/name;d.mkdir();before=c.manifest(c.files(source));c.atomic_json(d/'files-before.json',before)
        events=d/'events';events.mkdir()
        env=dict(os.environ);env.pop('NETHACK_ARENA_SECRET',None);env.update(PYTHONDONTWRITEBYTECODE='1',NETHACKERS_CAMPAIGN_EVENTS_DIR=str(events))
        with tempfile.TemporaryDirectory(prefix='strategy-control-') as temporary:
            snapshot=Path(temporary)/'solution';snapshot.mkdir()
            for name,data in c.files(source).items():
                p=snapshot/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
            command=c.arena_command(snapshot,seeds,d/'results.json')
            c.atomic_json(d/'command.json',command)
            with (d/'run.log').open('w') as log:
                subprocess.run(command,check=True,timeout=1200,stdout=log,stderr=log,env=env)
            rows=c.validate_rows(json.loads((d/'results.json').read_text()),seeds)
            after=c.manifest(c.files(snapshot));assert before==after
        assert before==c.manifest(c.files(source))
        c.atomic_json(d/'files-after.json',after)
        assert all(row['status']=='completed' and row.get('error') is None for row in rows),rows
    write_markdown()

def write_markdown():
    r=report(); control=OUT/'controls';label=r['final_publication_candidate']
    if control.exists() and (control/label/'results.json').exists():
        old=json.loads((control/'baseline/results.json').read_text());new=json.loads((control/label/'results.json').read_text())
        original={p['seed']:p['delta'] for pairs in r['comparisons'][label]['paired'].values() for p in pairs}
        control_rows=[]
        by_id={row['trajectory_id']:row for row in new}
        for a in old:
            seed=a['trajectory_id'];b=by_id[seed];delta=b['progress']-a['progress']
            control_rows.append({'seed':seed,'primary_delta':original[seed],'control_baseline':a,'control_candidate':b,'control_delta':delta,'reversal':delta*original[seed]<0,'changed':delta!=original[seed]})
        r['controls']={'rows':control_rows,'game_count':len(old)+len(new),'unexpected_reversal':any(p['reversal'] for p in control_rows),'changed_deltas':any(p['changed'] for p in control_rows)}
    r['confidence'] = 'low' if r.get('controls',{}).get('unexpected_reversal') else 'limited development evidence'
    r['confidence_reason'] = 'The sole primary Public gain reversed sign in the paired diagnostic repeat; no chosen-action-change diagnostic was recorded.' if r.get('controls',{}).get('unexpected_reversal') else 'Small development sample; native validation remains necessary.'
    r['campaign_complete'] = r['complete'] and 'controls' in r and r['controls']['game_count'] == 2 * len(json.loads((control/'preselection.json').read_text())['seeds'])
    r['total_game_count'] = r['primary_game_count'] + r.get('controls',{}).get('game_count',0)
    r['technical_retry_count'] = sum(len(attempts)-1 for p in (OUT/'variants').glob('*/evaluation.json') for attempts in json.loads(p.read_text())['phases'].values())
    c.atomic_json(OUT/'report.json',r)
    lines=['# Fixed-baseline three-strategy campaign', '',f"Request: `20260927T215044431526Z-eab26a5f56264b9391f20dd5ac976a24`.", '',f"**{r['recommendation_status']}**. Recommended: `{r['recommended']}`. Final publication candidate: `{label}`. These are separate decisions; native outer scoring and fresh validation remain authoritative.",'',f"Primary games completed: **{r['primary_game_count']}**. Every listed arm has all 15 Public and 5 development games. Additional seeds are selection data, not holdout. No ordinary death was rerolled.",'','| Variant | Games | Public mean | Development mean | Pooled | Public G/T/L | Development G/T/L | Errors |','|---|---:|---:|---:|---:|---|---|---:|']
    lines[6:6] = [f"**Confidence: {r['confidence']}.** {r['confidence_reason']}", '']
    for name,comp in r['comparisons'].items():
        fmt=lambda phase:'/'.join(str(comp['outcomes'][phase][k]) for k in ['gains','ties','losses'])
        lines.append(f"| {name} | {comp['game_count']} | {comp['means']['public']:.10f} | {comp['means']['development']:.10f} | {comp['pooled_mean']:.10f} | {fmt('public')} | {fmt('development')} | {len(comp['errors'])} |")
    lines+=['',f"Eligible singles: {r['eligible_singles'] or 'none'}. Required combinations: {r['required_combinations'] or 'none'}. Missing combinations: {r['missing_combinations'] or 'none'}.",'','Selection uses strict Public improvement and nonregressing development mean, with no errors. Combinations must beat the strongest eligible single on Public and not regress its development mean. No thresholds or seed lists were tuned after results.','', '## Implementation and fixtures','','The actual incoming tree was frozen at `/tmp/campaign-incoming`, not replaced by the older research snapshot. `/tmp/campaign-baseline` is the action-equivalent flags-off baseline, with common dormant implementations and opt-in bounded diagnostics. Every singleton starts from it. `incoming-manifest.json`, `baseline-manifest.json`, `common-from-incoming.patch`, `dormant-implementation.patch` and `instrumentation-only.patch` preserve provenance. Singleton patches relative to both B0 and incoming source are retained. Variant `files.json` and `files-after.json` confirm unchanged source bytes. See `B-implementation-note.md` for the premeasurement nutrition correction.','','A changes only cumulative branch probability and sibling range bookkeeping. B purchases at most one affordable noncursed food ration, using the total edible carried nutrition estimate, short known-shop paths, threat/hunger/location rechecks, an eight-turn start bound, mandatory settlement and 100-turn failed-target suppression. C scopes observed HP loss to consecutive protected observations on the same square and level, with unchanged maximum HP and no polymorph, and only bypasses the existing LR_ELBERETH suppression. Existing action ordering and unrelated parent improvements remain intact.','','Focused tests exercise actual projection and wand ranking, wrapped food shopping, and the compiled actual LR suppression branch, plus the observation helper. Logs and the retained fixture source are under this directory. Campaign helper tests use fake rows and are separate from native games.','','## Research basis','','The frozen RESEARCH.md, research-resources.md and research-tactics.md motivate the mechanisms using the AutoAscend NetHack Challenge report (Hambro et al., 2022), NetHack is Hard to Hack (2023), and NetHack hunger, ray and Elbereth mechanics. These sources motivate the hypotheses; they do not establish a score improvement for this bot. No peer strategy code or older champion replaced the incoming parent.','','## Coverage and limitations','']
    lines += ['- '+v for v in r['instrumentation_limitations']]
    for name,activation in r['activation'].items():
        counts=activation['selected_attempt_counts']
        lines+=['',f"**{name} aggregate counters:** `{json.dumps(counts,sort_keys=True)}`."]
        if 'B' in name and not counts.get('B.started',0): lines+=['B had zero observed starts: lack of game coverage, not evidence of uselessness. Any endpoint score differences without activation cannot be attributed to this reserve mechanism.']
        if 'C' in name and not counts.get('C.exception_activated',0): lines+=['C had zero observed exception activations: lack of game coverage.']
    lines+=['','Changed wand scores alone do not demonstrate changed selected actions. In particular, absence of a chosen_action_changed counter is not positive evidence that the scoring change caused an endpoint gain.','','HP loss is evidence of damage during apparent protection, not proof of attacker identity. Death causes and endpoint differences do not establish mechanism-level causality. Samples are bounded per process and category, and are not attributed to seeds.','','## Diagnostic repeats','']
    if 'controls' in r:
        lines += [f"Control games: {r['controls']['game_count']}; excluded from every primary mean. Preselection is saved separately.",'','| Seed | Primary delta | Repeat delta | Reversal |','|---:|---:|---:|---|']
        for p in r['controls']['rows']:lines.append(f"| {p['seed']} | {p['primary_delta']:.10f} | {p['control_delta']:.10f} | {p['reversal']} |")
        lines+=['', 'Unexpected reversal lowers confidence.' if r['controls']['unexpected_reversal'] else 'No sign reversal in these preselected controls.', 'Repeat deltas changed; trajectory variability limits confidence.' if r['controls']['changed_deltas'] else 'Repeat deltas matched the primary paired deltas.']
    else: lines+=['Controls not yet complete.']
    lines+=['','## Full paired rows','', 'Each arm retains exact raw JSON and native logs in `variants/<label>/`; controls are separate. The machine-readable report includes all original row fields, errors, depths, turns and death causes.','']
    for name,comp in r['comparisons'].items():
        lines += [f'### {name}','','| Phase | Seed | B0 score | Score | Delta | Status | Depth | Turns | Death |','|---|---:|---:|---:|---:|---|---:|---:|---|']
        for phase,rows in comp['rows'].items():
            pairs={p['seed']:p for p in comp['paired'][phase]}
            for row in rows:
                p=pairs[row['trajectory_id']];death=str(row.get('cause_of_death','')).replace('|','/')
                lines.append(f"| {phase} | {row['trajectory_id']} | {p['old']:.10f} | {row['progress']:.10f} | {p['delta']:+.10f} | {row['status']} | {row.get('max_depth','')} | {row.get('turns','')} | {death} |")
        lines+=['']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:r[k] for k in ['primary_game_count','eligible_singles','required_combinations','recommended','final_publication_candidate']},indent=2))

if __name__=='__main__':
    if sys.argv[1]=='controls':controls()
    else:write_markdown()
