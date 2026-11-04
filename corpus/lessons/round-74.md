# Round 74 — unit-fragment reading; literal claim error and routed repairs

Declaration `e51fb49d1790ef283b6aad6752a8c12fac347377`; true base
`d749a625b3054b7cb3435983fb9626ab3d0ed0c4`. The declaration's other full-base suffix is invalid.
C1 depth is **not verified as declared**: its volume alias set contradicts v262. The landed note
states the true timer/path set, reviewed by R1Reviewer. A lexical counter PASS does not rescue that claim.
C2 freshness repairs both r73 defects by append-only prose, under the unchanged frozen instrument.
No axis score uplift or admission is self-awarded; closure belongs to the outside verifier.

## Gate

All sources opened 2026-11-04. Three upstream v262 snapshots were pinned before declaration
under `.ufo/waves/round-74/before/src/`, with SHA256SUMS and SOURCES.json. S1Scout independently
re-fetched all three (HTTP 200, identical digests; `w1/S1Scout/receipts/refetch_summary.txt`).
Host systemd reports 262.1-1-arch; upstream code lines are not claimed to be Arch-patched line numbers.

| row | URL | located quote (at most 25 words) | disposition |
|---|---|---|---|
| S309 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.c | :416, "Search paths are ordered by priority (highest first), and we need to maintain this order." | mined, UF1-UF2 |
| S310 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/load-fragment.c | :6250, "don't allow perpetual units to ever be masked" | mined, UF5-UF6 |
| S311 | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/unit-file.h | :26-32, "return IN_SET(type, UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH);" | mined, UF3-UF4 |
| S312 | https://wiki.archlinux.org/title/Systemd | HTML title, "systemd - ArchWiki"; opened body 152032 bytes, HTTP 200 | rejected: administrative overview lacks code-level contracts; flip: locate an Arch-specific rule absent upstream |
| S313 | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit-load.c | HTTP status 404 (no source-content quote available) | rejected/unreachable, not fabricated: neither candidate core/shared path was available; flip: file available at a later tag |

S313's unavailable payload cannot provide a located content quote; that is disclosed, not represented
as a successfully quoted source. S312 title and refusal measurements: `w1/SC2Sources/rows.md:33-51`,
`w1/S1Scout/receipts/rejections_receipt.txt`; its fetched body is retained by S1Scout.
Three mined sources are tier A; refusals are tier B (S312) and A (S313). S309-S311 used-by the new note.
No pre-existing status, recheck or used-by field changed. Registry 308→313; notes 91→92.
Census start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
exit 0 with W04 duplicate-URL warnings only. End receipt is under round-74/after/.

## Search log

Question: which v262 code resolves unit names and alias symlinks, and how are masking and builtin
fallback handled? Searched the three pinned files and the registry for their basenames/symbols;
opened the ArchWiki administration page and tested candidate unit-load.c paths. Identified/screened
5 registry candidates, included 3, rejected 2. Stop: the pinned implementations ground all six true
rows, while the secondary overview and unavailable path add no rule authority. S309's draft anchor
misnamed the validation function; production uses `unit_validate_alias_symlink_or_warn`.

Assimilation: none. The prior open L0 tsukuroi round-64 collision quarantine is not treated as answered.
`considerthese/2026-10-26.md` reopened: counter-attack scoreboard and correction propagation proposals
motivate the attack ledger below; already-covered proposals are not relabelled newly implemented.

## Mistakes

- **R74-DECL-ALIAS-SET** · evidence R1Reviewer report F1 and unit-file.h:25-32 · captured-by
  source entailment / QUALITY 86 · fix: true six-type set landed, declaration explicitly not verified.
  Able to fail: reviewer rejects the literal volume statement but entails actual UF3.
- **R74-BASE-OID** · evidence R1Reviewer F2 and E2Routed base receipt · captured-by commit identity
  check, absent initially · fix: true full base appended; all measurements use real d749a625.
  Able to fail: cat-file rejects fabricated suffix; both counters otherwise vacuously emit expected
  before numbers on a nonexistent tree. Counts alone must not stand for object existence.
- **R74-C2-FIRST-MATCH** · evidence R2Reviewer HIGH-1, G1/G2 CLI fixtures, E2Routed Form A/B ·
  captured-by appended-shape control (missing from selftest) · fix: append honest unheaded correction
  inside existing last Round-73 block, leaving instrument frozen. Able to fail: headed EOF correction
  fails while Form A passes on the same original bytes. A general checker repair is not claimed.
- **R74-LEXICAL-NONREADER** · evidence E1Counter scripted-note and counter-runs; K1Critic D5/D6 ·
  captured-by QUALITY 88 / non-reader control · fix: separate mechanical counts from reviewed truth;
  C1 receives no frozen claim credit, R1Reviewer reviews actual note. Able to fail: opposite statements,
  duplicated content and unanchored quotes pass mechanical counter; semantic review refuses false set.
- **R73-GATE-QUOTE-LINE-DRIFT** · evidence r73 verifier §6.1 · captured-by located-quote rule · fix:
  appended lesson Correction 3 with install.c:2383 and three narrower S304 ranges. Able to fail:
  R2Reviewer omissions L1-L4 and E2Routed P3a-P3e each yield stale under the frozen checker.
- **R73-LOG-COUNT-STALE** · evidence r73 verifier §6.2 · captured-by corrections sweep · fix:
  append final 13/14 counts naming superseded 12/11 and r73 instruments. Able to fail:
  R2Reviewer G7/G8 omit superseded or final counts and yield stale (controlled fixtures).
- **Late protocol loading / incomplete wave context** · evidence SCORECARD r74 errata · captured-by
  load-order and scratch/pacman context rules · fix: disclose, load required contracts before further
  integration; no retroactive compliance asserted. Quota deaths are recorded by wave results.
- **L1 mechanical tooling error** · evidence this round transcript · captured-by edit tool warning ·
  fix: an incorrect selftest patch replaced unrelated evaluate lines, then was repaired before freeze;
  actual selftest control failed 12/13 first and passed 13/13 after repair. The script printed PASS
  even on a failing aggregate; exit code 3 was decisive. This misleading label remains a named defect
  in the frozen instrument, not a false claim of all-green first attempt.

## Attack ledger / verdict limits

E1Counter: 27 cases (mirror, scripted writer, three semantic blind spots, 22 isolated violations);
scripted writer and blind spots pass the lexical predicate. R2Reviewer: 20 cases, including headed
append shadow, numeric superstrings, direction inversion and wrong-instrument attribution. K1Critic:
entailed snapshot-count conjunct and dead own-work disjunct are redundancy, not independent kills.
C2 contains literal solution text in selftest. These limits remain visible; instruments unchanged.
M1Mutation evidence, if completed, is under its seat path and final wave results, not inferred here.

The report is filed only after WAVE-DONE. Dead/quota seats are not replaced or called successful.
No new capability row is claimed; no service or package transaction was performed.
