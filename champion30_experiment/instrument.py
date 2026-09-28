from pathlib import Path
import shutil,difflib
E=Path('/workspace/champion30_experiment')
for arm in ('baseline','hybrid'):
 root=E/arm; p=root/'autoascend/dive_logic.py'; old=p.read_text()
 s=old.replace('from . import objects as O','from . import objects as O\nfrom .deep_protection_diagnostics import observe as _deep_observe')
 start=s.index('    def _elbereth_before_digging_escape(self):');end=s.index('    def dig_with_tool',start)
 h=s[start:end]
 h=h.replace('        agent = self.agent\n','        _deep_observe("visit", locals())\n        agent = self.agent\n',1)
 h=h.replace('            return False', '            _deep_observe("safety_reject", locals())\n            return False',1)
 needle="        if not blind and (agent.inventory.engraving_below_me or '').lower() == 'elbereth':\n            return False"
 h=h.replace(needle,needle.replace('            return False','            _deep_observe("intact_reject", locals())\n            return False'))
 h=h.replace('        if not near and not (','        _deep_observe("eligibility", locals())\n        if not near and not (')
 h=h.replace('            return False\n        if blind:', '            _deep_observe("eligibility_reject", locals())\n            return False\n        if blind:')
 h=h.replace('                return False\n        elif', '                _deep_observe("blind_guard_reject", locals())\n                return False\n        elif')
 h=h.replace('        elif tries.get(spot, 0) >= ELBERETH_TRIES_ESCAPE:\n            return False','        elif tries.get(spot, 0) >= ELBERETH_TRIES_ESCAPE:\n            _deep_observe("sighted_cap_reject", locals())\n            return False')
 h=h.replace("        agent.engrave('Elbereth')", "        _deep_observe(\"engraving_call\", locals())\n        agent.engrave('Elbereth')")
 s=s[:start]+h+s[end:];p.write_text(s)
 shutil.copy2(E/'deep_protection_diagnostics.py',root/'autoascend/deep_protection_diagnostics.py')
 (E/(arm+'-instrumentation.diff')).write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile='before',tofile='after')))
