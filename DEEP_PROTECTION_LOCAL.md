# Preemptive deep-dive protection

One change: at dungeon depth >=20, allow the existing pre-dig Elbereth helper even without a visible nearby enemy. Existing blindness retry caps and all other guards remain unchanged. No peer code copied; mechanism reviewed against peer2's pinned pre-dig helper and the prior experiment history.

Eight seeds (0,1,2,3,7,8,11,13), val-dwa-law-fem, evaluated in two foreground batches with evaluation-id local. Supplied parent mean 0.461832811; candidate 0.470383131. Two gains, six ties, zero errors. Seed 8: depth 27 ->28; seed 13: 24 ->25. This is a sampled training result, not a new full-15 score or held-out estimate.

Compilation and bot.make_agent construction passed; reset/act exercised by arena runs. Raw results: evaluation/deep-protection-local.json.

Earlier screens were fully reverted: XL5 tool run regressed seeds 0/1/2/8; damage-triggered blind retries tied seeds 2/5/7/13. Neither is included in the final strategy.
