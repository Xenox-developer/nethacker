"""Focused fixtures; run with CAMPAIGN_SOURCE selecting the frozen source."""
import os, sys, unittest, contextlib
from types import SimpleNamespace as NS
from collections import defaultdict, namedtuple
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0, os.environ.get('CAMPAIGN_SOURCE', '/tmp/campaign-baseline'))
from autoascend.combat import fight_heur as fh
from autoascend import jf_config as cfg
from autoascend.dive_logic import DiveLogic
from autoascend.item.inventory import Inventory
from autoascend.item import Item
from autoascend.glyph import G, Hunger
from autoascend.agent import Agent
import numpy as np

class WandTests(unittest.TestCase):
    def setUp(self):
        self.agent=NS(blstats=NS(y=5,x=5,hitpoints=10,max_hitpoints=20),glyphs=np.full((21,79),2359,dtype=np.int16))
        self.mon=(1,5,8,namedtuple('Mon','mname')('giant'),0)
    def run_path(self, states, corrected, distance=13, monsters=()):
        hits=defaultdict(int)
        with patch.object(fh,'get_next_states',side_effect=states):
            fh._simulate_wand_path(self.agent,None,monsters,5,5,0,1,distance,hits,1.,corrected)
        return dict(hits)
    def test_straight_unchanged(self):
        states=lambda a,w,y,x,dy,dx: [(y,x+1,0,1,1.,0)] if x<15 else []
        self.assertEqual(self.run_path(states,True,monsters=[self.mon]),self.run_path(states,False,monsters=[self.mon]))
    def test_later_bounce_weight_and_sibling_permutation(self):
        def states(reverse=False):
            def f(a,w,y,x,dy,dx):
                if x==5:
                    values=[(5,6,0,1,.05,1),(6,6,0,1,.95,0)]
                    return values[::-1] if reverse else values
                return [(y,x+1,0,1,1.,0)] if x<10 else []
            return f
        corrected=self.run_path(states(),True,4,[self.mon])
        self.assertAlmostEqual(corrected[5,8,self.mon],.05)
        self.assertEqual(corrected,self.run_path(states(True),True,4,[self.mon]))
        self.assertNotEqual(corrected,self.run_path(states(),False,4,[self.mon]))
        self.assertIn((6,10,None),corrected)
    def test_mirrored_branches(self):
        def states(a,w,y,x,dy,dx):
            if x==5:return [(4,6,-1,1,.5,1),(6,6,1,1,.5,1)]
            return [(y+dy,x+1,dy,1,1.,0)] if x<9 else []
        hits=self.run_path(states,True)
        for (y,x,m),v in hits.items(): self.assertEqual(v,hits[10-y,x,m])
    def test_diagnostic_choice_distinguishes_scores_from_actions(self):
        wand=object();actual=('zap',0,1,wand,set());other=('zap',0,1,wand,set());melee=('melee',0,1)
        a=NS(_campaign_original_actions=[(10,actual),(5,melee)],
             _campaign_alternate_actions=[(9,other),(5,melee)])
        choice=fh.campaign_alternate_choice(a,a._campaign_original_actions)
        self.assertEqual(fh.campaign_action_key(choice),fh.campaign_action_key(actual))
        a._campaign_alternate_actions=[(4,other),(5,melee)]
        self.assertIs(fh.campaign_alternate_choice(a,a._campaign_original_actions),melee)

    def test_self_pet_peaceful_labels(self):
        self.agent.glyphs[5,6]=next(iter(G.PETS))
        self.agent.glyphs[5,7]=next(g for g in G.MONS if g not in G.PETS)
        def states(a,w,y,x,dy,dx):
            return [(5,5,0,1,1.,0),(5,6,0,1,1.,0),(5,7,0,1,1.,0)]
        hits=self.run_path(states,True,0)
        self.assertEqual({m for y,x,m in hits},{'self','pet','peaceful'})
    def test_existing_score_penalties_and_action_ranking(self):
        wand=NS(is_offensive_usable_wand=lambda:True)
        self.agent.inventory=NS(items=[wand],is_known_empty=lambda w:False,engraving_below_me='')
        targets=[(5,8,self.mon,1.),(5,5,'self',.1),(5,6,'pet',.2),(5,7,'peaceful',.3)]
        with patch.object(fh,'missiles_risk_the_watch',return_value=False),patch.object(fh,'simulate_wand_path',return_value=iter(targets)),patch.object(fh,'is_dangerous_monster',return_value=True):
            score,action=fh.get_potential_wand_usages(self.agent,[],0,1)[0]
        self.assertAlmostEqual(score,25-3-4-60-15)
        # Real scoring changes the winner against an unchanged melee candidate.
        for probability,expected in [(1.,'zap'),(.05,'melee')]:
            with patch.object(fh,'missiles_risk_the_watch',return_value=False),patch.object(fh,'simulate_wand_path',return_value=iter([(5,8,self.mon,probability)])),patch.object(fh,'is_dangerous_monster',return_value=True):
                actions=fh.get_potential_wand_usages(self.agent,[],0,1)+[(0,('melee',0,1))]
                self.assertEqual(max(actions,key=lambda x:x[0])[1][0],expected)

