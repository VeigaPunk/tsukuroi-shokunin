# CritClaimSizing — round 26 declaration against claim sizing and AXES.md lines 25-55

Verdict: partly holds. The declaration meets the structural rules: distinct axes, the lowest axis worked, one after-value and one command per claim, an enumerated K01 to K27 set, and a no-narrowing clause. But seven phrases let a claim pass by construction, four let a claim fail for a reason unrelated to the claim, and four are broader than anything their command counts. All of them are fixable by an appended pre-landing refinement. One of them, the SH5 row text, forces a false row if it lands as written. That would be a harm the judge must reject.

Inputs: the declaration is `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:874-908` at `b13e991fb96972b423b868ba122187f75357368c`. The session rule is `/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-26.md:342-350`. The canonical rule is `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:25-55`; its sha256 `04ea5c9e…7d993` equals the digest at SCORECARD.md:884, and the kimi checkout is at `e737d2ea`. All quotes below were checked byte-for-byte against the stated SCORECARD line.

## What holds

A. The claims are on distinct axes, and the lowest axis is worked. C1 is on depth and C2 on calibration. Depth is tied lowest at 8, with adjacency (SCORECARD.md:876; the axes rows are at SCORECARD.md:829-834). This satisfies AXES.md:31-34. [obs]

B. Each claim has one concrete after-value and one command. C1 is "6 verified rows, SH1 to SH6, exit 0" and C2 is "0 of the 27 fixed checks K01 to K27 mismatch, exit 0" (SCORECARD.md:892-893). Both universals are enumerated: the C1 ids are fixed as "exactly the ids SH1 to SH6" (line 897), and C2 fixes K01 to K27. [obs]

C. The no-narrowing rule is stated: "neither target will be narrowed" (line 908). [obs]

D. C2 counts mismatches between the self-assessment and repository state, as the session rule requires (prompt line 347). But see finding 12 for K01 to K06. [obs]

## Findings

1. **Pass by construction: an `UNVERIFIED` row counts as verified.** Line 897 accepts "a verdict (`HEALTHY`, `DEGRADED`, `BLOCKED` or `UNVERIFIED`) and an action". Line 892 counts the field `verified_rows`. So six rows whose verdict is all `UNVERIFIED` or `BLOCKED` meet "6 verified rows". [obs] Impacted: C1 and depth. Fixable. Smallest correction: state that the counted field counts rows by structural admission, whatever the verdict, and rename it (for example `admitted_rows`). Alternatively, state that only `HEALTHY` or `DEGRADED` rows count. A host verdict is a category error for the definitional rows SH1, SH2, SH3, SH5 and SH6 anyway. [inf]

2. **Pass by construction: the row content is declared but never bound.** Line 895 fixes the meaning of SH1 to SH6 ("C1 rows, fixed now"). Line 897 checks only these things:
   - "the row has a non-empty statement";
   - a quote that is a substring of any cited snapshot, with no relevance test;
   - "at least one capture pointer (line number and token of at least 3 characters)" into any unique line;
   - a SKILL.md table line whose first cell is the id.

   For example, SH6 could point at `capture.txt:13`, which reads `nvme-cli 3.1-1`, and quote any string from S129. It would count. [inf] Impacted: C1 and depth; it also hides row-truth harm to the quality trend. Fixable. Smallest correction: fix one required capture line per host-fact row: SH4 at capture.txt:121 (`no stats available`) and :131 (`disabled`), and SH5 at :181 (`PASSED`) and :184 (`0x00`). Fix one required source per definitional row, for example SH5 must cite S134. Then name a non-author row-truth reviewer.

