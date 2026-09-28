# Complete peer strategy replacement

One hypothesis: the coordinated survival, tool-search, and descent policy from the pinned peer improves progression as a complete package.

Source: `github.com/vkurenkov/nethacker@f15bb8c8e01d905d1946e32bfd2558e17394eab6`. All peer Python files were copied unchanged before evaluation; the only subsequent code edit is the hypothesis/provenance comment in `autoascend/__init__.py`. The existing identical MIT license is preserved. Source attribution is recorded in `nethackers.solution.json`. `bot.py` and `arena_adapter.py` are unchanged.

Validation used `python -m nethackers.arena.run --solution /workspace --batch ... --evaluation-id local --out ...`, in three foreground batches: `[0,1,2,8,11,13]`, `[3,4,5,6,7]`, and `[9,10,12,14]`, all as `val-dwa-law-fem`.

Parent mean: **0.480984085**. Candidate mean: **0.505439822**. Improvement: **0.024455737** (+5.08%). Five gains, five losses, five ties; no evaluation errors. These are training results, not evidence of performance on unseen seeds.

| Seed | Parent | Candidate |
| --- | ---: | ---: |
| 0 | 0.466376 | 0.466376 |
| 1 | 0.378957 | 0.161268 |
| 2 | 0.050758 | 0.445181 |
| 3 | 0.506761 | 0.554357 |
| 4 | 0.554357 | 0.554357 |
| 5 | 0.646505 | 0.601565 |
| 6 | 0.554357 | 0.466376 |
| 7 | 0.646505 | 0.466376 |
| 8 | 0.601565 | 0.554357 |
| 9 | 0.554357 | 0.554357 |
| 10 | 0.601565 | 0.601565 |
| 11 | 0.466376 | 0.601565 |
| 12 | 0.425836 | 0.554357 |
| 13 | 0.206129 | 0.445181 |
| 14 | 0.554357 | 0.554357 |

Full candidate results: `evaluation/peer2-local.json`. Parent references: `/refs/parent-eval.json`. Same-session unmodified-parent diagnostic runs on seeds 2 and 11 reproduced the supplied scores and turns (`evaluation/trace-parent-eval.json`). Compilation and all 15 gameplay runs passed.

Before the complete-policy test, three isolated screens were tried and fully reverted: longer Medusa dig routing (0/3/8/11), stair-arrival bookkeeping (1/2/8/13), and one emergency attempt per unknown wand (1/2/11/13). Each screen matched every sampled parent score and turn count. Their result files are retained in `evaluation/`; none of those patches is layered onto the peer baseline.
