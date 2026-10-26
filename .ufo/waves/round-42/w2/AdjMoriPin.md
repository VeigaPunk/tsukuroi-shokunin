VERDICT: supports (mori pin confirmed moved at the dispatch tip with corrected coordinates; w1's "re-aligned at tip" note is itself stale at 78abb8b5; two further moved sibling pins found beyond w1's scan — tameshi live knowledge doc, souji r32 record; C2 record surface still has zero sibling pins)

# AdjMoriPin — F-18 moved sibling pin handoff (round 42, wave w2)

Seat: AdjMoriPin (L2 connector, leaf). Scope: item F-18 — compute the content pinned by
`mori-shokunin/PROVINCE.md:287` at lane tip `78abb8b5cdc9da511b4fc523e661517a68dd33d3`, draft the
report-only handoff text for mori, and check every other sibling `tsukuroi-shokunin/` line pin for
motion between base `c8efaa3f120834541f8de1e5e0367e8d1593bae6` and the dispatch tip. Read-only on the
lane and all siblings; no counters run; no host mutation.

## Commands run (all read-only)

```sh
git -C tsukuroi-shokunin log --oneline c8efaa3f..78abb8b5 -- tools/tsukuroi-census.sh
git -C tsukuroi-shokunin diff c8efaa3f 78abb8b5 -- tools/tsukuroi-census.sh | grep '^@@'
git -C tsukuroi-shokunin show <rev>:tools/tsukuroi-census.sh | sed -n '<range>p'   # base & tip
git -C tsukuroi-shokunin diff c8efaa3f 78abb8b5 --name-only   # 725 files; lane-source set extracted
# sibling-wide pin scans (cwd = fleet root), receipts in AdjMoriPin/:
grep -rE  'tsukuroi-shokunin/[^[:space:])]*:[0-9]' --include='*.md' --include='*.sh' \
  --include='*.py' --include='*.txt' *-shokunin          # 677 hits
grep -rIE 'tsukuroi-shokunin/[^[:space:])]*:[0-9]' --exclude-dir=.git *-shokunin   # 731 hits
# per-pin motion check: same-coordinate content compare base vs tip (check-pins.sh, receipt)
```

Lane-source files changed base→tip (excluding `.ufo/waves/round-42/` wave artifacts):
`PROVINCE.md, SCORECARD.md, SKILL.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md,
corpus/knowledge/{adjacency-anchors-r19.json, alpm-package-anatomy-r41.md, btrfs-scrub-record-r42.md,
pacman-transaction-order-r39.md}, tools/{tsukuroi-census.sh, check-scrub-record-r42.py,
score-size-invariance-r42.py}`.

## 1. mori PROVINCE.md:287 — the named pin (MOVED, stale by +3 at the dispatch tip)

Pin text (mori-shokunin/PROVINCE.md:287, working tree, unchanged since round 30 `af42101d`):

> **Adjacency (wave-2 finding CriticHarmAxes A1; wave-1 ConnectSiblingPsi):** tsukuroi's census reads the same
> system `/proc/pressure/memory` file (`../tsukuroi-shokunin/tools/tsukuroi-census.sh:376,1100-1115`) for OS memory
> triage and routes fleet correlation of host pressure to mori (`../tsukuroi-shokunin/PROVINCE.md:30-33`). Shared
> evidence is not shared ownership …

Pinned content = the memory-pressure arm intro comment (`# Round-7 addition, lane S7-2 … the
operator remediates.`), 16 lines. Located by `grep -n "Round-7 addition"` on both revisions:

| revision | line range | shift |
|---|---|---|
| base c8efaa3f | **1097–1112** | — |
| w1 tip f50c28d (per w1 ConnSiblings) | 1100–1115 | +3 (447662088, `@@ -689,9 +689,12 @@`) |
| **dispatch tip 78abb8b5** | **1103–1118** | **+6** cumulative |

Shift attribution: `447662088` (C1 implementation) added +3 net at the probe_packages hunk;
`78abb8b5` (w1 integration) added +3 more in the same hunk (comment 3→6 lines and the `if grep -q`
line split into `local err_line=''` + an awk assignment — `git diff f50c28d 78abb8b5` shows
`@@ -691,10 +691,13 @@`). Content under the shift is byte-identical:
`diff <(git show c8efaa3f:… | sed -n 1097,1112p) <(git show 78abb8b5:… | sed -n 1103,1118p)` → empty.

**Correction to w1:** ConnSiblings.md states "at tip the named content happens to sit exactly at the
pinned coordinates again." That was true at w1's tip `f50c28d` (1100–1115) but is **no longer true
at the dispatch tip `78abb8b5`**: the content now sits at **1103–1118**, so the pin's coordinates
are stale by +3 (they name base 1094–1109).

`:376` half: unchanged — line 376 is the btrfs/sysfs bad-devid comment in both revisions (the
`/proc/pressure/memory` default constant `PRESSURE_FILE` is at line 455 both before and after, as w1
also noted). `PROVINCE.md:30-33` half: unchanged — round 42's PROVINCE.md +7 all appended after
line 235 (`@@ -235,3 +235,10 @@`).

## 2. Draft handoff text for the tsukuroi round report (report-only; no sibling edit)

