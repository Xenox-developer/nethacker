# Short emergency engraving

Hypothesis: when blind and beside a hostile, writing one Elbereth finishes sooner than the redundant two-word inscription, reducing exposure while writing. Keep the redundant inscription when no hostile is adjacent. The only strategy change is in `autoascend/agent.py`; the adapter and agent contract are unchanged.

The parent seed-2 trace showed multiple raven attacks followed by “You finish writing in the dust” during the two-word inscription. Peer inspection included the pinned peer1 deep escape implementation and peer3 engraving implementation; this change uses existing local engraving code, without copying new peer code.

Validation used `python -m nethackers.arena.run --solution /workspace --batch ... --evaluation-id local --out ...`, with foreground batches [1,2,7,13], [0,3,4,5,6,8], and [9,10,11,12,14]. All 15 completed without evaluation errors. Full per-seed results are in `short-engraving-eval.json`.

Mean progression: parent **0.484696468**, candidate **0.500987423**, change **+0.016290955**. Three gains, twelve ties, zero losses against `/refs/parent-eval.json`:

| Seed | Parent depth | Candidate depth |
| --- | --- | --- |
| 2 | 24 | 25 |
| 6 | 25 | 27 |
| 11 | 25 | 28 |

Compilation and make_agent/reset/act import checks passed. These results cover the supplied training seeds, not unseen games. A diagnostic parent rerun of seeds 1 and 2 reproduced their reference results.

An earlier sleep-wand candidate tied all eight tested seed scores (0,1,2,4,8,9,12,14) and was completely reverted before this change. Temporary engraving diagnostics were also removed.
