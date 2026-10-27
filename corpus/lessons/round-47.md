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
| S252 | https://man7.org/linux/man-pages/man1/mktemp.1.html | "if DIR is not specified, use $TMPDIR if set, else /tmp" | mktemp.1.html lines 94-99, the `-p DIR, --tmpdir[=DIR]` option |

Snapshot digest: `.ufo/waves/round-47/frozen/src/SHA256SUMS` (mktemp.1.html
`74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`), fetch log `frozen/src/FETCH.txt`.
Live re-open and byte-compare: wave seat SrcGate receipt.

### Reject rows (candidates considered this round and refused)

(none yet — updated at integration)

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R47-FRESHSTART-THREE-REJECTS | process — three consecutive rejected closures each carried a routed defect the next round repeated or left open | r44 D6 (report sections missing) was closed in r45, but r45 opened D4 (census not re-run at attempt start), D5 (post-freeze counter rebinding without a declared rule); r46 carried D1-D6, including late seats and stale outcomes. Round 47 ran its own sources census before claims and froze the counter digest before any seat | the fresh-start rule (addendum §6 run-10) — read the three rejections before declaring | the process gate `.ufo/waves/round-47/controls/process-gate.txt` checks the start receipt and counter digest; it prints PASS/PASS. Able to fail: the command exits nonzero if the start receipt is absent or the counter digest differs from the pre-seat freeze. |
| R47-C2-DIGEST-TRUNCATION | evidence handling — tool-output display truncation silently produced invalid sha256 pins | The first draft of `tools/check-scrub-admission-r47.py` pinned four snapshot digests copied from a `sha256sum` display that was column-truncated (63/60/62/62 hex chars instead of 64); the counter's quote leg then read `snapshot absent or digest moved` for S246/S244 quotes that were in fact intact. Caught by the L1's own smoke run before any seat | the L1 pre-wave counter smoke run (quote legs printed per-row `bad` lists) | the four pins re-derived locally with hashlib (64 chars) and the smoke run re-executed: quotes_ok 3, all 50 quotes verified. Able to fail: the quote leg fails closed on any digest mismatch, and the smoke run prints the per-row bad list. |
| R47-F1-TERMINATOR-CONTROL | frozen-counter blind spot — the first F1 guard stopped hashing at any `## ` line, then checked only inside that truncated prefix; its inner-header check could not detect the unbound tail it was meant to catch | `controls/f1-correction.md`: at counter revision `3629c46a`, F1a observed `structural_ok=1` on an injected `## Annotation` line; at `77e9e2b2`, the same fixture observed `structural_ok=0`; final battery `controls/battery-summary-r47.jsonl` F1a/F1b as expected | the pre-data F1a negative control from §9 (a counter that catches only the no-seat FAIL must not earn F1 credit) | Bind each row to its named expected successor header, and reject any other `## ` line before it. Able to fail: saved F1a receipt shows the initial guard reading structural_ok=1 and the corrected frozen counter reading 0, while the final battery has 12/12 expected controls. |
| R47-K22-S240-MAP | frozen-counter false negative — the citation resolver omits an in-scope source | `w1/R47CritGR2a.md` §Host reading cites S240 `ioctl.c:3190`; the frozen counter maps no `ioctl.c` snapshot (`tools/check-scrub-admission-r47.py`, `SNAPSHOTS` / `CITE`), so that bound report cannot satisfy K22 | the K22 citation-resolution check (which only proves membership in the counter's incomplete snapshot map) | Add S240's pinned ioctl.c snapshot and digest to the counter map before the next claim freeze. Able to fail: `controls/k22-s240-map.txt` observes `(False, 'ioctl.c not a pinned snapshot file')`. |
| R47-C2-TMPDIR-FALLBACK | scratch-scope defect — the new guard writes the selftest fixture under `/tmp` when a supplied TMPDIR contains a refused character | `.ufo/waves/round-47/w1/C2ExecRerunA.md` reports the 164/164 pass and that the fixture tree sat under `/tmp`; the frozen C2 kill rule explicitly requires no newly hardcoded `/tmp` write | the C2 kill rule in `SCORECARD.md` “Round 47 — declaration” | Replace the `/tmp` fallback with an alias path that remains within the supplied TMPDIR while presenting a whitespace-free root-override spelling (or declare a safe failure before freezing). Able to fail: the counted seat observed the actual `/tmp` fixture path during the spaced-TMPDIR run. |
| R47-GODSPEED-DIRECTIVE-BYTES | dispatch conformance — the pre-rendered L2 task text omitted lines from the verbatim directive | `.ufo/waves/round-47/w1-dispatch.json` first task begins `/skill:godspeed` then the numbered four lines and unheaded `IMMEDIATELY STOP…`; it omits the binding's `You are a Godspeed-enabled subagent.` line and `## ` heading from `skill://godspeed/directive.md` | the round prompt §3 Godspeed lead rule | Build future item prompts from the exact `skill://godspeed/directive.md` bytes; the wave is already dispatched and is not rewritten. Able to fail: byte-prefix comparison against the frozen directive identifies the first mismatch. |
| R47-GR2-AMENDMENT-CLASS | claim sizing — a frozen verdict universe too small for the amendment path it allows | Round 46's C2 rule allowed narrowing after `partly` but froze one residual pair per row; GR2 read `partly` twice and no counted seat remained (R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT, `corpus/lessons/round-46.md`). Round 47 sizes the universe for two amendment rounds (per-row admission plus two residual generations) and amends GR2 pre-wave from the counted critic's exact correction text, so the counted seats read the amended bytes once | round-46 lesson R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT (carried) | the round-47 counter universe lists `R47Res2*` seats and per-row `row_ok`; a second `partly` would leave seats to read a second narrowing. Able to fail: a row whose residual seats read `partly` on current bytes leaves `row_ok false` with bound seats visible in the receipt. |

## Re-opened rows and rows touched old→new

| Row | used-by old → new | In-round action |
|---|---|---|
| S251 | `corpus/knowledge/census-identity-r46.md` → unchanged | Re-opened man7 page on 2026-10-27; live digest `3a50ddef…ff27e` matches the prior pin. Anchor widened from raw HTML lines 72-81 to 72-81, 84 after the round-46 spot-check found that line 84 (`type:[inode]`) was cited but outside the locator. Snapshot: `.ufo/waves/round-47/frozen/src/proc_pid_fd.5.html`. |
| S252 | new row, used-by `corpus/lessons/round-47.md` | Opened `mktemp(1)` on 2026-10-27, digest `74186433…073266`; located the `--tmpdir` quote at raw HTML lines 94-99. |

## Round-46 routed defects — round-47 disposition

| Defect | State |
|---|---|
| D1 C1 kill rule fired | Corrected the current operability evidence to say round-46 C1 was not verified; removed `census-identity` from the admitted capabilities table. The behavior exists, but the r40 PASS→FAIL kill term overturns the claim. |
| D2 kill universe incomplete at measured revision | No retrospective PASS is claimed. Round 46 remains rejected; no omitted kill leg is represented as passing. |
| D3 C2 verdict count / future receipt pointer | Corrected the current scorecard's round-46 count to the verified `verdicts_ok 1`; the correction block records that GR1 was unbound and the old `2` count is superseded. |
| D4 receipts read before outcome commit | No round-47 outcome commit is made without reading the settled results and the frozen-counter receipts. |
| D5 late seats | Not closed at this wrap point: no `WAVE-DONE w1` / `w1-results.json` handoff was received. |
| D6 S251 anchor | Closed: S251 now locates lines 72-81 and 84; the live re-open digest matches the existing pin. |

## Assimilation and considerthese

Assimilation: none. The registry has 252 ids, the staged package 147 ids, and 53 collisions (S200-S252); no renumber map. Both lists and the indented-row guard receipt are `.ufo/waves/round-47/assimilation/{reg-ids,staged-ids,collisions,indented-collisions}`.

Mined one still-unimplemented proposal from `considerthese/2026-10-26.md:18` (accessed 2026-10-27): the “Counter-attack scoreboard” asks for per-counter attack arms, survivors, and defeating classes. This round's `controls/battery-summary-r47.jsonl` records 12 pre-data controls with 0 unexpected outcomes, but no longitudinal survivor ledger was added; the proposal remains open.

## Spot-check candidates

- C1 GR2: the counted critic found that the unmount suspend path does not call `btrfs_scrub_cancel`; the call at dev-replace.c:1143-1144 is in `btrfs_dev_replace_cancel`. The row was corrected in the working tree, but the corrected bytes were not re-read by a settled residual cohort before this wrap.
- C2 operability: the spaced-TMPDIR test passes 164/164, but the fix falls back to `/tmp` when TMPDIR is unsafe; a counted seat reports this conflicts with the frozen kill rule. The claim is not promoted.
- Wave settlement: no non-author closure or WAVE-DONE was received before this report.
