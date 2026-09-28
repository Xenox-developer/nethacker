import sys,json
from types import SimpleNamespace as N
from unittest.mock import patch
sys.path.insert(0,sys.argv[1])
import bot
from autoascend import dive_logic as d
hybrid=sys.argv[2]=='hybrid'
results=[]
def case(name,depth=19,medusa=False,weak=False,intact=False,blind=False,poly=False,can=True,swallow=False,pit=False,rewrite=False,near=False):
 a=N(character=N(prop=N(blind=blind,polymorph=poly)),inventory=N(engraving_below_me='Elbereth' if intact else ''),blstats=N(depth=depth,y=2,x=2,hunger_state=d.Hunger.WEAK if weak else 0,time=1),glyphs=[],can_engrave=lambda:can,current_level=lambda:N(key=lambda:(0,depth),dungeon_number=0),get_visible_monsters=lambda:[(0,2,3,N(mname='test'))] if near else [],log=lambda s:None)
 actions=[]; a.engrave=actions.append
 obj=d.DiveLogic.__new__(d.DiveLogic); obj.agent=a; obj.on_medusa_level=lambda:medusa; obj._in_own_pit=lambda:pit; obj._hurt_since=lambda t:True; obj._melee_ignores_elbereth=lambda m:False
 if rewrite: obj._elbereth_tries={((0,depth),2,2,False):1}
 with patch.object(d.utils,'any_in',return_value=swallow): value=obj._elbereth_before_digging_escape()
 assert value==bool(actions)
 results.append((name,value,len(actions)))
 return obj,actions,value
for name,kw,expected in [('depth19',{},False),('depth20',{'depth':20},hybrid),('medusa',{'medusa':True},True),('weak',{'weak':True},True),('intact',{'depth':20,'medusa':True,'intact':True},False),('poly',{'medusa':True,'poly':True},False),('cannot',{'medusa':True,'can':False},False),('swallowed',{'medusa':True,'swallow':True},False),('pit rewrite',{'pit':True,'rewrite':True},True),('near',{'near':True},True)]:
 assert case(name,**kw)[2]==expected,name
obj,actions,_=case('blind cap',blind=True,medusa=True)
for _ in range(20): obj.agent.blstats.time+=1; obj._elbereth_before_digging_escape()
assert len(actions)==d.ELBERETH_TRIES_BLIND==6
obj,actions,_=case('blind unhurt',blind=True,medusa=True); obj._hurt_since=lambda t:False
assert not obj._elbereth_before_digging_escape() and len(actions)==1
obj,actions,_=case('sighted cap',medusa=True)
for _ in range(20): obj._elbereth_before_digging_escape()
assert len(actions)==d.ELBERETH_TRIES_ESCAPE==4
obj._elbereth_before_digging_escape=lambda: 'dispatched'
assert obj._elbereth_before_digging()=='dispatched'
obj.agent.current_level=lambda:N(dungeon_number=d.GEHENNOM)
assert obj._elbereth_before_digging() is False
assert d.ELBERETH_ALWAYS is False and d.TOOL_RUN_XL is None and d.DIG_ESCAPE is True
print(json.dumps({'arm':sys.argv[2],'cases':results,'blind_cap':6,'sighted_cap':4,'blind_unhurt':True,'gehennom_no_dispatch':True,'imports':True}))
