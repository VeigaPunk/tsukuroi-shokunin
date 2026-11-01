# Round 59 — lesson (Windows host, base `c2e32b00`; declaration `c5a33d08`, work `2913b75d`, repair `c4aa0f5c`)

Shape: single-session inline round (no wave/AgentSwarm dispatch surface on this host; the standing L0
questions `tsukuroi | round-53` (`.ufo/l0-questions.md:229`), the round-1 kaidoku/revenger scope (PROVINCE
Frontier), and `tsukuroi | round-57` (S266 interact authorization, `.ufo/l0-questions.md:247`) all stand
unanswered and were routed around, never treated as answered). Claims declared before any after-measurement
(SCORECARD "Round 59 — declaration"): C1 depth (sourced scheduled-task STATUS plane), C2 operability
(the event-log plane's executable recheck arm, 11 rows), C3 freshness (the E-plane's operative pass block +
first executable pass). FRESH-START r50/r51/r52 re-spot-checked at the base (receipt
`.ufo/waves/round-59/before/freshstart-spotcheck.txt`: r50 FAIL 0/0/18, r51 evidence committed EMPTY, r52
FAIL 1/0/16) with five move classes ruled out for cause.

## Routed carry-in from the r58 closure (addressed first, not a claim)

- **D-R58-BEFORE-RECEIPTS-UNLANDED discharged at `81776bef`.** The three cited before-receipts were
  regenerated from the committed probe definitions (the r58 declaration's own plumbing commands; the r58
  report and lesson's census command) and landed under `.ufo/waves/round-58/before/`. Every r58 declared
  before-value re-derived exactly: cat-file rc 128, wevtutil sweep 0 files, SOURCES 271, literal T-rows 12,
  T13/T19/receipt-compared mentions 0, round58 registry heading 0, W-plane dated 0, stale `20 cases` 1,
  selftest 25/25 rc 0; freshstart r50 FAIL verdicts_ok 0 / marks_ok 0 / seats_ok 18, r51 evidence file
  0 bytes, r52 FAIL 1/0/16; census exit 0 with 42 W04. **Correction appended (the twice-repeated class
  closed with a named rule):** the r58 landed-changes table said "before-receipts (5)" but committed bytes
  cite exactly THREE distinct `round-58/before/` paths (`freshstart-spotcheck.txt`, `c1-c2-c3-at-base.txt`,
  `sources-census-start.txt` — SCORECARD:4051/4070/4083, LOG:2339, lesson:72, report:36/104); the remaining
  two of the five are named by no committed pointer anywhere in the lane, so no receipt can be regenerated
  for them without inventing a citation. Rule going forward: **a receipt count cited in a landed-changes
  table must equal the number of distinct receipt paths the round's committed bytes name — count the cited
  paths first, then write the count.** The r58 report itself lives in the FLEET repo (lane-unmutable); this
  lesson, the SCORECARD carry-in paragraph and the round report are the correction record. The regenerated
  census-start receipt carries a reconciliation header (the 271-row original predates the S272/S273 landing
  and is not byte-reproducible; the declared start values exit 0 / 42 W04 re-derive exactly).

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S274** — Microsoft Learn, `Task Scheduler error and success constants (WinError.h)` (Win32/taskschd,
  current), https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-error-and-success-constants .
  Opened 2026-11-01 by the L1 (HTTP fetch of the live page). Located quote (19 words, counted by `wc -w`
  before landing): "The constants that begin with SCHED_S_ are success constants, and the constants that
  begin with SCHED_E_ are error constants." Supporting located text: SCHED_S_TASK_READY 0x00041300 "The
  task is ready to run at its next scheduled time.", SCHED_S_TASK_RUNNING 0x00041301 "The task is currently
  running.", SCHED_S_TASK_DISABLED 0x00041302, SCHED_S_TASK_HAS_NOT_RUN 0x00041303 "The task has not yet
  run.", the 0x800413xx error-constant rows, the `net helpmsg` note for system/network error codes,
  Requirements row (Header WinError.h); frontmatter `ms.date` 2024-10-29, `updated_at`
  2024-10-29T23:32:00Z, `git_commit_id 008b6856680c0435cbb8b3761d128e84cf3a82ce`. The direct
  `task-scheduler-error-and-success-codes` URL returned HTTP 404 in the same session (recorded inside
  S274's row — nothing opened there, the S267/S273 precedent). The page documents the API HRESULT
  vocabulary, NOT the schtasks.exe display columns — the CLI mapping is measured (J1-J3 receipts).
  Used by `corpus/knowledge/windows-scheduled-task-status-plane-r59.md` — C1's sourced ground (with S261,
  opened 2026-10-31, reused).

Rejections this round: **0 — stated explicitly**: no source was opened and rejected; one lead never became
a row (the `task-scheduler-error-and-success-codes` 404 above — recorded inside S274's row, not a
rejection).

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0 at round
start AND round end (42 W04 duplicate-URL warnings at BOTH passes, 0 E-code; receipts committed at
`.ufo/waves/round-59/before/sources-census-start.txt` and `.ufo/waves/round-59/after/sources-census-end.txt`).
S274 was inserted at its id position inside `## Registry` (after S273), not appended at the file tail —
the R58-SOURCES-APPEND-POSITION rule applied on first use this time. Gates at the final tree `c4aa0f5c`:
knowledge-header PASS **75 notes / 0 findings**; registry-coverage PASS **96 tools / 96 rows / 0 findings**
(after the repair commit, see Mistakes); SCORECARD uniqueness ok rc 0; `RECEIPT_RUN_SELFTEST: PASS (7
cases)` and `RECEIPT_WRITE_SELFTEST: PASS (5 cases)` unchanged; `bash -n tools/recheck-eventlog-r59.sh`
rc 0.

Assimilation: `considerthese/` mined (latest 2026-10-26; seven notes, unchanged set since r57/r58 mined
them): the five self-improvement ideas remain aggregator/wave-class or Linux-host-class on this host;
nothing clears this round's bar; nothing adopted. The shokuknow register is not reachable from this host.
Assimilation: none — shokuknow unreachable.

## Mistakes

- **R59-ARM-FIRST-RUN** (class: the round's own new instrument failed its first run — judgment code, never
  the probes; the R58-RECHECK-EXTENSION-FIRST-RUN class recurring) — first run of
  `tools/recheck-eventlog-r59.sh` read `RECHECK_EVENTLOG: FAIL (2 drift)`: the E2b/E3b rows called
  `receipt-run.py` WITHOUT `--receipt`, and receipt-run's usage guard exits 2 (`--budget, --receipt and a
  command after -- are required`) before any probe runs. Captured-by: the first-run FAIL receipt committed
  under its honest name `.ufo/waves/round-59/receipts/recheck-eventlog-11-first-run-FAIL-2drift.txt`
  (bde06613 rule: FAIL kept beside the fixed pass, nothing substituted). Fix: spawn receipts go to a
  mktemp file deleted in the same leg (the T7 temp-dir precedent).
- **R59-RECEIPT-RUN-EXITS-ZERO** (class: the harness's exit code is not the child's exit code — judged
  from the wrong channel, caught by the second run of the same arm) — after the `--receipt` fix, E2b/E3b
  still drifted, now at rc=0: `receipt-run.py` REPORTS the child rc on the receipt's `rc=` line (and in its
  one-line summary) but its own process exit is 0 after executing a child — so `[rc]=$?` read the harness,
  not `wevtutil`. This second intermediate FAIL is named here rather than receipted: it was observed
  between two edits of the same uncommitted file and no byte receipt exists for it (the gap is itself
  recorded, per the honesty rule — an unreceipted intermediate observation is named, never silently
  dropped). Fix: judge the spawn receipt's `rc=` line (`grep -m1 '^rc=' <receipt> | cut -d= -f2`), never
  receipt-run's process exit; the fixed run passed 11/11, 0 drift.
- **R59-REGISTRY-TABLE-GAP** (class: an appended table whose carried rows are not CONTIGUOUS with the new
  row — a blank-line gap silently reverts the operative-table selection) — the round-59 superseding
  registry table was built by extracting the round-58 table block through the NEXT `## ` heading, which
  carried trailing blank lines INTO the new section ahead of the new row. The registry-coverage gate's
  parser stops at the first blank line after the table and reads the section from there — it parsed 95 rows
  (the round-58 set) and reported `REGISTRY-ROW-MISSING` for `tools/recheck-eventlog-r59.sh` at the work
  revision `2913b75d` while the round-59 table (96 rows) sat plainly in the file. Captured-by: the gate
  itself at the work revision (json receipt retained in scratch; the 95/95/1 reading is named in the
  after-battery). Fix: rows made contiguous (blank gap removed; diff `2913b75d..c4aa0f5c` shows only
  blank-line removals and the re-rendered Round-59 section — no row bytes changed; all 95 round-58 row
  names verified carried, exactly one name added); gate PASS 96/96/0 at `c4aa0f5c`. Rule: a superseding
  registry table is heading, intro, header, separator, ALL rows contiguous, nothing between the last
  carried row and the new row — run the gate BEFORE the work commit cites it.
- **R59-DECLARED-COMMAND-RECEIPT-SIDE** (class: the declared counting command reads a channel the
  instrument does not write — the R58-DECLARED-COMMAND class recurring, caught by running the declaration's
  own command before citing it) — the C3 declaration bound `grep -c "due 2026-11-30" <pass-receipt> >= 1`
  to the receipt; the instrument's receipt format carries only the rollup line, so the measured value is
  **0**. The due date lives in the NOTE's operative block (`grep -c "due 2026-11-30" <note>` = 1). Fix:
  the appended correction block in the after-battery re-targets that clause to the note (measured there);
  a `due=` line in the instrument's receipt header is the proper future fix, recorded as a planned item —
  not smuggled into the already-committed receipt bytes.
- **R58-carry-in correction, recorded per the closure's routing** (not a new defect this round): the
  "(before-receipts (5))" overcount and the three unlanded receipts — see the carry-in section above; the
  receipts landed at `81776bef`, the count rule is stated there, and every r58 cited pointer now resolves.

Sweep that found no further mistakes this round: before the outcome commit the round's files were re-read
against the declared predicates — the C1 note's receipt headers re-checked key by key (j1/j2/j2b/j3/j4/j5
all rc 0 through receipt-run), the S274 Gate quote recounted with `wc -w` (19), the SOURCES table re-run
through the malformed-row check (0) and the placement check (S274 inside Registry after S273), C3's
appended block diffed byte-identical against `c5a33d08` for the old prefix (sha256 09e7b6f2… recorded in
the after-battery), C2's declared counting commands all run before citation (11/11/11 + `rows=11`), the
registry-coverage and knowledge-header gates re-run at the final tree (96/96/0 and 75/0), and the declared
C3 receipt-side command run (read 0 — the correction above). The five mistakes above are the complete
defect set observed this round.
