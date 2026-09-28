# Blind dig interruption retry

An interrupted blind dig now permits another Elbereth attempt even without HP loss. Missed attacks can interrupt digging too. The existing six-attempt cap remains in force; retries are scoped to level, square, and pit phase.

Validation: all 15 val-dwa-law-fem training seeds, evaluation-id local, in foreground batches of 4, 6, and 5. Parent mean 0.482936352; candidate mean 0.488775812. Seed 11 improved from depth 25 to 28; seed 3 regressed from 27 to 26; thirteen scores tied. No episode errors. Raw results: blind-dig-eval.json.

Reviewed pinned peers, particularly kefirski/nethacker@454ae8df96e7ec68f0df2488b2b8a90368407cf1, whose blind engraving guard likewise relied on HP loss. This change uses the existing local dig interruption message; no peer code was copied.

Discarded probes: pet separation regressed over 15 seeds; proactive known blindness-curing potions and sleep-wand combat tied their four-seed probes; XL8 tool-dive training regressed its four-seed probe. All those runtime changes were reverted. The final patch contains only the interruption retry mechanism.
