# Local experiment history

These are measured outcomes from earlier runs. Avoid repeating failed ideas.

| attempt | hypothesis | public score | local validation | decision |
| --- | --- | --- | --- | --- |
| 1.1 | leave level-one farming at XL4 to find food and | 0.1086 | — | rejected |
| 2.1 | recovering HP before exploring prevents attrition deaths | 0.1512 | +0.0349 | promoted |
| 3.1 | keep distance from passive acid, paralysis, fire and stun attacks | 0.1080 | — | rejected |
| 5.1 | avoiding known petrifying corpses without gloves prevents | 0.2399 | — | rejected |
| 6.1 | starting descent at XL9 avoids attrition during the extended XL9-10 | 0.2670 | — | rejected |
| 7.1 | refusing petrifying sacrifice corpses without gloves avoids | 0.2862 | +0.0000 | promoted |
| 8.1 | three-turn tactical forecasts avoid near-term lethal exchanges | 0.2893 | — | rejected |

## Whole-peer baselines

These exact peer commits were evaluated locally on the same 15 public games. A high Private score need not beat this bot on the public batch.

| source | public mean | compared champion | decision |
| --- | --- | --- | --- |
| `github.com/Komershan/nethacker@6073d88ea81f05d20c46c57b8fb9a38a54bfe75e` | 0.1351 | 0.1512 | not adopted: lower local public mean |
| `github.com/vkurenkov/nethacker@a5f72915d2a27db4c3835df61196dafe1ca31d7b` | 0.2692 | 0.1512 | promoted as local baseline |

## Fainting hunger-prayer cooldown

Hypothesis: extending the fainting hunger-prayer cooldown from 400 to 1000 turns reduces premature prayers and divine anger during farming. Inspired by peer2 `github.com/daglar-dragomirov/nethacker@c4308340c16ceb94e2e7896dd5897676b1fc3512`. Only this cooldown changes.

Validation: `local` namespace, val-dwa-law-fem, seeds 0, 1, 2, 3, 6, 7, 9. Parent mean 0.216520; changed mean 0.286366; delta +0.069846. Results in `prayer-cooldown-eval.json`. Mixed per-seed results; full 15-seed mean not measured.

Discarded experiments: exact HP prayer trigger and suppressing prayer after anger each left scores unchanged on seeds 0, 1, 2, 6. A 1200-turn fainting cooldown regressed across the seven sampled seeds. All discarded edits were reverted.
