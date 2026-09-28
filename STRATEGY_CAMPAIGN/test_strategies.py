import ast
import contextlib
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
import numpy as np
from autoascend import jf_config
from autoascend.combat import fight_heur as fh
from autoascend.item.inventory import Inventory
from autoascend.item import Item
from autoascend.glyph import G, Hunger
from autoascend.protection_failure import ProtectionFailure
from autoascend.agent import Agent
import autoascend.agent as am

class WandTests(unittest.TestCase):
    def setUp(self):
        self.a=NS(blstats=NS(y=5,x=5,hitpoints=10,max_hitpoints=10),glyphs=np.full((15,15),next(iter(G.FLOOR)),dtype=np.int16))
    def ray(self, states, corrected=True, horizon=5, monsters=()):
        hits=defaultdict(float)
        with patch.object(fh,'get_next_states',side_effect=lambda a,w,y,x,dy,dx:states.get((y,x),[])):
            fh._simulate_wand_path(self.a,None,monsters,5,5,0,1,horizon,hits,1.,corrected)
        return dict(hits)
    def test_straight_unchanged(self):
        states={(5,5):[(5,6,0,1,1.,0)],(5,6):[(5,7,0,1,1.,0)]}
        self.assertEqual(self.ray(states),self.ray(states,False))
    def test_bounce_descendant(self):
        states={(5,5):[(5,6,0,1,.05,1),(6,5,1,0,.95,1)],(5,6):[(5,7,0,1,1.,0)]}
        self.assertEqual(self.ray(states)[5,7,None],.05)
        self.assertEqual(self.ray(states,False)[5,7,None],1.)
    def test_sibling_order_and_range(self):
        states={(5,5):[(5,5,0,1,.05,1),(6,5,1,0,.95,1)],(6,5):[(7,5,1,0,1.,0)]}
        forward=self.ray(states,horizon=2)
        states[5,5].reverse()
        self.assertEqual(forward,self.ray(states,horizon=2))
        self.assertEqual(forward[7,5,None],.95)
    def test_mirrored(self):
        states={(5,5):[(5,6,0,1,.5,1),(5,4,0,-1,.5,1)],(5,6):[(5,7,0,1,1.,0)],(5,4):[(5,3,0,-1,1.,0)]}
        hits=self.ray(states)
        self.assertEqual(hits[5,7,None],hits[5,3,None])
    def test_deterministic_bounce_unchanged(self):
        states={(5,5):[(5,6,0,-1,1.,1)],(5,6):[(4,6,-1,0,1.,0)]}
        self.assertEqual(self.ray(states),self.ray(states,False))
    def test_actual_projection_changes_selected_action(self):
        wand=NS(is_offensive_usable_wand=lambda:True)
        self.a.inventory=NS(items=[wand],is_known_empty=lambda i:False,engraving_below_me='')
        monster=(1,6,5,__import__('collections').namedtuple('Monster','mname')('newt'),0)
        states={(5,5,0,1):[(5,6,0,1,.05,1),(6,5,1,0,.95,1)],
                (5,6,0,1):[(5,5,0,-1,1.,0)]}
        with patch.object(fh,'get_next_states',side_effect=lambda a,w,y,x,dy,dx:states.get((y,x,dy,dx),[])), patch.object(fh,'missiles_risk_the_watch',return_value=False), patch.object(fh,'is_dangerous_monster',return_value=False), patch.object(fh,'WEAK_MONSTERS',set()):
            old=fh.get_potential_wand_usages(self.a,[monster],0,1,False)
            new=fh.get_potential_wand_usages(self.a,[monster],0,1,True)
            self.assertEqual(max(old+[(-10,('melee',))],key=lambda p:p[0])[1][0],'melee')
            self.assertEqual(max(new+[(-10,('melee',))],key=lambda p:p[0])[1][0],'zap')

    def test_friend_labels(self):
        self.a.glyphs[5,6]=next(iter(G.PETS));self.a.glyphs[5,7]=next(iter(G.MONS-G.PETS))
        hits=self.ray({(5,5):[(5,6,0,1,1.,0)],(5,6):[(5,7,0,1,1.,0)],(5,7):[(5,5,0,-1,1.,0)]},horizon=10)
        self.assertIn((5,6,'pet'),hits);self.assertIn((5,7,'peaceful'),hits);self.assertIn((5,5,'self'),hits)
    def test_penalties_and_action_rank(self):
        wand=NS(is_offensive_usable_wand=lambda:True)
        self.a.inventory=NS(items=[wand],is_known_empty=lambda i:False,engraving_below_me='')
        monster=(1,5,8,__import__('collections').namedtuple('Monster','mname')('newt'),0)
        # Score preserves all penalties: 10 - 15 - 20p - 200p - 30p.
        with patch.object(fh,'missiles_risk_the_watch',return_value=False),patch.object(fh,'is_dangerous_monster',return_value=False),patch.object(fh,'WEAK_MONSTERS',set()),patch.object(fh,'simulate_wand_path',return_value=[(5,8,monster,1),(5,6,'pet',.05),(5,7,'peaceful',.05),(5,5,'self',.05)]):
            score=fh.get_potential_wand_usages(self.a,[],0,1,True)[0][0]
            self.assertAlmostEqual(score,-17.5)
            self.assertEqual(max([(score,'zap'),(-20,'melee')])[1],'zap')
            self.assertEqual(max([(-255,'zap'),(-20,'melee')])[1],'melee')