3. **Forced false row: the declared SH5 statement contradicts its own source S134.** Line 895 says SH5 names "which fields (critical warning, available spare against its threshold, percentage used, media and data integrity errors) decide it".
   - In smartmontools 7.5, the overall result depends only on the critical-warning byte. `https://raw.githubusercontent.com/smartmontools/smartmontools/RELEASE_7_5/smartmontools/nvmeprint.cpp` (sha256 `4770d985…0e4e98`) lines 448-452 read: `jout("SMART overall-health self-assessment test result: %s\n",` and `(!w ? "PASSED" : "FAILED!"));`.
   - The caller passes that byte at lines 840-842: `print_critical_warning(smart_log.critical_warning);` and `if (smart_log.critical_warning)`.
   - The spare, percentage-used and media-error fields are only printed (lines 501-511 and 530). Spare below threshold enters only as the device-set bit 0x01 (lines 458-460). [obs]

   Impacted: C1, depth, and the quality trend. If the row lands as declared it is false, a harm the judge must reject. If it lands corrected, it departs from a row "fixed now". Fixable before landing. Smallest correction: append a refinement restating SH5 as follows. The result is PASSED when the critical-warning byte is 0x00. Spare below threshold and degraded reliability enter only as bits the device sets in that byte. Percentage used and media errors are reported, not evaluated.

4. **Too broad: SH4 uses a universal that the capture cannot support.** Line 895 says "stored data has never been verified end to end".
   - The capture shows only that no status file exists: capture.txt:121 is `no stats available`, :127 is `ls: cannot access '/var/lib/btrfs': No such file or directory`, and :131 is `disabled`.
   - The S129 tag source says the status is file-backed. `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-scrub.rst` lines 136-138 read: "show statistics of the last finished or cancelled scrub for that filesystem or device. The status is read from the file located in :file:`/var/lib/btrfs`." [obs]
   - A scrub whose status file was later lost (for example by a snapshot rollback of `/@`, with the root at `/@` per capture.txt:20) is indistinguishable from no scrub at all. [inf]

   Impacted: C1 and depth; it would also be a false-universal pattern. Fixable. Smallest correction: "no scrub status record exists on this host and the root scrub timer instance is disabled at capture time".

5. **Fails for an unrelated reason: the pre-assigned S131 path does not exist.** The goal names "btrfs-progs v7.1 units/btrfs-scrub@.timer".
   - `curl -s -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/units/btrfs-scrub%40.timer` returned `404`. So did `https://github.com/kdave/btrfs-progs/tree/v7.1/units`. Over the same session, `Documentation/btrfs-scrub.rst` at v7.1 returned 200. [obs]
   - `pacman -Qo /usr/lib/systemd/system/btrfs-scrub@.timer` returned `owned by btrfs-progs 7.1-1`, exit 0. `https://gitlab.archlinux.org/archlinux/packaging/packages/btrfs-progs/-/raw/7.1-1/btrfs-scrub@.timer` returned 200. So the unit is Arch packaging, not upstream. [obs] [inf]

   Impacted: C1, the SH4 sourcing. Fixable. Smallest correction: re-point S131 to the Arch packaging file at tag `7.1-1`, and record its tier honestly.

6. **Fails for an unrelated reason: a PDF source cannot meet the substring rule.** Line 897 requires the quote to be "a substring of the committed snapshot" whose sha256 is in the anchor cell. S135 is most likely the NVMe Base Specification PDF. [inf] `https://nvmexpress.org/wp-content/uploads/NVM-Express-Base-Specification-Revision-2.1-2024.08.05-Ratified.pdf` returned 200, `application/pdf`, 11755505 bytes, sha256 `4e31f826…dc746`. `grep -a -c -i "unsafe shutdowns"` on the raw bytes gave `0`, and `grep -a -c FlateDecode` gave `2960`. [obs] Impacted: C1, SH6. Either SH6 cannot use its primary source, or its snapshot is a derived text file whose digest is not the fetched bytes. Fixable. Smallest correction: declare that a PDF snapshot is a text extraction, with both the fetched-bytes and extracted-text digests recorded and the extraction command named. Or name a text-form primary source.

7. **Pass by construction: the author certifies snapshot authenticity.** Line 897 says "whose sha256 is written in that source's anchor cell". Both the snapshot and the anchor cell are written by the round's own seats. Nothing compares the snapshot to the pinned URL's bytes. So a hand-made snapshot containing the quote passes. [inf] Impacted: C1, and sourcing honesty in the calibration trend. Correction: the closure re-fetches each cited URL and compares the sha256, or a non-author spot-check does so. This is a tradeoff: a live re-fetch adds a network dependency to the count. So keep it as an outside check, not as a field of `verified_rows`.

