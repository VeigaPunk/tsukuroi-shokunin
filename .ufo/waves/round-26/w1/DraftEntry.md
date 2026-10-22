# DraftEntry — C1 storage-integrity entry draft (round 26, wave 1)

Verdict: done — the two draft files exist in my seat path, every quote is a verified substring of a
committed snapshot under `.ufo/waves/round-26/sources/`, every capture pointer was checked with
`grep -n -x -F` and counted, and the row set is exactly SH1 to SH6 with one verdict from
HEALTHY/DEGRADED/BLOCKED/UNVERIFIED each. The L1 integrated its own version of the entry while this
seat was working, so this draft is a parallel, independently verified copy, not the landed text.

## What this seat drafted and where

1. [obs] `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/DraftEntry/storage-health-r26.md`
   (15252 bytes, 114 lines). It opens with the `source:`, `verified-at:` and `recheck:` lines, then
   `## Scope`, then one `## SH1` to `## SH6` section per row, each with **Statement**, **Host
   reading**, **Verdict**, **Action**, **Sources** (with the located quotes) and **Capture
   pointers**, then `## Adjacent` and `## Limits`.
2. [obs] `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w1/DraftEntry/storage-health-r26.json`
   (15447 bytes). Schema `tsukuroi-storage-health-r26-v1`, a `capture` block carrying the path
   `.ufo/waves/round-26/capture/capture.txt` and the pinned sha256
   `002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd`, a `rows` array with the ids
   SH1 to SH6 exactly once each, and per row `id`, `statement`, `host_reading`, `verdict`, `action`,
   `sources`, `quotes` (each with exactly `source`, `text`, `location`) and `capture_pointers` (each
   with exactly `line`, `token`).

No other lane file was written by this seat. The lane's `corpus/knowledge/storage-health-r26.md`,
`corpus/knowledge/storage-health-r26.json`, `corpus/lessons/round-26.md`, `corpus/SOURCES.md`,
`SKILL.md`, `SCORECARD.md`, `PROVINCE.md` and the counting tools were not touched by me.

## Findings

1. [obs] The source ids are the pre-assigned set only: S128 (btrfs-device.rst), S129
   (btrfs-scrub.rst), S130 (mkfs.btrfs.rst), S131 (the Arch-packaged btrfs-scrub@.timer), S132
   (fs/btrfs/volumes.c), S133 (fs/btrfs/sysfs.c), S134 (smartmontools/nvmeprint.cpp), S135 (the
   NVM Express Base Specification 2.4 SMART / Health Information page) and S139
   (ch-scrub-intro.rst). S136, S137 and S138 are the round-25 supersede rows for S121, S122 and
   S118 and are not cited here; S139 is the next free id and is the chapter S129 includes.
   Evidence: `corpus/SOURCES.md:134-145`, each row `mined`, opened 2026-10-22, recheck `on-release`,
   used-by `corpus/knowledge/storage-health-r26.md`, tier A.

2. [obs] Every quote in the draft is a whitespace-normalised substring of the committed snapshot for
   its source id, checked by script over `.ufo/waves/round-26/sources/S1*`; the script reported zero
   problems for all 26 quotes, and every quote is at most 25 words. The same quote texts appear in
   the lesson's `## Gate` table at `corpus/lessons/round-26.md`, which the checker requires. Evidence:
   the verification run over the 26 quotes returned `problems: []`, and a second pass confirmed each
   quote string is present in the lesson text.

3. [obs] Every capture pointer names a line of `.ufo/waves/round-26/capture/capture.txt` whose text
   occurs exactly once in that file, which is not a `### ` header, a `$ ` command echo or an `[exit `
   line, and whose line contains the named token of at least three characters. Each pointer was
   confirmed with `grep -n -x -F` and a count: all 20 pointers return count 1. Two candidate
   pointers were rejected and not used: `dup` (lines 79 and 100 are identical, count 2) and the
   bare `7` on line 164 (token shorter than three characters). Evidence: the pointer validation run
   printed `problems: []` for the final set.

4. [obs] The four rows that needed narrowing were narrowed to what the sources support. SH2 states
   that the `bdev ... errs:` text is printed twice, at error level when an error is counted and at
   info level at mount when a stored counter is non-zero, so only the error-level line dates an
   increment; S132 line 8446 (`return; /* all values == 0, suppress message */`) is the ground.
   SH3 states that a data checksum error under the `single` profile is detected and reported as
   uncorrectable rather than repaired, and that NOCOW file data is not verified at all. SH4 says
   "no scrub record exists on this host" and never "never scrubbed"; no source shows that scrub
   status files are kept forever, so the stronger universal claim is not made, and the verdict is
   `UNVERIFIED` rather than `DEGRADED`. SH5 states that only the Critical Warning byte decides the
   PASSED or FAILED result and that Available Spare, Percentage Used and Media and Data Integrity
   Errors are printed but are not inputs to it. Evidence: S128 lines 231-233 and 260-261; S129 lines
   78-80 and 190-193; S130 lines 635-641; S132 lines 8428-8456 and 8490; S133 lines 2074-2100;
   S134 lines 448-482 and 838-843; S135 excerpt lines 13-15, 48, 104-115, 235-276; S139 lines 1-3,
   13-18, 20-35, 67-74.

