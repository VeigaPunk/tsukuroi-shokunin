Verdict: partly holds. All three replaced SHONEN.md evidence lines (boxes 1, 3 and 4) resolve to the cited paths and line ranges and describe them accurately; the box text and the `[~]` marks are unchanged; and no cited corpus note carries a whole-file superseded marker. But box 4's statement that recipient acknowledgement is "unobserved" is contradicted by a recipient-side receipt that the lane's own cited sources record, and the new sentences "no superseded note is cited here" (boxes 1 and 3) hold only for whole notes, because the SKILL.md ranges they cite contain readings that the same file supersedes.

## Method

Revision under review: 7dfea9244a84a0e2439f0698e54491e5d7b7c467 (base e9f5356cd68c9281d07a22e54d1bfd72b12306ac is an ancestor). I extracted the revision with `git archive` into /fast/scratch/hyaku/tsuku26/w2/RevShonenEvidence/rev/ and read every cited file there. Evidence pointers name the lane path (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/...); the relative path is the same in the extraction. I compared the new lines with the old lines recorded at corpus/lessons/round-26.md:76-78. The lane was not written.

## Findings, most severe first

1. Box 4 states an absence that its own sources contradict (medium). [obs] [inf]
- SHONEN.md:12 says "recipient acknowledgement and acceptance are unobserved".
- PROVINCE.md:83, inside a cited range, says: "The committed-kaika receipt sweep found one recipient-side packet response in mori; acceptance/resolution are not inferred."
- corpus/knowledge/adjacency-recheck-2026-10-19.md:89-91 (cited by box 4) records that mori's committed HEAD adds the packet identifier, a 0-to-1 recipient-side response. Line 91 calls it "receipt/answer evidence only".
- corpus/knowledge/adjacency-handoffs-fleet-r1.md:226 says mori's committed HEAD "records receipt of `TSUKUROI-F1-MEM-01`" and that this "supersedes the packet's earlier `prepared`-only status for receipt evidence".
- The lane's own lifecycle definition, corpus/knowledge/adjacency-handoffs-fleet-r1.json:131, reads "acknowledged": "Named recipient has supplied a durable receipt." On its face, mori's committed receipt meets that definition. [inf]
- The ledger was not updated. The same JSON still gives ADJ-04 the state "prepared" (line 82). The 22:07 table in adjacency-recheck-2026-10-19.md:47 and :52 says no named-recipient receipt was found. The 22:57 snapshot (line 74) supersedes only the pin-match total, so the lifecycle conflict is open. [unk] which state the lane intends.
- Effect: the sentence is wrong as written. The error understates the recipient evidence rather than inflating the box, but it misleads a reader. Accurate wording: a recipient-side receipt is observed in mori; acceptance and resolution are unobserved; the ledger state reads "prepared" and is stale.

2. Box 1's "so no superseded note is cited here" holds for whole notes only (medium). [obs] [inf]
- SHONEN.md:6 cites SKILL.md:38-50, 90-141, 179-209 and 1676-1753. Inside those ranges:
- Checklist step 6 (SKILL.md:118 and :120) says "both `7.2.3` today" and calls the 7.1.4 dkms registration present. The round-18 freshness notice at SKILL.md:1923-1924 says both readings are superseded.
- Checklist step 9 (SKILL.md:129-133) runs `snapper list-configs` and reports "→ empty" and "no snapshot net is configured". SKILL.md:1925 says those readings are superseded for config presence. SKILL.md:1742-1745 says `snapper list-configs` "is not a non-activating probe" and to "Do not invoke it in the new procedure".
- Step 10 (SKILL.md:135) gives "last: 2026-10-13 16:37"; SKILL.md:1926 supersedes that reading.
- The decision table row for update safety (SKILL.md:50) and the Sources section (SKILL.md:203) repeat the "`snapper list-configs` (empty)" reading. SKILL.md:1932 supersedes "every repeated current-use restatement of the same premise in this file."
- The range 1676-1753 contains the pointer at SKILL.md:1694-1695 to corpus/knowledge/root-dac-decision-r12.md, which is marked "Superseded after outside rejection" at its own line 7. The marker at SKILL.md:1719 calls "the round-12 matrix pointer above" historical. [inf] "above" refers to that pointer. The box does not name the note, but the range it cites leads to it.
- The round-12 section ends at SKILL.md:1716. The cited range runs on into the round-13 unit-path section, which starts at SKILL.md:1717. [obs]
- The four per-plane notes have no whole-file marker in their first 20 lines. They do carry current-use caveats further in: driver-firmware-plane.md:274-281 is a "Stale:" list that includes the "driver plane is healthy" verdict quoted by the decision table at SKILL.md:49; aur-risk-plane.md:351-425 has notices that "supersede it for current use only" (for example line 357); package-state-plane.md:333 supersedes recheck commands for some rounds. [obs]
- Effect: the existence claims (decision table, checklist, error patterns, Sources) are true. The sentence about superseded notes overstates how clean the cited SKILL ranges are. Fix by citing the current-use notices next to the checklist, or by narrowing the sentence to "no cited corpus note carries a whole-file superseded marker".

