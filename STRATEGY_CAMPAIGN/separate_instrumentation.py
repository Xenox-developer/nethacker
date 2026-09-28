"""Reconstruct a valid logging-free precursor and retain its instrumentation-only diff."""
import sys,ast
from pathlib import Path
sys.path.insert(0,str(next(Path('/workspace/EXPERIMENT_ASSETS').glob('*/campaign.py')).parent))
import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN');current=campaign.files('/tmp/campaign-baseline');plain=dict(current)
for name,data in current.items():
 if not name.endswith('.py') or name=='campaign_events.py':continue
 source=data.decode();tree=ast.parse(source);lines=source.splitlines(keepends=True);remove=set();replacements={}
 for node in ast.walk(tree):
  if isinstance(node,ast.Import) and any(a.name=='campaign_events' for a in node.names):
   remove.update(range(node.lineno-1,node.end_lineno))
  elif isinstance(node,ast.If) and 'ce.enabled()' in ast.unparse(node.test) and name!='autoascend/item/inventory.py':
   remove.update(range(node.lineno-1,node.end_lineno))
  elif isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and isinstance(node.value.func.value,ast.Name) and node.value.func.value.id=='ce':
   remove.update(range(node.lineno-1,node.end_lineno));replacements[node.lineno-1]=' '*node.col_offset+'pass  # optional diagnostic hook\n'
 # Do not retain replacements contained inside removed diagnostic-only If blocks.
 for node in ast.walk(tree):
  if isinstance(node,ast.If) and 'ce.enabled()' in ast.unparse(node.test) and name!='autoascend/item/inventory.py':
   for i in range(node.lineno-1,node.end_lineno):replacements.pop(i,None)
 text=''.join(replacements.get(i,line if i not in remove else '') for i,line in enumerate(lines))
 text=text.replace('(jf_config.TOOL_SHOP_RESERVE or ce.enabled())','jf_config.TOOL_SHOP_RESERVE').replace('            self._campaign_wand_scores = {}\n','')
 ast.parse(text)
 plain[name]=text.encode()
plain.pop('campaign_events.py')
(out/'instrumentation-only.patch').write_text(campaign.patch(plain,current))
(out/'implementation-common.patch').write_text(campaign.patch(campaign.files('/tmp/campaign-incoming'),plain))
campaign.atomic_json(out/'implementation-without-diagnostics-manifest.json',campaign.manifest(plain))
print('Logging-free precursor parses; patches reconstruct the frozen common baseline.')
