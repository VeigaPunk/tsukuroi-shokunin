# Round 61 — lesson (Windows host, base `6b26c338`; declaration `136bfb00`, work `abb2a161`)

Shape: single-session inline round (no wave/AgentSwarm dispatch surface on this host; the standing L0
questions `tsukuroi | round-53` (fleet `.ufo/l0-questions.md:229`), the round-1 kaidoku/revenger scope
(PROVINCE Frontier), `tsukuroi | round-57` (S266 interact authorization, `:247`) and `tsukuroi |
round-60` (whole-SKILL SHONEN verification, `:253`) all stand unanswered and were routed around, never
treated as answered). Claims declared before any after-measurement (SCORECARD "Round 61 — declaration"):
C1 depth (sourced Windows driver query plane, rows DQ1-DQ5), C2 operability (`tools/recheck-registry-r61.sh`
10-row registry recheck arm), C3 coverage (the corpus README Windows-host transition map rows). FRESH-START
r50/r51/r52 re-spot-checked at the base (receipt `.ufo/waves/round-61/before/freshstart-spotcheck.txt`:
r50 FAIL verdicts_ok 0 / marks_ok 0 / seats_ok 18, r51 evidence committed EMPTY 0 bytes, r52 FAIL 1/0/16)
with five move classes ruled out for cause. S276 was fetched live BEFORE the declaration text was written
(fetched 2026-11-01) — the disclosure order the r60 S275 precedent set, not the r59 S274 post-declaration
order.

## Routed carry-ins from the r60 closure (addressed first, not claims)

- **The bde06613 gate-receipt rule re-applied.** The routed r59 item (the intermediate 95/95/1
  registry-coverage FAIL raw JSON) was already discharged at r60's `e1e10178`; this round verified the
  committed receipt PRESENT at the base (`git cat-file -e 6b26c338:.ufo/waves/round-59/after/registry-coverage-FAIL-at-2913b75d.regenerated-r60.json`
  → rc 0, before-receipt). The rule stayed in force: any r61 gate red state commits its raw receipt the
  same round, named FAIL + revision + original-or-regeneration. No r61 gate red state occurred — the C2
  arm's first-run FAIL is a probe-instrument first run, not a gate red state, and was receipted anyway.
- **Byte-stable writers (the r60 C3 convention, kept):** every append written binary-mode against the
  target file's own convention (SCORECARD/SKILL/SOURCES CRLF — verified CRLF at the tails; LOG/README
  LF), proven on committed bytes by the final five-file append-receipt measurement (lands
  receipt-after-subject, `--require-raw` exit 0 expected — no rewrite to disclose).
