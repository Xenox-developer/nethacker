# Resource and routing research for the fixed-baseline campaign

Prepared 28 September 2026 from champion 20, digest `39c189656f92b62e57ea28399e2e8794c9446afe3f6dc21fec0afdf5002836aa`, and experiment notes through 20. This is a research specification, not an implemented or evaluated improvement. Only this note was written; no games, cycles, submissions, queue changes, or active-tree edits were performed.

## Evidence and existing behavior

The original challenge report and AutoAscend appendix support a hierarchy of concrete resource, exploration and combat behaviors, with persistent knowledge of items, shops and stairs. The challenge trajectory analysis specifically identifies deaths aggravated by food-related fainting and praying. Its historical score metric and entrants differ from the present progression objective; it does not establish that this proposed purchase policy improves this bot. [Official challenge report](https://nethackchallenge.com/report.html), [competition paper and AutoAscend appendix, Figure 8 / Appendix C](https://proceedings.mlr.press/v176/hambro22a/hambro22a-supp.pdf).

The official NetHack 3.6.6 implementation consumes nutrition over time and classifies nutrition 51–150 as Hungry, 1–50 as Weak, and nonpositive nutrition as Fainting; fainting interrupts activity and consumes turns without control. A food ration has nominal nutrition 800. These are game-mechanism facts, not hidden values the bot should read. Use observed hunger state and existing inventory estimates only. [NetHack eat.c: gethungry/newuhs](https://raw.githubusercontent.com/NetHack/NetHack/NetHack-3.6.6_Released/src/eat.c), [NetHack objects.c: food ration](https://raw.githubusercontent.com/NetHack/NetHack/NetHack-3.6.6_Released/src/objects.c).

Piterbarg, Pinto and Fergus describe AutoAscend's explicit strategy hierarchy and per-action strategy logging. This supports measuring which option actually ran before interpreting endpoint differences. It does not prescribe the thresholds below. [NetHack is Hard to Hack, §3.2](https://arxiv.org/html/2305.19240v2#S3.SS2).

Champion 20's relevant hooks, relative to its root:

| Hook | Current behavior and implication |
| --- | --- |
| `autoascend/dive_logic.py:2380`, `jf_config.py:172` | Tool route begins at XL7. `DIVE_FED=False` makes `fed_for_dive()` return true immediately; there is no effective food-readiness gate. |
| `autoascend/agent.py:2500` | `eat_from_inventory()` already consumes carried food at Hungry during the dive. Adding another generic Hungry-eat hook would often duplicate existing behavior. |
| `autoascend/agent.py:2572` | `carried_food_nutrition()` estimates nutrition of existing edible inventory, including lichen/lizard corpses; unknown item nutrition is zero. Reuse this as an estimate, not true remaining hunger. |
| `autoascend/item/inventory.py:1630` | `buy_food()` refuses all digging-tool carriers after settling existing unpaid goods. This refusal also applies while already inside a shop with an affordable ration nearby. |
| `autoascend/item/inventory.py:1472,1492` | Known-price shop selection and `pay_or_drop_unpaid()` already exist. The selector favors nutrition/price with only a tiny distance penalty; new local eligibility must filter candidates before ranking. |
| `autoascend/global_logic.py:896` | Inventory eating and shopping are existing periodic preemptions. Combat/emergency control must retain its priority. |

Avoid repeating these measured interventions: attempt 14's age/distance-limited corpse collection improved Public `0.4069901063 → 0.4221446135` but failed fresh `0.4013412921 → 0.1935119149`; its age-15 rule was only an initial selection filter. Inherited `FOOD_FIRST_MIN` is disabled after a documented 20-activation regression. Broad XL/dive thresholds, early tool retention, prayer cooldowns and quiet recovery have also been explored. Do not enable `DIVE_FED`, `DIVE_EAT`, nearby corpse collection, or a global food-first policy as part of this resource hypothesis.

## B: one local shop ration for a hungry tool carrier

Priority resource hypothesis for the parent's three-strategy campaign. Proposed flag `TOOL_SHOP_RESERVE`, default false before environment overrides, isolates the change to the current tool-carrier rejection in `buy_food()`. Pre-tool shopping and the existing unpaid-item cleanup keep their behavior.

All entry conditions must hold:

1. Hero carries a digging tool; observed hunger is exactly Hungry or Weak; `agent.carried_food_nutrition() < 400`.
2. Hero is already on a known shop-interior tile on the current level. No travel to another shop or level and no waiting for food to appear.
3. No visible hostile, no unresolved dangerous status that would prevent ordinary safe shopping, and a known legal path stays within the same shop floor. Path distance is at most two moves, with no door-opening, trap crossing, creature interaction or unknown square required.
4. Target is exactly one unambiguously identified **food ration**, for sale, with observed known affordable price. Reject explicitly `Item.CURSED`; allow `Item.UNKNOWN` beatitude when ordinary existing food rules accept it, and count those cases. Here “known” means ration identity and price, not a new beatitude-identification requirement. Ordinary in-game food risk remains measurable. Do not broaden to tins, corpses, unknown food types or snacks in this variant.
5. A prior failed attempt at this `(level, position, item identity)` is at least 100 game turns old. If the item instance cannot be tracked reliably, cool down the location instead.

Behavior and bounds:

- Take at most two deliberate movement actions, rechecking current hunger/stock, hostiles, path validity, target identity/BUC/price, level and shop membership before continuing and before pickup. Stop and return to the normal strategy if any prerequisite fails. A blocking `go_to()` without intermediate checks does not satisfy this contract.
- Buy quantity one with the existing inventory/prompt helpers and settle through `pay_or_drop_unpaid()`. Do not add a second purchase in the same invocation. Eating remains the existing inventory strategy.
- Use an eight-game-turn budget measured from entry. It gates additional travel and pickup; it must **never interrupt settlement of goods already picked up**. If a threat or timeout occurs after pickup, finish the existing payment-or-drop cleanup before handing back control. Record any cleanup overrun instead of pretending the transaction has an absolute eight-turn duration. An unsettled purchase must not be left behind by an early return.
- If a legal local path or an affordable observed price cannot be established, bypass the extension. An underfoot-only implementation is a valid narrower fallback, but record `radius=0` in the experiment definition rather than quietly comparing it as the radius-two hypothesis.
- Keep `DIVE_FED=False`, XL thresholds, prayer behavior, corpse rules, baseline shopping outside the tool branch and emergency ordering unchanged.

Minimal activation evidence: register real StatsLogger counters for `tool_shop_eligible`, `tool_shop_started`, `tool_shop_purchased`, `tool_shop_aborted`, `tool_shop_unknown_buc_accepted`, `tool_shop_unpaid_cleanup`, and `tool_shop_budget_overrun`. Log reasons including cursed/unknown-price food, no local path, threat and cooldown; record level/turn, before/after estimated stock, target distance, price, elapsed game turns, and whether cleanup left unpaid inventory. Counters must measure successful item acquisition and settlement, not merely predicate entry. Count preliminary eligibility separately so a coverage bottleneck is visible.

No-game fixtures should execute the real wrapped strategy and StatsLogger: underfoot purchase; a two-step path; unknown-beatitude ordinary ration accepted and counted; explicitly cursed/unknown-type food rejected; low gold; pre-tool behavior unchanged; new hostile after the first step; changed price/item after travel; timeout before pickup; timeout/threat after pickup still settles or drops; failed-target cooldown. A fixture proves integration, not actual gameplay activation.

## Secondary routing hypothesis, not part of B

`DiveLogic.should_fetch_digging_tool()` at `autoascend/dive_logic.py:2221` gives every reachable same-level tool `cost=0`. Consequently it selects the first remembered tool in scan order, even if another is much closer. `_local_tool_spot()` already chooses by distance, but the active fetch selector at `plan_step()` uses this different method.

A separate `FETCH_NEAREST_LOCAL_TOOL` flag could preserve all current cross-level choices and same-level priority, breaking only same-level ties by BFS distance (`distance-to-neighbor + 1` for the already-supported fresh-tunnel endpoint case). Compute BFS once per scan, retain current inventory/shield/shop/give-up guards and stable tie order. Do not compare raw map steps against cross-level edge counts or alter `FETCH_TOOL_TURNS` in the same patch.

Measure scans with at least two eligible same-level targets, old versus new selection, distance saved on the selected path, successful retrieval, actual elapsed turns and failures. Fixtures should cover a far first-scanned tool versus a near second tool, unreachable candidates, equal distances, one candidate, a carried usable tool, and preservation of cross-level ordering. This is a plausible low-risk routing correction, but may have too few opportunities in 20 games; reserve it for a later independent arm if B is selected now. The mechanism is a local code finding, not a published claim of improved NetHack score.

## Campaign interpretation

The parent campaign specifies the same pinned baseline for each independent strategy and N=20 games: Public seeds 0–14 plus extra seeds 2000–2004. Report the actual count, errors, paired per-game scores, mean, wins/ties/losses, depth, turns and death cause, with Public and extra subsets separately as well as pooled. Preserve exact Evidence and program/tree identities. The 20 games are a screening experiment, not proof of general superiority; score-identical reruns have already shown timing/death differences.

For B, also report games with eligibility, started/purchased transactions, aborted transactions, time spent and unpaid cleanup outcomes. Zero real activations means **not covered**, even if scores tie; fixture success does not change that. Do not silently change radius or hunger gates mid-batch to manufacture coverage. A changed specification becomes a separate experiment. Only combine separately qualified strategies, then evaluate the combination against the same baseline and its constituent winners; additive effects are not guaranteed. Root owns execution and qualification rules. Existing autonomous publication and local promotion gates remain independent of this research recommendation.
