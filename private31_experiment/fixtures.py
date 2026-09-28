import sys,contextlib,json
from pathlib import Path
from types import SimpleNamespace as NS
sys.path.insert(0,str(Path(__file__).resolve().parent/sys.argv[1]))
from autoascend.item.inventory import Inventory
from autoascend.item import Item
from autoascend import objects as O
from nle.nethack import actions as A
from autoascend.strategy import Strategy
C=sys.argv[1]=='candidate'
slots=[(O.ARM_SHIELD,'off_hand'),(O.ARM_HELM,'helm'),(O.ARM_GLOVES,'gloves'),(O.ARM_BOOTS,'boots'),(O.ARM_SHIRT,'shirt'),(O.ARM_SUIT,'suit'),(O.ARM_CLOAK,'cloak')]
class Armor:
 def __init__(self,slot,equipped=False):
  self.object=NS(sub=slot);self.objs=[NS(bi=False)];self.equipped=equipped;self.status=Item.UNCURSED;self.text=str(slot);self.count=1;self.shop_status=Item.NOT_SHOP;self.content=None
 def is_armor(self):return True
 def is_container(self):return False
 def can_be_dropped_from_inventory(self):return not self.equipped
class Items(list):
 main_hand=None
 @property
 def all_items(self):return self
 @property
 def all_letters(self):return [chr(97+i) for i in range(len(self))]
 def get_letter(self,item):return chr(97+self.index(item))
 def __getattr__(self,name):
  for slot,n in slots:
   if n==name:return next((i for i in self if i.equipped and i.object.sub==slot),None)
  raise AttributeError(name)
class Agent:
 def __init__(self,items):
  self.message='';self.blstats=NS(time=100);self.items=items;self.calls=[];self.responses={};self.welded=False
  self.env=NS(debug_log=lambda **kw:contextlib.nullcontext())
  self.character=NS(prop=NS(polymorph=False),carrying_capacity=100)
  self.global_logic=NS(item_priority=NS(split=self.split))
 def split(self,free,forced,capacity):
  self.forced=forced;return {None:[0]*len(free)}
 def hands_welded(self):return self.welded
 def atom_operation(self):return contextlib.nullcontext()
 def step(self,cmd):
  self.calls.append(cmd);assert len(self.calls)<30,'zero-turn loop'
  self.cmd=cmd
  if cmd==A.Command.WEAR:self.message='What do you want to wear?'
  else:
   equipped=[i for i in self.items if i.equipped]
   if len(equipped)>1:self.message='What do you want to take off?'
   else:self.respond(equipped[0])
 def type_text(self,letter):self.respond(self.items[ord(letter)-97])
 def respond(self,item):
  self.message=self.responses.get(item.object.sub,'You are now wearing armor.' if self.cmd==A.Command.WEAR else 'You were wearing armor.')
  if self.message.startswith(('You are now wearing','You were wearing')):item.equipped=self.cmd==A.Command.WEAR

def setup(*items):
 inv=Inventory.__new__(Inventory);inv.items=Items(items);inv.agent=Agent(inv.items);inv.items_below_me=[];inv.multi_container_squares=set();inv._here=lambda:(0,0,0,0);inv.move_to_inventory=lambda i:i
 inv.get_best_armorset=lambda:{slot:next((i for i in inv.items if i.object.sub==slot),None) for slot,name in slots}
 return inv
rows=[]
def check(name,fn):
 fn();rows.append({'fixture':name,'passed':True});print(json.dumps(rows[-1]),flush=True)
messages=['Your foot is trapped!','Your feet are stuck in the floor!','Your foot is attached to the buried ball!','The bear trap prevents you from pulling your foot out.','You are stuck and cannot pull your feet free.']
for message in messages:
 for op in ['wear','takeoff']:
  def test(message=message,op=op):
   item=Armor(O.ARM_BOOTS,op=='takeoff');inv=setup(item);inv.agent.responses[O.ARM_BOOTS]=message
   if C:
    assert getattr(inv,op)(item) is False
    assert inv._trap_armor_until[O.ARM_BOOTS]==120
    calls=len(inv.agent.calls)
    assert getattr(inv,op)(item) is False and len(inv.agent.calls)==calls
    inv.agent.blstats.time=119;assert getattr(inv,op)(item) is False
    assert inv._trap_armor_until[O.ARM_BOOTS]==120
    inv.agent.blstats.time=120;inv.agent.responses.clear();assert getattr(inv,op)(item) is True
    assert len(inv.agent.calls)==calls+1
   else:
    if op=='wear' and message==messages[0]:assert inv.wear(item) is True
    else:
     try:getattr(inv,op)(item)
     except AssertionError:pass
     else:raise AssertionError('baseline must retain assertion')
    assert not hasattr(inv,'_trap_armor_until')
  check(op+': '+message,test)