class ProtectionTests(unittest.TestCase):
    def setUp(self):
        self.level=NS(key=lambda:(0,3),dungeon_number=0,objects=np.zeros((21,79),dtype=int))
        self.a=NS(blstats=NS(time=10,y=5,x=5,hitpoints=10,max_hitpoints=20),current_level=lambda:self.level,
                  inventory=NS(engraving_below_me='Elbereth'),character=NS(prop=NS(polymorph=False,blind=False)))
        self.d=DiveLogic.__new__(DiveLogic);self.d.agent=self.a
    def observe(self,**changes):
        for k,v in changes.items():setattr(self.a.blstats,k,v)
        self.d._observe_protection()
        return self.d.protection_failed_recently()
    def test_loss_boundary_and_same_turn(self):
        self.assertFalse(self.observe())
        self.assertFalse(self.observe(hitpoints=9))
        self.assertFalse(self.observe(time=11,hitpoints=8))
        self.assertTrue(self.observe(time=12,hitpoints=7))
        self.assertTrue(self.observe(time=15))
        self.assertFalse(self.observe(time=16))
    def test_invalid_pairs(self):
        for change in ['tile','level','broken','gap','maxhp','poly','new_engraving']:
            with self.subTest(change=change):
                self.setUp()
                if change=='new_engraving':self.a.inventory.engraving_below_me=''
                self.observe()
                self.a.blstats.time=11;self.a.blstats.hitpoints=5
                if change=='tile':self.a.blstats.x=6
                if change=='level':self.level.key=lambda:(0,4)
                if change=='broken':self.a.inventory.engraving_below_me='Elberet'
                if change=='gap':self.a.blstats.time=13
                if change=='maxhp':self.a.blstats.max_hitpoints=21
                if change=='poly':self.a.character.prop.polymorph=True
                if change=='new_engraving':self.a.inventory.engraving_below_me='Elbereth'
                self.assertFalse(self.observe())
    def test_clear_evidence_on_leaving_or_erasure(self):
        for change in ['tile','level','broken']:
            self.setUp();self.observe();self.assertTrue(self.observe(time=11,hitpoints=5))
            if change=='tile':self.a.blstats.x=6
            if change=='level':self.level.key=lambda:(1,3)
            if change=='broken':self.a.inventory.engraving_below_me=''
            self.assertFalse(self.observe());self.assertIsNone(self.d._protection_failure)
    def test_actual_last_resort_branch_and_gates(self):
        self.observe();self.observe(time=11,hitpoints=5)
        a=self.a;b=a.blstats
        a.agent=a;a.env=NS(debug_log=lambda *args,**kwargs:contextlib.nullcontext())
        b.carrying_capacity=0;b.hunger_state=Hunger.NOT_HUNGRY;b.depth=3
        a.last_observation={'blstats':np.zeros(27,dtype=int)}
        a.inventory.items=[]
        a.character.poly_hp_is_buffer=lambda:False
        a._critically_low_hp=lambda:True;a.is_safe_to_pray=lambda *args,**kw:False
        a.fainting_prayer_due=lambda:False;a.threat_prayer_due=lambda:False;a.prayer_failed=False
        mon=(1,5,6,NS(mname='jackal'),0)
        a.get_visible_monsters=lambda:[mon];a.can_engrave=lambda:True
        self.d._near_hostiles=lambda **kw:[mon];self.d._ignores_elbereth=lambda m:False
        self.d.undiggable=set();a.global_logic=NS(dive=self.d)
        a._last_resort_stairs_turn=-100;a.log=lambda *args:None
        actions=[];a.move=actions.append
        self.level.objects[5,5]=next(iter(G.STAIR_DOWN))
        with patch.multiple(cfg,ELBERETH_FAILURE_OVERRIDE=False,LAST_RESORT=True,LR_ELBERETH=True,EARLY_FIXES=True):
            self.assertFalse(Agent.emergency_strategy(a).check_condition())
        with patch.multiple(cfg,ELBERETH_FAILURE_OVERRIDE=True,LAST_RESORT=True,LR_ELBERETH=True,EARLY_FIXES=True):
            self.assertTrue(Agent.emergency_strategy(a).run(return_condition=True));self.assertEqual(actions,['>'])
            b.carrying_capacity=4
            self.assertFalse(Agent.emergency_strategy(a).check_condition())
            b.carrying_capacity=0;a._critically_low_hp=lambda:False
            self.assertFalse(Agent.emergency_strategy(a).check_condition())