5. [obs] Every action in the draft is operator-owned: the lane never runs a scrub, never resets a
   counter, never enables a timer and never changes a profile. SH1 forbids `-z`/`--reset` in the
   lane's own read commands, SH4 hands the scrub run and the timer enablement to the operator, and
   SH3 states that changing the data profile is an operator decision and is not proposed.

6. [obs] The Adjacent section names where the entry adds to the lane's journal-boot plane: the NVMe
   lifetime counters are undated device totals that sit beside the boot list recorded in
   `corpus/knowledge/journal-boot-plane.md`, and the entry dates nothing. It names the wave-1
   ScoutJournalBoots finding that five of five completed retained boots have no persisted final
   shutdown record and that one of them is a proven orderly reboot, so a missing record is not an
   unsafe shutdown. It also keeps disk-space runway with mori (`mori-shokunin/PROVINCE.md`,
   `SURFACE disk`) and confines Percentage Used and Data Units Written to device-health facts.
   Evidence: `.ufo/waves/round-26/w1/ScoutJournalBoots.md` findings 5 and 9,
   `.ufo/waves/round-26/w1/ConnSiblingOverlap.md` findings 1, 2 and 3,
   `.ufo/waves/round-26/w1/CritLearningFrontier.md` finding 6.

7. [obs] One wording limit is carried in the row rather than in the sources: the S135 page names the
   159:144 field "Unexpected Power Losses" and notes that it was previously named Unsafe Shutdowns,
   so SH6 says the field smartctl and nvme-cli still label Unsafe Shutdowns is the specification's
   Unexpected Power Losses counter, and it says "over the life of the controller" rather than "of the
   device". Evidence: S135 excerpt lines 238 and 258.

8. [unk] The L1 integrated `corpus/knowledge/storage-health-r26.md` and
   `corpus/knowledge/storage-health-r26.json` itself while this seat was running; the landed text at
   `corpus/knowledge/storage-health-r26.md` and the JSON at the same path are the L1's, not mine.
   This draft was written to the seat path only, so nothing here has been integrated and nothing
   here has been re-checked by the counting tool at a revision. Whether the L1 wants any part of this
   draft substituted into the landed text is the L1's decision.

## Gates and touched surfaces

- [obs] Read-only surfaces read: `SCORECARD.md` (round-26 declaration and refinements),
  `corpus/SOURCES.md` (registry rows S115-S139), `corpus/lessons/round-26.md` (`## Gate` table),
  `corpus/knowledge/memory-pressure-r25.md` and `memory-pressure-r25.json` (the shape to follow),
  `corpus/knowledge/journal-boot-plane.md`, `corpus/knowledge/boot-plane.md`, `PROVINCE.md`,
  `SKILL.md` (§Verdict vocabulary and the read-only verb list), `tools/check-storage-health.py` and
  `tools/check-memory-pressure.py` (the row rule), the frozen capture and the capture script, the
  wave-1 seat reports, and the committed source snapshots.
- [obs] Files written by this seat, and only these: `.ufo/waves/round-26/w1/DraftEntry/storage-health-r26.md`,
  `.ufo/waves/round-26/w1/DraftEntry/storage-health-r26.json` and this report at
  `.ufo/waves/round-26/w1/DraftEntry.md`.
- [obs] No host mutation of any kind: no scrub, no counter reset, no timer or service action, no
  package transaction, no configuration write, no mount, no boot action, no sudo command beyond the
  read-only queries already inside the frozen capture, and no git or jj write command against the
  lane repository or the fleet root.
- [obs] The upstream files were opened by plain curl only, into a scratch directory under
  `/fast/scratch/hyaku/tsuku26/DraftEntry/`, to confirm the quote texts; no source snapshot was
  written by this seat.

Scope: read=SCORECARD.md round-26 declaration, corpus/SOURCES.md, corpus/lessons/round-26.md, corpus/knowledge/{memory-pressure-r25.md,memory-pressure-r25.json,journal-boot-plane.md,boot-plane.md}, PROVINCE.md, SKILL.md, tools/{check-storage-health.py,check-memory-pressure.py}, .ufo/waves/round-26/{capture/capture.txt,capture/capture.sh,sources/S1*}, .ufo/waves/round-26/w1/{SrcBtrfsDeviceDoc,SrcBtrfsScrubDoc,SrcBtrfsProfilesDoc,SrcBtrfsScrubUnit,SrcKernelVolumes,SrcSmartNvmeprint,SrcNvmeLifetimeFields,ScoutJournalBoots,ScoutPriorCorpus,ConnSiblingOverlap,CritLearningFrontier}.md, and the upstream pages btrfs-device.rst, btrfs-scrub.rst, mkfs.btrfs.rst, ch-scrub-intro.rst, fs/btrfs/volumes.c, fs/btrfs/sysfs.c, nvmeprint.cpp at the pinned tags; wrote=.ufo/waves/round-26/w1/DraftEntry/storage-health-r26.md, .ufo/waves/round-26/w1/DraftEntry/storage-health-r26.json, .ufo/waves/round-26/w1/DraftEntry.md; executed=plain curl fetches of the upstream pages and the GitHub/GitLab release endpoints, git ls-remote --tags on github.com/kdave/btrfs-progs and github.com/smartmontools/smartmontools, tarball listings, sha256sum, wc, cmp, grep -n -x -F, and two python3 verification passes over the quotes and the capture pointers
Model: opencode-go/minimax-m3.1-flash-free
Installs: none
