Verdict: No sibling at its current tip cites this lane's `coredump=` or `class=coredumps` value as a number of crashes or cores, and none carries a pointer into a file changed this round that has drifted; mori's five inbound pointers still resolve to unchanged lines.

## Findings

1. [obs] Sibling scan (git grep across all 20 lane repos at current tip) for `class=coredumps` returned no hits outside tsukuroi. Sibling scan for `coredump=` found only mori/tameshi references to tsukuroi census fixture syntax (`coredump=1` in mori's r13/r14 regression harness and tameshi's census mutation cases), which treat it as a fixture field, not as a crash/core count. No sibling cites the round-34 values 1621/252/1365/4.

2. [obs] Mori (tip `cedb0ec4`, round 35) is the adjacency owner for signal-11 coredump classification (PROVINCE.md OUT-005). Its round-34/35 work is the disk-write-rate tool (SKILL.md §Round34) and sources S199-S204; it does not import or cite `corpus/knowledge/coredump-count-unit-r34.md` or any new round-34 tsukuroi file. Searched tokens `coredump-count-unit-r34`, `adjacency-mori-oom-r27`-adjacent new files, `check-knowledge-header`, `probe-child-env-allowlist-r34`, `879daa95`, `df661507`, `3457f287`: no hits in mori except the pre-existing `adjacency-mori-oom-r27.md` pointers below.

3. [obs] Mori inbound pointers into files changed this round, verified against the landed tree:
   - `mori-shokunin/.ufo/waves/round-28/w1/ConnSiblingOverlap.md:84,110` and `round-30/w1/ConnectorSiblings.md:36-37,73` cite `tsukuroi corpus/knowledge/adjacency-mori-oom-r27.md:14-24,17,23,30-34,34`. This round's only edit to that file appended "recheck cadence: on-release" to line 4, changing no line count, so all cited lines still hold their recorded content (verified: line 14 = OV1 row, 17 = OV4, 23 = observed bullet, 34 = Q12 bullet).
   - `mori-shokunin/.ufo/waves/round-30/w1/ConnectorSiblings.md:73` cites `memory-pressure-r25.md:387,390,398`; this round appended "Recheck cadence: 30d" to line 3 only, so lines 387 (MP4), 390 (MP4 action) and 398 (JSON supersession) are unchanged.
   - `mori-shokunin/.ufo/waves/round-26/w1/ConnSiblingOverlap.md:56` and `round-28/w1/ConnSiblingOverlap.md:60` cite `tools/check-boot-chain.py:74,82` (earlyoom package list); this round edited only line 799 of that file, so both lines still read `EXPECTED_PACKAGES` and the capture quote.
   - `mori-shokunin/.ufo/waves/round-32/w1/ConnectorSiblings.md:87` cites `tools/check-recheck-commands.py:2` (docstring); this round edited only line 796, so line 2 is unchanged.
   - `mori-shokunin/.ufo/waves/round-17/build/SiblingSeatDeathTools.md:91` cites `tools/check-seat-scope.py:12-15` (findings list); this round edited lines 171 and 540, so 12-15 are unchanged.

4. [obs] Other siblings' pointers into changed tool files (kagi `check-boot-chain.py:378-382`, mado `check-boot-chain.py:35-36,612-614` and `check-section-citations.py:20-24,456-458,489-490`, tameshi `check-*-scope.py:162` etc.) point at lines untouched this round (edits are at 799/796/171/540 and the new `check-knowledge-header.py`/`probe-child-env-allowlist-r34.py` have no inbound pointers yet). `SKILL.md` and `SCORECARD.md` changes this round are pure appends, so earlier line-number citations in siblings are unaffected.

5. [inf] Net: the round-34 changes add a reading rule and a knowledge-header gate without moving any line a sibling points at; no inbound pointer drifts. The new C2 note is self-contained and explicitly disclaims crash-cause classification, so mori's OUT-005 ownership is not contested by it.

Scope: read=git grep across 20 sibling lanes, targeted line verification in tsukuroi changed files; wrote=.ufo/waves/round-34/w2/ConnSiblingAfter.md; executed=git grep, git diff, nl line checks.
Model: not exposed
Installs: none