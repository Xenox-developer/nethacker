# Dive rescue prayer model

One mechanism: estimate prayer cooldown success, divine anger and immediate combat danger to time rescue prayers during the dive. Observe the whole game to maintain prayer history; retain the parent decision policy during the leveling tour. Existing fallback rules remain available if the model raises repeated errors.

Source: github.com/kefirski/nethacker@454ae8df96e7ec68f0df2488b2b8a90368407cf1, peer3 agent prayer integration and autoascend/nhmodel. MIT license preserved at autoascend/nhmodel/LICENSE; source recorded in the solution manifest. No other peer policies were copied. The parent's engraving behavior is preserved.

## Evaluation

Final variant evaluated on all training seeds 0–14 as val-dwa-law-fem, using evaluation-id local, in foreground batches [4,6,8,14], [2,5,7,12], [0,1,3,9], [10,11,13]. Results: evaluation/prayer-model-local.json.

Stored parent mean: 0.4861094614. Candidate mean: 0.4919489210. One gain (11, depth 25 to 28), one loss (14, depth 27 to 26), thirteen score ties. All fifteen completed without arena errors.

This is an observed +0.0058394596, not a confirmed causal gain. An unchanged-parent control on [3,7,11,13] also reached depth 28 on seed 11. The supplied experiment history likewise reports variation between unchanged runs. Do not attribute the entire aggregate improvement to the model.

Probability bounds/monotonicity, critical-HP boundaries, imminent-death rescue versus low-risk waiting, divine-anger rejection, tour fallback, imports and make_agent/reset/act interface were checked. No adapter changes.

## Discarded candidates in this session

Engulfed weapon switching, flood-exit guarding, combat teleportation, point-blank throwing, boot retention, crossing-item retention, independent eel response, beam dodging and self-ricochet rejection did not demonstrate a reliable improvement in their samples and were reverted. The unrestricted peer prayer model caused an early regression; the final variant applies model decisions only during the dive. Only the dive prayer model remains in strategy code.
