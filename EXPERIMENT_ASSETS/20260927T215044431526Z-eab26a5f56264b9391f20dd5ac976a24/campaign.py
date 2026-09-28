"""Sequential, fixed-baseline development campaign inside the native mutator.

This never publishes or promotes. Outer native evolve does both afterward.
All variants use Public0..14 + additional DEVELOPMENT2000..2004, not holdout.
The CLI refuses game execution outside Docker; report needs only the stdlib.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import fcntl
import hashlib
import itertools
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

IDENTITY = "val-dwa-law-fem"
BATCHES = {"public": list(range(15)), "development": list(range(2000, 2005))}
CONFIG = {"identity": IDENTITY, "secret": "public", "evaluation_id": "local",
          "max_steps": 1_000_000, "no_progress_timeout": 10_000,
          "action_timeout": 120.0, "max_parallel_evals": 4,
          "batches": BATCHES, "development_is_holdout": False}
IGNORED = {".git", "__pycache__", ".pytest_cache", "EXPERIMENT_ASSETS",
           "STRATEGY_CAMPAIGN"}


def atomic_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True))
    os.replace(temporary, path)


def files(tree):
    tree = Path(tree)
    result = {}
    for path in sorted(tree.rglob("*")):
        relative = path.relative_to(tree)
        if any(part in IGNORED for part in relative.parts):
            continue
        if path.suffix in {".pyc", ".nbi", ".nbc"}:
            continue
        if path.is_symlink():
            raise ValueError(f"Snapshot contains a symlink: {relative}")
        if path.is_file():
            result[relative.as_posix()] = path.read_bytes()
    if "bot.py" not in result:
        raise ValueError("Snapshot has no bot.py")
    return result


def manifest(contents):
    # Same sorted path+content hashing as native eval.runner._solution_digest;
    # applies to the sanitized snapshot actually evaluated, never the input tree.
    digest = hashlib.sha256()
    for name, content in sorted(contents.items()):
        digest.update(name.encode())
        digest.update(content)
    return {"digest": "sha256:" + digest.hexdigest(), "files": {
        name: hashlib.sha256(content).hexdigest() for name, content in contents.items()}}


def patch(base, candidate):
    chunks = []
    for name in sorted(base.keys() | candidate.keys()):
        if base.get(name) == candidate.get(name):
            continue
        try:
            old = base.get(name, b"").decode().splitlines(keepends=True)
            new = candidate.get(name, b"").decode().splitlines(keepends=True)
        except UnicodeDecodeError as exc:
            raise ValueError(f"Binary change cannot be preserved as a patch: {name}") from exc
        chunks.extend(difflib.unified_diff(old, new, fromfile=f"a/{name}", tofile=f"b/{name}"))
    return "".join(chunks)


def validate_rows(rows, seeds):
    if not isinstance(rows, list) or len(rows) != len(seeds):
        raise ValueError("Missing or extra game rows")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or row.get("character") != IDENTITY:
            raise ValueError("Wrong identity or malformed row")
        seed = row.get("trajectory_id")
        if type(seed) is not int or seed not in seeds or seed in seen:
            raise ValueError("Wrong or duplicate trajectory")
        seen.add(seed)
        score = row.get("progress")
        if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("Invalid progression score")
    return sorted(rows, key=lambda row: row["trajectory_id"])


def arena_command(solution, seeds, output):
    return [sys.executable, "-m", "nethackers.arena.run", "--solution", str(solution),
            "--batch", json.dumps([[seed, IDENTITY] for seed in seeds]),
            "--secret", "public", "--evaluation-id", "local", "--max-steps", "1000000",
            "--no-progress-timeout", "10000", "--action-timeout", "120",
            "--max-parallel-evals", "4", "--out", str(output)]


def evaluate(label, members, solution, baseline, out, *, runner=subprocess.run):
    solution, baseline = Path(solution).resolve(), Path(baseline).resolve()
    out = Path(out).resolve()
    if solution == out or solution in out.parents or baseline == out or baseline in out.parents:
        raise ValueError("Evidence output must be outside both solution snapshots")
    out.mkdir(parents=True, exist_ok=True)
    with (out / ".campaign.lock").open("a") as guard:
        try:
            fcntl.flock(guard.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another evaluation already owns this campaign") from exc
        return _evaluate(label, members, solution, baseline, out, runner=runner)


def _evaluate(label, members, solution, baseline, out, *, runner):
    members = sorted(members)
    expected_label = "+".join(members) if members else "baseline"
    if label != expected_label or len(set(members)) != len(members):
        raise ValueError("Use canonical labels: baseline, A, A+B, A+B+C")
    if any(not name.isalnum() for name in members):
        raise ValueError("Strategy names must be alphanumeric")
    solution = Path(solution).resolve()
    baseline, out = Path(baseline).resolve(), Path(out).resolve()
    if solution == out or solution in out.parents or baseline == out or baseline in out.parents:
        raise ValueError("Evidence output must be outside both solution snapshots")
    base_files, candidate_files = files(baseline), files(solution)
    baseline_manifest, candidate_manifest = manifest(base_files), manifest(candidate_files)
    if not members and baseline_manifest != candidate_manifest:
        raise ValueError("Baseline label must evaluate the fixed baseline itself")
    if members and baseline_manifest == candidate_manifest:
        raise ValueError("A strategy variant must differ from the fixed baseline")
    variant = out / "variants" / label
    variant.mkdir(parents=True, exist_ok=False)  # Never overwrite/reselect a completed variant.
    (variant / "change.patch").write_text(patch(base_files, candidate_files))
    atomic_json(variant / "files.json", candidate_manifest)
    record = {"schema": 1, "label": label, "members": members, "config": CONFIG,
              "baseline_digest": baseline_manifest["digest"],
              "solution_digest": candidate_manifest["digest"],
              "created_at": dt.datetime.now(dt.UTC).isoformat(), "phases": {},
              "complete": False}
    atomic_json(variant / "evaluation.json", record)
    # Native arena imports can create caches; isolate them from source identity.
    # The exact sanitized runtime snapshot is disposable; patches+hashes persist.
    with tempfile.TemporaryDirectory(prefix="strategy-campaign-") as temporary:
        snapshot = Path(temporary) / "solution"
        snapshot.mkdir()
        for name, content in candidate_files.items():
            target = snapshot / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        for phase, seeds in BATCHES.items():
            attempts = record["phases"][phase] = []
            for retry in range(2):
                output = variant / f"{phase}-{retry}.json"
                events = variant / f"{phase}-{retry}-events"
                events.mkdir()
                environment = dict(os.environ)
                environment.pop("NETHACK_ARENA_SECRET", None)
                environment.update(PYTHONDONTWRITEBYTECODE="1",
                                   NETHACKERS_CAMPAIGN_EVENTS_DIR=str(events))
                item = {"attempt": retry, "results_file": output.name,
                        "events_directory": events.name}
                attempts.append(item)
                try:
                    with (variant / f"{phase}-{retry}.log").open("w") as log:
                        runner(arena_command(snapshot, seeds, output), check=True,
                               timeout=1200, stdout=log, stderr=log, env=environment)
                    rows = validate_rows(json.loads(output.read_text()), seeds)
                    item["results"] = rows
                    item["technical_failure"] = any(
                        row.get("status") == "infrastructure_error" for row in rows)
                except (subprocess.SubprocessError, OSError, ValueError) as exc:
                    item.update(technical_failure=True, failure=f"{type(exc).__name__}: {exc}")
                atomic_json(variant / "evaluation.json", record)
                if not item["technical_failure"]:
                    break  # Deaths and bot failures are outcomes, never retry reasons.
            if attempts[-1]["technical_failure"]:
                raise RuntimeError(
                    f"{label}/{phase}: technical retry exhausted; evidence preserved")
        after = manifest(files(snapshot))
        if after != candidate_manifest:
            raise RuntimeError("Source snapshot changed during evaluation; refuse comparison")
    record["complete"] = True
    atomic_json(variant / "evaluation.json", record)
    return record


def selected_rows(record, phase):
    if not record.get("complete") or record.get("config") != CONFIG:
        raise ValueError("Incomplete variant or mismatched campaign configuration")
    attempts = record["phases"][phase]
    if not 1 <= len(attempts) <= 2:
        raise ValueError("Wrong number of technical attempts")
    if len(attempts) == 2 and not attempts[0].get("technical_failure"):
        raise ValueError("Nontechnical reroll is not allowed")
    if attempts[-1].get("technical_failure"):
        raise ValueError("Unresolved technical failure")
    return validate_rows(attempts[-1]["results"], BATCHES[phase])


def means(record):
    return {phase: sum(row["progress"] for row in selected_rows(record, phase)) / len(seeds)
            for phase, seeds in BATCHES.items()}


def clean(record):
    return all(row.get("status") == "completed" and row.get("error") is None
               for phase in BATCHES for row in selected_rows(record, phase))


def comparison(base, candidate):
    result = {"means": means(candidate), "clean": clean(candidate), "paired": {}}
    for phase in BATCHES:
        old, new = selected_rows(base, phase), selected_rows(candidate, phase)
        pairs = [{"seed": a["trajectory_id"], "old": a["progress"], "new": b["progress"],
                  "delta": b["progress"] - a["progress"],
                  "old_status": a["status"], "new_status": b["status"]}
                 for a, b in zip(old, new, strict=True)]
        result["paired"][phase] = pairs
        result[f"{phase}_delta"] = sum(row["delta"] for row in pairs) / len(pairs)
    return result


def activation_summary(variant, record):
    selected, attempts = {}, {}
    for phase in BATCHES:
        for index, attempt in enumerate(record["phases"][phase]):
            counts = {}
            directory = attempt.get("events_directory")
            if directory:
                for path in sorted((Path(variant) / directory).glob("events-*.json")):
                    data = json.loads(path.read_text())
                    for name, count in data["counts"].items():
                        counts[name] = counts.get(name, 0) + count
            attempts[f"{phase}-{index}"] = counts
            if index == len(record["phases"][phase]) - 1:
                for name, count in counts.items():
                    selected[name] = selected.get(name, 0) + count
    return {"selected_attempt_counts": selected, "all_attempts": attempts,
            "counts_are_lower_bounds": True, "per_game_attribution": False}


def report(out, singles):
    out = Path(out)
    singles = sorted(singles)
    if len(singles) != 3 or len(set(singles)) != 3:
        raise ValueError("Exactly three distinct single strategies are required")
    records = {}
    for path in sorted((out / "variants").glob("*/evaluation.json")):
        record = json.loads(path.read_text())
        if record["label"] != path.parent.name:
            raise ValueError("Variant label/path mismatch")
        members = record["members"]
        expected = "+".join(sorted(members)) if members else "baseline"
        if record["label"] != expected or len(set(members)) != len(members):
            raise ValueError("Variant membership mismatch")
        records[record["label"]] = record
    if any(label not in records for label in ["baseline", *singles]):
        raise ValueError("Fresh baseline20 and all three complete singles20 are required")
    base = records["baseline"]
    base_means = means(base)
    if not clean(base):
        raise ValueError("Baseline contains errors; no comparison is valid")
    if any(record["baseline_digest"] != base["solution_digest"] for record in records.values()):
        raise ValueError("Variants do not share one fixed baseline")
    comparisons = {label: comparison(base, record) for label, record in records.items()}
    eligible = [label for label in singles if comparisons[label]["clean"]
                and comparisons[label]["means"]["public"] > base_means["public"]
                and comparisons[label]["means"]["development"] >= base_means["development"]]
    required = ["+".join(group) for size in range(2, len(eligible) + 1)
                for group in itertools.combinations(eligible, size)]
    missing = [label for label in required if label not in records]
    def rank(label):
        return (-comparisons[label]["means"]["public"],
                -comparisons[label]["means"]["development"], label)

    best = min(eligible, key=rank, default="baseline")
    best_single = best
    best_tested = min((label for label in singles if comparisons[label]["clean"]),
                     key=rank, default=None)
    if not missing:
        # Every eligible combination must be measured; a lucky early pair is
        # never selected before the other required combinations finish.
        for label in required:
            value, strongest = comparisons[label], comparisons[best_single]
            if (value["clean"] and value["means"]["public"] > strongest["means"]["public"]
                    and value["means"]["development"] >= strongest["means"]["development"]
                    and rank(label) < rank(best)):
                best = label
    final_candidate = None if missing else (best if best != "baseline" else best_tested)
    return {"config": CONFIG, "baseline_digest": base["solution_digest"],
            "eligible_singles": eligible, "required_combinations": required,
            "missing_combinations": missing, "complete": not missing,
            "best_single": best_single, "selected": best if not missing else None,
            "recommended": best if not missing else None, "best_tested_single": best_tested,
            "final_publication_candidate": final_candidate,
            "comparisons": comparisons, "activation": {
                label: activation_summary(out / "variants" / label, record)
                for label, record in records.items()},
            "warning": "Development selection only; native Public/gate/publication still required."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    evaluation = commands.add_parser("evaluate")
    evaluation.add_argument("--label", required=True)
    evaluation.add_argument("--members", nargs="*", default=[])
    evaluation.add_argument("--solution", required=True, type=Path)
    evaluation.add_argument("--baseline", required=True, type=Path)
    evaluation.add_argument("--out", required=True, type=Path)
    summary = commands.add_parser("report")
    summary.add_argument("--out", required=True, type=Path)
    summary.add_argument("--singles", nargs=3, required=True)
    args = parser.parse_args()
    if args.command == "evaluate":
        if not Path("/.dockerenv").exists():
            parser.error("Game execution is only allowed inside the native mutator container")
        evaluate(args.label, args.members, args.solution, args.baseline, args.out)
    else:
        result = report(args.out, args.singles)
        atomic_json(args.out / "report.json", result)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