class ProtectionTests(unittest.TestCase):
    def observe(self,p,t=1,loc=(0,1,2),hp=10,maxhp=20,intact=True,poly=False):
        p.observe(t,loc,hp,maxhp,intact,poly)
    def active(self,p,t=2,loc=(0,1,2),intact=True,poly=False):
        return p.active(t,loc,intact,poly)
    def test_loss_and_expiry(self):
        p=ProtectionFailure();self.observe(p);self.observe(p,t=2,hp=9)
        self.assertTrue(self.active(p));self.assertTrue(self.active(p,t=5));self.assertFalse(self.active(p,t=6))
        self.observe(p,t=2,hp=8);self.assertEqual(p.failure[0],2)
    def test_invalid_pairs(self):
        for changes in [dict(t=1,hp=9),dict(t=3,hp=9),dict(loc=(0,2,2),hp=9),dict(loc=(1,1,2),hp=9),dict(intact=False,hp=9),dict(maxhp=21,hp=9),dict(poly=True,hp=9)]:
            p=ProtectionFailure();self.observe(p);self.observe(p,**(dict(t=2)|changes));self.assertFalse(self.active(p))
        for changes in [dict(intact=False),dict(poly=True)]:
            p=ProtectionFailure();self.observe(p,**changes);self.observe(p,t=2,hp=9);self.assertFalse(self.active(p))
    def test_clear_on_departure_or_erasure(self):
        for changes in [dict(loc=(2,1,2)),dict(intact=False)]:
            p=ProtectionFailure();self.observe(p);self.observe(p,t=2,hp=9);self.observe(p,t=3,hp=9,**changes)
            self.assertIsNone(p.failure)
    def test_actual_lr_branch(self):
        # Compile the actual LR block, including its outer HP/burden/poly gates and action ordering.
        tree=ast.parse(Path(am.__file__).read_text())
        fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='emergency_strategy')
        block=next(n for n in fn.body if isinstance(n,ast.If) and 'jf_config.LAST_RESORT and' in ast.unparse(n.test))
        source='def branch(self, poly_buffer=False):\n'+__import__('textwrap').indent(ast.unparse(block),'    ')+'\n    yield False\n'
        env=vars(am).copy();exec(source,env)
        monster=(1,1,2,NS(),0);level=NS(dungeon_number=0,key=lambda:(0,1),objects=np.full((3,3),next(iter(G.STAIR_DOWN))))
        dive=NS(_near_hostiles=lambda radius:[monster],_ignores_elbereth=lambda m:False,protection_failed=lambda:True)
        a=NS(blstats=NS(y=1,x=1,time=100,carrying_capacity=0),_critically_low_hp=lambda:True,
            get_visible_monsters=lambda:[monster],current_level=lambda:level,global_logic=NS(dive=dive),
            inventory=NS(engraving_below_me='Elbereth'),character=NS(prop=NS(blind=False)),
            _last_resort_stairs_turn=0,can_engrave=lambda:True,log=lambda x:None,move=lambda x:None)
        with patch.object(jf_config,'LAST_RESORT',True),patch.object(jf_config,'LR_ELBERETH',True),patch.object(jf_config,'PROTECTION_FAILURE',True):
            self.assertTrue(next(env['branch'](a)))
            self.assertFalse(next(env['branch'](a,True)))
            a.blstats.carrying_capacity=4;self.assertFalse(next(env['branch'](a)));a.blstats.carrying_capacity=0
            dive.protection_failed=lambda:False;self.assertFalse(next(env['branch'](a)))

