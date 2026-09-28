import copy
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import campaign


def rows(seeds, score=0.5, status="completed", error=None):
    return [{"trajectory_id": seed, "character": campaign.IDENTITY, "progress": score,
             "status": status, "error": error} for seed in seeds]


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.base = self.root / "base"
        self.base.mkdir()
        (self.base / "bot.py").write_text("BASE = True\n")
        self.out = self.root / "evidence"

    def record(self, label, public=0.5, development=0.5, error=None):
        digest = campaign.manifest(campaign.files(self.base))["digest"]
        record = {"label": label, "members": [] if label == "baseline" else label.split("+"),
                  "config": copy.deepcopy(campaign.CONFIG), "baseline_digest": digest,
                  "solution_digest": digest if label == "baseline" else f"sha256:{label}",
                  "complete": True, "phases": {}}
        for phase, seeds in campaign.BATCHES.items():
            record["phases"][phase] = [{"technical_failure": False,
                "results": rows(seeds, public if phase == "public" else development,
                                "bot_error" if error else "completed", error)}]
        path = self.out / "variants" / label
        path.mkdir(parents=True)
        campaign.atomic_json(path / "evaluation.json", record)
        return record

    def default_records(self):
        self.record("baseline")
        self.record("A", 0.6, 0.5)
        self.record("B", 0.58, 0.5)
        self.record("C", 0.4, 0.7)

    def test_missing_single_refuses_selection(self):
        self.record("baseline")
        self.record("A")
        with self.assertRaisesRegex(ValueError, "all three"):
            campaign.report(self.out, ["A", "B", "C"])

    def test_all_twenty_rows_required_without_duplicates(self):
        for bad in (rows([0] * 15), rows(range(14)), rows(range(1, 16))):
            with self.assertRaises(ValueError):
                campaign.validate_rows(bad, list(range(15)))

    def test_nonfinite_and_wrong_identity_rejected(self):
        for value in (float("nan"), float("inf"), -1, 2, True):
            with self.assertRaises(ValueError):
                campaign.validate_rows(rows([0], value), [0])
        wrong = rows([0])
        wrong[0]["character"] = "wrong"
        with self.assertRaises(ValueError):
            campaign.validate_rows(wrong, [0])

    def test_required_combo_missing_blocks_final_recommendation(self):
        self.default_records()
        report = campaign.report(self.out, ["A", "B", "C"])
        self.assertEqual(report["eligible_singles"], ["A", "B"])
        self.assertEqual(report["missing_combinations"], ["A+B"])
        self.assertIsNone(report["recommended"])
        self.assertIsNone(report["final_publication_candidate"])

    def test_combo_must_beat_best_single_and_not_regress_development(self):
        self.default_records()
        self.record("A+B", 0.61, 0.49)
        report = campaign.report(self.out, ["A", "B", "C"])
        self.assertEqual(report["recommended"], "A")
        self.assertEqual(len(report["comparisons"]["A+B"]["paired"]["public"]), 15)

    def test_combo_beats_strongest_single(self):
        self.default_records()
        self.record("A+B", 0.61, 0.5)
        report = campaign.report(self.out, ["A", "B", "C"])
        self.assertEqual(report["recommended"], "A+B")
        self.assertEqual(report["final_publication_candidate"], "A+B")

    def test_equal_public_combinations_prefer_higher_development(self):
        self.record("baseline")
        for label in ["A", "B", "C"]:
            self.record(label, 0.6, 0.5)
        self.record("A+B", 0.7, 0.6)
        self.record("A+C", 0.7, 0.7)
        self.record("B+C", 0.65, 0.5)
        self.record("A+B+C", 0.6, 0.9)  # Must strictly beat strongest single's Public.
        self.assertEqual(campaign.report(self.out, ["A", "B", "C"])["recommended"], "A+C")

    def test_all_three_eligible_require_all_four_combinations(self):
        self.record("baseline")
        for label in ("A", "B", "C"):
            self.record(label, 0.6, 0.5)
        report = campaign.report(self.out, ["A", "B", "C"])
        self.assertEqual(report["required_combinations"], ["A+B", "A+C", "B+C", "A+B+C"])

    def test_no_eligible_single_recommends_baseline_and_reports_best_tested(self):
        self.record("baseline")
        self.record("A", 0.49, 0.5)
        self.record("B", 0.5, 0.6)
        self.record("C", 0.48, 0.7)
        report = campaign.report(self.out, ["A", "B", "C"])
        self.assertEqual(report["recommended"], "baseline")
        self.assertEqual(report["best_tested_single"], "B")
        self.assertEqual(report["final_publication_candidate"], "B")
        self.assertEqual(report["required_combinations"], [])

    def test_exact_ties_choose_lower_label_and_all_unclean_has_no_final_candidate(self):
        self.record("baseline")
        for label in ["A", "B", "C"]:
            self.record(label, 0.4, 0.4)
        self.assertEqual(campaign.report(self.out, ["A", "B", "C"])["best_tested_single"], "A")
        for label in ["A", "B", "C"]:
            path = self.out / "variants" / label / "evaluation.json"
            record = json.loads(path.read_text())
            for phase in campaign.BATCHES:
                record["phases"][phase][0]["results"][0]["error"] = "failure"
            campaign.atomic_json(path, record)
        self.assertIsNone(campaign.report(self.out, ["A", "B", "C"])[
            "final_publication_candidate"])

    def test_errors_disqualify_single_even_with_high_score(self):
        self.record("baseline")
        self.record("A", 0.9, 0.9, "failure")
        self.record("B", 0.4, 0.4)
        self.record("C", 0.4, 0.4)
        self.assertEqual(campaign.report(self.out, ["A", "B", "C"])["recommended"], "baseline")

    def test_fixed_baseline_enforced(self):
        self.default_records()
        path = self.out / "variants" / "B" / "evaluation.json"
        value = json.loads(path.read_text())
        value["baseline_digest"] = "another parent"
        campaign.atomic_json(path, value)
        with self.assertRaisesRegex(ValueError, "one fixed baseline"):
            campaign.report(self.out, ["A", "B", "C"])

    def test_rejects_undocumented_reroll(self):
        record = self.record("baseline")
        record["phases"]["public"] *= 2
        with self.assertRaisesRegex(ValueError, "Nontechnical reroll"):
            campaign.means(record)

    def test_evaluate_fake_only_two_batches_canonical_parameters_and_hashes(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            self.assertEqual(command[command.index("--secret") + 1], "public")
            self.assertEqual(command[command.index("--evaluation-id") + 1], "local")
            self.assertNotIn("NETHACK_ARENA_SECRET", kwargs["env"])
            batch = json.loads(command[command.index("--batch") + 1])
            Path(command[-1]).write_text(json.dumps(rows([seed for seed, _ in batch])))

        with patch.dict(os.environ, {"NETHACK_ARENA_SECRET": "fake-irrelevant-value"}):
            record = campaign.evaluate("baseline", [], self.base, self.base, self.out,
                                       runner=runner)
        self.assertTrue(record["complete"])
        self.assertEqual(len(calls), 2)
        self.assertEqual([len(json.loads(c[c.index("--batch") + 1])) for c in calls], [15, 5])
        self.assertEqual(record["baseline_digest"], record["solution_digest"])
        with self.assertRaises(FileExistsError):
            campaign.evaluate("baseline", [], self.base, self.base, self.out, runner=runner)

    def test_only_infrastructure_failure_retries_and_preserves_original_rows(self):
        calls = []

        def runner(command, **kwargs):
            seeds = [seed for seed, _ in json.loads(command[command.index("--batch") + 1])]
            status = "infrastructure_error" if not calls else "completed"
            calls.append(status)
            Path(command[-1]).write_text(json.dumps(rows(seeds, status=status)))

        record = campaign.evaluate("baseline", [], self.base, self.base, self.out, runner=runner)
        self.assertEqual(len(calls), 3)
        self.assertEqual(len(record["phases"]["public"]), 2)
        self.assertEqual(record["phases"]["public"][0]["results"][0]["status"],
                         "infrastructure_error")

    def test_bot_failure_never_retried(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            seeds = [seed for seed, _ in json.loads(command[command.index("--batch") + 1])]
            Path(command[-1]).write_text(json.dumps(rows(seeds, 0, "bot_error", "failed")))

        record = campaign.evaluate("baseline", [], self.base, self.base, self.out, runner=runner)
        self.assertEqual(len(calls), 2)
        self.assertFalse(campaign.clean(record))

    def test_concurrent_campaign_evaluation_is_refused_before_another_arena(self):
        calls = []

        def runner(command, **kwargs):
            calls.append(command)
            with self.assertRaisesRegex(RuntimeError, "already owns"):
                campaign.evaluate("A", ["A"], self.base, self.base, self.out, runner=runner)
            seeds = [seed for seed, _ in json.loads(command[command.index("--batch") + 1])]
            Path(command[-1]).write_text(json.dumps(rows(seeds)))

        record = campaign.evaluate("baseline", [], self.base, self.base, self.out, runner=runner)
        self.assertTrue(record["complete"])
        self.assertEqual(len(calls), 2)
        self.assertFalse((self.out / "variants" / "A").exists())

    def test_variant_sources_must_remain_unchanged_during_evaluation(self):
        def runner(command, **kwargs):
            snapshot = Path(command[command.index("--solution") + 1])
            (snapshot / "bot.py").write_text("MUTATED = True\n")
            seeds = [seed for seed, _ in json.loads(command[command.index("--batch") + 1])]
            Path(command[-1]).write_text(json.dumps(rows(seeds)))

        with self.assertRaisesRegex(RuntimeError, "Source snapshot changed"):
            campaign.evaluate("baseline", [], self.base, self.base, self.out, runner=runner)
        stored = json.loads((self.out / "variants" / "baseline" / "evaluation.json").read_text())
        self.assertFalse(stored["complete"])

    def test_snapshot_rejects_links_and_output_inside_source(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            campaign.evaluate("baseline", [], self.base, self.base, self.base / "evidence")
        (self.base / "linked.py").symlink_to(self.base / "bot.py")
        with self.assertRaisesRegex(ValueError, "symlink"):
            campaign.files(self.base)

    def test_patch_and_hash_change_when_strategy_changes(self):
        base = campaign.files(self.base)
        candidate = {**base, "bot.py": b"BASE = False\n"}
        self.assertNotEqual(campaign.manifest(base), campaign.manifest(candidate))
        self.assertIn("+BASE = False", campaign.patch(base, candidate))

    def test_unchanged_baseline_cannot_be_evaluated_as_a_single_strategy(self):
        with self.assertRaisesRegex(ValueError, "must differ from the fixed baseline"):
            campaign.evaluate("A", ["A"], self.base, self.base, self.out,
                              runner=lambda *a, **kw: self.fail("Must not run an arena"))
        self.assertFalse((self.out / "variants" / "A").exists())


class EventsTests(unittest.TestCase):
    def load(self):
        spec = importlib.util.spec_from_file_location("fresh_events", Path(__file__).with_name(
            "campaign_events.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_disabled_by_default_and_does_not_affect_actions(self):
        with patch.dict(os.environ, {}, clear=True):
            module = self.load()
            self.assertIsNone(module.hit("A.applied"))
            self.assertEqual(module._counts, {})

    def test_bounded_checkpoints_are_honest_lower_bounds(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(
            os.environ, {"NETHACKERS_CAMPAIGN_EVENTS_DIR": temporary}
        ):
            module = self.load()
            for _ in range(1000):
                module.hit("A.applied")
            path = next(Path(temporary).glob("events-*.json"))
            data = json.loads(path.read_text())
            self.assertEqual(data["counts"]["A.applied"], 512)
            self.assertTrue(data["counts_are_lower_bounds"])
            self.assertEqual(data["writes"], 10)
            module.flush(exact=True)
            self.assertEqual(json.loads(path.read_text())["counts"]["A.applied"], 1000)


if __name__ == "__main__":
    unittest.main()
