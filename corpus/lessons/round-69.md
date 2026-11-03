# Round 69 — lesson (tsukuroi, hyaku run 15, attempt 1)

author: tsukuroi L1 (round 69), integrating the wave `.ufo/waves/round-69/` (13 seats, one v1 wave)
basis: declaration `920a9eea` (frozen before data; base `acce353b`); the pre-data receipts in
`.ufo/waves/round-69/before/`; wave results `.ufo/waves/round-69/w1-results.json` and the seat
receipts in `.ufo/waves/round-69/w1/` and `.ufo/waves/round-69/probes/`.

## Gate

**Trigger and sources.** Two source documents were fetched before the declaration text and committed
byte-exact under `.ufo/waves/round-69/before/src/`:

1. Linux v7.2.11 stable `Documentation/admin-guide/tainted-kernels.rst` — sha256 `727ddb82…841`
   (`.ufo/waves/round-69/before/src/SHA256SUMS`, `sha256sum -c` rc 0). **Admitted as S288, as a
   re-pin**: the bytes are byte-identical to S140's torvalds v7.2 snapshot (`cmp` rc 0,
   `.ufo/waves/round-69/probes/l1/s288-vs-s140.txt`), so no new document content is claimed; the row
   exists so the entry's applicability claim cites the tag the host runs, following the registry's
   re-pin convention (S280/S281, round 64). The teaches cell says `supersedes S140 — re-pin:`.
2. Linux v7.2.11 stable `include/linux/vermagic.h` — sha256 `0556c28f…aea`. **Admitted as S289**:
   no prior registry row exists for this file (`git grep -in vermagic corpus/SOURCES.md` before the
   append → no row), and the lane held only an observed string (`driver-firmware-plane.md:85`), never
   the composition rule. A second fetch route (`raw.githubusercontent.com/gregkh/linux/v7.2.11/…`)
   reproduces both files byte-for-byte (`.ufo/waves/round-69/probes/S1Scout-sources.md` §2).

**Candidates refused in-round.** (a) A second torvalds-v7.2 registration of `tainted-kernels.rst` —
the same bytes as S140, adding no authority; refused. (b) An `own-work` capture row for the host
readings — QUALITY 86: an own-work row may carry a host observation and never verifies a rule;
refused. (c) A row for `MODULE_ARCH_VERMAGIC` from `<asm/vermagic.h>` — the value is not inside the
pinned bytes; named as a limit of the note instead of sourced.

**The round's own novelty check failed and was caught by a seat.** The declaration presented the
"kernel taint, vermagic and module-tree plane" as new depth. It was not: `corpus/knowledge/
kernel-taint-r27.md` already holds KT1-KT6 (the same `12288 = bits 12 + 13` decode on this host,
per-module taint, clearing, reporting) with S140-S145. The connector seat enumerated 19 duplication
loci across 15 files (`probes/C1Connector/overlap.md`) and the C1 reviewer refused KR1/KR2 as
additive depth evidence (`probes/R1Reviewer/attack.md`). The integrator restructured the note so
four rows carry the new mechanism and host binding and one row states the re-grounding, and the
depth verdict is reported as **unchanged**, not improved. See Mistakes 1.

**Non-author checks on record.** `S1Scout` independently re-fetched both documents by a second route,
extracted the 0-19 table (20 rows, numbers `2^bit`), decoded 12288 to bits 12 and 13, and reproduced
the host vermagic string from the pinned macro (`probes/S1Scout-sources.md`). `R1Reviewer`
re-derived every row's digest and quote from the bytes and graded each row additive /
re-grounding / duplicate. `C1Connector` proved the S288/S140 byte identity and found two stale
contradictions in the lane's own notes (`update-safety-note.md:296-298`,
`host-health-report-r3.md:320`, both carrying a 7.2.3 pairing), repaired by appended errata this
round. These are seat checks; the closure judge's outside spot-check is still owed.

**The one seat finding not accepted.** The connector reported the wave spec's base string as "41 hex
chars (trailing 9)". Measured: `echo -n acce353bacad74043636018d829e9e9b8e0fdf1c | wc -c` → `40`, and
that is the base commit this round measures from. Recorded here rather than propagated into the
report.

