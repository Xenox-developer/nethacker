import sys, json, random, os
from pathlib import Path
from types import SimpleNamespace as N
import numpy as np
sys.path.insert(0,sys.argv[1])
from autoascend import dive_logic as d
from autoascend import deep_protection_diagnostics as diag
from autoascend.glyph import Hunger,G
hybrid=sys.argv[2]=='hybrid'
checks=[]
def fixture(depth=19,blind=False,polymorph=False,engraving='',can=True,pit=False,medusa=False,hunger=0,monsters=(),tries=0,last=None,hurt=True,swallow=False,dungeon=0):
 level=N(key=lambda:(dungeon,depth),dungeon_number=dungeon)
 actions=[]
 agent=N(blstats=N(depth=depth,time=100,y=2,x=2,hunger_state=hunger),character=N(prop=N(blind=blind,polymorph=polymorph)), inventory=N(engraving_below_me=engraving),can_engrave=lambda:can,glyphs=np.array([[next(iter(G.SWALLOW)) if swallow else 0]]), current_level=lambda:level,get_visible_monsters=lambda:list(monsters),engrave=lambda text:actions.append(text),log=lambda x:None)
 obj=d.DiveLogic.__new__(d.DiveLogic);obj.agent=agent;obj.medusa_level=level.key() if medusa else None;obj._pit_at=(level.key(),(2,2)) if pit else None;obj._hurt_on_elbereth=-100;obj._hurt_since=lambda t:hurt
 spot=(level.key(),2,2,pit);obj._elbereth_tries={spot:tries};obj._engrave_turn={} if last is None else {spot:last}
 return obj,actions,spot

def check(name,expect,**kw):
 obj,actions,spot=fixture(**kw)
 before=random.getstate(); npbefore=np.random.get_state()
 result=obj._elbereth_before_digging_escape()
 assert result==expect and len(actions)==int(expect),(name,result,actions)
 assert random.getstate()==before
 assert all(np.array_equal(a,b) for a,b in zip(npbefore,np.random.get_state()))
 checks.append(name)
check('depth19',False)
check('depth20',hybrid,depth=20)
check('medusa19',True,medusa=True)
check('weak19',True,hunger=Hunger.WEAK)
obj,actions,spot=fixture(pit=True);obj._elbereth_tries[spot[:3]+(False,)]=1
assert obj._elbereth_before_digging_escape() and actions==['Elbereth'];checks.append('pit rewrite19')
for depth in (19,20):
 for name,kw in [('intact',dict(engraving='ElBeReTh')),('polymorph',dict(polymorph=True)),('cannot',dict(can=False)),('swallow',dict(swallow=True)),('sighted cap4',dict(tries=4)),('blind cap6',dict(blind=True,tries=6)),('blind unhurt',dict(blind=True,last=99,hurt=False))]:
  check(name+str(depth),False,depth=depth,medusa=True,**kw)
check('sighted3',True,medusa=True,tries=3)
check('blind5 hurt',True,medusa=True,blind=True,tries=5,last=99)
check('blind intact unreadable',True,medusa=True,blind=True,engraving='Elbereth')
immune=(0,2,3,N(mname='minotaur',mlet='H'))
susceptible=(0,2,3,N(mname='newt',mlet=':'))
check('immune19',False,monsters=[immune]);check('immune20',hybrid,depth=20,monsters=[immune])
check('susceptible19',True,monsters=[susceptible]);check('far19',False,monsters=[(0,99,99,susceptible[3])])
for depth in (19,20):
 obj,actions,_=fixture(depth=depth,dungeon=d.GEHENNOM,medusa=True)
 assert obj._elbereth_before_digging() is False and actions==[]
 checks.append('Gehennom dispatch'+str(depth))
 obj,actions,_=fixture(depth=depth)
 assert obj._elbereth_before_digging()==(hybrid and depth==20)
 checks.append('normal dispatch'+str(depth))
assert d.TOOL_RUN_XL is None and not d.ELBERETH_ALWAYS and not d.DROWN_GUARD
assert d.ELBERETH_TRIES_ESCAPE==4 and d.ELBERETH_TRIES_BLIND==6
# Enabled and disabled observations leave identical helper state and actions.
for enabled in (False,True):
 diag._ENABLED=enabled
 check('logging toggle '+str(enabled),True,depth=20,medusa=True)
# Failed logging must not affect the action.
diag._ENABLED=True;diag._path=Path('/dev/null/not-a-directory')
check('logging failure',True,medusa=True)
print(json.dumps({'arm':sys.argv[2],'passed':len(checks),'checks':checks}))
