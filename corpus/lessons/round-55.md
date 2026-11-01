# Round 55 — lesson (Windows host, base `59a62bfe`; declaration `76b9d9e5`, work `3ac4b124`)

Shape: single-session inline round (unchanged since r53: no wave/AgentSwarm dispatch surface on this
host; the L0 question `tsukuroi | round-53` stands unanswered and was routed around, never treated as
answered; the round-1 contested kaidoku/revenger scope question likewise stands). The three routed
defects of closure `59a62bfe` landed first as repairs R1-R2 (R3 was "route the next T-probe through
receipt-run", which became C1's whole surface; defect-count framing: R1 = SCORECARD dedupe, R2 =
S265 correction row, defect 2 = the reissued receipts). Claims declared before any measurement
(SCORECARD "Round 55 — declaration"): C1 operability (reissued-r54 self-describing receipts), C2
depth (sourced `windows-services-plane-r55.md`), C3 calibration (`check-scorecard-unique-sections`
gate). All probes read-only; every repair operator-gated; receipts live in the lane tree, never
scratch. The FRESH-START ruled-out set (r50/r51/r52 spot-checks) is in the SCORECARD declaration.

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S263** — Microsoft Learn ARCHIVE, `Sc queryex` (Windows Server 2012 R2 library),
  https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dd228921(v=ws.11) .
  Opened 2026-10-31 by the L1 (HTTP fetch of the live page). Located quote (page thesis, 17 words,
  counted by `wc -w` before landing): "Obtains and displays extended information about the specified
  service, driver, type of service, or type of driver." Supporting located text: the Remarks
  displayed-fields list ending "…CHECKPOINT, WAIT_HINT, PID, and FLAGS" (the extended set), the
  equal-sign/space rules (same sentences as S262), and the frontmatter identity (`is_archived:
  true`, `ms.date` 2016-08-31, `updated_at` 2021-11-12, archive `git_commit_id
  5327995ac358bee6eaf26e4214a7ac52b67607f1`). The CURRENT Windows Server commands reference TOC
  (fetched same day, `git_commit_id ad6a18bd…`) lists only sc config/create/delete/query — queryex
  exists only in the archive. Used by `corpus/knowledge/windows-services-plane-r55.md` — C2's
  sourced ground.
- **S264** — Microsoft Learn ARCHIVE, `Sc qc` (same library),
  https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742055(v=ws.11) .
  Opened 2026-10-31 by the L1 (HTTP fetch of the live page). Located quote (8 words, counted by
  `wc -w` before landing): "Queries the configuration information for a specified service."
  Supporting located text: the Remarks displayed-fields list (SERVICE_NAME … SERVICE_START_NAME,
  which OMITS START_TYPE — the measured output displays it; recorded in row T11 as doc-list
  incompleteness, not smoothed), the qc/Services.exe/Svchost.exe shared-process note, and the same
  archive frontmatter identity as S263. Used by `corpus/knowledge/windows-services-plane-r55.md`.
- **S265** — correction note on S262 (same URL as S262, re-opened 2026-10-31 by HTTP fetch):
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-query . The
  page's Remarks sentence literally reads "TYPE, STATE (as well as states which are not available),
  WIN32_EXIT_B, SERVICE_EXIT_B, CHECKPOINT, and WAIT_HINT" (15-word fragment counted by `wc -w`);
  the tool prints WIN32_EXIT_CODE / SERVICE_EXIT_CODE (receipts r54 `t4-sc-active.txt`, r55
  `t9-queryex-wuauserv.txt`, `t11-qc-wuauserv.txt`), so the typo is on the page and S262's row is
  right about the tool — S262 stands, no supersedes. The same typo appears in S263's archived
  Remarks, so it is a library-wide sentence template. This is repair R2 (routed defect 3 of closure
  `59a62bfe`).

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0
at round start and round end (41 W04 warnings at start, 42 at end — the +1 is S265's same-URL
duplicate-URL warning, warning-class; no E-code either pass; receipts
`.ufo/waves/round-55/before/sources-census-start.txt` and
`.ufo/waves/round-55/after/sources-census-end.txt`).

Assimilation: `considerthese/` mined (latest 2026-10-26; the 2026-10-19..25 proposal files re-read
this round — none of the still-unimplemented proposals clears this round's bar: they are either
Linux-host-class work unavailable here or already superseded by admitted rounds). The shokuknow
register is not reachable from this host. Assimilation: none — shokuknow unreachable.

