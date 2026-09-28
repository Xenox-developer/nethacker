"""Freeze common baseline and independent flags; no evaluation or selection tuning."""
import sys, shutil, ast
from pathlib import Path
sys.path.insert(0,str(next(Path('/workspace/EXPERIMENT_ASSETS').glob('*/campaign.py')).parent))
import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN')
current=campaign.files('/workspace')
incoming=campaign.files('/tmp/campaign-incoming')
# Separate logging-only additions from the implementation by deleting only diagnostic AST nodes.
plain=dict(current)
for name,data in current.items():
 if not name.endswith('.py') or name=='campaign_events.py':continue
 text=data.decode();tree=ast.parse(text);lines=text.splitlines(keepends=True);remove=set()
 for node in ast.walk(tree):
  diagnostic=(isinstance(node,ast.Import) and any(a.name=='campaign_events' for a in node.names))
  diagnostic |= isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and isinstance(node.value.func.value,ast.Name) and node.value.func.value.id=='ce'
  diagnostic |= isinstance(node,ast.If) and 'ce.enabled()' in ast.unparse(node.test) and name != 'autoascend/item/inventory.py'
  if diagnostic:remove.update(range(node.lineno-1,node.end_lineno))
 # Leave pass statements for now-empty diagnostic branches, without formatting unrelated code.
 for node in ast.walk(tree):
  if isinstance(node,ast.If) and node.lineno-1 not in remove and node.body and all(n.lineno-1 in remove for n in node.body):
   first=node.body[0];lines[first.lineno-1]=' ' * first.col_offset+'pass\n';remove.discard(first.lineno-1)
 text=''.join(line for i,line in enumerate(lines) if i not in remove)
 text=text.replace('(jf_config.TOOL_SHOP_RESERVE or ce.enabled())','jf_config.TOOL_SHOP_RESERVE')
 # Shadow bookkeeping has no gameplay use.
 text=text.replace('            self._campaign_wand_scores = {}\n','')
 plain[name]=text.encode()
plain.pop('campaign_events.py')
(out/'instrumentation-only.patch').write_text(campaign.patch(plain,current))
(out/'implementation-common.patch').write_text(campaign.patch(incoming,plain))
(out/'incoming-to-baseline.patch').write_text(campaign.patch(incoming,current))
for label,members in [('baseline',[]),('A',['A']),('B',['B']),('C',['C'])]:
 dest=Path('/tmp/campaign-'+label);dest.mkdir(exist_ok=False)
 for name,data in current.items():
  if name=='autoascend/jf_config.py':
   for m,flag in [('A','CAMPAIGN_WAND'),('B','TOOL_SHOP_RESERVE'),('C','PROTECTION_FAILURE')]:
    if m in members:data=data.replace((flag+' = False').encode(),(flag+' = True').encode())
  target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 campaign.atomic_json(out/(label+'-before.json'),campaign.manifest(campaign.files(dest)))
