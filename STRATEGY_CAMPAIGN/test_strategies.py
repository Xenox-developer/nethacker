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
from autoascend.glyph import Hunger, G
from autoascend.dive_logic import DiveLogic
import campaign_events as ce

class WandTests(unittest.TestCase):
    def setUp(self):
        self.a=NS(blstats=NS(y=8,x=8),glyphs=np.full((12,12),-1))
    def run_path(self, states, corrected=True, horizon=4):
        hits=defaultdict(int)
        with patch.object(fh,'get_next_states',side_effect=states):
            fh._simulate_wand_path(self.a,None,[],1,1,0,1,horizon,hits,1.,corrected)
        return dict(hits)
    def test_straight_unchanged(self):
        f=lambda a,w,y,x,dy,dx:[(y,x+1,dy,dx,1.,0)]
        self.assertEqual(self.run_path(f),self.run_path(f,False))
    def test_bounce_weight_later_target(self):
        def f(a,w,y,x,dy,dx):
            return [(2,2,0,1,.05,1),(3,2,0,1,.95,1)] if (y,x)==(1,1) else [(y,x+1,dy,dx,1.,0)]
        self.assertAlmostEqual(self.run_path(f)[(2,3,None)],.05)
        self.assertEqual(self.run_path(f,False)[(2,3,None)],1.)
    def test_sibling_order_and_independent_range(self):
        def f(reverse):
            def states(a,w,y,x,dy,dx):
                if (y,x)==(1,1):
                    v=[(2,2,0,1,.05,2),(3,2,0,1,.95,0)]
                    return v[::-1] if reverse else v
                return [(y,x+1,dy,dx,1.,0)]
            return states
        self.assertEqual(self.run_path(f(False)),self.run_path(f(True)))
        self.assertIn((3,6,None),self.run_path(f(False)))
    def test_mirrored_branches(self):
        def f(a,w,y,x,dy,dx):
            return [(2,2,0,1,.5,0),(4,2,0,1,.5,0)] if (y,x)==(1,1) else [(y,x+1,dy,dx,1.,0)]
        h=self.run_path(f)
        self.assertEqual(h[(2,4,None)],h[(4,4,None)])
    def test_self_pet_peaceful_penalties(self):
        wand=NS(is_offensive_usable_wand=lambda:True)
        self.a.inventory=NS(items=[wand],is_known_empty=lambda i:False,engraving_below_me='')
        self.a.blstats.hitpoints=10; self.a.blstats.max_hitpoints=20
        monster=(1,3,3,NS(mname='test'),0)
        # Hashable monster is needed in action's set.
        from collections import namedtuple
        monster=(1,3,3,namedtuple('Mon','mname')('test'),0)
        for label,penalty in [('self',30),('pet',20),('peaceful',200)]:
            with patch.object(fh,'missiles_risk_the_watch',return_value=False),patch.object(fh,'is_dangerous_monster',return_value=False),patch.object(fh,'simulate_wand_path',return_value=iter([(3,3,monster,1),(2,2,label,.5)])):
                self.assertEqual(fh.get_potential_wand_usages(self.a,[],0,1)[0][0],10-15-penalty*.5)