def ordinary():
 i=Armor(O.ARM_BOOTS);inv=setup(i);assert inv.wear(i);assert i.equipped;assert inv.takeoff(i);assert not i.equipped
 inv.agent.responses[O.ARM_BOOTS]='Unexpected unrelated response'
 try:inv.wear(i)
 except AssertionError:pass
 else:raise AssertionError('unrelated message accepted')
 assert not getattr(inv,'_trap_armor_until',{})
check('ordinary success and unrelated assertions',ordinary)
def cursed():
 i=Armor(O.ARM_BOOTS,True);inv=setup(i);i.status=Item.CURSED
 try:inv.takeoff(i)
 except AssertionError:pass
 else:raise AssertionError('known curse accepted')
 assert not inv.agent.calls
 i.status=Item.UNCURSED
 for msg in ['It is cursed.','They are cursed.']:
  inv.agent.responses[O.ARM_BOOTS]=msg;assert inv.takeoff(i) is False
 assert not getattr(inv,'_trap_armor_until',{})
check('cursed guards',cursed)
def welded():
 i=Armor(O.ARM_BOOTS);inv=setup(i);inv.agent.welded=True
 assert inv.wear_best_stuff().run(return_condition=True) is False;assert not inv.agent.calls
 inv.agent.welded=False;inv.agent.responses[O.ARM_BOOTS]='You cannot do that while holding your weapon.'
 try:inv.wear(i)
 except AssertionError:pass
 else:raise AssertionError('original assertion changed')
 assert not getattr(inv,'_trap_armor_until',{})
check('welded guard and original refusal behavior',welded)
if C:
 def strategy():
  boots=Armor(O.ARM_BOOTS);shirt=Armor(O.ARM_SHIRT);inv=setup(boots,shirt)
  inv.agent.responses[O.ARM_BOOTS]=messages[0]
  assert inv.wear_best_stuff().run(return_condition=True)
  assert shirt.equipped and not boots.equipped and len(inv.agent.calls)==2
  assert inv.wear_best_stuff().run(return_condition=True) is False
  inv.agent.blstats.time=119;assert not inv.wear_best_stuff().run(return_condition=True)
  inv.agent.blstats.time=120;inv.agent.responses.clear();assert inv.wear_best_stuff().run(return_condition=True);assert boots.equipped
 check('wear strategy exits; other slots proceed; expiry',strategy)
 def retention():
  old=Armor(O.ARM_BOOTS,True);new=Armor(O.ARM_BOOTS);inv=setup(new,old)
  inv.agent.responses[O.ARM_BOOTS]=messages[0]
  assert inv.wear_best_stuff().run(return_condition=True);assert len(inv.agent.calls)==1
  # Remove spare from this fixture so arrange has only the retained equipped item.
  inv.items.remove(new)
  assert not inv.arrange_items().run(return_condition=True)
  assert old in inv.agent.forced and old.equipped and len(inv.agent.calls)==1
  assert inv.drop([old],smart=False) is False
  assert len(inv.agent.calls)==1
  inv.agent.blstats.time=120;inv.agent.responses.clear();assert inv.takeoff(old)
 check('takeoff strategy exits and arrange retains blocked equipment',retention)
 def layers():
  cloak=Armor(O.ARM_CLOAK,True);shirt=Armor(O.ARM_SHIRT);inv=setup(cloak,shirt)
  inv.agent.responses[O.ARM_CLOAK]=messages[0]
  assert inv.wear_best_stuff().run(return_condition=True);assert len(inv.agent.calls)==1
  assert not inv.wear_best_stuff().run(return_condition=True)
 check('blocked outer layer does not create zero-turn loop',layers)
 def progression():
  inv=setup(Armor(O.ARM_BOOTS));inv.agent.responses[O.ARM_BOOTS]=messages[0]
  inv.wear_best_stuff().run()
  def normal():
   yield True
   inv.agent.blstats.time+=1
  inv.wear_best_stuff().before(Strategy(normal)).run()
  assert inv.agent.blstats.time==101 and len(inv.agent.calls)==1
 check('normal strategy progresses after blocked armor',progression)
print(json.dumps({'arm':sys.argv[1],'passed':len(rows)}))
