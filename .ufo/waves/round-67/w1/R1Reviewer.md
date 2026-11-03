2026-11-03T21:53:06Z
# R1Reviewer — C1 frozen predicate attack (scoped findings)

VERDICT=FAILS
CONTROLS_PASSING=2 of 3

Full commands, rc and observed output: .ufo/waves/round-67/drafts/R1Reviewer-c1-attack.md

Findings:
1. Sourceless S284 row at NF 13, directly after S283, passes every SOURCES clause of the frozen C1 predicate (grep count 284; adjacency; NF 13). The predicate does not check source, tier, Gate quote or fetched bytes.
2. Four SL rows citing scrub.c:9999 (file has 2233 lines; `sed -n '9999p'` empty) pass `grep -cE '^\| SL[0-9]+ \|' >= 4`. No frozen clause reads the cited lines.
3. Four rows with duplicate id SL1 pass the SL count (4). Ids are not required to be distinct.
4. Do-nothing control (base 5abc31d9: note cat-file rc 128, SOURCES 283, SL count 0) is killed.
5. Only the sha256/line-mismatch kill rule touches source bytes; it concerns the re-fetched scrub.c, not the note's cites, and is not in the frozen counting command list.

Not applied: predicates are frozen. Suggested amendments are recorded in the draft for L1 consideration.