8. **Not re-derivable: the lesson path is unnamed.** Line 897 says "the same quote text appears in that source's row of the lesson `## Gate` table". No lesson path is fixed, so the checker chooses its own file, and a judge cannot re-derive which bytes were compared. [obs] Impacted: C1. Fixable. Smallest correction: name `corpus/lessons/<round-26 lesson>.md` in an appended refinement before the checker lands.

9. **Not re-derivable: neither before-value comes from the declared command.** The table header says "Counting command (tool from the measured commit, data from `<REV>`)" (line 890).
   - C1 before: "0 verified rows (entry and checker absent)" (line 892). At `e9f5356c` the checker does not exist, so the command emits no `verified_rows` field. [obs] `git ls-tree --name-only e9f5356c tools/` lists no `check-storage-health.py`.
   - C2 before: "the number the v2 tool reports at `e9f5356c` (hand count by the L1 predicts 3 of 27: K10, K24, K26)" (line 893). The tool from that commit is v1. `python3 tools/check-self-assessment.py --revision e9f5356c` returned exit 1 with `checked 23, mismatches 1, ['K10']`. The same run at `HEAD`, which is `b13e991`, gave the same result. [obs]
   - So the literal header rule yields 1 of 23, not the stated v2 base. A hand prediction is not a value.

   Impacted: C1 and C2, and the falsifiable before-to-after required by AXES.md:28-31. Fixable. Smallest correction: define the before-value as the measured-commit tool run against `--revision e9f5356c`, which is tool from REV and data from the base. Record that number when the tool lands; neither target changes.

10. **Pass by construction: the tool and the data come from the same commit.** Again "tool from the measured commit, data from `<REV>`" (line 890). Both checkers are authored this round. No checker sha256 is pinned before the data bytes land. So a lenient checker and lenient data can be committed together. Routed defect 4 already found 9 surviving mutants in the round-25 checker (`corpus/lessons/round-25-verifier-spotcheck.md:105`). [obs] Impacted: C1, C2, and calibration. Fixable. Smallest correction: freeze each checker's sha256 in an appended refinement commit before the entry or axes-table commits. The closure then runs that frozen tool. Name at least the mutants that line 897 promises (a duplicate id, a quote mismatch, a capture digest change) as selftest cases with their expected exits.

11. **Routed defect 3 recurs, and the after-state cannot show that it is repaired.** Line 903 says "The declaring round N is the number in the heading of the current axes table" and excludes "every line inside a section whose heading (any level) names round N".
   - Until the round-26 axes table lands, N stays 25. So the round-26 declaration's own table lines ("depth 8 → 8 (tied lowest)" at line 892, "calibration 9 → 9" at line 893) are the ordinal references.
   - Evidence: I simulated the v2 rule over `git show b13e991:SCORECARD.md`, with notes in `/fast/scratch/hyaku/tsuku26/CritClaimSizing/`. Under both the flat and nested readings, N is 25, depth binds to line 892 and calibration to line 893. At `e9f5356c` they bind to 759 and 771. [obs]
   - At landing no ordinal moves (line 908: "No … ordinal change"). So K01 to K06 match through the round-25 lines whether or not the exclusion works. A count of 0 therefore cannot show that defect 3 is repaired, yet line 893 claims "repairs routed defects 3 and 7". [inf]
   - The phrase "heading (any level)" is ambiguous between flat and nested sections. The round-25 outcome at SCORECARD.md:863 is a `###` heading nested under `## Capabilities — current (round 25)` at :840. At `e9f5356c` both readings give the same references. [obs]
   - The clause "unless that heading also contains `measured outcome`" re-admits any heading that uses that phrase, whatever the section holds. [inf]

   Impacted: C2 and calibration. Fixable. Smallest correction: take N from the highest `Round N — declaration` heading, not from the axes-table heading. Define a section as running to the next heading of any level. Add a named selftest fixture where the declaration says "depth 8 → 9", the table says 9 and there is no outcome; it must report a K01 mismatch.

