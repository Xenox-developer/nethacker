# Fixed-baseline strategy campaign helper

These helpers are development tools for the **next official mutator container**.
They do not run a host arena, publish, change the local champion, or edit a worker.
No games were run while preparing them. `test_campaign.py` uses fake result rows.

Prepare an immutable baseline in `/tmp/campaign-baseline`, with all three
strategy implementations, all strategy flags off, and the same diagnostic
hooks as every variant. Prepare A/B/C and later eligible combinations as
separate sibling `/tmp` trees from that baseline. Never nest copies of full
bots inside `/workspace`, and never modify a baseline after evaluation begins.
The active request's brief defines A/B/C; the helper does not invent strategies.

From the directory containing these helper files, evaluate the fresh baseline:

```bash
python campaign.py evaluate --label baseline \
  --solution /tmp/campaign-baseline --baseline /tmp/campaign-baseline \
  --out /workspace/STRATEGY_CAMPAIGN
```

Then run each single **sequentially**, in the foreground:

```bash
python campaign.py evaluate --label A --members A \
  --solution /tmp/campaign-A --baseline /tmp/campaign-baseline \
  --out /workspace/STRATEGY_CAMPAIGN
```

Repeat for B and C, then obtain required combinations:

```bash
python campaign.py report --out /workspace/STRATEGY_CAMPAIGN --singles A B C
```

Each variant receives exactly 15 Public games (0–14) and five shared additional
development games (2000–2004), using explicit `public` / `local` seed derivation,
1,000,000 steps, 10,000 no-progress limit, 120-second action timeout, and four
parallel episodes **inside one arena invocation**. Complete each invocation
before starting the next. These five development games are used for selection;
they are not holdout or organizer Private evidence. The native unseen local
promotion gate still follows after the mutator returns its final tree.

Evaluate every required eligible combination. For example:

```bash
python campaign.py evaluate --label A+B --members A B \
  --solution /tmp/campaign-AB --baseline /tmp/campaign-baseline \
  --out /workspace/STRATEGY_CAMPAIGN
```

A single is eligible only with a strict Public improvement, nonregressing
additional-development mean, and no errors. With three eligible singles all
three pairs and the triple are required. A combination is recommended only
after every required combination completes, beats the strongest eligible
single's Public mean, and does not regress its development mean. The report
includes all paired per-seed deltas and disqualifying statuses. If no single
qualifies, `recommended` is `baseline`; `best_tested_single` separately identifies
the highest-scoring error-free tested single for the brief's explicit negative
experiment fallback. Never describe that fallback as an improvement.
`final_publication_candidate` explicitly names that final tested mutation: the
eligible recommendation when one exists, otherwise the best error-free single
as a negative/mixed experiment. It is null while required combinations are
missing or all singles contain errors; it never selects the semantic baseline
as a new candidate. Score ties prefer higher development score, then the lower
alphabetical label. This helper's selection never overrides the native Public
scoring and fresh-three-game promotion gate.

Evidence is atomic under `STRATEGY_CAMPAIGN/variants/<label>/`: full result rows,
fixed configuration, exact sanitized snapshot digest/file hashes, baseline-relative
patch, and logs. Existing labels cannot be overwritten. One identical retry is
allowed only after a technical/infrastructure failure; its original rows/logs
remain separate. Deaths, low scores, and bot errors are never retry reasons.
A nonblocking lock covering the whole evaluation refuses a second simultaneous
`evaluate` command using this same campaign output directory.
The helper makes a temporary sanitized runtime copy, preserves required source
files, rejects symlinks, and checks that its source bytes remain unchanged.
It excludes `.git`, build caches, `EXPERIMENT_ASSETS` and `STRATEGY_CAMPAIGN` from
runtime snapshots; recorded digests describe these sanitized snapshots, not
the final native published tree containing development documentation.

Copy `campaign_events.py` into the common baseline root and import it in each
strategy module. Record `hit('A.considered')` at the common gate and
`hit('A.applied')` **only when A actually changes behavior**. Equivalent hooks
must exist in the baseline and all variants. These counters must never influence
action choice, RNG calls, target ordering, or thresholds. They are disabled
outside helper runs because the native arena does not set their output variable.
Counters checkpoint at powers of two with bounded I/O; persisted counts are
honest lower bounds unless an explicit normal-shutdown `flush(exact=True)` ran.
Do not claim exact counts, seed attribution, or behavior activation from an
absent counter. The report separates selected evaluation attempts from earlier
technical failures. The built-in arena does not export AutoAscend StatsLogger.

The native mutator has an eight-hour ceiling, 4 CPUs and 8 GiB. Baseline plus
three singles costs 80 games; all four combinations make 160 before technical
retries and final native scoring. Run each helper command in the foreground
with sufficient command timeout; never background a batch or silently omit
unfavorable seeds. Install only the brief's selected final behavior into
`/workspace`; retain compact evidence there, not full candidate-tree copies.

Local helper validation, with no games:

```bash
python -m unittest discover -s . -p test_campaign.py
```
