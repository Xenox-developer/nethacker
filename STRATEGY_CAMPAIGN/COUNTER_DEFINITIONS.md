# Diagnostic interpretation

All counts are aggregate process counters across the selected attempts. Persisted counts are lower bounds because checkpointing is bounded; no seed attribution is inferred from process IDs. Counters are enabled only by the helper's events-output environment variable. No seed, score or evaluator state enters gameplay decisions. Samples are capped at64/process, counter names at64/process and counter checkpoints at512/process. No exact shutdown flush is claimed.

| Counter | Meaning |
|---|---|
| A.evaluations | Ray projections, including actual and diagnostic opposite-calculation projections. |
| A.branch_nodes | Nodes with multiple geometric successor states, in both calculation modes. Not a count of turns or actions. |
| A.branching_evaluations | Projections containing at least one such branch, in both calculation modes. |
| A.score_changed | Direction evaluations whose wand-score/candidate maps differ between modes. This is not action activation. |
| A.chosen_action_changed | The actual root choice differs from the opposite-calculation root choice after the existing candidate filters. Action identity compares wand/direction, not merely newly allocated tuple identity. |
| B.considered | Calls to the ordinary buy_food strategy, including checks that fail its original gates. |
| B.eligible | Tool-carrier local-shopping preliminary gate passed: stock, hunger, location, threat and status. An affordable reachable ration need not exist yet. |
| B.started | Execution entered the reserve transaction after yielding an eligible strategy. |
| B.purchased | Carried estimated food nutrition increased after settlement, with no remaining unpaid inventory. |
| B.unknown_buc | Selected ration's beatitude was unknown at pickup. |
| B.settlement | Unpaid goods were present at the post-pickup settlement check. |
| B.settlement_overrun | Pickup/settlement completed after elapsed8; settlement was not abandoned. |
| B.bail.* | The checked gate failed. Reasons: location, threat, stock_hunger, status, timeout, cooldown, no_local_affordable_ration, path_or_price_changed. The combined no-local-food reason does not distinguish absent stock from rejected price/curse/path. |
| C.observations | Dive update calls, including repeated same-turn observations. These are not all distinct game turns. |
| C.qualified_loss | Two valid consecutive distinct-turn observations establish observed HP loss on the same intact engraving. This is collected even when C's bypass flag is off. |
| C.suppression_considered | The original LR_ELBERETH suppression predicate was satisfied. |
| C.exception_activated | C bypassed that suppression during a strategy eligibility check. Repeated checks need not take actions. |
| C.action.* | An ensuing last-resort action actually executed after yielding true: dig, stairs_down, stairs_up, prayer, wand, potion or scroll. |

Bounded `food_transaction` samples contain observed target/price/path distance, estimated stock before/after, elapsed game turns, purchase status and remaining debt. They are samples, not full transaction totals. `wand_scores` and `wand_action` samples separate score effects from root-choice effects. `protection_loss` samples contain the observed location/turn and successive HP values without an attacker claim.

An absent activation counter establishes no recorded activation, not universal uselessness. If no reserve transaction is recorded, food stock/elapsed-turn transaction measurements have no gameplay coverage; fixture transactions are not counted as games. Endpoint score variation without a recorded relevant action change has no direct causal attribution to the proposed mechanism. Control repeats and native validation remain necessary.