class FoodTests(unittest.TestCase):
    def setUp(self):
        self.inv=Inventory.__new__(Inventory); self.stock=0; self.moves=0; self.pickups=0; self.pays=0
        self.b=NS(y=2,x=2,time=100,gold=100,hunger_state=Hunger.HUNGRY)
        self.level=NS(shop_interior=np.ones((5,5),bool),item_count=np.zeros((5,5),int),items={},key=lambda:(0,1))
        self.food=NS(shop_status=Item.FOR_SALE,is_unambiguous=lambda:True,object=NS(name='food ration'),is_container=lambda:False,status=0,price=50,count=1)
        self.level.item_count[2,4]=1; self.level.items[2,4]=[self.food]
        self.hostiles=[]; self.tool=True; self.after_move=lambda:None; self.after_pick=lambda:None
        def bfs(y=None,x=None):
            y=self.b.y if y is None else y; x=self.b.x if x is None else x
            yy,xx=np.indices((5,5)); return np.maximum(abs(yy-y),abs(xx-x))
        def move(y,x):
            self.moves+=1; self.b.y=y; self.b.x=x; self.b.time+=1; self.after_move()
        self.a=NS(blstats=self.b,current_level=lambda:self.level,bfs=bfs,move=move,
                  get_visible_monsters=lambda:self.hostiles,_carries_digging_tool=lambda:self.tool)
        self.a.env=NS(debug_log=lambda **kw:contextlib.nullcontext()); self.inv.agent=self.a; self.inv.items=[]; self.inv.items_below_me=[self.food]
        self.inv.carried_nutrition=lambda:self.stock
        self.a.carried_food_nutrition=lambda:self.stock
        def pickup(item,n):
            self.pickups+=1; self.stock+=800; item.shop_status=Item.UNPAID; self.inv.items=[item]; self.b.time+=1; self.after_pick()
        def pay():
            self.pays+=1; self.food.shop_status=Item.NOT_SHOP; self.b.time+=1
        self.inv.pickup=pickup; self.inv.pay_or_drop_unpaid=pay
        self.flag=patch.object(jf_config,'CAMPAIGN_B',True); self.flag.start(); self.addCleanup(self.flag.stop)
    def run_buy(self):
        gen=self.inv.buy_food().strategy(); eligible=next(gen)
        if eligible:
            with self.assertRaises(StopIteration): next(gen)
        return eligible
    def test_purchase_unknown_buc(self):
        self.assertTrue(self.run_buy()); self.assertEqual((self.moves,self.pickups,self.pays),(2,1,1))
    def test_underfoot_and_one_unit(self):
        self.b.x=4
        self.assertTrue(self.run_buy()); self.assertEqual((self.moves,self.pickups,self.pays),(0,1,1))
    def test_change_level_after_travel(self):
        self.after_move=lambda:setattr(self.level,'key',lambda:(0,2))
        self.assertTrue(self.run_buy()); self.assertEqual(self.pickups,0)
    def test_stock_gate(self):
        self.stock=400; self.assertFalse(self.run_buy())
    def test_seven_turns_allows_pickup(self):
        self.b.x=3
        self.after_move=lambda:setattr(self.b,'time',107)
        self.assertTrue(self.run_buy()); self.assertEqual(self.pickups,1)
    def test_off_tool_unchanged(self):
        self.tool=False; self.inv._food_for_sale=lambda dis:None
        self.assertFalse(self.run_buy()); self.assertEqual(self.pickups,0)
    def test_flag_off(self):
        with patch.object(jf_config,'CAMPAIGN_B',False): self.assertFalse(self.run_buy())
    def test_price_curse_and_hunger(self):
        for attr,value in [('price',None),('price',101),('status',Item.CURSED)]:
            with self.subTest(attr=attr,value=value),patch.object(self.food,attr,value): self.assertFalse(self.run_buy())
        self.b.hunger_state=Hunger.NOT_HUNGRY
        self.assertFalse(self.run_buy())
    def test_offshop_and_unreachable(self):
        self.level.shop_interior[2,4]=False; self.assertFalse(self.run_buy())
        self.level.shop_interior[:]=False; self.level.shop_interior[2,2]=True; self.level.shop_interior[2,4]=True
        self.assertFalse(self.run_buy())
        self.level.shop_interior[:]=True
        self.a.bfs=lambda *args:np.full((5,5),-1)
        self.assertFalse(self.run_buy())
    def test_hostile_after_travel_and_cooldown(self):
        self.after_move=lambda:self.hostiles.append('hostile')
        self.assertTrue(self.run_buy()); self.assertEqual(self.pickups,0)
        self.hostiles=[]; self.after_move=lambda:None
        self.assertFalse(self.run_buy())
        self.b.time+=100; self.assertTrue(self.run_buy())
    def test_eight_turn_boundary(self):
        self.after_move=lambda:setattr(self.b,'time',108)
        self.assertTrue(self.run_buy()); self.assertEqual((self.moves,self.pickups),(1,0))
    def test_price_changes_after_travel(self):
        self.after_move=lambda:setattr(self.food,'price',200)
        self.assertTrue(self.run_buy()); self.assertEqual(self.pickups,0)
    def test_cleanup_despite_timeout_and_hostile(self):
        def change(): self.b.time=110; self.hostiles.append('hostile')
        self.after_pick=change
        self.assertTrue(self.run_buy()); self.assertEqual(self.pays,1)
        self.assertEqual(self.food.shop_status,Item.NOT_SHOP)

