import json
from pathlib import Path
out=Path('/workspace/STRATEGY_CAMPAIGN');r=json.loads((out/'report.json').read_text())
lines=['# Three-strategy campaign — N=20', '',
'Request `20260927T215044431526Z-eab26a5f56264b9391f20dd5ac976a24`.', '',
'## Selection', '',
f"Recommended: **{r['recommended']}**. Final publication candidate: **{r['final_publication_candidate']}**.",
('NO recommended improvement. The publication candidate is the best fully tested error-free singleton, a negative/mixed experiment, not a demonstrated improvement.' if r['recommended']=='baseline' else 'This is a development selection, not promotion. Native outer Public scoring and fresh local validation remain authoritative.'), '',
f"Primary games: **{r['primary_game_count']}**. Eligible singles: {r['eligible_singles']}. Required combinations: {r['required_combinations']}. Missing combinations: {r['missing_combinations']}.", '',
'| Variant | Games | Public mean | Development mean | Public gains/ties/losses | Development gains/ties/losses | Errors |',
'|---|---:|---:|---:|---|---|---:|']
for label,c in r['comparisons'].items():
 def gtl(phase):
  d=c[phase+'_gains_ties_losses'];return '/'.join(str(d[k]) for k in ('gains','ties','losses'))
 errors=sum(x.get('status')!='completed' or x.get('error') is not None for rows in c['rows'].values() for x in rows)
 lines.append(f"| {label} | {c['game_count']} | {c['means']['public']:.12f} | {c['means']['development']:.12f} | {gtl('public')} | {gtl('development')} | {errors} |")
lines+=['', '## Protocol and provenance', '',
'The actual incoming tree was frozen at `/tmp/campaign-incoming`; no champion20 replacement was used. `incoming-manifest.json` records sanitized source hashes and `incoming-full-file-hashes.json` also includes supplied assets. The common all-flags-off baseline and every independent singleton live outside the published tree in `/tmp/campaign-*`. All unrelated parent code, adapter, entrypoint, and license were retained.', '',
'Every primary variant received Public 0–14 and development 2000–2004 with secret `public`, namespace `local`, 1,000,000 steps, 10,000 no-progress limit, 120-second action timeout, and at most four concurrent episodes. Variant batches ran sequentially through the supplied `campaign.py`; both phases must finish before a variant counts. Development is selection data, not holdout.', '',
'Complete raw JSON, logs, diagnostics, per-file hashes, canonical membership, and baseline-relative patches are under `variants/<label>/`. The helper verifies the sanitized runtime snapshot after evaluation; separate before/after manifests also verify the frozen source trees. `incoming-to-baseline.patch`, `implementation-common.patch`, and `instrumentation-only.patch` preserve the common scaffold and separate action-neutral logging. Singletons enable only their named flag. Hypotheses, thresholds, and seed lists were fixed. Two contract-boundary corrections were made to unevaluated B/C while A ran; see `pre-evaluation-corrections.md` and retained initial/corrected manifests. No completed or running variant was changed or replaced.', '',
'## Mechanisms and focused validation', '',
'- **A:** cumulative branch probability and sibling-local remaining range in the existing range-13 wand simulation. Geometry, encounter costs, friendly/self penalties, and action priorities are unchanged.',
'- **B:** one affordable known-price food ration, unknown beatitude permitted and known cursed excluded, for a hungry/weak tool carrier with estimated nutrition below 400. Only known same-shop floor paths of at most two moves are considered; prerequisites are rechecked before each move and pickup. At elapsed eight turns no new move/pickup begins. Existing payment-or-drop cleanup always follows pickup, with overrun logging and a 100-turn failed-location cooldown.',
'- **C:** a separately scoped consecutive-turn same-level/tile intact-Elbereth HP-loss marker, excluding maximum-HP changes and polymorph, expires after three elapsed turns. Its flag only bypasses the existing LR_ELBERETH suppression. All outer emergency gates and action ordering remain unchanged; existing damage/rest/dig policies are retained.', '',
'`test_strategies.py` has 22 focused tests, including straight and deterministic rays, weighted descendants, branch order/mirror symmetry, self/friendly penalties, actual score-driven action ranking, tool/no-tool shopping, price/BUC/path/threat gates, timeout and debt cleanup, scoped HP evidence, and the actual source LR branch with its ordinary gates. Initial fixture setup errors (monster glyph zero used as empty floor and an unhashable fake monster) were corrected before any games; production strategy was not changed by those fixture fixes. `fixtures.log`, `fixtures-expanded.log`, and per-variant fixture logs retain outcomes. Additional pre-evaluation boundary suites passed for B (11 tests, including full cooldown from failure exit) and C (5 tests, including no deferred same-turn loss). All 23 supplied campaign-helper tests passed.', '',
'## Diagnostics and limits', '',
'All diagnostics are disabled unless the campaign output environment variable is set. They read in-game state only and never seed, score, or evaluator internals. Counters are aggregate process lower bounds, not exact totals or per-seed counts. Branching counts include recursive calls in both actual and counterfactual projections, not distinct decisions. `A.considered` counts direction evaluations, including those with no usable wand. Score and root-action changes are recorded separately. Root comparisons rescore the existing filtered candidate list; they do not reconstruct a counterfactual combat policy with a different candidate set, and paired wand score comparisons use the existing enumeration. Thus they are diagnostic coverage, not a complete causal attribution of endpoint differences.', '',
'`B.eligible` is preliminary hunger/stock/location/status eligibility, before finding qualifying stock. No purchase activation means lack of coverage, not evidence that buying is useless. B bail categories and bounded transaction samples give stock before/after and elapsed turns. `C.qualified_loss` records observed HP loss, not an identified attacker. The dormant baseline/A/B observer predates the same-turn boundary correction in C; its qualified-loss count is not an equivalent control for C activation. Emergency class counters include all last-resort actions; bounded `emergency_action` samples separately mark whether the suppression exception was active. Samples are capped by kind, so their absence is not proof an event never happened.', '']
lines += ['### Coverage findings', '']
for label,key in [('A','A.applied'),('B','B.purchased'),('C','C.applied')]:
 counts=r['activation'][label]['selected_attempt_counts']
 lines.append(f"- {label}: `{key}` has {counts.get(key,0)} recorded events as an aggregate lower bound." + (' No behavioral activation was recorded; these games do not establish the mechanism’s benefit.' if not counts.get(key) else ' This establishes some recorded activation, not causal attribution of the final scores.'))
