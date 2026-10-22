# Round 26 — lesson (tsukuroi, attempt 1, 2026-10-22)

author: TsukuroiR26 (L1). Claim base `e9f5356cd68c9281d07a22e54d1bfd72b12306ac`; declaration `b13e991fb96972b423b868ba122187f75357368c`; tools pinned with the refinements at `4de2b6b1c0cde1f7c7ca9e5727965bcf6aa6ba9e`. The canonical protocol files were read and their sha256 recorded in the declaration commit before any wave (routed defect 6, closed this round; verified by wave-1 RevCanonicalDigests).

## Gate

Candidates considered: the btrfs-progs v7.1 documentation for device stats, scrub (and the chapter it includes), and block group profiles; the packaged scrub timer; the Linux v7.2 btrfs device-stats and sysfs code; the smartmontools 7.5 NVMe printer; the NVM Express Base Specification 2.4; and three systemd v262 and Linux v7.2 pages re-opened to correct round-25 rows. Opened by wave-1 seats SrcBtrfsDeviceDoc, SrcBtrfsScrubDoc, SrcBtrfsProfilesDoc, SrcBtrfsScrubUnit, SrcKernelVolumes, SrcKernelSysfs, SrcSmartNvmeprint, SrcNvmeLifetimeFields, ScribeSupersedeTeaches and ScribeGateS126S127, and by the L1 (S139). Every quote below was checked by the L1 as a whitespace-normalised substring of the committed snapshot under `.ufo/waves/round-26/sources/` (S126 and S127 against the seat's re-fetched copies), and every snapshot's sha256 is in its row's anchor cell.

Admitted rows (all `mined`, opened 2026-10-22, recheck `on-release`): S128 to S135 and S139 (tier A, used-by `corpus/knowledge/storage-health-r26.md`); S136, S137 and S138 (tier A, superseding S121, S122 and S118, used-by `corpus/knowledge/memory-pressure-r25.md`). The S126 and S127 records below are the Gate records round 25 owed (routed defect 2).

| Source | URL | Opened | Located quote (at most 25 words) | Location |
|---|---|---|---|---|
| S128 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-device.rst | 2026-10-22 | "corruption_errs" | btrfs-device.rst line 254, entry row SH1 |
| S128 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-device.rst | 2026-10-22 | "A block checksum mismatched or a corrupted metadata header was found." | btrfs-device.rst line 255, entry row SH1 |
| S128 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-device.rst | 2026-10-22 | "Since kernel 5.14 the device stats are also available in textual form in" | btrfs-device.rst line 260, entry row SH1 |
| S133 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c | 2026-10-22 | "static ssize_t btrfs_devinfo_error_stats_show(struct kobject *kobj," | fs/btrfs/sysfs.c line 2074, entry row SH1 |
| S132 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/volumes.c | 2026-10-22 | "stats->values[i] = btrfs_dev_stat_read(dev, i);" | fs/btrfs/volumes.c line 8490, entry row SH1 |
| S132 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/volumes.c | 2026-10-22 | "called from commit_transaction. Writes all changed device stats to disk." | fs/btrfs/volumes.c line 8352, entry row SH2 |
| S132 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/volumes.c | 2026-10-22 | `"bdev %s errs: wr %u, rd %u, flush %u, corrupt %u, gen %u",` | fs/btrfs/volumes.c line 8429, entry row SH2 |
| S132 | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/volumes.c | 2026-10-22 | "return; /* all values == 0, suppress message */" | fs/btrfs/volumes.c line 8446, entry row SH2 |
| S128 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-device.rst | 2026-10-22 | "The device stats keep persistent record of several error classes related to" | btrfs-device.rst line 231, entry row SH2 |
| S139 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst | 2026-10-22 | "On filesystems that use replicated block group profiles (e.g. RAID1), read-write" | ch-scrub-intro.rst line 13, entry row SH3 |
| S139 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst | 2026-10-22 | "scrub will also automatically repair any damage by copying verified good data" | ch-scrub-intro.rst line 14, entry row SH3 |
| S139 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst | 2026-10-22 | "be validated and corrected by scrub, the actual file data is not." | ch-scrub-intro.rst line 24, entry row SH3 |
| S130 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst | 2026-10-22 | "For example, a SSD drive can remap the blocks internally to a single copy--thus" | mkfs.btrfs.rst line 639, entry row SH3 |
| S129 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-scrub.rst | 2026-10-22 | "*  *Uncorrectable* -- errors detected at read time but not possible to repair from other copy" | btrfs-scrub.rst line 190, entry row SH3 |
| S130 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst | 2026-10-22 | "The mkfs utility will let the user create a filesystem with profiles that write" | mkfs.btrfs.rst line 635, entry row SH3 |
| S139 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst | 2026-10-22 | "The scrubbing status is recorded in :file:`/var/lib/btrfs/` in textual files named" | ch-scrub-intro.rst line 71, entry row SH4 |
| S139 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst | 2026-10-22 | "recommended period is a month but it could be less." | ch-scrub-intro.rst line 68, entry row SH4 |
| S139 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/ch-scrub-intro.rst | 2026-10-22 | "Such automatic repair is also carried out when reading metadata or data from a" | ch-scrub-intro.rst line 17, entry row SH4 |
| S131 | https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/0c0a4d77b318084ecd35aeeb6888d8a5b4d6e3e0/btrfs-scrub@.timer | 2026-10-22 | "OnCalendar=monthly" | btrfs-scrub@.timer line 5, entry row SH4 |
| S129 | https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-scrub.rst | 2026-10-22 | "Show status of a running scrub for the filesystem identified by *path*" | btrfs-scrub.rst line 133, entry row SH4 |
| S134 | https://github.com/smartmontools/smartmontools/blob/RELEASE_7_5/smartmontools/nvmeprint.cpp | 2026-10-22 | `(!w ? "PASSED" : "FAILED!"));` | smartmontools/nvmeprint.cpp line 451, entry row SH5 |
| S134 | https://github.com/smartmontools/smartmontools/blob/RELEASE_7_5/smartmontools/nvmeprint.cpp | 2026-10-22 | `jout("- available spare has fallen below threshold\n");` | smartmontools/nvmeprint.cpp line 459, entry row SH5 |
| S134 | https://github.com/smartmontools/smartmontools/blob/RELEASE_7_5/smartmontools/nvmeprint.cpp | 2026-10-22 | "print_critical_warning(smart_log.critical_warning);" | smartmontools/nvmeprint.cpp line 840, entry row SH5 |
| S135 | https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf | 2026-10-22 | "the life of the controller and is retained across power cycles unless otherwise specified." | NVMe Base Specification 2.4, SMART / Health Information log page, excerpt line 14, entry row SH6 |
| S135 | https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf | 2026-10-22 | "Note that this field was previously named Unsafe Shutdowns." | excerpt line 258, entry row SH6 |
| S135 | https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.4-Ratified-2026.07.31.pdf | 2026-10-22 | "Entries over the life of the controller." | excerpt line 276, entry row SH6 |
| S134 | https://github.com/smartmontools/smartmontools/blob/RELEASE_7_5/smartmontools/nvmeprint.cpp | 2026-10-22 | `jout("Unsafe Shutdowns:                   %s\n", le128_to_str(buf, smart_log.unsafe_shutdowns));` | smartmontools/nvmeprint.cpp line 528, entry row SH6 |
| S136 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml | 2026-10-22 | "systemd-oomd.service will monitor this unit's cgroup and evaluate the specified rulesets against it." | systemd.resource-control.xml lines 1643-1644, tag v262 (tag-free text) |
| S137 | https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml | 2026-10-22 | "Cgroups of units with ManagedOOMSwap= or ManagedOOMMemoryPressure= set to kill will be monitored." | systemd-oomd.service.xml lines 43-44, tag v262 (tag-free text) |
| S138 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst | 2026-10-22 | "Note that all fields in this file are hierarchical and the file modified event can be generated due to an event down the hierarchy." | cgroup-v2.rst lines 1474-1476, tag v7.2 |
| S126 | https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | 2026-10-22 | "Defaults to 60%." | oomd.conf.xml line 190, tag v262; re-fetched bytes sha256 36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617 equal the S126 anchor (round-25 row; Gate record owed from round 25) |
| S126 | https://raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml | 2026-10-22 | "Defaults to 30 seconds when unset or 0." | oomd.conf.xml line 202, tag v262 |
| S127 | mori-shokunin/corpus/knowledge/system-pressure-r24.md at commit 4f05dd5a (blob d4ccce4262d8224e362da65eb5ba4b851ad0fea2) | 2026-10-22 | "records what those files are, exactly which shapes the kernel emits, which error codes the kernel returns," | line 46, section Scope; re-read bytes sha256 5d3a322aadb00c6ba3700b6c5b31d4e5b5305b404731f0eb37a5a3474c019ce5 equal the S127 anchor (round-25 row; Gate record owed from round 25) |

Rejected or not registered:

- `kdave/btrfs-progs` v7.1 `units/btrfs-scrub@.timer`: HTTP 404; upstream v7.1 ships no systemd unit (SrcBtrfsScrubUnit). Registered instead as S131 from the Arch packaging repository at `7.1-1`, byte-identical to the installed unit. Flip: none needed.
- The NVMe specification PDF bytes as a snapshot: the text is compressed, so no quote is a substring of the fetched bytes (SrcNvmeLifetimeFields, CritClaimSizing). The committed S135 snapshot is a `pdftotext` excerpt; the PDF digest stays in the anchor. Flip: a text edition of the specification.
- Linux v7.2 `include/linux/nvme.h` and nvme-cli v3.1 smart-log documentation: not opened as rows; the primary specification was reachable, so the fallback was not needed.
- btrfs-progs v7.1 `Documentation/ch-sysfs.rst` (fetched by SrcKernelSysfs as a supporting read): not registered; S128 line 260 and S133 already carry the sysfs mirror. Flip: a row that needs the sysfs file list.
- Mori's committed copy of `fs/btrfs/sysfs.c` (`mori-shokunin` commit `c1e8b81`): same sha256 as S133 (ConnSiblingOverlap); not registered as a separate row, since mori used it for quotas and this lane for error counters.

Registry recheck log (old -> new): none. No existing row changed `status`, `recheck` or `used-by` this round; S136 to S138 are new rows, so the superseded rows S121, S122 and S118 stay as written.

Spot-check result: owed to the non-author closure; not self-granted.

## Routed defects from the round-25 spot-check

| Defect (spot-check line) | Disposition this round |
|---|---|
| 1 Undisclosed in-place edit of `SCORECARD.md:51` (103) | Fixed by an appended correction in `SCORECARD.md` (section `Round 26 correction to the round-25 record`), quoting the original wording and naming both round-25 in-place edits; Mistakes R26-UNDISCLOSED-INPLACE; QUALITY 60. |
| 2 S126 and S127 lack Gate records (104) | Fixed: Gate records above, from sources re-opened this round with digests equal to the anchors; Mistakes R26-GATE-RECORD-MISSING; QUALITY 61. |
| 3 C1 ordinal checks satisfiable by the round's own prose; live counts drift (105) | Fixed in check set v2: K01 to K06 read only measured-outcome sections of any round (refinement after CritC2Construction showed that excluding only the declaring round still let earlier plan prose certify ordinals). The round-26 axes table states counts at the revision that adds it; the tool always measures at the revision given. Mistakes R26-SELF-REFERENT-ORDINAL; QUALITY 62. |
| 4 Harden the C2 memory-pressure checker (106) | Assigned to wave-1 ExecMemCheckerHarden in its own clone; its outcome (tool hardening and the replay of the 17 round-25 mutants) is appended to this lesson in a later commit of this round, or the lesson records why it did not land. |
| 5 Seat push and seat wake-writes (107) | Fixed in contexts: executor clones have push URL `/nonexistent/no-push-to-lane`, every wave context forbids seat-to-seat messages, `jj-lane.sh state` showed `ahead=0` before each helper commit (wave-1 RevRouted5Bounds verified the clones, the context and `ahead=0`). |
| 6 Late canonical load (108) | Fixed: seven sha256 values recorded in the declaration commit `b13e991f` before any wave; RevCanonicalDigests re-derived all seven and the commit time. |
| 7 SHONEN boxes 3 and 4 cite superseded or untested notes (109) | Fixed in text and counted by new checks K24 to K27: boxes 1, 3 and 4 no longer cite `corpus/knowledge/root-dac-decision-r12.md` (superseded at its line 7) or the round-12 PROVINCE paragraph as current. All boxes stay `[~]`. Box 4's repair is not counted by any check (K27 reads only corpus notes). |
| 8 S121, S122 and S118 teaches cells overstate or omit (110) | Fixed by superseding rows S136, S137 and S138 and an appended note in `corpus/knowledge/memory-pressure-r25.md`. |

## Record of in-place edits this round

Three evidence lines of `SHONEN.md` (boxes 1, 3 and 4) were replaced; the box lines and marks are unchanged. Old lines, for the record:

- Box 1: `Author-side evidence: SKILL.md health-verdict table, error classes, update-safety checklist and round-12 root-metadata procedure; corpus/knowledge/root-dac-decision-r12.md. Non-author verification remains owed.`
- Box 3: `Author-side evidence: corpus/knowledge/adjacency-handoffs-fleet-r1.md sections 4-5 and corpus/knowledge/root-dac-decision-r12.md; whole-SKILL post-append no-oral-context retest remains unverified (corpus/knowledge/executor-test-sufficiency.md).`
- Box 4: `Author-side evidence: PROVINCE.md round-12 refinement and .ufo/waves/round-12/resumed/OverlapHostR.md; OS diagnosis remains here, reusable verification methods and recipient acceptance are not claimed.`

New lines come from wave-1 ScribeShonenBoxes. No other non-append change was made to `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md` or `SHONEN.md`; the sweep `git diff -U0 e9f5356c <REV> -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` prints exactly those three lines.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R26-UNDISCLOSED-INPLACE | disclosure | `c93bd70f` changed `SCORECARD.md:51` ("loop with its mismeasure rows" to "loop for rounds 1 to 9"); the round-25 lesson recorded only the SHONEN edit | none (the append-only rule in PROTOCOL covers LOG.md; no lane check compared disclosed edits with the diff) | QUALITY 60: the lesson lists every removed line of the append-only and canonical files, and the sweep command above must print exactly that list. Red before: at `b9046016..e9f5356c` the sweep prints 2 lines while the round-25 lesson disclosed 1. |
| R26-GATE-RECORD-MISSING | curation | S126 and S127 were added in round-25 wave-2 repairs; `grep -c S127 corpus/lessons/round-25.md` is 0 | CORPUS SOURCES rule 1 (no mechanical check) | QUALITY 61; the round-26 checker blocks a row whose cited source has no Gate quote (`SH-GATE-QUOTE-MISSING`, selftest case and wave-2 mutants). Red before: the same grep exits with 0 matches. |
| R26-SELF-REFERENT-ORDINAL | measurement | At `157ee255` K01, K04 and K05 resolved to round-25 declaration lines 793, 807 and 792 (spot-check line 62) | QUALITY 57 (partly: it required re-measurement, not dated records) | QUALITY 62; v2 reads only measured-outcome sections. Red before: the v1 tool at `e9f5356c` reports K01 from `SCORECARD.md:793`, a declaration line; v2 at the same revision reports `SCORECARD.md:730`, a measured-outcome line. |
| R26-PREMISE-BEFORE-SOURCE | stale-premise | The declaration at `b13e991f` named smartctl's deciding fields, an upstream path for the scrub timer and a PDF snapshot before the sources were opened; S134 lines 450-451 and 840-842, the 404 on `units/`, and the compressed PDF contradicted all three (SrcSmartNvmeprint, SrcBtrfsScrubUnit, SrcNvmeLifetimeFields) | none | QUALITY 63; refinements were appended before any measurement and the targets were not changed. Red before: the declared SH5 wording is false against S134 line 451. |
| R26-GATE-COLUMN-OFFSET | tool | The pinned `tools/check-storage-health.py` reads a Gate row from the column after `Opened` onward (its cell spans keep the empty leading cell), so a plain unquoted quote is not found; quoted values work because the scan runs to the line end (L1 sandbox run: 0 of 6 with unquoted quotes, 6 of 6 with quoted ones) | none | Not fixed after pinning (the tool bytes are fixed for this round's measurement); every Gate quote here is wrapped in quotes or backticks. Fix owed next round with a selftest case for an unquoted quote. |

Misroot sweep and seat leftovers: recorded in the round report.

## Routed defect 4 — memory-pressure checker hardened (appended after wave 1)

Wave-1 ExecMemCheckerHarden changed `tools/check-memory-pressure.py` in its own clone (sha256 `019a9fa5a446d65577ec3c7dd50ca59acbc29562b43d62fed0516067298edbd7`; diff `.ufo/waves/round-26/w1/ExecMemCheckerHarden/tool.diff`) and the L1 copied it into the lane unchanged. Six changes: a Gate or entry quote mismatch blocks the row; a Gate quote over 25 words blocks the row; the SKILL rule needs the id in the first cell of a table line inside the round-25 section; duplicate row ids are an error; each row needs a tier-A source; a lesson prose line with an S id and "recheck" but no arrow no longer crashes the parser (the `c93bd70f` crash). Evidence, re-run by the L1 at integration: selftest PASS (41 cases), exit 0; `--revision 157ee2556a75bf4d1ae4893d4a06c020ae531ac0` and `--revision 7dfea9244a84a0e2439f0698e54491e5d7b7c467` both 6 of 6, exit 0. Replay of the 17 round-25 wave-2 mutants (`ExecMemCheckerHarden/result-w2.json`): 16 killed, 1 survived (N17 changes the Gate quote and the entry quote consistently, which a committed-bytes check cannot see; recorded as a limit). Wave-1 catalogue (`result-w1.json`): 10 killed, 1 killed under another finding id, 1 inconclusive (M11, inapplicable to the real tree as round 25 recorded). Round 25 recorded 8 of 17 killed. The round-25 claim is not re-measured or changed by this: it was measured with the old tool at its own revision.

## Wave-1 findings recorded after integration

- QUALITY 60's sweep reads only base-to-head diffs of five files, so an in-place edit made and then disclosed inside a round, or an edit to `SKILL.md`, `PROVINCE.md` or a knowledge entry, escapes it (ScribeMistakes finding 5, ScribeRouted1Scorecard51 finding 5). Round 25 also rewrote nine lines of `corpus/knowledge/memory-pressure-r25.json` and three lines of `SKILL.md` in place; the `SKILL.md` lines were disclosed in its Gate errata, the JSON lines were not. That JSON rewrite is recorded here as a second undisclosed round-25 in-place edit (class disclosure, same fix as R26-UNDISCLOSED-INPLACE). QUALITY 60 is clarified below the criteria to cover every tracked lane file and each commit pair of the round.
- The declared hand prediction for C2's base (3 of 27) was wrong; the tool measured 5 of 27 because coverage and adjacency had no dated measured-outcome record (ScribeMistakes finding 4, MutSelfAssessPlan). The before-value was declared as the tool's number, so the target is unaffected.

## Wave-2 findings and corrections (appended 2026-10-22, before closure)

Wave 2 had 35 seats at measured revision `7dfea9244a84a0e2439f0698e54491e5d7b7c467`. The four mutation-tester seats died at start ("Error: No model selected."); they were not replaced, and the L1 ran the mutation evidence itself (`.ufo/waves/round-26/l1-mutation/README.md`: C1 20 of 20 rule mutants killed, 1 control survives; C2 8 of 8 rule mutants killed, plan prose correctly ignored). The wave-1 C1 mutation runner reported 37 of 37 survived against the same tool that kills the same mutant by hand; that runner result is a runner defect and is not used.

Corrections to this lesson's own text:

- The routed-defect table above says defects 3, 5 and 7 are "Fixed". They are partly fixed (wave-2 CritRoutedDefects). Defect 3: the self-reference moved rather than disappeared; at the measured revision all six ordinal checks read `SCORECARD.md:960`, a line this round wrote, and a sandbox mutant that sets depth to 10 in both the table and that line passes (CritRoutedDefects, CritCalibrationClaim). Defect 5: `ahead=0` was observed before each helper commit by the L1 (`jj-lane.sh state` lines in the round transcript) but only one reading is in a seat report. Defect 7: box 3 still rests on a test of a 444-line SKILL.md; no box is checkable by a non-author yet. Defect 4 landed at `7f9f0889`, one commit after the measured revision.
- "Wave-1 findings recorded after integration" says the hand prediction of 3 was wrong. It was right under the rule as declared at `b13e991f`; the refinement at `4de2b6b1` raised the base to 5 by adding K02 and K06 `no dated move record` (CritCalibrationClaim reproduced 3 with the declared rule).
- What C2's 0 of 27 proves (CritCalibrationClaim): K07 to K27, 21 checks, compare the self-assessment with observed repository state, and they moved from 3 mismatches (K10, K24, K26) to 0. K01 to K06 compare the axes table with an ordinal-record line written by the same round in the same commit; they show the two agree, not that any ordinal is deserved. K02 and K06 were cleared only by that line.

Entry and registry corrections, each appended where it lives (entry section "Wave-2 corrections", SKILL notes, memory-pressure note, README correction, SOURCES search log and lead clarification):

- SH6's Unexpected Power Losses trigger omitted a second branch, and "not a count of host-visible crashes" was withdrawn; the SH6 verdict is split (`UNVERIFIED` for the power-loss count). The S135 teaches cell carries the same omission (RevS135, RevRowSH6). The journal dates boot ends, not abruptness. `nvme0` named different PCI devices in boots -1 and 0.
- SH5's "otherwise" holds only after a successful SMART log read (RevRowSH5). SH1's "shorter names" applies to three of the five counters (RevS133). SH2 omitted that a scrub run also updates the counters (RevS128). S128's teaches cell adds an "only" the source lacks (RevS128). S136's Gate quote was not exact and its teaches cell widens the ancestor case (RevS136).
- SE2 and SE3 carry operator cautions not stated by a source; `UNVERIFIED` and the entry's `DEGRADED` are entry-local vocabulary (CritLearningClaim).
- The README Frontier bullet overstated which part of the old lead was opened (CritTrendVerdicts).
- No round-26 search-log note existed (CORPUS SOURCES rule 5); one is now in `corpus/SOURCES.md`.

Registry rows S128, S135 and S136 are not rewritten (append-only outside status, recheck and used-by); superseding rows with Gate records are owed next round.

### Mistakes added after wave 2

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R26-SELF-AGREEMENT-ORDINAL | measurement | At `7dfea924` K01 to K06 all read `SCORECARD.md:960`, written in the same commit as the table they check; a sandbox mutant with depth 10 in both passes (CritCalibrationClaim, CritRoutedDefects) | QUALITY 62 (it binds to dated records but allows the declaring round's own record) | QUALITY 65. Red before: the depth-10 mutant exits 0 under the pinned tool. Tool change owed next round (reference only records of rounds earlier than the declaring round, anchor the heading match). |
| R26-TEACHES-OVERSTATED | curation | Routed defect 8 (S121, S122, S118) recurred in this round's own rows: S128 "only", S135 trigger, S136 ancestor case (RevS128, RevS135, RevS136) | CORPUS SOURCES rule 1 (teaches grounded by a quote); no lane criterion | QUALITY 66. Red before: the S135 teaches cell states one branch where excerpt lines 239-256 state two. |
| R26-DRAFT-DRIFT | quality | The wave-1 source seat stated both SH6 branches correctly (`w1/SrcNvmeLifetimeFields.md` line 41); the L1's integrated entry kept one | none | QUALITY 66 covers it: a statement integrated from a seat report is compared with that report's quoted source lines before landing. |
| R26-LEAD-OVERSTATED | disclosure | README Frontier bullet claimed the release-notes half of the old lead was opened (CritTrendVerdicts) | QUALITY 60 does not cover wording | Appended README correction; red before: `grep -c "release notes" corpus/README.md` names them as opened at `7dfea924`. |

QUALITY 64 records R26-GATE-COLUMN-OFFSET (a tool mistake no criterion caught), so that mistake now has a criterion.

### Late wave-2 findings (appended before the final commit)

- PROVINCE overreach on free-capacity ownership and the unstated privilege and device scope are corrected by an appended PROVINCE paragraph (RevProvinceReadme). Cross-lane observation for mori, reported not absorbed: `/tmp` is now an xfs partition on the second NVMe device (`systemctl show tmp.mount`), while mori's corpus records it as tmpfs (RevProvinceReadme finding 5).
- S131's teaches cell says more than the timer file (the paired service and catch-up semantics come from the packaged service and systemd.timer, not S131); the round-26 rows' used-by cells name only the Markdown entry, not the JSON (RevS131, RevS129). Owed next round with superseding rows.
- S129's teaches cell adds "only" and "at all" the source lacks; SH4's S129 citation does not carry its claim (RevS129).
- The axes table was re-stated after the repair commit because two counts changed (`measure/c2-75449b13.json`, K08 and K11); the re-stated table is the current one.