class ProtectionTests(unittest.TestCase):
    def setUp(self):
        self.b=NS(time=10,y=2,x=2,hitpoints=20,max_hitpoints=30)
        self.level=NS(key=lambda:(0,1),dungeon_number=0)
        self.a=NS(blstats=self.b,current_level=lambda:self.level,
                  inventory=NS(engraving_below_me='Elbereth'),character=NS(prop=NS(polymorph=False,blind=False)))
        self.d=DiveLogic.__new__(DiveLogic); self.d.agent=self.a; self.d._protection_observation=None; self.d._protection_failure=None
    def loss(self):
        self.d._observe_protection(); self.b.time+=1; self.b.hitpoints-=3; self.d._observe_protection()
    def test_trigger_and_exact_expiry(self):
        self.loss(); self.assertTrue(self.d.protection_failure_active())
        self.b.time=13; self.assertTrue(self.d.protection_failure_active())
        self.b.time=14; self.d._observe_protection(); self.assertFalse(self.d.protection_failure_active())
    def test_same_turn_loss_never_extends_marker(self):
        self.loss(); mark=self.d._protection_failure
        self.b.hitpoints-=1; self.d._observe_protection()
        self.assertEqual(self.d._protection_failure,mark)
        self.b.time=mark[1]+3
        self.assertFalse(self.d.protection_failure_active())
    def test_disqualifiers(self):
        changes=[lambda:setattr(self.b,'time',10),lambda:setattr(self.b,'time',13),lambda:setattr(self.b,'x',3),lambda:setattr(self.level,'key',lambda:(0,2)),lambda:setattr(self.a.inventory,'engraving_below_me','Elberet'),lambda:setattr(self.b,'max_hitpoints',31),lambda:setattr(self.a.character.prop,'polymorph',True)]
        for change in changes:
            self.setUp(); self.d._observe_protection(); self.b.time=11; self.b.hitpoints=17; change(); self.d._observe_protection(); self.assertFalse(self.d.protection_failure_active())
    def test_previous_engraving_required(self):
        self.a.inventory.engraving_below_me=''; self.d._observe_protection()
        self.a.inventory.engraving_below_me='Elbereth'; self.b.time+=1; self.b.hitpoints-=3
        self.d._observe_protection(); self.assertFalse(self.d.protection_failure_active())
    def test_clear_on_departure_or_erasure(self):
        for change in [lambda:setattr(self.b,'x',4),lambda:setattr(self.a.inventory,'engraving_below_me','')]:
            self.setUp(); self.loss(); change(); self.d._observe_protection(); self.assertFalse(self.d.protection_failure_active())
    def test_actual_lr_suppression_branch(self):
        # Compile the actual LR_ELBERETH branch from agent.py, not a duplicate predicate.
        tree=ast.parse((Path(__file__).resolve().parents[1]/'autoascend/agent.py').read_text())
        node=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and 'adjacent and jf_config.LR_ELBERETH' in ast.unparse(n.test))
        code=compile(ast.fix_missing_locations(ast.Module(body=[node],type_ignores=[])),'actual-LR-branch','exec')
        self.d._near_hostiles=lambda radius:[]; self.d._ignores_elbereth=lambda m:False
        self.a.global_logic=NS(dive=self.d); self.a.can_engrave=lambda:True
        for active,flag,expected in [(False,True,False),(True,False,False),(True,True,True)]:
            self.d._protection_failure=None
            if active:self.loss()
            env={'self':self.a,'adjacent':['hostile'],'jf_config':jf_config,'ce':ce}
            with patch.object(jf_config,'CAMPAIGN_C',flag),patch.object(jf_config,'LR_ELBERETH',True):exec(code,env)
            self.assertEqual(bool(env['adjacent']),expected)


class AdditionalFixtures(unittest.TestCase):
    def test_real_projection_changes_wand_ranking(self):
        # Two real wand scores compete with a retained melee action; only branch math changes.
        from collections import namedtuple
        Mon=namedtuple('Mon','mname')
        monster=(1,2,3,Mon('test target'),0)
        wand=NS(is_offensive_usable_wand=lambda:True)
        a=NS(blstats=NS(y=8,x=8,hitpoints=10,max_hitpoints=20),glyphs=np.full((12,12),-1),
             inventory=NS(items=[wand],is_known_empty=lambda i:False,engraving_below_me=''))
        def states(a,w,y,x,dy,dx):
            if (y,x)==(8,8):return [(2,2,0,1,.05,1),(4,2,0,1,.95,1)]
            if (y,x)==(2,2):return [(2,3,0,1,1.,0)]
            return []
        with patch.object(fh,'get_next_states',side_effect=states),patch.object(fh,'missiles_risk_the_watch',return_value=False),patch.object(fh,'is_dangerous_monster',return_value=True):
            old=fh.get_potential_wand_usages(a,[monster],0,1,False)
            new=fh.get_potential_wand_usages(a,[monster],0,1,True)
        self.assertEqual(max(old+[(0,('melee',))],key=lambda x:x[0])[1][0],'zap')
        self.assertEqual(max(new+[(0,('melee',))],key=lambda x:x[0])[1][0],'melee')
    def test_deterministic_reflection_unchanged(self):
        a=NS(blstats=NS(y=3,x=3),glyphs=np.full((7,7),-1),current_level=lambda:NS(walkable=np.pad(np.ones((3,3),bool),2)))
        wand=NS(is_ray_wand=lambda:True)
        self.assertEqual(list(fh.simulate_wand_path(a,wand,[],0,1,False)),list(fh.simulate_wand_path(a,wand,[],0,1,True)))

if __name__=='__main__':unittest.main()