Rejections this round: **0 — stated explicitly** (line added round 56, carry-in 2 of the r55
verifier spot-check, closure `aeb268f3`): all three source records above are admits; no
`SOURCES.md` row was opened-then-rejected in round 55. No row quota applies (CORPUS contract v1
rule 4); the same-day S265 decision was a no-supersedes correction note on S262, not a rejection.

## Mistakes

- **R55-HEREDOC-TRUNCATION** (class: bulk content pushed through a shell heredoc without a
  post-write structural check) — the first attempt to append the round declaration to SCORECARD.md
  via a heredoc was cut off mid-line (the tool's terminator line was never recognized; the shell
  warned "here-document delimited by end-of-file" only after writing a partial section). Captured-by:
  reading the file tail before the commit step (the prompt's verify-after-write discipline), this
  round. Fix: large content is written to a scratch file first and appended with
  `cat file >> target`, followed by a structural check (`grep -c` for the section heading,
  `wc -l`, tail). The committed declaration landed whole.
- **R55-MSYS-NO-PATHCONV-SELF** (class: an env var set for one layer of a pipeline silently breaks
  a different layer) — invoking `MSYS_NO_PATHCONV=1 python tools/receipt-run.py …` (to keep the
  inner `/query`-style argv intact) also disabled MSYS's POSIX→Windows conversion for the
  instrument's own `/c/Users/...` script path, so python failed instantly with `can't open file
  'C:\c\Users\...'` (POSIX path passed through verbatim to a native binary). Captured-by: the
  probe's own immediate failure (P2 of the C1 battery), this round. Fix: paths passed TO the
  instrument are spelled Windows-style (`C:/...`); the `MSYS_NO_PATHCONV=1` prefix lives INSIDE the
  `bash -c` command string, where the receipt's `command=` line records it — which also makes the
  receipt self-documenting.
- **R55-ZERO-DUP-PREDICATE** (class: a gate predicate written from the routed defect's symptom
  instead of the defect's class) — C3's first design was "exit 1 on ANY duplicate level-2 heading",
  which made the honest fix a full dedupe. Diffing the three OTHER duplicate-heading pairs before
  removal (the r54-verifier had routed only the r54 pair) showed they are this file's
  declared-correction convention: the later copy's body names its predecessor and restates only the
  corrected rows — a zero-duplicate sweep would have DELETED historical rows (the round-26
  operability/freshness/calibration/adjacency cells live only in the "superseded" first copy).
  The round-30 second copy, by contrast, is a byte-exact 15-line prefix repost (`b == a[:len(b)]`)
  with no unique content. Captured-by: pre-removal `diff` of each pair's true section bodies, this
  round. Fix: only UNMARKED duplicates were removed (r54 first copy — one-word divergence, named in
  the correction block; r30 prefix repost), the three marked legacy pairs stay, and the gate's
  predicate enforces exactly that convention: a duplicate heading pair is a finding only when
  NEITHER body declares supersession. The gate's own limit (it cannot prove a marker true) is named
  in the tool docstring and the registry row.
- **R55-UGREP-PIPE** (class: counting one-liner written against a remembered grep, not the host's
  grep) — the battery's "every T row cites a source" check used `grep "a\|b" <(grep …)` (BRE
  alternation + process substitution); this host's `grep` is ugrep, which parsed the `/dev/fd/N`
  path as an option and errored. Captured-by: the battery receipt itself showing the error line,
  this round (the receipt keeps the failed line — a counting receipt that hides a failed counter
  would be self-flattering). Fix: the count was re-issued as a python check (4/4 rows cite
  S263/S264/S265 or a dated capture), and the receipt records the substitution.

Sweep that found no further mistakes this round: before the outcome commit the round's files were
re-read against the declared predicates (C1 11/11 receipts and each receipt's rc re-checked against
the r54 signatures — the only signature drift is the host's own: wuauserv RUNNING today vs STOPPED
in r54, and 109 vs 110 active services, both the documented drift class; C2's four rows, header
trio and per-row citations re-read; C3's correction block re-read against the diff evidence; the
word counts of all three Gate quotes re-run). The four mistakes above are the complete defect set
observed this round.