- **Standing L0s:** routed around, never answered; no new L0 question owed this round.

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S276** — Microsoft Learn, `driverquery` (Windows Commands, current reference),
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/driverquery .
  Opened 2026-11-01 by the L1 (live fetch of the page). Located quote (14 words, counted by `wc -w`
  before landing): "Enables an administrator to display a list of installed device drivers and their
  properties." (page lede). Supporting located text: the Syntax block (`driverquery [/s <system> [/u
  [<domain>\]<username> [/p <password>]]] [/fo {table | list | csv}] [/nh] [/v | /si]`); the `/fo
  table` row ("Formats the output as a table. This is the default."); the `/nh` row ("Omits the header
  row from the displayed driver information. Not valid if the /fo parameter is set to list."); the
  `/v` row ("Displays verbose output. /v is not valid for signed drivers."); the `/si` row ("Provides
  information about signed drivers."); the Examples. Frontmatter `ms.date` 2017-10-16,
  `updated_at` 2026-02-16T18:34:00Z, `git_commit_id 1dde3f071fa8b65476a0f278d15ed67c19b07896`. The
  page documents the CLI contract but NOT a return-value table, NOT any message text and NOT the
  output column sets — all three host-measured (dq3/dq3b/dq4b/dq1/dq2 receipts); its two documented
  restrictions (/nh-with-list, /v-with-signed) are MEASURED on the host with matching refusal messages
  (dq3b/dq4b). Used by `corpus/knowledge/windows-driver-query-plane-r61.md` — C1's sourced ground.

Rejections this round: **0 — stated explicitly**: no source was opened and rejected; no lead was
carried over from r60 (r60 recorded zero open leads; the S274 `-codes` 404 stays recorded inside
S274's row).

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0 at
round start (42 W04 duplicate-URL warnings, 0 E-code; receipt
`.ufo/waves/round-61/before/sources-census-start.txt`, verbatim capture) — the end receipt lands with
the final commit. S276 was inserted at its id position directly after S275 (line 285 after 284, inside
the single Registry section that holds the whole table — the R58-SOURCES-APPEND-POSITION rule). Gates
at the work revision `abb2a161`: knowledge-header PASS **77 notes / 0 findings / 77 complete**;
registry-coverage PASS **98 tools / 98 rows / 0 findings** (JSON receipts under
`.ufo/waves/round-61/after/`; both gates re-run at the final tree in the receipts commit); SCORECARD
uniqueness ok rc 0; `RECEIPT_RUN_SELFTEST: PASS (7 cases)`, `RECEIPT_WRITE_SELFTEST: PASS (5 cases)`,
`APPEND_RECEIPT_SELFTEST: PASS (5 cases)` unchanged; `bash -n tools/recheck-registry-r61.sh` rc 0; the
final five-file append-receipt measurement (LOG, SCORECARD, SKILL, SOURCES, README at base → final
tree) lands in the receipts commit (receipt-after-subject, the tameshi r63 precedent — the outcome
cannot measure its own commit's bytes before they exist).

Assimilation: `considerthese/` mined (latest 2026-10-26; seven notes, unchanged set since r57/r58/r59/r60
mined them): the reflection notes are aggregator/wave-class or Linux-host-class on this host; nothing
clears this round's bar; nothing adopted. The shokuknow register is not reachable from this host.
Assimilation: none — shokuknow unreachable.

## Mistakes

- **R61-ARM-FIRST-RUN** (class: an extraction pattern in a new instrument is wrong at its first live
  run — the R59-ARM-FIRST-RUN class, second occurrence, caught by running the arm BEFORE the outcome
  cited it) — the C2 arm's R4 type census extracted tokens with `grep -oE 'REG_[A-Z]+'`: the class
  stops at the underscore, so `REG_EXPAND_SZ`/`REG_MULTI_SZ` were read as `REG_EXPAND`/`REG_MULTI`
  and judged outside the documented-superset — first run FAILED 1 drift, rollup
  `RECHECK_REGISTRY: FAIL (1 drift)`. Captured-by: the r59 rule (run the instrument, cite only what
  ran). Fix: the extraction class widened to `REG_[A-Z_]+`; the fixed run passes 10/10 (due and
  no-due); the FAIL receipt is committed under its honest name
  `.ufo/waves/round-61/receipts/recheck-registry-FIRST-RUN-FAIL-at-authoring.txt` beside the pass
  receipts — nothing substituted. Rule going forward: a token-extraction class for REG_* values is
  `REG_[A-Z_]+` (underscore inside), and a new arm's first run is a live test of the extraction, not
  only of the host.
- **R61-SOURCES-ROW-DELIMITER** (class: a table row's cell text carries the delimiter itself) — the
  first S276 row draft embedded the syntax verbatim (`[/fo {table | list | csv}]` and `/v | /si`),
  three raw pipes inside cells; the awk `-F'|'` pre-landing check read **14 fields against the
  13-field rule** (S275's NF) — the census E01 malformed-row shape, caught BEFORE any commit and
  BEFORE any census run. Fix: the cells rewritten pipe-free (formats joined with slashes, the
  alternative pair written `/v-/si`); the working-tree row replaced in the same session — **no
  committed byte ever carried the 14-cell shape** (provable by the final append-receipt measurement:
  SOURCES old-only 0, a pure single-line insert). Rule: any SOURCES row whose source is a CLI
  reference gets its syntax cells rewritten delimiter-free, and the awk NF check against the previous
  row runs before the insert.
- **R61-SPAWN-VAR-POSITION** (class: the boundary-conversion var put on the wrong side of the spawn —
  the r59 E2b class met in authoring) — the first dq1 spawn passed `env MSYS_NO_PATHCONV=1` on the
  CHILD argv through receipt-run; the conversion fires at the bash→python boundary before any child
  env can matter, so the child saw the mangled `/FO` and returned rc 1 (the receipt's own rc= line
  caught it). Fix: the var rides on the receipt-run INVOCATION (`MSYS_NO_PATHCONV=1 python
  tools/receipt-run.py …`); the corrected run overwritten the working-tree dq1 receipt before any
  commit (the committed dq1 receipt is the correct-form run — the first spawn left no committed
  trace; disclosed here rather than silently dropped). The r60 note's RG5/DQ5 statement of the rule
  was already correct — the mistake was this session's first spawn, not the recorded rule.

Sweep that found no further mistakes this round: before the outcome commit the round's files were
re-read against the declared predicates — the battery receipt re-checked value by value (DQ rows 5,
SOURCES 276 with S276 at line 285 after S275 and 0 duplicate ids, quote 14 words, due= 1/0, both
rollups PASS 10/10 0-drift, README windows rows 9, PROVINCE blob `23198d74…` identical at base and
work, gates 98/98/0 and 77/0/77, selftests 7/7 5/5 5/5, `bash -n` 0), the nine probe receipts re-read
(rc and message lines), the 97 carried registry rows byte-compared to the round-60 table (identical),
the new registry row's NF matched against the r59 row shape, the SKILL round-61 section re-read for
unverified numbers (none: every figure cites a receipt or this lesson's Gate), the README map rows
cross-checked against each note's own row-ids and source-id header lines, and the protected surfaces
diffed byte-identical to the base (README counted as changed-by-claim C3; PROVINCE, SHONEN, QUALITY,
AGENTS identical). The three mistakes above are the complete defect set observed this round.
