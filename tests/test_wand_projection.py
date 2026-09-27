"""Regression checks for independent, probability-weighted wand branches."""
from collections import defaultdict
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
from autoascend.combat import fight_heur as fight


class WandProjectionTest(unittest.TestCase):
    def project(self, branches, horizon=4):
        agent = SimpleNamespace(glyphs=np.full((8, 8), -1),
                                blstats=SimpleNamespace(y=7, x=7))
        monsters = [(0, 1, 2, 'left', 0), (0, 2, 2, 'right', 0)]
        def next_states(agent, wand, y, x, dy, dx):
            if (y, x) == (0, 0):
                return branches
            if (y, x) in ((1, 1), (2, 1)):
                return [(y, 2, 0, 1, 1.0, 0)]
            return []
        hits = defaultdict(int)
        with patch.object(fight, 'get_next_states', next_states):
            fight._simulate_wand_path(agent, None, monsters, 0, 0, 0, 1,
                                      horizon, hits, 1.0)
        return hits

    def test_later_hits_retain_branch_probability(self):
        hits = self.project([(1, 1, 0, 1, .25, 1), (2, 1, 0, 1, .75, 1)])
        targets = {(y, x): p for (y, x, m), p in hits.items() if m is not None}
        self.assertEqual(targets, {(1, 2): .25, (2, 2): .75})

    def test_sibling_order_does_not_change_range(self):
        branches = [(1, 1, 0, 1, .25, 2), (2, 1, 0, 1, .75, 2)]
        forward = self.project(branches, horizon=3)
        self.assertEqual(forward, self.project(branches[::-1], horizon=3))
        self.assertTrue(any(y == 2 and x == 2 for y, x, m in forward))

    def test_straight_ray_keeps_full_weight(self):
        hits = self.project([(1, 1, 0, 1, 1.0, 0)])
        self.assertEqual([p for (y, x, m), p in hits.items() if m is not None], [1.0])


if __name__ == '__main__':
    unittest.main()
