from pathlib import Path
import shutil,difflib
E=Path(__file__).resolve().parent
for arm in ['baseline','candidate']:
 p=E/arm/'autoascend/item/inventory.py';s=p.read_text();old=s
 s='from ..trap_diagnostics import operation, slot_check\n'+s
 for name in ['wear','takeoff']: s=s.replace('    def '+name+'(', '    @operation\n    def '+name+'(',1)
 s=s.replace('    def _trap_slot_blocked(', '    @slot_check\n    def _trap_slot_blocked(',1)
 p.write_text(s)
 shutil.copyfile(E/'trap_diagnostics.py',E/arm/'autoascend/trap_diagnostics.py')
 (E/(arm+'-diagnostic.diff')).write_text(''.join(difflib.unified_diff(old.splitlines(True),s.splitlines(True),fromfile=arm+'/policy',tofile=arm+'/instrumented')))
