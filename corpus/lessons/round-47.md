# Round 47 — lesson (tsukuroi, hyaku run 10)

author: tsukuroi L1 (`TsukuroiR47`), 2026-10-27. Base `916019057147d7e9ba6b137647b2cee26decf4b8`
(the lane tip at round start). Fresh-start round: rounds 44, 45 and 46 were closed `rejected-harmed`,
`rejected-honest-stop` and `rejected-harmed`; their spot-checks were read before any claim was
declared (`corpus/lessons/round-4{4,5,6}-verifier-spotcheck.md`). Claims and frozen counters:
`SCORECARD.md` "Round 47 — declaration". This file is updated with the wave outcome at integration.

## Outcome (author-side; non-author closure pending)

- **C1 depth — admission of GR1-GR3** with GR2 amended pre-wave per the round-46 counted residual
  critic's exact correction (`.ufo/waves/round-46/r1/V46ResCritGR2.md`): the filesystem-closing
  `-EAGAIN` return (scrub.c:3094-3095, quoted) leads the ordering, and the suspend sentence is
  narrowed to the unmount path (dev-replace.c:1143-1144). Counter `tools/check-scrub-admission-r47.py`
  closes the round-46 wave findings F1-F3 and K22/K23 and is sized for two amendment rounds
  (per-row admission; residual generations `R47Res{,2}{Rev,Crit}GR<n>`).
- **C2 operability — the selftest TMPDIR-space contract** (`round-46 w1/C1ExecRerunB.md`, planned row
  item 2): the harness derives a classifiable fixture base (falling back to /tmp when TMPDIR holds
  characters `root_locator_class` refuses) and gains two `(R47-C2)` pinning cases.

## Gate

### New SOURCES rows (opened 2026-10-27; L1 fetch, re-opened live by wave seat SrcGate)

| Row | URL (access 2026-10-27) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S252 | https://man7.org/linux/man-pages/man1/mktemp.1.html | "-t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set" | mktemp.1.html, the -t option description |

Snapshot digest: `.ufo/waves/round-47/frozen/src/SHA256SUMS` (mktemp.1.html
`74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`), fetch log `frozen/src/FETCH.txt`.
Live re-open and byte-compare: wave seat SrcGate receipt.

### Reject rows (candidates considered this round and refused)

(none yet — updated at integration)

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R47-FRESHSTART-THREE-REJECTS | process — three consecutive rejected closures each carried a routed defect the next round repeated or left open | r44 D6 (report sections missing) was closed in r45, but r45 opened D4 (census not re-run at attempt start), D5 (post-freeze counter rebinding without a declared rule); r46 repeated D4's shape (it did run its own start census — the one clean carry) and added D5 (uncommitted late seat files, closed by the orchestrator, not the lane). Round 47's declaration runs the census at its own start, declares the frozen-counter binding rule up front (no post-freeze rebinding; a defect that forces a counter change converts to an honest stop), and lands every wave file through the L1 before the report | the fresh-start rule (addendum §6 run-10) — read the three rejections before declaring | this round's receipts: `.ufo/waves/round-47/before/sources-census-start.txt` (own start, routed D4); the frozen counters are bound by name in the declaration before any seat; all wave files are committed by the L1 before the report is filed. Able to fail: the declaration names the expectation, and a missing start-census or post-freeze edit is visible in the commit diff. |
| R47-C2-DIGEST-TRUNCATION | evidence handling — tool-output display truncation silently produced invalid sha256 pins | The first draft of `tools/check-scrub-admission-r47.py` pinned four snapshot digests copied from a `sha256sum` display that was column-truncated (63/60/62/62 hex chars instead of 64); the counter's quote leg then read `snapshot absent or digest moved` for S246/S244 quotes that were in fact intact. Caught by the L1's own smoke run before any seat | the L1 pre-wave counter smoke run (quote legs printed per-row `bad` lists) | the four pins re-derived locally with hashlib (64 chars) and the smoke run re-executed: quotes_ok 3, all 50 quotes verified. Able to fail: the quote leg fails closed on any digest mismatch, and the smoke run prints the per-row bad list. |
| R47-GR2-AMENDMENT-CLASS | claim sizing — a frozen verdict universe too small for the amendment path it allows | Round 46's C2 rule allowed narrowing after `partly` but froze one residual pair per row; GR2 read `partly` twice and no counted seat remained (R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT, `corpus/lessons/round-46.md`). Round 47 sizes the universe for two amendment rounds (per-row admission plus two residual generations) and amends GR2 pre-wave from the counted critic's exact correction text, so the counted seats read the amended bytes once | round-46 lesson R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT (carried) | the round-47 counter universe lists `R47Res2*` seats and per-row `row_ok`; a second `partly` would leave seats to read a second narrowing. Able to fail: a row whose residual seats read `partly` on current bytes leaves `row_ok false` with bound seats visible in the receipt. |
