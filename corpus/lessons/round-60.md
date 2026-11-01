# Round 60 — lesson (Windows host, base `5dd83fa3`; carry-in `e1e10178`, declaration `41c18296`, work `bef165c4`, addendum `6d65fc0f`; outcome and receipts follow)

Shape: single-session inline round (no wave/AgentSwarm dispatch surface on this host; the standing L0
questions `tsukuroi | round-53` (`.ufo/l0-questions.md:229`), the round-1 kaidoku/revenger scope (PROVINCE
Frontier), and `tsukuroi | round-57` (S266 interact authorization, `.ufo/l0-questions.md:247`) all stand
unanswered and were routed around, never treated as answered). Claims declared before any after-measurement
(SCORECARD "Round 60 — declaration"): C1 depth (sourced Windows registry READ plane, RG1-RG5), C2 operability
(the `--due` receipt anchor on both recheck arms), C3 calibration (the `tools/append-receipt.py` byte-stable
append verifier). FRESH-START r50/r51/r52 re-spot-checked at the base (receipt
`.ufo/waves/round-60/before/freshstart-spotcheck.txt`: r50 FAIL verdicts_ok 0 / marks_ok 0 / seats_ok 18,
r51 evidence committed EMPTY 0 bytes, r52 FAIL 1/0/16) with five move classes ruled out for cause. The r59
S274 post-declaration source-opening order was NOT kept this round: S275 was fetched live before the
declaration text was written, and the declaration discloses that order instead of claiming the precedent —
the row lands with the work commit, opened this round, quote counted (21 words by `wc -w`).

## Routed carry-ins from the r59 closure (addressed first, not claims)

- **R59-GATE-FAIL-RECEIPT-UNLANDED discharged at `e1e10178`.** The intermediate registry-coverage FAIL
  reading (95/95/1 at `2913b75d`) regenerated from the committed gate code at this base
  (`python tools/check-registry-coverage.py --revision 2913b75d`: registered 95, rows_total 95, findings 1
  REGISTRY-ROW-MISSING for `tools/recheck-eventlog-r59.sh`, status FAIL — exactly the recorded reading) and
  committed raw under its honest name `.ufo/waves/round-59/after/registry-coverage-FAIL-at-2913b75d.regenerated-r60.json`
  with a regeneration note. The r59 original run's JSON died with the round scratch; byte-equality to it is
  NOT claimed and cannot be checked — the receipt says so. PASS 96/96/0 re-run at `c4aa0f5c` and at the
  base. Routing rule named in the note: **a gate red state that is part of a repair story commits its raw
  receipt beside the correction in the same round, named FAIL + revision + original-or-regeneration.**
- **Byte-stable writers**: every append this round went through a binary-mode writer against the target
  file's own line-ending convention (SCORECARD CRLF, SKILL CRLF, SOURCES CRLF rows, LOG and the new files
  LF), and C3's instrument proves the property on committed bytes — work-tree pairs measured old-only 0/0
  raw and normalized, `--require-raw` exit 0. The tameshi additivity-receipt convention (r63) is the fleet
  precedent; tsukuroi's implementation credits it in the tool docstring and the registry row (ADJ-07: method
  advice, not gate ownership).
