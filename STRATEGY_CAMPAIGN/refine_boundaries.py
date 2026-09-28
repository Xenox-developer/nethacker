"""Pre-evaluation correctness corrections to unevaluated B/C; no threshold tuning."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(next(Path('/workspace/EXPERIMENT_ASSETS').glob('*/campaign.py')).parent))
import campaign
out=Path('/workspace/STRATEGY_CAMPAIGN')
p=Path('/tmp/campaign-B/autoascend/item/inventory.py');s=p.read_text();old="        finally:\n            ce.sample('food_transaction'";new="        finally:\n            if (key, target) in self._reserve_failed:\n                self._reserve_failed[key, target] = a.blstats.time + 100\n            ce.sample('food_transaction'";assert old in s;s=s.replace(old,new);p.write_text(s)
p=Path('/tmp/campaign-C/autoascend/protection_failure.py');s=p.read_text();old='''            if location != prev[1] or not intact or polymorph or maxhp != prev[3]:
                self.previous = None
            return''';new='''            self.previous = current
            return''';assert old in s;s=s.replace(old,new);p.write_text(s)
for label in ['B','C']:
 (out/(label+'-before-initial.json')).write_bytes((out/(label+'-before.json')).read_bytes())
 campaign.atomic_json(out/(label+'-before.json'),campaign.manifest(campaign.files('/tmp/campaign-'+label)))
(out/'pre-evaluation-corrections.md').write_text('''# Corrections before B/C evaluation

After baseline completion and while A was running, a source-boundary review found:
- B initially set failed-location cooldown to entry time +100. It now refreshes to exit time +100 in finally, so a failed multi-turn attempt receives the full specified suppression period.
- C initially ignored same-turn observations entirely. It now retains the latest same-turn observation without creating/extending evidence, preventing an ignored same-turn HP reduction from being misattributed to the next turn.

Neither B nor C had started games. These are contract corrections, not changed hypotheses, thresholds, seed lists, or score-driven replacements. Baseline and A remain immutable; original and corrected B/C pre-evaluation manifests are retained. The common inactive scaffold in baseline/A retains the original dormant implementations; each evaluated singleton patch captures its exact active implementation. Qualified-loss diagnostic counts from the original dormant observer are not strictly equivalent to C's corrected observer; do not use their difference as a causal activation estimate.
''')
