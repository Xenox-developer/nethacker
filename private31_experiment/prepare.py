from pathlib import Path
import json,hashlib,shutil,difflib,tarfile
E=Path(__file__).resolve().parent
W=E.parent
A=W/'EXPERIMENT_ASSETS/20260928T054415304296Z-130a7ec3b8744f2fad4a17b97e75da07'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
h=json.loads((A/'base31-runtime-hashes.json').read_text())
assert all(sha(A/'base31-runtime'/p)==v for p,v in h.items())
prov=json.loads((A/'provenance.json').read_text())
assert all(sha(A/'reference-dag'/p)==v for p,v in prov['reference_files_sha256'].items())
(E/'asset-verification.json').write_text(json.dumps({'verified':h,'reference':prov},indent=2))
with tarfile.open(E/'incoming-outer-champion.tar.gz','w:gz') as t:
 for p in ['autoascend','arena_adapter.py','bot.py','LICENSE','nethackers.solution.json']: t.add(W/p,arcname=p)
for arm in ['baseline','candidate']: shutil.copytree(A/'base31-runtime',E/arm)
p=E/'candidate/autoascend/item/inventory.py'
s=p.read_text()
s=s.replace('    def wear(self, item, smart=True):', '''    def _trap_slot_blocked(self, slot):
        return self.agent.blstats.time < getattr(self, '_trap_armor_until', {}).get(slot, 0)

    def _blocked_by_trap(self, item):
        # hypothesis: a 20-game-turn slot cooldown lets normal play proceed after
        # explicit trap refusals, without renewing the deadline on skipped retries.
        # Adapted from eL1fe/nethacker a9e63ae engines/dag (MIT).
        if re.search(r'Your foot is trapped!|Your feet are stuck in the |is attached to the buried ball!|'
                     r'bear trap prevents you from pulling your |and cannot pull your ', self.agent.message):
            if not hasattr(self, '_trap_armor_until'):
                self._trap_armor_until = {}
            self._trap_armor_until[item.object.sub] = self.agent.blstats.time + 20
            return True
        return False

    def wear(self, item, smart=True):''')
s=s.replace('        for i in self.items:\n            assert not isinstance(i, O.Armor)', "        if self._trap_slot_blocked(item.object.sub):\n            return False\n\n        for i in self.items:\n            assert not isinstance(i, O.Armor)")
s=s.replace("            assert 'You finish your dressing maneuver.'", "            if self._blocked_by_trap(item):\n                return False\n            assert 'You finish your dressing maneuver.'",1)
s=s.replace("'You are now wearing ' in self.agent.message or \\\n                   'Your foot is trapped!' in self.agent.message", "'You are now wearing ' in self.agent.message")
s=s.replace('        assert item in equipped_armors\n', '        assert item in equipped_armors\n        if self._trap_slot_blocked(item.object.sub):\n            return False\n',1)
s=s.replace('            assert is_take_off_message(), self.agent.message', '            if self._blocked_by_trap(item):\n                return False\n            assert is_take_off_message(), self.agent.message',1)
s=s.replace('        if not item.can_be_dropped_from_inventory():', "        if item.equipped and item.is_armor() and self._trap_slot_blocked(item.object.sub):\n            return False\n        if not item.can_be_dropped_from_inventory():",1)
s=s.replace('                additional_cond = True', '''                if self._trap_slot_blocked(slot):
                    continue
                # A blocked outer layer also prevents changing the armor beneath it.
                if slot in (O.ARM_SHIRT, O.ARM_SUIT) and self.items.cloak is not None and self._trap_slot_blocked(O.ARM_CLOAK):
                    continue
                if slot == O.ARM_SHIRT and self.items.suit is not None and self._trap_slot_blocked(O.ARM_SUIT):
                    continue
                additional_cond = True''',1)
p.write_text(s)
orig=(A/'base31-runtime/autoascend/item/inventory.py').read_text()
(E/'policy.diff').write_text(''.join(difflib.unified_diff(orig.splitlines(True),s.splitlines(True),fromfile='base31/inventory.py',tofile='candidate/inventory.py')))
m=json.loads((W/'nethackers.solution.json').read_text())
m['name']='private31-trap-armor-cooldown'
m['influences']=list(dict.fromkeys(m['influences']+json.loads((A/'base31-runtime/nethackers.solution.json').read_text())['influences']+[prov['baseline_reference'],prov['reference']]))
m['runtime_authorship']={'baseline':prov['baseline_reference'],'mechanism':prov['reference']+'/engines/dag/autoascend/item/inventory.py','license':'MIT','note':'Native parents retained separately from runtime authorship; attempt31 daglar5d0d455 plus attempt28 depth>=20 guard, exact adapter and blind cap6.'}
(E/'candidate/nethackers.solution.json').write_text(json.dumps(m,indent=2)+'\n')
