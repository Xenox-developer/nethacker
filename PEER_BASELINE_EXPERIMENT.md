# Pinned peer generalization baseline

Request: `20260928T024027587450Z-432074eedaca447e949a88d40490e3ef`.

# hypothesis: the complete pinned peer policy may transfer differently from the actual incoming champion; benchmark its unchanged runtime without tuning or combining policies.

## Identity, provenance, and licensing

Verified `/refs/peers/SOURCES.md` maps peer1 to `github.com/daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b`. No moving branch was used. The candidate contains all 50 runtime/license files from that reference byte-for-byte, including its adapter, entrypoint, strategy defaults, and complete MIT license: Copyright © 2022 Maciej Sypetkowski, Michał Sypetkowski. Existing runtime attribution is preserved.

`PEER_BASELINE_ASSETS/runtime-hashes.json` records each pinned and candidate SHA-256. The incoming policy is different (18 candidate paths differ or are absent in incoming). `incoming-hashes.json` and `incoming-runtime.tar.gz` preserve the actual incoming runtime before replacement. The incoming champion is solely the comparison parent, not a claimed source author. `/refs/parent` remains untouched.

The sole packaging change is `nethackers.solution.json`: direct parent is now the exact requested pin, and existing upstream parents/influences are retained as influences. Original metadata is preserved as `pinned-solution.json`. Experiment evidence stays outside `autoascend/`. No Git metadata, AGENTS.md, credentials, or source caches were copied. No behavioral diagnostics were added. The hypothesis comment lives in this report to preserve runtime identity.

## Protocol

Both arms passed isolated entrypoint import, construction, reset/act callable checks and close before games (`compatibility.log`). Actual reset/action compatibility is also exercised by the native episodes. Runs use the installed native `python -m nethackers.arena.run` in this supplied environment; no evaluator modifications, alternate evaluator, or policy access to evaluation internals/seed data. An independent container image digest is not exposed in the supplied evidence.

Each batch is one foreground native command, awaited to completion. All batches are sequential. Public15 uses trajectories 0–14; additional development panel uses exactly 3000–3007 for each arm. Every batch uses val-dwa-law-fem, evaluation-id local, native public-secret default, max_steps=1000000, no_progress_timeout=10000, action_timeout=120, max_parallel_evals=4. Exact batch plan is in `experiment-plan.json`. Standard output and error logs and all raw output rows are retained in `PEER_BASELINE_ASSETS`.

## Interpretation limits

The supplied parent Public15 mean is 0.49585056253228327. The request's historical champion20 Public0.47506047628647746 and Private0.22437158128169327 are external aggregates, not this actual incoming run. The cited peer program prog_f362a746154d95ec970ee492174a1fd8 had published Public0.4269430291497873 and organizer Private0.4029787867320985 at the supplied timestamp; these are reported context, not locally reproduced or promised scores. Attempt19's cited Private0.30553778869019693 is likewise external context.

The additional panel is eight development trajectories, not organizer Private, not the fresh native promotion gate, and not an estimate guaranteed to generalize. No favorable subset selection, tuning, death rerolls, or manual Private promotion is allowed. Publication and local champion selection are separate. Final outer native Public and future organizer Private require their own evidence and are not inferred here.

## Completed measured results

| Native local batch | Rows | Mean progress | Errors |
|---|---:|---:|---:|
| incoming-public15 | 15 | 0.4809840847749231 | 0 |
| candidate-public15 | 15 | 0.4283560229465442 | 0 |
| incoming-panel | 8 | 0.2819553536430530 | 0 |
| candidate-panel | 8 | 0.3852968977178186 | 0 |

public15: candidate minus incoming = -0.0526280618283789; wins/ties/losses = 4/5/6.

panel: candidate minus incoming = +0.1033415440747656; wins/ties/losses = 5/0/3.

All 46 episodes returned completed status, with no reported errors. Completed does not mean victory; deaths are retained. No technical retries, death rerolls, or post-result policy edits occurred. Both source trees passed post-evaluation SHA-256 verification.

### Public15 paired scores