12. **K01 to K06 compare one self-assessment text with another.** They compare the SCORECARD axes table against SCORECARD prose, both written by the lane, not against repository state (the evaluation code is at `tools/check-self-assessment.py:385-422`). The session rule asks for mismatches "between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state" (prompt lines 347-348). So 6 of the 27 counted checks are internal-consistency checks. [obs] Impacted: C2 and calibration. This is a tradeoff, not a defect. Defect 3's alternative remedy, "bind to dated move records" (`round-25-verifier-spotcheck.md:104`), would make them repository-state checks. At minimum, say in the claim that K01 to K06 are consistency checks.

13. **K24 to K27 flag the wrong notes, and "repairs routed defect 7" is broader than the count.** Line 904: "none of its first 20 lines matches the case-insensitive word `superseded`".
   - **False positives at `e9f5356c`**: `corpus/knowledge/closeout-r11.md:18` ("Errata are append-only: a superseded") and `corpus/knowledge/source-locator-clarification-r15.md:19` ("only the supplemental locator is superseded"). The second is an active correction note. A box citing either fails for a reason unrelated to supersession. [obs]
   - **False negatives**: the lane marks supersession by appended notices, which are never in the first 20 lines. Examples are `kill-event-deep-r8.md:381` and `oom-event-plane.md:444-452`, the round-25 markers that the round-25 verifier spot-check describes as "Both are marked" (`round-25-verifier-spotcheck.md:98`). Only the in-place banner at `root-dac-decision-r12.md:7` is caught. [obs]
   - **Defect 7 scope**: defect 7 names boxes 3 and 4 (`round-25-verifier-spotcheck.md:109`). Box 4's actual defect is a superseded PROVINCE.md refinement: `.ufo/waves/round-25/w2/RevShonen.md:38`: "The cited "round-12 refinement" at … `PROVINCE.md:85-90` is superseded." Box 4 names no `corpus/knowledge/*.md` path (`SHONEN.md:11-12` at `e9f5356c`), so "every `corpus/knowledge/*.md` path the box names" is vacuously true and K27 passes. Box 3's "untested" half (RevShonen.md:43-47) is not counted at all. [obs]
   - **Cheap by-construction path**: rewording the banner at `root-dac-decision-r12.md:7` clears K24 and K26 without touching SHONEN. The declaration does not forbid it. [inf]

   Impacted: C2 and calibration. Fixable. Smallest correction: narrow the claim cell before landing to "repairs the superseded-note half of defect 7 for boxes 1 and 3". Define the marker as the lane's actual convention: a `> **Superseded` banner, or an appended `Superseded`/`supersedes` notice anywhere in the note. Forbid edits to cited notes' markers this round.

14. **Fails for an unrelated reason: `<REV>` is never bound, and live counts drift.** Line 906: "the tool always measures at the revision given, so a later commit cannot change the measured result, and every later round re-measures." The declaration never names which revision the closure must pass. Round 25 failed exactly this way: "this spot-check's own commit makes K10 read 27 files against the stated 26" (`round-25-verifier-spotcheck.md:104`). An integrator lesson file added after landing flips K10 at the tip. [obs] "every later round re-measures" is a universal about future rounds that no command enumerates. [inf] Impacted: C2. Fixable. Smallest correction: bind `<REV>` to the landing commit that the round-26 measured outcome records. State that later drift is not a C2 miss. Drop the future-rounds clause.

15. **The separability sentence is false for C1 and vacuous for C2, and it hides an ordering hazard.** Line 888 says "C1 reads only this round's storage capture, newly opened sources, their committed snapshots and its own entry." and "C2 reads only SCORECARD.md, SHONEN.md and repository state at a named revision."
   - Line 897 makes C1 also read `corpus/SOURCES.md`, the lesson `## Gate` table and `SKILL.md`. [obs]
   - C1's bytes are inputs to C2: the new note changes K07 (depth row "47 notes", SCORECARD.md:829), the new SKILL.md section changes K08 (2355 lines) and K09 (297 table lines), and the lesson changes K10. [obs]
   - AXES.md:31 separability still holds, because C2 is verifiable whether or not C1 lands. But if the round-26 axes table is written before C1's last byte, C2 misses for a reason unrelated to calibration. [inf]

   Impacted: C2. Fixable. Smallest correction: correct the sentence, and state that the axes table is the last write before `<REV>`.