class FoodTests(unittest.TestCase):
    def setUp(self):
        self.flag=patch.object(jf_config,'TOOL_SHOP_RESERVE',True);self.flag.start();self.addCleanup(self.flag.stop)
        self.i=Inventory.__new__(Inventory);self.stock=0;self.hostile=[];self.tool=True;self.picked=0;self.settled=0
        self.food=NS(shop_status=Item.FOR_SALE,is_unambiguous=lambda:True,object=NS(name='food ration'),status=Item.UNKNOWN,price=40)
        self.level=NS(key=lambda:(0,1),shop_interior=np.ones((5,5),bool),walkable=np.ones((5,5),bool),objects=np.full((5,5),next(iter(G.FLOOR)),np.int16),intact_doors=np.zeros((5,5),bool),items={})
        for y in range(5):
            for x in range(5):self.level.items[y,x]=[]
        self.level.items[2,4]=[self.food]
        self.bl=NS(time=100,y=2,x=2,gold=100,hunger_state=Hunger.HUNGRY,carrying_capacity=0)
        self.a=NS(blstats=self.bl,current_level=lambda:self.level,get_visible_monsters=lambda:self.hostile,
            carried_food_nutrition=lambda:self.stock,character=NS(prop=NS(blind=False,hallu=False,confusion=False,stun=False)),
            bfs=lambda:np.zeros((5,5),int),glyphs=np.zeros((5,5),np.int16),monster_tracker=NS(monster_mask=np.zeros((5,5),bool)),
            _carries_digging_tool=lambda:self.tool,env=NS(debug_log=lambda **kw:contextlib.nullcontext()),log=lambda s:None)
        self.i.agent=self.a;self.i.items=[];self.i.items_below_me=[];self.i.carried_nutrition=lambda:self.stock
        self.a.move=self.move;self.i.pickup=self.pickup;self.i.pay_or_drop_unpaid=self.settle
    def move(self,y,x):
        self.bl.y=y;self.bl.x=x;self.bl.time+=1;self.i.items_below_me=self.level.items[y,x]
    def pickup(self,item,n):
        self.assertEqual(n,1);self.picked+=1;self.bl.time+=1;self.stock=800;self.i.items=[NS(shop_status=Item.UNPAID,content=None)]
    def settle(self):
        self.settled+=1;self.bl.time+=1;self.i.items=[]
    def run_buy(self):
        return self.i.buy_food().run(return_condition=True)
    def test_two_steps_unknown_buc(self):
        self.assertTrue(self.run_buy());self.assertEqual((self.picked,self.settled),(1,1));self.assertEqual(self.bl.time,104)
    def test_underfoot(self):
        self.level.items[2,2]=[self.food];self.i.items_below_me=[self.food]
        self.assertTrue(self.run_buy());self.assertEqual(self.bl.time,102)
    def test_rejected_food_and_affordability(self):
        for field,value in [('price',None),('price',101),('status',Item.CURSED),('object',NS(name='apple'))]:
            old=getattr(self.food,field);setattr(self.food,field,value);self.assertFalse(self.run_buy());setattr(self.food,field,old)
    def test_offshop_unreachable(self):
        self.level.shop_interior[2,4]=False;self.assertFalse(self.run_buy())
        self.level.shop_interior[2,4]=True;self.a.bfs=lambda:np.full((5,5),-1);self.assertFalse(self.run_buy())
    def test_hostile_after_travel_and_cooldown(self):
        def move(y,x):self.move(y,x);self.hostile=[1]
        self.a.move=move;self.assertTrue(self.run_buy());self.assertEqual(self.picked,0)
        self.hostile=[];self.assertFalse(self.run_buy())
    def test_changed_price_after_travel(self):
        def move(y,x):self.move(y,x);self.food.price=101
        self.a.move=move;self.assertTrue(self.run_buy());self.assertEqual(self.picked,0)
    def test_eight_turn_boundary(self):
        def move(y,x):self.move(y,x);self.bl.time=108
        self.a.move=move;self.assertTrue(self.run_buy());self.assertEqual(self.picked,0)
    def test_cleanup_after_timeout_threat(self):
        def pickup(i,n):self.pickup(i,n);self.bl.time=110;self.hostile=[1]
        self.i.pickup=pickup;self.assertTrue(self.run_buy());self.assertEqual(self.settled,1)
    def test_tool_flag_off(self):
        with patch.object(jf_config,'TOOL_SHOP_RESERVE',False):self.assertFalse(self.run_buy())
    def test_no_tool_original_branch(self):
        self.tool=False;self.i._food_for_sale=lambda dis:(1,2,2,'food ration',40);self.i.items_below_me=[self.food]
        self.assertTrue(self.run_buy());self.assertEqual(self.picked,1)

if __name__=='__main__':unittest.main(verbosity=2)
