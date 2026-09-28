"""Pre-game B integration correction: nested atomic pickup requires inventory refresh."""
from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'autoascend/item/inventory.py';s=p.read_text()
s=s.replace('    def pickup(self, items, counts=None):','    def pickup(self, items, counts=None, refresh_inventory=False):',1)
s=s.replace('        if one_item and drop_count:\n            self.drop(','''        if refresh_inventory:
            # Tool-reserve transaction defers callbacks across pickup and settlement.
            self.items.update(force=True)
        if one_item and drop_count:
            self.drop(''',1)
s=s.replace('            with a.atom_operation():\n                try:\n                    self.pickup(item, 1)\n                finally:', '''            with a.atom_operation(allow_update=True):
                try:
                    self.pickup(item, 1, refresh_inventory=True)
                finally:
                    self.items.update(force=True)''',1)
s=s.replace('                    self.pay_or_drop_unpaid()\n                    if a.blstats.time - start > 8:', '                    self.pay_or_drop_unpaid()\n                    self.items.update(force=True)\n                    if a.blstats.time - start > 8:',1)
p.write_text(s)
