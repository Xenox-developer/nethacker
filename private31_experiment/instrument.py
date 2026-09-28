from pathlib import Path
import difflib
R=Path(__file__).resolve().parent
for arm in ['baseline','candidate']:
 d=R/arm; diffs=[]
 changes={}
 p=d/'autoascend/agent.py'; s=p.read_text(); t='from . import engraving_diagnostics as engraving_diag\n'+s
 t=t.replace('    def engrave(self, text):','    @engraving_diag.attempt\n    def engrave(self, text):')
 what='inscription' if arm=='candidate' else 'text'
 t=t.replace("            yield from "+what+"\n            yield '\\r'", "            yield from engraving_diag.emit(self, text, "+what+" + '\\r')")
 changes[p]=(s,t)
 p=d/'autoascend/item/inventory.py'; s=p.read_text(); t='from .. import engraving_diagnostics as engraving_diag\n'+s
 line=next(l for l in s.splitlines() if 'self.engraving_below_me = ' in l and 'engraving' in l.split(' = ')[-1])
 t=t.replace(line,line+"\n                    engraving_diag.event('reading', self.agent, raw=engraving[:1024], raw_length=len(engraving), stored=self.engraving_below_me[:1024], truncated=len(engraving)>1024)")
 changes[p]=(s,t)
 p=d/'bot.py'; s=p.read_text(); t=s.replace('from arena_adapter import AutoAscendDriver  # noqa: E402','from arena_adapter import AutoAscendDriver  # noqa: E402\nfrom autoascend import engraving_diagnostics as engraving_diag')
 t=t.replace('        self._driver.reset(initial_observation)','        engraving_diag.start()\n        self._driver.reset(initial_observation)').replace('        self._driver.close()','        self._driver.close()\n        engraving_diag.end()')
 changes[p]=(s,t)
 for p,(s,t) in changes.items():
  p.write_text(t); diffs.extend(difflib.unified_diff(s.splitlines(True),t.splitlines(True),fromfile='a/'+str(p.relative_to(d)),tofile='b/'+str(p.relative_to(d))))
 diag=(R/'diagnostics.py').read_text(); (d/'autoascend/engraving_diagnostics.py').write_text(diag)
 diffs.extend(difflib.unified_diff([],diag.splitlines(True),fromfile='/dev/null',tofile='b/autoascend/engraving_diagnostics.py'))
 (R/(arm+'-diagnostic.diff')).write_text(''.join(diffs))
