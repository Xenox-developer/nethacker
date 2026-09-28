# Corrections before B/C evaluation

After baseline completion and while A was running, a source-boundary review found:
- B initially set failed-location cooldown to entry time +100. It now refreshes to exit time +100 in finally, so a failed multi-turn attempt receives the full specified suppression period.
- C initially ignored same-turn observations entirely. It now retains the latest same-turn observation without creating/extending evidence, preventing an ignored same-turn HP reduction from being misattributed to the next turn.

Neither B nor C had started games. These are contract corrections, not changed hypotheses, thresholds, seed lists, or score-driven replacements. Baseline and A remain immutable; original and corrected B/C pre-evaluation manifests are retained. The common inactive scaffold in baseline/A retains the original dormant implementations; each evaluated singleton patch captures its exact active implementation. Qualified-loss diagnostic counts from the original dormant observer are not strictly equivalent to C's corrected observer; do not use their difference as a causal activation estimate.
