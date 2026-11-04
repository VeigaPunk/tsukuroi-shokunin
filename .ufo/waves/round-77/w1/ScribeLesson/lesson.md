# Round 77 — lesson draft (ScribeLesson; not integrated)

Axes: depth (8, lowest tied with adjacency) and freshness (9). Frozen declaration: eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5; base: 06f1bbbb803790b35358d277bb7807b82a9fab99. C1 is exactly **six pinned arithmetic vectors match**; C2 is exactly **three exact corrective blocks exist**. No predicate, instrument or expected-data alteration is proposed. Production integration is solely L1's.

## Gate

These version-pinned URLs were reopened in this seat; the matching local frozen source ranges were read too. Decisions below are source decisions, not votes that bind closure.

| Candidate | Decision | Opened evidence | Reason / flip |
|---|---|---|---|
| S324, code, tier A | admit | https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro.h — lines 320–326 and 337–350 | LESS_BY subtracts only if a > b, otherwise zero; CLAMP tests high, then low. Pinned snapshot digest: 1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8. |
| S325, code, tier A | admit | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c — lines 143–186 | At 168, free-minus-keep_free saturates; at 170, limit clamps used plus allowance; at 171, remaining allowance saturates. Supersedes S320's false minimum wording rather than rewriting the historical row. Pinned snapshot digest: 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2. |
| Prior pre-correction JD3 / declaration minimum formula | reject | Same manager source, line 168, and macro definition, line 325 | min(free, keep_free) contradicts LESS_BY. Flip: a source revision actually using minimum; a lexical counter PASS is not such evidence. |
| S326, guessed header | reject | https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro-fundamental.h — opened, HTTP 404 | Absent guessed path supplies no located quote. Actual path is S324. Flip: a reachable version-pinned file containing a located relevant quote. |

Spot-check result: **outside round-77 closure pending; not self-verified**. This seat's reopening is author-side source evidence, not an independent closure. Outside round-76 disagreement is recorded in corpus/lessons/round-76-verifier-spotcheck.md §2 and §3: closure rejected the minimum conjunct despite the mechanical PASS; it agreed with the round's substantive rejections but disagreed with the missing reject row in the Gate table. That historical outside review does not certify round 77.

## Red example and finite boundary

With free=1000 and keep_free=100, the rejected minimum gives 100; the actual LESS_BY gives 900. For frozen A1, used=100, min_use=0, max_use=2000 yields limit=1000 and available=900. This fixes the red example rather than describing minimum as subtraction. The frozen pre-data receipt .ufo/waves/round-77/before/controls.json records the minimum control as C1 count=0, met=0, reason=vectors, exit 1; sourceless and held-restatement controls are red too. Those are inherited receipts, not checks executed by this seat.

The six frozen vectors use small non-overflowing uint64 values with min_use <= max_use. They are finite worked examples, not a universal arithmetic oracle, live manager observations, or claims about startup-normalized metrics. patch_min_use at 176–186 changes a floor on startup; these examples do not derive actual startup metrics or authorize a restart.

## Mistakes

| Class | Mistake / evidence | Correction and propagation |
|---|---|---|
| stale-premise/number-drift | The prior minimum premise contradicts LESS_BY. QUALITY 106 already says a post-freeze contradiction is an honest claim miss even if a lexical counter passes corrected prose. The landed JD3 correction did not propagate to S320's teaches cell, which still says minimum. Round-76 outside closure also found the missing Gate reject row, stale registry count 322 (actual 323), and stale collision count 114 (fresh base 124). | Preserve the honest miss; use scoped superseding S325 for S320 correction propagation. Include explicit reject decisions and outside disagreement here. The three byte-exact C2 repair strings are in repairs.md for L1's append to the round-76 lesson; drafts here do not themselves satisfy the production C2 gate. |

## Sources, counts and hold

Sources reopened: S324 and S325 pinned URLs; guessed S326 reopened and returned HTTP 404. Full frozen digests are recorded in .ufo/waves/round-77/before/src/SHA256SUMS; no new checksum verification was run by this seat. Base collision receipt .ufo/waves/round-77/before/collisions.json and frozen declaration report 323 registry ids, 147 staged ids, **124/147 collisions**, not 114/147. This is receipt provenance, not a fresh recount by this seat.

Assimilation: **none**. Package and promotion remain operator-held. No ordinal gain: depth 8 and freshness 9 remain the stated baseline; no production gate result or round admission is claimed. No production files were edited.