**Census.** Round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi` → rc 0, 287 rows (`before/census-before-receipt.txt`). Round end: rc 0, 289 rows
(`after/census.txt`).

**QUALITY 98 watch (standing duty).** The upstream release trigger fired on Linux v7.3. S243's
v7.2.11 `fs/btrfs/sysfs.c` pin (`ce146120…`) re-read at the v7.3 stable tag → digest `098cb522…`,
**changed**, equal to S287's torvalds-v7.3 pin; the single v7.2→v7.3 change is the comment line
outside S243's registered ranges (round-68 S287 finding). No contradiction in
`btrfs-scrub-record-r44.md` or `btrfs-scrub-grounding-r45.md` was measured; the re-read is recorded
in `.ufo/waves/round-69/before/s243-v73-recheck.txt` with an appended correction that no seat
re-verifies S243 this round.

## Mistakes

- **R69-DECLARATION-NOVELTY-UNCHECKED** — class `declaration-overclaim` · evidence: SCORECARD round-69
  declaration, C1 "the kernel taint, vermagic and module-tree plane measured against this host";
  `corpus/knowledge/kernel-taint-r27.md:19` already states `12288 = bit 12 (O) + bit 13 (E)` and
  KT1-KT6 hold the mechanism with S140-S145; `probes/C1Connector/overlap.md` lists 19 loci in 15
  files; `probes/R1Reviewer/attack.md` "KR1 DUPLICATE; KR2 RE-GROUNDING". The premise was written
  without the one command that would have shown it (`git grep -n 'taint\|vermagic' -- corpus/`) ·
  captured-by: none at freeze; the connector and reviewer seats caught it after the wave · fix:
  QUALITY 102 clause (b) makes the held-ground sweep a pre-freeze duty; the note is restructured to
  four additive rows plus one re-grounding row; the depth verdict is reported as unchanged.
- **R69-DECLARED-BOILERPLATE-KILL** — class `spec-overreach` · evidence: the wave item E2Counter told
  the seat that a boilerplate six-row note "must not reach 5", while the frozen predicate counts the
  statement's words only (`KR_VERIFIED >= 5`, clauses id/unique-id/statement/source/snapshot/digest/
  quote). The seat measured the acceptance and refused to add semantic filtering
  (`w1/E2Counter.md`; `probes/E2Counter/battery.txt`: the well-formed control reads 5, the five
  malformed fixtures read 3 or 4, the boilerplate fixture reads 5) · captured-by: the declaration's
  kill rule, which names five malformed fixtures and no boilerplate arm · fix: the limit is stated in
  the counter's SKILL registry row and in the report; no predicate change after data; a
  content-sensitivity class for statements is routed to the next frozen-counter amendment.
- **R69-HOST-FACT-DRIFT-SUPERSEDES-HELD-NOTES** — class `freshness-drift` · evidence:
  `corpus/knowledge/update-safety-note.md:296-298` and `host-health-report-r3.md:320` both carry a
  7.2.3 kernel pairing with "no reboot is pending"; the host now runs 7.2.11
  (`before/host.txt`) · captured-by: the connector's lane-duplication scan, not the freshness
  cadence · fix: appended dated errata in both notes naming the stale sentences and the superseding
  measurement; the predicate and its transform now live in the round-69 entry.

## Trend verdicts

- **expansion: improved.** One new registry row on ground the lane never held (S289, the vermagic
  header), one re-pin row (S288) with its reason stated, one knowledge entry (KR1-KR5), and one new
  capability — the census `KERNEL` arm with 192 selftest cases (177 → 192).
- **quality: improved.** The r68 routed shape-only-counter debt is answered by a content-sensitive
  counter frozen before data with a five-fixture battery (`probes/E2Counter/battery.txt`); the r68
  closure's declaration-hygiene routing lands as QUALITY 102 with a checklist that finds the round-68
  block's three defects by name; two stale kernel-pairing sentences are corrected by appended errata;
  the census arm is neutral (live diff: timestamps, time-varying counters and the new line only).
- **discernment: unchanged.** The lane declared a novelty it did not have and the wave caught it; the
  entry was restructured, not relabelled. No non-author admit/reject spot-check is recorded in this
  lesson; the closure judge's is owed (LEARNING.md: a seat this lane dispatched is still the lane).

## Considerthese

Mined one proposal: **Downstream patch-offset check**, `considerthese/2026-10-26.md` (opened this
round), which asks the lane to flag knowledge anchors citing upstream line numbers for code the host
runs as a patched Arch build. Landed as QUALITY 103: a line pin taken from an upstream tag is not a
host-build line number, and an entry that cites upstream lines for code the host runs states that
the offsets are unverified. The round's own entry is the worked case: S289's anchors are tag line
numbers, while the host's modules come from Arch's `linux 7.2.11.arch1-1` build, which may carry
patches; the entry cites no host-side line numbers and says so in Limits. Other proposals remain
untouched.

## Sources

- **S288** — Linux v7.2.11 stable `Documentation/admin-guide/tainted-kernels.rst`, opened 2026-11-03,
  kind `docs`, tier A, `mined`, re-pin of S140 (bytes identical); used by
  `corpus/knowledge/kernel-taint-plane-r69.md`.
- **S289** — Linux v7.2.11 stable `include/linux/vermagic.h`, opened 2026-11-03, kind `code`, tier A,
  `mined`; used by `corpus/knowledge/kernel-taint-plane-r69.md`.
