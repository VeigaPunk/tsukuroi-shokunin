# ConnSaturation

Axes: depth, adjacency (tied 8), operability, freshness.

## Evidence
[obs] No waiver. `AXES.md:68-70` waives the lowest-axis duty only if every owned axis is at least line 9 and no capability row landed inside N=3 (`SCORECARD.md:177-178`). Depth 8 and adjacency 8 are below 9 (`SCORECARD.md:295-298`, `:541`). The r17 `boot-chain-audit` row resets the idle counter only (`SCORECARD.md:527`). [inf] “Window3 unchanged” (`:541`) names declared N, not the pre-r17 idle count. [obs] Rounds 13–16 were four idle rounds; the nudge did not fire (`.ufo/waves/round-17/build/ConnCapabilityWindow.md:4`).

[obs] Distinct axes. R17: C1 depth, C2 freshness, C3 operability; capability inside C1 (`SCORECARD.md:502-507`). Closure admitted all three, none harmed (`corpus/lessons/round-17-verifier-spotcheck.md:37-38`, `:139`). R18 uses that split (`SCORECARD.md:533-541`). Two claims on one axis count as one (`AXES.md:31-33`).

[obs] Depth-8 duty is per round, not an ordinal exit (`AXES.md:33-34`). R17 met it by C1 0→5, ordinal 8→8 (`spotcheck:121`). The capability did not, so the duty still binds. R18 C1 is unmeasured (`SCORECARD.md:544`), so it has not met the duty yet.

[obs] `spotcheck:123` cites the audit under operability; `SCORECARD.md:507` puts it in C1. Cell 44/44 (`SCORECARD.md:164`) contradicts `.ufo/waves/round-17/measure/final/selftests.txt:11` (`total=45 failed=0`) and `:520`.

## Affected axes
Calibration, via stale 44/44.

## Move
Non-claim r18 sentence: waiver false; N=3; counter reset at r17; C1 stays depth; no new capability row. Append that `:164` 44/44 is superseded by `selftests.txt:11` and `:520`; do not edit `:164` (`spotcheck:87`). Exclude `SCORECARD.md` from both registries (defect 3 `spotcheck:197-200`; defect 5 `:207-213`). Do not credit the audit or `_revision.py` as depth or as a repertoire row.

## Risks
In-place 44→45 rewrites closure-cited bytes. Filing 44/44 under C1 or C3 mixes defect 4 into a routed count. Moving C1 to adjacency drops depth or exceeds three claims.

## Verification
R18 text keeps saturation 9, window 3, retired none, no capability row, C1 on depth. Registries omit `SCORECARD.md`. `check-revision-binding.py` does not import `_revision`.

Scope: executed=none