16. **Too broad: "new PROVINCE frontier area" in the C1 cell.** The cell says "new PROVINCE frontier area" (line 892). LEARNING.md:33 credits "frontier areas entered" to expansion, and AXES.md:21 maps expansion to "`coverage` + `adjacency`". No command counts a PROVINCE.md or coverage-map change. A judge can read this as a second axis inside C1, which AXES.md:32-33 counts as one claim, or as an uncounted rider. [obs] Impacted: C1, depth versus coverage. Fixable. Smallest correction: remove the phrase from the claim cell, or keep it as a non-claim note.

17. **Too broad: a universal commitment outside both counts.** Line 876 says "its eight routed defects are each fixed or explained in this round's lesson." No command enumerates the eight defects. Defects 1, 2, 4, 5 and 8 are in neither claim, and "or explained" is an unbounded escape. [obs] The negative list at line 908 (no package transaction, scrub, and so on) is an operating constraint, not a claim. It is low risk, but it is also uncounted. [inf] Impacted: calibration, through the overreach signal. Fixable. Smallest correction: label line 876 as a non-claim commitment, or name a count such as one `Routed defect N` heading per defect, 1 to 8, in the named lesson.

## Summary of the smallest safe correction

Make one appended refinement commit before any checker or entry lands. It should:
- restate SH4 and SH5 (findings 3 and 4);
- re-point S131 and fix the PDF snapshot rule (findings 5 and 6);
- name the lesson path and bind `<REV>` (findings 8 and 14);
- define both before-values as the frozen REV tool run on the base data (finding 9);
- pin the checker digests and the mutant cases (finding 10);
- take N from the declaration heading and add a self-reference fixture (finding 11);
- define the supersession marker by the lane's real convention and narrow the "defect 7" wording to what K24 to K27 count (finding 13);
- rename or restrict `verified_rows` (finding 1);
- bind per-row required pointers (finding 2);
- drop "new PROVINCE frontier area", "every later round re-measures" and the "each fixed or explained" universal, or mark them as non-claims (findings 14, 16 and 17).

None of these changes either after-value.

Scope: read=SCORECARD.md lines 829-834 and 874-908 at b13e991 and e9f5356c, SHONEN.md at e9f5356c, tools/check-self-assessment.py (sections 36-310 and 320-640), corpus/lessons/round-25-verifier-spotcheck.md lines 95-110, .ufo/waves/round-25/w2/RevShonen.md (grep), corpus/knowledge/*.md first 20 lines and superseded hits at e9f5356c, corpus/SOURCES.md (grep), PROVINCE.md headings, .ufo/waves/round-26/capture/capture.txt lines 1-175 plus grep (sha256 verified 002bef16…a71dd; capture.sh sha256 verified 81234ae1…75364), AXES.md lines 1-59 (sha256 04ea5c9e…7d993), LEARNING.md:33 (grep), .ufo/prompts/tsukuroi-round-26.md lines 335-350, ~/.agents/skills/godspeed/SKILL.md, public upstream files (smartmontools RELEASE_7_5 nvmeprint.cpp and smartctl.cpp, linux v7.2 fs/btrfs/sysfs.c and volumes.c, btrfs-progs v7.1 btrfs-scrub.rst, URL probes for btrfs-progs v7.1 units, btrfs-device.rst, mkfs.btrfs.rst and ch-profiles.rst, Arch packaging btrfs-scrub@.timer at main and 7.1-1, NVMe Base Specification 2.1 PDF); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/CritClaimSizing.md, /fast/scratch/hyaku/tsuku26/CritClaimSizing/ (v1 checker JSON outputs, SCORECARD copies, fetched upstream files, NVMe PDF); executed=python3 tools/check-self-assessment.py --revision e9f5356c (exit 1) and --revision HEAD (exit 1), a local Python simulation of the declared v2 K01 to K06 rule, git show/ls-tree/rev-parse/diff --stat (read-only), sha256sum, grep, sed, awk, curl of public URLs, pacman -Qo
Model: not exposed
Installs: none