3. Box 3 cites a checklist and an adjacency range that contain superseded text (low to medium). [obs] [inf]
- SHONEN.md:10 cites SKILL.md:522-532 as the "no-oral-context executor checklist". Step 1 says "Confirm gate identity (md5 above). Mismatch → stop" and step 2 expects "PASS (26 cases, 26 passed, 0 failed)" (SKILL.md:524-526). SKILL.md:627-628 and :690-693 supersede the 26-case pin and the md5 pins; lines 692-693 say step 2 "is superseded to `PASS (35 cases, 35 passed, 0 failed)`". Later counts are at SKILL.md:1599 (80 cases). [inf] As written, step 1 would stop an executor at the current gate, so the checklist cannot be run at this revision without the re-distillation that SKILL.md:524 itself says is owed. The box line discloses the 444-line test but not this.
- The adjacency range (corpus/knowledge/adjacency-handoffs-fleet-r1.md:156-157) says "one prepared observation". The note's later section at line 226 supersedes the prepared-only status for receipt evidence (see finding 1).
- The accurate parts: corpus/knowledge/executor-test-sufficiency.md:19 records 444 lines for the SKILL under test; lines 3-4 say one executor seat ran the test; lines 106-136 hold the per-step table and tally.
- "Remains unexecuted" matches the record. A bounded search of corpus/, SKILL.md, LOG.md, SCORECARD.md and plans/ (22 matching files) found no later whole-SKILL run. LOG.md:153-154 lists the retest as open, and corpus/lessons/round-18-verifier-spotcheck.md:278 says Box 3 "still has no context-naive whole-SKILL retest". Only 20 of the 22 matching files were displayed. [unk]

4. Box 4 cites the pin re-check without its drift result (low). [obs]
- SHONEN.md:12 cites "the sibling pin re-check" in corpus/knowledge/adjacency-recheck-2026-10-19.md, plus PROVINCE.md:121-146 "with their pinned digests". The 22:57 snapshot in that note reports one of eight sibling pins matching (adjacency-recheck-2026-10-19.md:76-87; line 87: "The original pin match count is now 1/8 (mado)"). PROVINCE.md:132 says the pins "are stale by design once a sibling commits again". Box 4 is titled "PROVINCE.md still accurate". The anchors do resolve (8 of 8 in range, per the same note), but the line omits the drift.

5. The machine check cannot see most of this (low; residual risk). [obs]
- tools/check-self-assessment.py describes the box checks K24 to K27 at lines 26-29 and their logic at lines 724-761. By its own description, they read only the first 20 lines of each corpus/knowledge note a box names, and they test only for the word "superseded". They do not read SKILL.md or PROVINCE.md ranges. K20 to K23 test that named paths exist, not line numbers. "Supersedes" wording such as adjacency-recheck-2026-10-19.md:74, adjacency-handoffs-fleet-r1.md:222 and :226 and aur-risk-plane.md:357 is outside the check's wording.
- I checked the first 20 lines of the eight cited notes by grep. None contains "superseded". So the check should pass all three new lines, and findings 1 to 4 are invisible to it.

## Confirmed (no finding)

