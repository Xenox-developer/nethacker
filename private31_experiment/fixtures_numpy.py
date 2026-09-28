import sys,os,json,contextlib
import numpy as np
from pathlib import Path
from types import SimpleNamespace as NS
arm,mode=sys.argv[1:]; root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/arm))
from autoascend.agent import Agent,A
from autoascend.item.inventory import Inventory
from autoascend import engraving_diagnostics as diag
if mode=='on':
 out=root/'numpy-fixture-traces'; out.mkdir(exist_ok=True); os.environ['PRIVATE31_TRACE_DIR']=str(out)
elif mode=='unwritable': os.environ['PRIVATE31_TRACE_DIR']='/proc/no-such-directory'
else: os.environ.pop('PRIVATE31_TRACE_DIR',None)
diag.start(); records=[]
class Fake:
 def __init__(self,blind,append=False,denial=0,interrupt=False):
  self.character=NS(prop=NS(blind=blind,polymorph=False)); self.blstats=NS(time=10,y=3,x=4)
  self._observation={'misc':[0,0,0]}; self.single_message=''; self.message=''; self.popup=[]
  self._forbidden_engrave_position=(-1,-1); self.actions=[]; self.append=append; self.denial=denial; self.interrupt=interrupt
  self.inventory=NS(get_items_below_me=lambda:None)
  self.stats_logger=NS(log_event=lambda *a:None)
 def atom_operation(self): return contextlib.nullcontext()
 def panic_if_position_changes(self): return contextlib.nullcontext()
 def current_level(self): return NS(key=lambda:(np.int64(0),np.int64(1)))
 def hands_welded(self): return False
 def step(self,command,gen=None):
  self.actions.append(int(command))
  if gen is None: return
  self.single_message='denied' if self.denial==1 else 'What do you want to write with?'
  for c in gen:
   self.actions.append(c if isinstance(c,str) else int(c))
   if c=='-': self.single_message='Do you want to add to the current engraving?' if self.append else ('denied' if self.denial==2 else 'What do you want to write in the dust here?')
   if c=='n': self.single_message='What do you want to write in the dust here?'
   if c=='\r': self.blstats.time+=3
   if self.interrupt and c=='l':
    gen.close(); raise RuntimeError('fixture interruption')
for text,blind,append,denial in [('Elbereth',True,False,0),('eLbErEtH',True,False,0),('Elbereth',False,False,0),('other',True,False,0),('Elbereth',True,True,0),('Elbereth',True,False,1),('Elbereth',True,False,2)]:
 a=Fake(blind,append,denial); result=Agent.engrave(a,text)
 expected='Elbereth Elbereth' if arm=='candidate' and blind and text.lower()=='elbereth' else text
 assert result==(not denial)
 assert a.actions[1:]==([int(A.Command.ESC)] if denial==1 else ['-',int(A.Command.ESC)] if denial==2 else ['-']+(['n'] if append else [])+list(expected+'\r')),a.actions
 records.append(dict(kind='write',text=text,blind=blind,append=append,denial=denial,actions=a.actions,result=result))
a=Fake(True,interrupt=True)
try: Agent.engrave(a,'Elbereth')
except RuntimeError: pass
else: assert False
records.append(dict(kind='interruption',actions=a.actions))
for raw in ['Elbereth','eLbErEtH','Elbereth Elbereth','El?ere?h Elbereth','El?ere?h','hello',None]:
 a=Fake(False); a.message='You see no objects here.' if raw is None else 'Something is written here. You read: "'+raw+'"'
 inv=Inventory.__new__(Inventory); inv.agent=a
 inv.get_items_below_me(assume_appropriate_message=True)
 expected='' if raw is None else 'Elbereth' if arm=='candidate' and 'elbereth' in raw.lower() else raw
 assert inv.engraving_below_me==expected
 records.append(dict(kind='parse',raw=raw,stored=inv.engraving_below_me,actions=a.actions))
a=Fake(False); assert Agent.can_engrave(a)
a.character.prop.polymorph=True; assert not Agent.can_engrave(a)
a.character.prop.polymorph=False; a._forbidden_engrave_position=(3,4); assert not Agent.can_engrave(a)
a._forbidden_engrave_position=(-1,-1); a.hands_welded=lambda:True; assert not Agent.can_engrave(a)
diag.end()
print(json.dumps(records,indent=2))
