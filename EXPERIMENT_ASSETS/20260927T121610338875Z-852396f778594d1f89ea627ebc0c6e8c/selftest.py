"""Run with plain Python from this asset directory; no pytest or NLE required."""
import unittest

from planner import Action, Config, Monster, State, Topology, choose_action


class TacticalModelTests(unittest.TestCase):
    def test_three_turn_dead_end(self):
        cells = frozenset({(0, 1), (1, 1), (2, 1), (1, 2), (1, 3), (1, 4)})
        state = State(Topology(cells), (1, 1), 10, 3,
                      (Monster("pursuer", (2, 1), 30, 4),))
        actions = (Action("pocket", "move", (0, 1)), Action("corridor", "move", (1, 2)))
        self.assertIsNone(choose_action(state, actions, "pocket", Config(depth=1)).override_key)
        result = choose_action(state, actions, "pocket")
        self.assertEqual(result.override_key, "corridor")
        self.assertEqual(result.roots[0].lethal_scenarios, 1)
        self.assertGreater(result.roots[1].worst_min_hp, 0)

    def test_bounded_and_deterministic(self):
        topology = Topology(frozenset((y, x) for y in range(5) for x in range(5)))
        state = State(topology, (2, 2), 20, 3, (Monster("enemy", (0, 0), 30, 4),))
        actions = (Action("left", "move", (2, 1)), Action("right", "move", (2, 3)))
        config = Config(max_nodes_per_root=3)
        result = choose_action(state, actions, "left", config)
        self.assertEqual(result, choose_action(state, actions, "left", config))
        self.assertEqual(result.reason, "incomplete_horizon")
        self.assertLessEqual(result.nodes, len(actions) * config.max_nodes_per_root)
        self.assertIsNone(result.override_key)

    def test_unsupported_fallback(self):
        self.assertIsNone(choose_action(None, (), "pray").override_key)

    def test_death_is_absorbing(self):
        state = State(Topology(frozenset({(0, 0), (0, 1)})), (0, 0), 2, 4,
                      (Monster("enemy", (0, 1), 10, 3),))
        result = choose_action(state, (Action("hit", "melee", (0, 1)),), "hit")
        self.assertEqual(result.roots[0].lethal_scenarios, 2)
        self.assertLess(result.roots[0].score, -1_000_000)
        self.assertEqual(result.roots[0].principal_variation, ((0, 1),))

    def test_no_player_corner_clearance_assumption_for_enemies(self):
        topology = Topology(frozenset({(0, 0), (0, 1), (1, 2), (2, 3)}))
        state = State(topology, (0, 0), 20, 1,
                      (Monster("small-enemy", (2, 3), 100, 4),))
        result = choose_action(state, (Action("step", "move", (0, 1)),), "step")
        self.assertGreaterEqual(result.roots[0].worst_damage, 5.4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
