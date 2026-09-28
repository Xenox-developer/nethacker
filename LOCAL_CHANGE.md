# Blind inscription experiment

One retained hypothesis: write two Elbereth words when blind, so per-letter engraving errors have two chances to leave a protective word. Recognize an intact Elbereth substring when the inscription becomes readable. Sighted engraving stays unchanged.

Seed batch: 2, 7, 11, 14; identity: val-dwa-law-fem; evaluation-id: local.
Candidate mean: 0.516869945. Fresh parent mean: 0.471173651. Stored parent mean on this batch: 0.483072811.
Seed 11 reaches depth 28 instead of 25 in both parent references. Candidate scores on the other three seeds match the stored parent. Fresh parent seed 14 reached depth 26 instead of its stored depth 27, demonstrating execution variation. This is a small sample, not a full 15-seed score claim.

Command (run separately for each solution):
```sh
python -m nethackers.arena.run --solution /workspace --batch '[[2,"val-dwa-law-fem"],[7,"val-dwa-law-fem"],[11,"val-dwa-law-fem"],[14,"val-dwa-law-fem"]]' --evaluation-id local --out /tmp/eval-inscription.json
```
Parent command substitutes `--solution /refs/parent` and `/tmp/eval-parent-confirm.json`.

Validation: package imports and compileall pass; engraving prompt fixtures pass for blind Elbereth, sighted Elbereth, and unrelated text. Adapter unchanged. All eight final comparison episodes completed without errors.

Peer review: inspected daglar-dragomirov/nethacker@5d0d455a1585271143aa47fbd5b44c2f6dae7d4b prayer and Elbereth handling, plus peer3's val descent policy. Full peer prayer policy and a narrower emergency-only port were experimentally rejected for regressions and completely removed. Final change contains no newly copied peer code. Prior attempts at additional blind retries and appending inscriptions were reviewed; this change instead writes redundant words in a single command.