- Path existence: SKILL.md, PROVINCE.md and all eight cited notes (package-state-plane.md, systemd-user-plane.md, driver-firmware-plane.md, aur-risk-plane.md, adjacency-handoffs-fleet-r1.md, executor-test-sufficiency.md, adjacency-recheck-2026-10-19.md, adjacency-anchors-r19.md) exist at the revision. Every cited range lies within its file.
- Range boundaries: SKILL.md:38-50 (heading at 38, update-safety row at 50); 90-141 (heading at 90, checklist ends at 140); 179-209 (Sources; next heading 211); 453-551 (round-3 append; next heading 552); 2028-2036 (Error patterns heading at 2028, entries E1 to E6 at 2030-2035); 1717-1721 (round-13 heading at 1717, historical marker at 1719). adjacency-handoffs-fleet-r1.md:136-186 is exactly sections 4 and 5 (section 6 starts at 187). PROVINCE.md:44-52 (table header at 44, ADJ-01 to ADJ-07 at 46-52); 75-83 (Frontier); 121-146 (anchor rows 121-130, limits at 132, digests 137-146); 148-152 (R20 section); 85-90 (round-12 paragraph); 92-106 (round-13 correction at 92-96, round-14 erratum at 98-106). SKILL.md:1078 starts the kill-event classes section, which the 1078-1102 cite covers.
- Old lines: corpus/lessons/round-26.md:76-78 match the base e9f5356c text exactly. The base-to-revision diff changes only SHONEN.md lines 6, 10 and 12 (three hunks).
- Box text and marks: lines 5, 7, 9 and 11 are identical at base and at the revision, and each box reads `- [~]` at both.
- Sweep: `git diff -U0 e9f5356c 7dfea92 -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/SOURCES.md SHONEN.md | grep -E '^-[^-]'` prints exactly the three old SHONEN lines. The numstat shows no deletions in the other four files (LOG.md 10/0, SCORECARD.md 88/0, corpus/QUALITY.md 5/0, corpus/SOURCES.md 12/0).
- Superseded note removed: corpus/knowledge/root-dac-decision-r12.md is marked superseded at its line 7, and neither new box 1 nor new box 3 line names it.
- Box 4's "historical, not current" for PROVINCE.md:85-90 holds. PROVINCE.md:92-96 says the active refinement is root-dac-correction-r13 and that the round-12 entry is retained with a supersession notice.
- Box 4's limitation statements hold: the kill and OOM boundary is unexamined (PROVINCE.md:125 gives mori the kill/OOM classification row, and SKILL.md:1078 is tsukuroi's own class table), and kaidoku and revenger ownership is unruled (PROVINCE.md:51 and :79-80).

## Old lines compared with new lines

| Box | Old line (round-26.md:76-78) | New line (SHONEN.md) | Verdict |
|---|---|---|---|
| 1 | Cites SKILL sections and corpus/knowledge/root-dac-decision-r12.md | Cites SKILL ranges and four plane notes; no root-DAC note named | Removal correct; "no superseded note" sentence overstates (finding 2) |
| 3 | Cites root-dac-decision-r12.md and adjacency sections 4-5 | Cites adjacency 136-186, SKILL 522-532, 453-551, executor 15-20 and 106-136, SKILL 1717-1721 | Removal correct; checklist and adjacency range carry superseded text (finding 3) |
| 4 | Cites PROVINCE round-12 refinement and .ufo/waves/round-12/resumed/OverlapHostR.md; "OS diagnosis remains here" | Cites PROVINCE 44-52, 75-83, 85-90, 92-106, 121-146, 148-152, SKILL 1078-1102 and two notes | "Acknowledgement unobserved" is wrong (finding 1); the OS-diagnosis phrase was dropped without comment [obs] |

## Residual risk and verification gaps

- I did not run tools/check-self-assessment.py or any other lane tool. I read the K24 to K27 logic from grep excerpts. Whether its results at 7dfea92 match the round-26 lesson is outside this review. [unk]
- No check covers line ranges. The content checks here were by hand.
- The four plane notes were surveyed for supersession markers, not read line by line.
- Two of the 22 matching files in the no-oral-context search were not displayed. [unk]
- The lane working copy of SHONEN.md was not compared, because the assignment is the revision.

Suggested repairs for the lane owner (not applied): replace "recipient acknowledgement and acceptance are unobserved" in SHONEN.md:12 with "a recipient-side receipt is observed in mori; acceptance and resolution are unobserved; the ledger state is stale". In SHONEN.md:6 and :10, replace "no superseded note is cited here" with a precise statement, or cite SKILL.md:1919-1932 and 1742-1745 next to the checklist.

Scope: read=SHONEN.md and corpus/lessons/round-26.md at 7dfea92 and base e9f5356c; SKILL.md, PROVINCE.md, corpus/knowledge/{package-state-plane,systemd-user-plane,driver-firmware-plane,aur-risk-plane,adjacency-handoffs-fleet-r1,executor-test-sufficiency,adjacency-recheck-2026-10-19,adjacency-anchors-r19,root-dac-decision-r12}.md and the .json ledger at 7dfea92, by read and grep over the cited ranges; grep excerpts of tools/check-self-assessment.py; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevShonenEvidence.md; executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 7dfea9244a84a0e2439f0698e54491e5d7b7c467 | tar -x -C /fast/scratch/hyaku/tsuku26/w2/RevShonenEvidence/rev; read-only git cat-file, merge-base, ls-tree, show, diff -U0, diff --numstat and log -1 against the lane; wc -l and awk line lengths on the extracted copy; file-existence tests and grep on the extracted copy
Model: anthropic/claude-haiku-5-5
Installs: none
