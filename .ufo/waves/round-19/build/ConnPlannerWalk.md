# ConnPlannerWalk

Model: Grok 4.7 (cursor/grok-4.7-fast), trained by SpaceXAI. No install.

Axes: depth, coverage, operability, freshness, calibration, adjacency.

(a) [obs] SCORECARD.md:587: depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8; retired none :598. Last row boot-chain-audit, round 17 (:164). Saturation 9, window 3 (:177-178). Nudge needs every axis ≥9 and three quiet rounds (AXES.md:68-73). Depth and adjacency at 8 block it; round 18 is the only close since round 17. Use :587. :39-52 is the round-11 table (adjacency 7).

(b) [obs] Distinct axes and commands (SCORECARD.md:591-593): C1 adjacency `check-adjacency-anchors.py`, C2 depth `check-boot-writers.py`, C3 calibration `check-registry-coverage.py`. Files absent. Registry 13 rows (SKILL.md:1958-1970); `_revision.py` prose only (:1974); 14 tool files. Isolation gap: open `--registry-from`, and SOURCES inside the depth count (SCORECARD.md:592). Corrections: C1 reads PROVINCE anchors plus `adjacency-pointers-r19.json`; C2 reads its writer registry plus the three captures; SOURCES stays frontier; C3 exits on a named 14-file list versus the highest registry heading (SKILL.md:1952, :1997).

(c) 1 Green at dispatch (SCORECARD.md:596). Correction: `check-seat-scope.py` on build and falsify at the landed hash; token in the item (lesson :256-260). 2 C3 row. Mapped. 3 Three captures. Correction: exec-log names `capture-r19.sh`, `capture-r19b.sh`, `capture-r19c.sh` (lesson :264-266). 4 Load order first; shell helpers stay retained (lesson :267-268). 5 PROVINCE:66 = IN-067/068/069 (census :1663-1728); ADJ-04 is PROVINCE.md:49, outside 35-44. SKILL:318 absent; live quote is mori SKILL.md:327 = IN-072 → PROVINCE.md:19; "never restarts" is :28. Hand off IN-072 and record 318→327; leave mori unedited (lesson :269-270). 6 → C2. Mapped.

Move (depth): key writes by timestamp and pid. [obs] Ten rows host-capture-r19c.txt:11-20; ALPM host-capture-r19.txt:578 and :597 (log 3015, 3047). Repeats host-capture-r19.txt:446-560. Extra 2026-10-11 at host-capture-r19b.txt:1695. [inf] Raw line count exceeds 12. Outbound 10 (PROVINCE.md:33, :46-52); inbound 114. Risk: omitting an ALPM id. Check: writer gate emits these 12 and rejects the Oct 11 line plus journal duplicates.

Scope: executed=none
