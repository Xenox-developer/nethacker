"""Preserve the full action-neutral diagnostic diff separately from mechanisms."""
import ast,sys
from pathlib import Path
assets=next(Path('/workspace/EXPERIMENT_ASSETS').glob('20260927T215044*'))
sys.path.insert(0,str(assets));import campaign
base=campaign.files('/tmp/campaign-baseline');plain=dict(base);plain.pop('campaign_events.py')
def ce_call(node):
    return isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and isinstance(node.value.func.value,ast.Name) and node.value.func.value.id=='ce'
for name in ['autoascend/agent.py','autoascend/dive_logic.py','autoascend/combat/fight_heur.py','autoascend/item/inventory.py']:
    text=base[name].decode();tree=ast.parse(text);lines=text.splitlines(True);remove=[]; placeholders={}
    for node in ast.walk(tree):
        if isinstance(node,ast.Import) and any(a.name=='campaign_events' for a in node.names):remove.append((node.lineno,node.end_lineno))
        elif ce_call(node):
            remove.append((node.lineno,node.end_lineno))
            placeholders[node.lineno] = " " * node.col_offset + "pass  # diagnostic removed\n"
        elif isinstance(node,ast.If):
            condition=ast.get_source_segment(text,node.test)
            if condition=='ce.enabled()' or (node.body and all(ce_call(n) for n in node.body) and not node.orelse):
                remove.append((node.lineno,node.end_lineno))
        elif isinstance(node,ast.FunctionDef) and node.name in ['campaign_action_key','campaign_alternate_choice']:
            remove.append((node.lineno,node.end_lineno))
    removed={n for start,end in remove for n in range(start,end+1)}
    # Retain legal suites for mixed diagnostic-only branches without touching mechanisms.
    whole = [(a,b) for a,b in remove if a not in placeholders]
    result=''.join(placeholders[i] if i in placeholders and not any(a<=i<=b for a,b in whole) else (line if i not in removed else '') for i,line in enumerate(lines,1))
    result=result.replace(' or ce.enabled()','').replace('trace = [False] if ce.enabled() else None','trace = None')
    # Ray trace and shadow lists do not influence gameplay. They are harmless in this reference;
    # remove their conditional-only empty blocks if diagnostics were their sole body.
    result=result.replace('    if len(states) > 1:\n        if trace is not None:\n            trace[0] = True\n','')
    ast.parse(result)
    plain[name]=result.encode()
out=Path('/workspace/STRATEGY_CAMPAIGN')
(out/'instrumentation-initial.patch').write_bytes((out/'instrumentation-only.patch').read_bytes())
(out/'instrumentation-only.patch').write_text(campaign.patch(plain,base))
campaign.atomic_json(out/'instrumentation-reference-manifest.json',campaign.manifest(plain))
print('Preserved full diagnostic-only diff against the same dormant mechanisms without event hooks.')
