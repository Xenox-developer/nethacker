# Target-size melee weapon selection

Hypothesis: choosing a melee weapon using the target's size improves damage
against large monsters. The parent always evaluates small-monster damage.

The melee action now reads the visible target's size and passes it through to
the existing weapon evaluator. Other callers retain small-monster evaluation;
existing curse and identification restrictions remain in place. No adapter or
entrypoint changes were made.

Reviewed pinned peer3 (`kefirski/nethacker@454ae8df96e7ec68f0df2488b2b8a90368407cf1`,
MIT) and peer1's dag engine. Their shared combat architecture helped identify
the unconditional small-monster weapon evaluation. This change is an original
modification; those peer sources are already recorded in the solution manifest.

Validation used the arena command with `--evaluation-id local`, identity
`val-dwa-law-fem`, and sequential foreground batches 0–3, 4–7, 8–11, 12–14.
Combined per-seed output is in `target-size-eval.json`.

| Result | Parent | Candidate |
| --- | ---: | ---: |
| Mean over all 15 seeds | 0.4905359272 | 0.4995744292 |
| Seed 3 deepest level | 26 | 27 |
| Seed 6 deepest level | 25 | 27 |

Two score gains, 13 ties, zero regressions, zero bot errors. This is training-set
evidence, not a held-out estimate. Imports and compilation passed. A direct
check using real weapon damage tables selected a broadsword for small targets
and a long sword for large targets, and still excluded a cursed long sword.

Discarded probes, fully reverted before this candidate: minotaur wand priority
(eight score ties), monster-speed classification (one loss among four seeds),
and Quest exploration with a pick (one loss among three completed games; one
startup failure from a truncated bytecode cache). Caches were rebuilt before
the final candidate's runs.