class MockItems(list):
    def update(self, force=False): pass

class FoodTests(unittest.TestCase):
    def setUp(self):
        shape=(21,79)
        self.level=NS(key=lambda:(0,3),shop_interior=np.zeros(shape,dtype=bool),walkable=np.ones(shape,dtype=bool),objects=np.full(shape,2359,dtype=np.int16),items=np.empty(shape,dtype=object))
        for pos in np.ndindex(shape):self.level.items[pos]=[]
        self.level.shop_interior[5,5:8]=True
        self.a=NS(blstats=NS(time=10,y=5,x=5,gold=100,hunger_state=Hunger.HUNGRY,carrying_capacity=0),
                  current_level=lambda:self.level,character=NS(prop=NS(blind=False,hallu=False,polymorph=False)),
                  monster_tracker=NS(monster_mask=np.zeros(shape,dtype=bool)),
                  get_visible_monsters=lambda:[],atom_operation=lambda **kwargs:contextlib.nullcontext(),
                  _carries_digging_tool=lambda:True,log=lambda *args:None)
        self.stock=0;self.a.carried_food_nutrition=lambda:self.stock
        self.inv=Inventory.__new__(Inventory);self.inv.agent=self.a;self.inv.items=MockItems();self.inv.items_below_me=[]
        self.inv.carried_nutrition=lambda:self.stock
        self.item=NS(shop_status=Item.FOR_SALE,is_unambiguous=lambda:True,object=NS(name='food ration'),status=Item.UNKNOWN,price=50,is_container=lambda:False)
        self.level.items[5,7]=[self.item]
        self.a.neighbors=lambda y,x,shuffle=False:[(y,x-1),(y,x+1)]
        def bfs(y=None,x=None):
            if y is None:y,x=self.a.blstats.y,self.a.blstats.x
            dis=np.full(shape,-1);dis[y,x]=0
            for pos in self.a.neighbors(y,x):
                if self.level.shop_interior[pos]:dis[pos]=1
            return dis
        self.a.bfs=bfs;self.a.calc_direction=lambda y,x,ny,nx:(ny,nx)
        self.move_hook=lambda:None
        def move(pos):
            self.a.blstats.y,self.a.blstats.x=pos;self.a.blstats.time+=1
            self.inv.items_below_me=self.level.items[pos];self.move_hook()
        self.a.env=NS(debug_log=lambda *args,**kwargs:contextlib.nullcontext())
        self.a.move=move
        self.picked=0;self.settled=0;self.pick_hook=lambda:None
        def pickup(item,count,**kwargs):
            self.assertEqual(count,1);self.picked+=1;self.a.blstats.time+=1
            item.shop_status=Item.UNPAID;self.inv.items=MockItems([item]);self.pick_hook()
        def settle():
            self.settled+=1;self.a.blstats.time+=1
            for i in self.inv.items:i.shop_status=Item.NOT_SHOP
            self.stock=800
        self.inv.pickup=pickup;self.inv.pay_or_drop_unpaid=settle
    def run_buy(self):
        with patch.multiple(cfg,BUY_FOOD=True,TOOL_SHOP_RESERVE=True):
            return self.inv.buy_food().run(return_condition=True)
    def test_two_steps_unknown_buc_one_unit(self):
        self.assertTrue(self.run_buy());self.assertEqual((self.picked,self.settled),(1,1));self.assertEqual(self.a.blstats.time,14)
    def test_underfoot(self):
        self.a.blstats.x=7;self.inv.items_below_me=[self.item]
        self.assertTrue(self.run_buy());self.assertEqual(self.picked,1)
    def test_bad_stock_price_path_and_curse(self):
        for why in ['price','unknown_price','cursed','unreachable','offshop','stock','hunger','wrong_food']:
            self.setUp()
            if why=='price':self.item.price=101
            if why=='unknown_price':self.item.price=None
            if why=='cursed':self.item.status=Item.CURSED
            if why=='unreachable':self.a.bfs=lambda *args:np.full((21,79),-1)
            if why=='offshop':self.level.shop_interior[5,6]=False
            if why=='stock':self.stock=400
            if why=='hunger':self.a.blstats.hunger_state=Hunger.NOT_HUNGRY
            if why=='wrong_food':self.item.object.name='apple'
            with self.subTest(why=why):self.assertFalse(self.run_buy());self.assertEqual(self.picked,0)
    def test_recheck_after_travel(self):
        for why in ['threat','price','timeout','level']:
            self.setUp()
            def hook():
                if why=='threat':self.a.get_visible_monsters=lambda:[1]
                if why=='price':self.item.price=101
                if why=='timeout':self.a.blstats.time=18
                if why=='level':self.level.key=lambda:(0,4)
            self.move_hook=hook
            self.run_buy();self.assertEqual(self.picked,0)
            self.assertTrue(self.inv._reserve_failed)
    def test_exact_eight_boundary(self):
        self.assertIsNone(self.inv._reserve_gate((0,3),3)) # seven elapsed
        self.assertEqual(self.inv._reserve_gate((0,3),2),'timeout')
    def test_settlement_even_after_threat_timeout(self):
        def hook():
            self.a.blstats.time=19;self.a.get_visible_monsters=lambda:[1]
        self.pick_hook=hook;self.run_buy()
        self.assertEqual((self.picked,self.settled),(1,1));self.assertEqual(self.item.shop_status,Item.NOT_SHOP)
    def test_failed_target_cooldown(self):
        self.inv._reserve_failed={((0,3),(5,7)):10}
        self.assertIsNone(self.inv._reserve_target())
        self.a.blstats.time=110;self.assertIsNotNone(self.inv._reserve_target())
    def test_real_pickup_refreshes_stack_before_dropping_excess(self):
        import inspect
        if 'refresh_inventory' not in inspect.signature(Inventory.pickup).parameters:
            self.skipTest('Refresh option belongs only to B and combinations containing B')
        item=self.item;item.count=2;item.text='2 food rations'
        self.inv.items_below_me=[item];self.inv.letters_below_me=['a']
        self.inv.panic_if_items_below_me_change=contextlib.nullcontext
        self.inv.get_items_below_me=lambda:None
        self.a.message='a - 2 food rations';self.a.step=lambda *args:None
        self.a.single_message=''
        events=[]
        state=NS(all_items=[],all_letters=[])
        def update(force=False):
            events.append('refresh');state.all_items=[item];state.all_letters=['a']
        state.update=update;self.inv.items=state
        self.inv.drop=lambda picked,count,smart=False:events.append(('drop',count))
        Inventory.pickup(self.inv,[item],[1],refresh_inventory=True)
        self.assertEqual(events,['refresh',('drop',1)])

    def test_tool_flag_and_no_tool_original_branch(self):
        with patch.multiple(cfg,BUY_FOOD=True,TOOL_SHOP_RESERVE=False):
            self.assertFalse(self.inv.buy_food().check_condition())
        self.a._carries_digging_tool=lambda:False
        self.inv._food_for_sale=lambda dis:(1,5,5,'food ration',50)
        self.inv.items_below_me=[self.item]
        self.assertTrue(self.run_buy());self.assertEqual(self.picked,1)

if __name__=='__main__':unittest.main(verbosity=2)
