# FxCritUniverse — C3 88-record / 17-path universe attack

## Verdict: FAILS (one concrete defect)

## Counterexample
`SKILL.md` (a covered primary file) carries a superseded current-use claim with
**no** R18-FRESHNESS record, falsified by the same S060 evidence the sweep used:

- Baseline `842a531…` SKILL.md:1123-1124 (also present at target):
  "`sar`/`atop`/`dool`/`dstat` absent, no `/var/log/sa`, `systemd-cgtop`
  live-only … **Report the missing capture capability as a standing row.**"
- R18 capture `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:84` lists
  `/usr/bin/sar`; `:87-88` shows `/var/log/sa` exists (empty). "sar absent" and
  "no /var/log/sa" are both false at R18; a consumer following the standing-row
  instruction writes a false row.
- The sibling plane `kill-event-deep-r8.md` was corrected for the **same
  premise** (R18-FRESH-SUPPLEMENT-11) — proof the sweep classed it as a
  current-use restatement — while the SKILL.md twin stayed unflagged.
- `check-appended-notices.py` cannot see this: it verifies declared records
  only (`_record_findings`); no completeness pass enumerates uncorrected stale
  loci. A PASS therefore never certifies "no residual stale claims in the 17
  paths." `distinct_paths` also counts paths of structurally invalid records.

## What survives
- Counts verified: 88 records, 49 primary across the 8 named files (10+12+3+11+
  10+4+6+3 minus… enumerates to 49), 39 R18-FRESH-SUPPLEMENT, 17 distinct paths.
- No all-host-fresh claim; dated observations marked historical (NoticeHealth-06
  cites R17 capture :59 correctly as a logged past event); pending count kept
  UNKNOWN (SUPPLEMENT-13/15/17, NoticeHealth-03); snapper records keep rollback/
  snapshot unverified (SUPPLEMENT-05-08, NoticePackages-09); no package/boot/
  service clearance asserted.

## Smallest safe correction
Append one record + notice in SKILL.md covering :1123-1124 (sar now resolves;
/var/log/sa exists-empty; atop/dool/dstat still unverified), and state the
checker verifies records, not sweep completeness.

Scope: executed=read-only git show/sed/grep of committed blobs; no writes outside this report
