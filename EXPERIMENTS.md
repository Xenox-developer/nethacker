# Local experiment history

These are measured outcomes from earlier runs. Avoid repeating failed ideas.

| attempt | hypothesis | public score | local validation | decision |
| --- | --- | --- | --- | --- |
| 1.1 | leave level-one farming at XL4 to find food and | 0.1086 | — | rejected |
| 2.1 | recovering HP before exploring prevents attrition deaths | 0.1512 | +0.0349 | promoted |
| 3.1 | keep distance from passive acid, paralysis, fire and stun attacks | 0.1080 | — | rejected |
| 5.1 | avoiding known petrifying corpses without gloves prevents | 0.2399 | — | rejected |

## Whole-peer baselines

These exact peer commits were evaluated locally on the same 15 public games. A high Private score need not beat this bot on the public batch.

| source | public mean | compared champion | decision |
| --- | --- | --- | --- |
| `github.com/Komershan/nethacker@6073d88ea81f05d20c46c57b8fb9a38a54bfe75e` | 0.1351 | 0.1512 | not adopted: lower local public mean |
| `github.com/vkurenkov/nethacker@a5f72915d2a27db4c3835df61196dafe1ca31d7b` | 0.2692 | 0.1512 | promoted as local baseline |

## XL9 descent threshold (val-dwa-law-fem)

One strategy change: begin the existing descent phase at XL9 instead of XL10.
Inspired by the earlier descent threshold in MIT-licensed peer
`github.com/vkurenkov/nethacker@ef6acf87e265f74600b914060f620d06117070a3`;
no peer implementation was copied. Initial XL8 training is retained.

Evaluation namespace: `local`; seeds: 3, 5, 11.

| Seed | Parent | XL9 |
| --- | --- | --- |
| 3 | 0.117050 | 0.206129 |
| 5 | 0.206129 | 0.206129 |
| 11 | 0.366113 | 0.466376 |
| Mean | 0.229764 | 0.292878 |

Imports pass and all three episodes completed without evaluation errors.
The full 15-seed mean has not been measured for this change.

Discarded experiments on the same batch: retaining a digging tool during the
tour produced identical results; XL8 descent averaged 0.229662, slightly below
the parent. Both were reverted.