- **Whole-SKILL non-author SHONEN verification (owed since r55)**: operator's call — the L0 question
  `tsukuroi | round-60` appended to `.ufo/l0-questions.md`; the box marks stay untouched; routed around,
  never treated as answered.

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S275** — Microsoft Learn, `reg query` (Windows Commands, current reference),
  https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/reg-query .
  Opened 2026-11-01 by the L1 (live HTTP fetch of the page). Located quote (21 words, counted by `wc -w`
  before landing): "Returns a list of the next tier of subkeys and entries that are located under a
  specified subkey in the registry." (page lede). Supporting located text: the Syntax block
  (`reg query <keyname> [{/v <valuename> | /ve}] [/s] [/se <separator>] [/f <data>] [{/k | /d}] [/c] [/e]
  [/t <Type>] [/z] [/reg:32] [/reg:64]`); the `/v` parameter row ("Specifies the registry value name that
  is to be queried. If omitted, all value names for keyname are returned."); the `/s` row; the `/t` row's
  type set (REG_SZ, REG_MULTI_SZ, REG_EXPAND_SZ, REG_DWORD, REG_BINARY, REG_NONE); the Remarks
  return-value table (0 Success, 1 Failure — no message text). Frontmatter `ms.date` 2022-11-02,
  `updated_at` 2025-10-22T17:33:00Z, `git_commit_id 4282dd47a285a65de44c1512e8e9abd2384582a8`. The page
  documents the reg.exe CLI contract but NOT the absence message text or the forward-slash refusal (both
  host-measured, RG2/RG5), and its `/t` set omits REG_QWORD, which the host CLI accepts (rg4c receipt —
  the measured divergence, the documentation the stale side, the r59 J3 class). Used by
  `corpus/knowledge/windows-registry-read-plane-r60.md` — C1's sourced ground.

Rejections this round: **0 — stated explicitly**: no source was opened and rejected; no lead was carried
over from r59 (the only r59 lead, the `-codes` 404, is recorded inside S274's row, not reopened).

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0 at round
start (42 W04 duplicate-URL warnings, 0 E-code; receipt
`.ufo/waves/round-60/before/sources-census-start.txt`, verbatim capture) — the end receipt lands with the
final commit. S275 was inserted at its id position inside `## Registry` (line 284, directly after S274) —
the R58-SOURCES-APPEND-POSITION rule; the insert is a pure single-line insertion (old bytes byte-identical,
verified by the removal round-trip in the landing script). Gates at the work trees: knowledge-header PASS
**76 notes / 0 findings / 76 complete**; registry-coverage PASS **97 tools / 97 rows / 0 findings** (JSON
receipts at `bef165c4` under `.ufo/waves/round-60/after/`; the `6d65fc0f` addendum touches neither tools/
nor header keys; both gates re-run at the final tree in the receipts commit); SCORECARD uniqueness ok rc 0;
`RECEIPT_RUN_SELFTEST: PASS (7 cases)` and `RECEIPT_WRITE_SELFTEST: PASS (5 cases)` unchanged;
`bash -n tools/recheck-eventlog-r59.sh` and `bash -n tools/recheck-services-r56.sh` rc 0; the final
four-file append-receipt measurement lands in the receipts commit (receipt-after-subject, the tameshi r63
precedent — the outcome cannot measure its own commit's bytes before they exist).

Assimilation: `considerthese/` mined (latest 2026-10-26; seven notes, unchanged set since r57/r58/r59 mined
them): the five self-improvement ideas remain aggregator/wave-class or Linux-host-class on this host;
nothing clears this round's bar; nothing adopted. The shokuknow register is not reachable from this host.
Assimilation: none — shokuknow unreachable.

## Mistakes

- **R60-C1-DECLARED-GREP** (class: the declared counting command reads a shape the artifact does not have —
  the R58-DECLARED-COMMAND class, third occurrence, caught BEFORE the outcome cited it) — the C1
  declaration bound `grep -c "^| RG" <note>` ≥ 3; the note landed with the RG rows as `## RG1 — …`
  headings, so the declared command read **0** at the first work tree `bef165c4`. Captured-by: the
  R58-DECLARED-COMMAND rule (run the declaration's own command, on the channel it names, before citing it)
  — the battery ran it and measured 0. Fix: work addendum `6d65fc0f` adds the row-index decision table the
  declaration promised (RG1-RG5 rows with surface/invariant/drift-class/receipt columns — the grep now
  reads 5); the FAIL state is re-derived from committed bytes and receipted
  (`.ufo/waves/round-60/after/c1-declared-grep-first-run-FAIL-at-bef165c4.txt`), nothing substituted. Rule
  going forward: a declared grep binds to the artifact's DELIVERED shape — write the counting command
  against a fixture of the planned shape (or run it against a draft) BEFORE the declaration commits it.
- **R60-STRAY-RECEIPT** (class: a refusal-gate test leaked bytes outside the lane tree — the r53 D7
  anti-pattern in a new place) — the first malformed-`--due` check passed `--receipt /tmp/should-not-exist.txt`
  with `2026-13-45` under the then shape-only gate; the gate accepted the shape, the probes ran, and the
  arm wrote its receipt to /tmp (never citable, outside the lane). Caught by the battery's own expectation
  (rc 2 expected, measured 0). Fix: the gate on BOTH arms strengthened to calendar range (month 01-12,
  day 01-31; the exact month-length is deliberately NOT validated — documented in the arms' headers), the
  refusal fires at the argument gate BEFORE any probe runs and before any receipt write; the stray /tmp
  file deleted in the same session; the re-run refuses all three malformed shapes (`2026-13-45`, `30d`,
  `2026-11-3X`) with rc 2 and writes no receipt. Rule: a refusal-gate test names a receipt path inside the
  lane (or none), so a gate miss cannot leak bytes off-repo.
- **R60-SELFTEST-SHAPE** (named for the pattern, no committed byte ever carried it): the append-receipt
  selftest's first form ran 6 checks against the declaration's `APPEND_RECEIPT_SELFTEST: PASS (5 cases)` —
  caught pre-landing, the instrument reshaped to the declared 5-arm semantics (the rewrite arm binds both
  its exits) before any commit cited the string. Same class as R60-C1-DECLARED-GREP: the declared output
  string is a contract — make the artifact meet it before landing, not after.

Sweep that found no further mistakes this round: before the outcome commit the round's files were re-read
against the declared predicates — the C2 receipts re-checked key by key (`due=` counts 1/1/0, rows/matched/
drift 22/22/0 and 11/11/0, `due=2026-11-30` literal), the registry probe receipts re-read (rg1-rg5c rc and
message lines), the S275 Gate quote recounted with `wc -w` (21), the SOURCES table re-run through the
malformed-row check (0), duplicate-id check (none) and enum check (clean), placement verified (S275 at line
284 after S274), the SKILL registry table contiguity verified by the gate itself (97/97/0), the append
receipts measured (old-only 0/0, `--require-raw` exit 0), `bash -n` both arms (rc 0), the standing selftests
re-run (7/7, 5/5), and the protected surfaces diffed byte-identical to the base (README, PROVINCE, SHONEN,
QUALITY, AGENTS). The three mistakes above are the complete defect set observed this round.
