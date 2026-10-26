VERDICT: supports

# CritNoHarmFinal — Item N-1 no-harm, 6951ead9 (base) → 8acf0b02 (tip)

Seat CritNoHarmFinal (L2, leaf, read-only). Base `6951ead90566b2d74f7c45b4efca29246badad64`, tip under test
`8acf0b022586a0f3164c77659fb96ba5f90949b6`. Wave-1 integration commit `9b974f2a`; implementation `717b716a`.
All commands below are read-only `git` against the lane; no counter was run, nothing was written to the lane or the
host. Receipts: `.ufo/waves/round-43/w2/CritNoHarmFinal/` (`name-status.txt`, `numstat.txt`, `bca.diff`,
`sources.diff`, `append.diff`). Scratch `/fast/scratch/hyaku/tsukuroi-r43/CritNoHarmFinal/` removed on exit.

## 1. Deleted files / deleted lines outside the claims' surfaces

`git -C $L diff --name-status 6951ead9 8acf0b02` → no `D` entry (44 A, 8 M). `diff --numstat` → deletions in
exactly two files:
- `tools/boot-chain-audit.sh` 32 insertions / 7 deletions — the 7 deleted lines are the old
  `if find <8 start points> -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then … fi` block inside
  `boot_inputs_newer` (base 480-487), replaced by the `inputs_newer_than` call (`bca.diff` hunk `@@ -477,14 +491,9 @@`).
  This is the C1 claim surface itself (the routed fail-open fix; in scope). Nothing else deleted in that file.
- `corpus/SOURCES.md` 3 insertions / 1 deletion — the deleted line is the S237 row, re-added in place with only its
  `used-by` column extended (see §4). All other 44 added files and the remaining M files are additions-only.

No deleted file, and no deleted line outside the two claim surfaces. (The binary `patch.zst` receipt shows `- -`
in numstat; it is a new file, not a deletion.)

## 2. SCORECARD.md append-only

`git diff 6951ead9 8acf0b02 -- SCORECARD.md` → single hunk `@@ -2644,3 +2644,41 @@`, additions only (38/0 in
numstat): the "Round 43 — declaration" section appended after the round-42 "**retired:** none." line. No middle
edit, no deletion. Verified visually and by numstat.

## 3. Moved pins (lane-internal pins into boot-chain-audit.sh and btrfs-scrub-record-r42.md lines)

Grep over the live tracked docs at tip for `boot-chain-audit.sh:<n>` / `btrfs-scrub-record-r42.md:<n>`:
- `SCORECARD.md:2642` — "fix `tools/boot-chain-audit.sh:480-487` (`find -quit | grep -q` under pipefail)".
  Pre-existing round-42 planned-item note; the pinned range is the base coordinate of the buggy block that round 43
  replaced. The appended round-43 declaration marks the surface movement explicitly: "Surface moved | `tools/boot-chain-audit.sh` `boot_inputs_newer` (base :480-487)". Historical base-coordinate statement; correct as history (same classification as wave-1 `.ufo/waves/round-43/w1/AdjPins.md` §1, which lists exactly these self-pins). Tip positions: helper `inputs_newer_than` at :463, call at :494-496 — the pinned content no longer exists, which is the fix, not drift.
- `SKILL.md:3893` — "Not fixed here (routed): `tools/boot-chain-audit.sh:480-487`". Round-42 section directly above the new round-43 section that records the fix; same base-coordinate classification.
- `SKILL.md:2058` — pins `tools/boot-chain-audit.sh:60`; line 60 is unmoved (round-43 hunks start at 463), so this pin did not move.
- `corpus/README.md` and `SKILL.md` new scrub-record sections cite r42.md "its header line 4" — at tip, r42.md line 4 is exactly the new `superseded-in-part:` line (`git show tip:corpus/knowledge/btrfs-scrub-record-r42.md | sed -n 4p`), so the pin is accurate at tip.
- No other live doc (PROVINCE.md, corpus/SOURCES.md, r43.md, corpus/lessons/round-43.md, the two new counters) carries a line pin into either file; `corpus/lessons/round-43.md` grep → no hits.
- r42.md itself gained one line at :4 (header pointer, 1/0 in numstat); lines ≥4 moved +1. The only live pins into it are the heading/line-4 refs above, both accurate at tip. No unmarked moved live pin.

## 4. corpus/SOURCES.md rows only added or used-by changed

Numstat 3/1, matching: the S237 row was re-written in place and only its `used-by` column changed
(`corpus/knowledge/btrfs-scrub-record-r42.md` → `…r42.md, corpus/knowledge/btrfs-scrub-record-r43.md`); field-level
comparison shows all 12 other columns byte-identical (base field 11 = "corpus/knowledge/btrfs-scrub-record-r42.md",
tip field 11 = "corpus/knowledge/btrfs-scrub-record-r42.md, corpus/knowledge/btrfs-scrub-record-r43.md"). S240 and
S241 are new rows (additions). No other row was deleted, reworded or re-anchored.

## 5. PROVINCE/README edits append-only

- `PROVINCE.md` +10/0, single trailing hunk (`@@ -242,3 +242,13 @@`): round-43 scrub-record note appended.
- `corpus/README.md` +11/0, single trailing hunk (`@@ -412,3 +412,14 @@`): round-43 coverage note appended.
- `SKILL.md` +156/0, single trailing hunk (`@@ -3954,3 +3954,159 @@`): round-43 sections + registry rows appended.
- `corpus/knowledge/btrfs-scrub-record-r42.md` +1/0: header `superseded-in-part:` pointer line appended at :4.

## 6. What I did not do

Did not run the C1/C2 counters, the census or the audit (heavy runs; not this axis). Did not check sibling repos,
untracked files, or pins into other lane files (wave-1 `AdjPins` covered siblings; this seat's axes are the five
above). Did not modify anything in the lane, host, or PATH. No tool installs.