> **Handoff — mori-shokunin PROVINCE.md:287 census pin (round 42 bookkeeping; report, never edit a sibling).**
> Round 42 (base `c8efaa3f` → dispatch tip `78abb8b5`) moved the census content named by
> `mori-shokunin/PROVINCE.md:287`:
>
> - `tools/tsukuroi-census.sh:1100-1115` — the memory-pressure arm intro (`# Round-7 addition, lane S7-2 …
>   the operator remediates.`) now sits at **1103-1118** at `78abb8b5` (base: 1097-1112). Net +6:
>   +3 from the C1 pipefail implementation (`447662088`, probe_packages comment/awk rewrite) and +3 more
>   from the wave-1 integration (`78abb8b5`, same hunk's comment expansion and `err_line` assignment
>   split). The 16 lines are byte-identical under the shift; only the coordinate is stale (+3).
> - `tools/tsukuroi-census.sh:376` — unchanged; line 376 is a btrfs/sysfs bad-devid comment in both
>   revisions. For the record, the `/proc/pressure/memory` default constant is at line 455 in both.
> - `tsukuroi-shokunin/PROVINCE.md:30-33` (routing half of the same note) — unchanged; round 42's
>   PROVINCE.md insertions all landed after line 235.
>
> mori's adjacency note ("Shared evidence is not shared ownership") remains semantically true; this is
> a bookkeeping side effect of the C1 fix, not a semantic change. mori may refresh the coordinate in
> its own round; tsukuroi claims no edit right into the sibling and made none.

## 3. Other sibling pins into lane files — full check (beyond w1's PROVINCE.md/SKILL.md-only scan)

Two scans of all 20 sibling repos (receipts `all-pins.txt` 677 hits, `all-pins-full.txt` 731 hits
extension-free); each hit into a round-42-changed lane file checked by same-coordinate content
compare base vs tip (`pin-motion-results.txt`). Live sibling docs = lane-root PROVINCE.md / SKILL.md /
corpus knowledge docs; sibling `.ufo/waves/*`, `census/*` transcript trees and scratch clones are
frozen historical records (listed for completeness, not adjacency).

**Moved pins found (3 total, including mori):**

1. **mori-shokunin/PROVINCE.md:287 → census.sh:1100-1115** — stale by +3 (section 1).
2. **tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153 → census.sh:915-970** — stale by
   +6 (base 915-970 content now at tip 921-976; verified byte-identical under the shift). Live durable
   knowledge doc (probation r7 vintage) citing tsukuroi's round-5/7 selftest block shape ("9 new cases,
   26 → 35, block `tsukuroi-census.sh:915-970`"). w1's scan missed it because it covered only sibling
   root PROVINCE.md/SKILL.md. The citation was already a loose historical one; the round-42 shift adds
   +6 staleness. tameshi's SKILL.md blob tables self-flag `stale`; this doc has no such flag.
3. **souji-shokunin/census/round-32/waves/a2w1/deliver-sibling-overlap-w2.md → SKILL.md:3452** — stale
   by +2 (base row now at tip 3454, byte-identical; shift from SKILL.md `@@ -3119,6 +3119,8 @@`).
   Frozen round-32 wave record (duplicated under souji `.ufo/waves/round-32/a2w1/`); historical, not
   adjacency. Its other pins (`SKILL.md:50,95,96,219`, `corpus/README.md:7`, `corpus/SOURCES.md:105`)
   are unchanged at their coordinates.

**Checked and NOT moved:** mado r12 evidence `SKILL.md:101,404,755,842`; mori `PROVINCE.md:8-14`,
`SKILL.md:19` (→PROVINCE.md:19), `oom-event-plane.md` and `kill-event-deep-r8.md` pins (those two
files untouched by round 42); revenger knowledge `PROVINCE.md:51`; souji r12 `PROVINCE.md:3,18`;
souji r33 `SKILL.md:2870,2940,3001,3106`; tameshi `SKILL.md:558-568,599-609,611-617,1059-1063`;
souji r30 record. All identical at the pinned coordinate base vs tip.

**C2 record surface:** zero sibling pins into `corpus/knowledge/btrfs-scrub-record-r42.md`,
`tools/check-scrub-record-r42.py`, or `tools/score-size-invariance-r42.py` — consistent with w1's
zero-hit; nothing moved because nothing pins it.

## Net effect on the round's axes

Adjacency axis: the w1 "one moved pin" finding stands at the dispatch tip with a corrected offset
(+3, not re-aligned) and grows by two pins outside w1's scan scope (one live tameshi knowledge doc,
one frozen souji record). All shifts are pure line offsets from the C1 implementation and w1
integration commits; no pinned content was edited, deleted, or reworded. No contested scope: mori's
note explicitly disclaims ownership; tameshi and souji records make no claim on C1/C2 surfaces. No
action proposed beyond carrying the handoff text in the round report (report, do not absorb; no
sibling was edited).

## What I did not do

Did not run the C1/C2 counters; did not run the census; did not modify anything in the lane, the
fleet root, or any sibling; did not check pins into files outside the base→tip changed set (they
cannot have moved in this round); did not re-verify sibling pins whose targets are tsukuroi
`.ufo/waves/*` receipts (frozen committed snapshots; motion not defined for them).

## Receipts (AdjMoriPin/)

`changed-files.txt` (base→tip changed list), `all-pins.txt` / `all-pins-full.txt` (sibling pin
scans), `pins-into-changed.txt`, `check-pins.sh`, `pin-motion-results.txt` (same-coordinate compare
output).