lines += ['']
for label,activation in r['activation'].items():
 lines += [f'### {label} aggregate lower-bound counters','', '```json',json.dumps(activation['selected_attempt_counts'],sort_keys=True,indent=2),'```','']
lines += ['## Paired primary results','']
for label,c in r['comparisons'].items():
 lines += [f'### {label}', '', '| Group | Seed | B0 score | Score | Delta | Status | Turns | Depth | Death / ending |', '|---|---:|---:|---:|---:|---|---:|---:|---|']
 for phase,rows in c['rows'].items():
  pairs={p['seed']:p for p in c['paired'][phase]}
  for row in rows:
   p=pairs[row['trajectory_id']];death=str(row.get('cause_of_death') or row.get('end_status','')).replace('|','/')
   lines.append(f"| {phase} | {row['trajectory_id']} | {p['old']:.12f} | {p['new']:.12f} | {p['delta']:+.12f} | {row['status']} | {row.get('turns')} | {row.get('max_depth')} | {death} |")
 lines+=['']
lines+=['## Separate diagnostic repeats','',
'The repeat seeds were selected before repeating: largest Public gain, largest Public loss, and largest absolute development difference, with lower seed ID breaking ties and duplicates removed. They are controls only and never replace primary outcomes.', '',
f"Preselected seeds: {r.get('diagnostic_seeds')}. See `controls/` for full original results, logs, configuration, and before/after hashes.", '']
controls={}
for path in (out/'controls').glob('*/control.json'):
 data=json.loads(path.read_text());assert data['complete'];controls[data['label']]=data
if len(controls)==2:
 label=r['final_publication_candidate'];base={x['trajectory_id']:x for x in controls['baseline']['attempts'][-1]['results']};cand={x['trajectory_id']:x for x in controls[label]['attempts'][-1]['results']}
 pairs={p['seed']:p for rows in r['comparisons'][label]['paired'].values() for p in rows}
 lines+=['| Seed | Primary delta | Repeat B0 | Repeat candidate | Repeat delta |','|---|---:|---:|---:|---:|']
 repeat=[]
 for seed in r['diagnostic_seeds']:
  delta=cand[seed]['progress']-base[seed]['progress'];original=pairs[seed]['delta']
  repeat.append({'seed':seed,'primary_delta':original,'repeat_delta':delta,'baseline':base[seed],'candidate':cand[seed],'sign_reversal':original*delta<0})
  lines.append(f"| {seed} | {original:+.12f} | {base[seed]['progress']:.12f} | {cand[seed]['progress']:.12f} | {delta:+.12f} |")
 changed=any(x['repeat_delta']!=x['primary_delta'] for x in repeat);reversed_=any(x['sign_reversal'] for x in repeat)
 lines += ['', ('**A sign reversal occurred in the controls; confidence is lower.**' if reversed_ else 'No strict sign reversal occurred in the controls.'), ('Some paired deltas changed on repetition. Endpoint gains are therefore not fully reproducible and should not be treated as established causal improvements.' if changed else 'The selected paired score deltas reproduced.'),'']
 r['diagnostic_controls']={'game_count':2*len(base),'paired':repeat,'sign_reversal':reversed_,'paired_deltas_changed':changed};r['total_game_count']=r['primary_game_count']+2*len(base)
 activation_key={'A':'A.applied','B':'B.purchased','C':'C.applied'}
 recorded=any(r['activation'][label]['selected_attempt_counts'].get(activation_key[m],0) for m in label.split('+'))
 reasons=[]
 if not recorded:reasons.append('No selected-mechanism behavioral activation was recorded.')
 if changed:reasons.append('The paired primary score differences did not fully reproduce in controls.')
 if reversed_:reasons.append('A control reversed the sign of a primary paired difference.')
 r['confidence']={'assessment':'low' if reasons else 'screening evidence only','reasons':reasons}
 if reasons:lines[8:8]=['', '**Confidence is low.** '+' '.join(reasons)+' The numerical selection rule still selects the tested candidate; this is not proof of a causal improvement.']

 lines += [f"Completed primary plus control games: **{r['total_game_count']}**. Technical retries, if any, remain separately preserved in each evaluation record.",'']
else:raise RuntimeError('Required controls missing')
r['recommended_improvement'] = None if r['recommended']=='baseline' else r['recommended']
(out/'REPORT.md').write_text('\n'.join(lines)+'\n');(out/'report.json').write_text(json.dumps(r,indent=2,sort_keys=True))