| Trajectory | Supplied parent | Fresh incoming | Pinned peer |
|---|---:|---:|---:|
| 0 | 0.466376315653 | 0.466376315653 | 0.466376315653 |
| 1 | 0.646504941599 | 0.378956679233 | 0.161267782277 |
| 2 | 0.050758371235 | 0.050758371235 | 0.445181408702 |
| 3 | 0.554357204487 | 0.506760563380 | 0.554357204487 |
| 4 | 0.554357204487 | 0.554357204487 | 0.036887590648 |
| 5 | 0.554357204487 | 0.646504941599 | 0.601564851038 |
| 6 | 0.554357204487 | 0.554357204487 | 0.466376315653 |
| 7 | 0.646504941599 | 0.646504941599 | 0.466376315653 |
| 8 | 0.601564851038 | 0.601564851038 | 0.050758371235 |
| 9 | 0.554357204487 | 0.554357204487 | 0.554357204487 |
| 10 | 0.601564851038 | 0.601564851038 | 0.601564851038 |
| 11 | 0.466376315653 | 0.466376315653 | 0.466376315653 |
| 12 | 0.425836074886 | 0.425836074886 | 0.554357204487 |
| 13 | 0.206128548363 | 0.206128548363 | 0.445181408702 |
| 14 | 0.554357204487 | 0.554357204487 | 0.554357204487 |

Fresh incoming runtime exactly matches pristine `/refs/parent`, but scores differ from supplied rows on trajectories 1, 3, and 5. The observed variation is not diagnosed by this identity-only benchmark. The fresh incoming mean is used for the paired comparison; supplied rows remain preserved separately. Peer mean is also below the supplied parent mean by -0.06749453958573914.

### All 16 additional-panel rows

| Arm | Trajectory | Progress | Status | Steps | Turns | Max depth | Milestone | Cause of death | Error |
|---|---:|---:|---|---:|---:|---:|---|---|---|
| incoming | 3000 | 0.5067605633802816 | completed | 24296 | 20339 | 26 | Dlvl:26 | killed by a xorn | None |
| incoming | 3001 | 0.5067605633802816 | completed | 25096 | 16059 | 26 | Dlvl:26 | killed by a cobra | None |
| incoming | 3002 | 0.5543572044866264 | completed | 28904 | 18244 | 27 | Dlvl:27 | killed by a wand | None |
| incoming | 3003 | 0.0745359527388401 | completed | 26910 | 19915 | 5 | Xp:8 | killed by a black unicorn | None |
| incoming | 3004 | 0.4663763156530306 | completed | 54057 | 19033 | 25 | Dlvl:25 | killed by a raven | None |
| incoming | 3005 | 0.0354286861181730 | completed | 3875 | 3616 | 6 | Dlvl:6 | killed by a jackal | None |
| incoming | 3006 | 0.0745359527388401 | completed | 27238 | 20895 | 3 | Xp:8 | killed by a gray unicorn | None |
| incoming | 3007 | 0.0368875906483502 | completed | 49948 | 46690 | 4 | Xp:6 | killed by a rothe | None |
| candidate | 3000 | 0.1170499647356557 | completed | 48001 | 23624 | 3 | Xp:9 | killed by a soldier ant | None |
| candidate | 3001 | 0.5543572044866264 | completed | 11515 | 9280 | 27 | Dlvl:27 | killed by a minotaur | None |
| candidate | 3002 | 0.5067605633802816 | completed | 12647 | 10740 | 26 | Dlvl:26 | killed by a captain | None |
| candidate | 3003 | 0.4663763156530306 | completed | 16400 | 10852 | 25 | Dlvl:25 | killed by a shark | None |
| candidate | 3004 | 0.5543572044866264 | completed | 13982 | 11671 | 27 | Dlvl:27 | killed by a minotaur | None |
| candidate | 3005 | 0.4663763156530306 | completed | 16115 | 10641 | 25 | Dlvl:25 | killed by a gremlin | None |
| candidate | 3006 | 0.3929374767967505 | completed | 17449 | 11751 | 21 | Dlvl:21 | killed by a frost giant | None |
| candidate | 3007 | 0.0241601365505470 | completed | 9604 | 11345 | 1 | Xp:4 | killed by a bolt of lightning | None |

Raw JSON retains all additional fields, including wall times and end status; unfiltered stdout/stderr is in the four corresponding `.log` files. Commands are recorded in `commands.json`.

## Gate and handoff

The exact peer fails the strict Public improvement gate against both fresh incoming and supplied parent. Fresh promotion validation is therefore not triggered; no local champion promotion is claimed or performed. The saved incoming runtime remains intact. The complete pinned candidate is nevertheless left in `/workspace` for normal outer scoring/publication, as explicitly requested. No final outer score or publication result is available inside this experiment; future organizer Private remains unmeasured here. The additional panel cannot override this gate.
