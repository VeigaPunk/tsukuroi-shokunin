# InClass068 — inbound census slice IN-068..IN-076

Model: commandcode/deepseek/deepseek-v4.1-flash.

## Counts (9 records, all operative)
- RESOLVES 8: IN-068, IN-069, IN-070, IN-071, IN-073, IN-074, IN-075, IN-076.
- DRIFTED 1: IN-072.
- UNRESOLVABLE 0.

Draft `.ufo/waves/round-19/build/drafts/InClass068.inbound.json`: 9 objects, exact keys; each `evidence_quote` re-verified as an exact, unique, <=25-word substring of the line named.

## Operative drift (owner handoff; sibling never edited)
- IN-072 — owner lane mori (`SKILL.md:327` at commit 91940fa). The sibling quotes "never restarts services. Detection and report; the operator remediates." at `tsukuroi-shokunin/PROVINCE.md:19`. [obs] Current line 19 is `|---|---|---|` (`PROVINCE.md:19`); the sentence is verbatim at line 28 (`PROVINCE.md:28`). [obs] Cause: lane commit 459e3ce (2026-10-19) inserted the additional-surfaces table above it; `git show 9b70381:PROVINCE.md` line 19 held the sentence before that commit. Suggested portable replacement: heading `## Core` plus quote `never restarts services. Detection and report; the operator remediates.`

## Census caveat (not sibling drift)
[obs] `.ufo/waves/round-19/l1-capture/extract-adjacency-r19.py:24` accepts ASCII `-` only, so four mori records with en-dash ranges are stored truncated at their first number: IN-073 (:23–42 to [23,23]), IN-074 (:120–135 to [120,120]), IN-075 (:245–257 to [245,245]), IN-076 (:344–346 to [344,344]). I classified against the current file and each sibling's real citation. Rejected reading: calling IN-075 DRIFTED from the truncated range; the presence-flag rule is at `corpus/knowledge/oom-event-plane.md:256`, inside the sibling's :245–257. I quoted the cited section heading (`:245`) and recorded the rule line in the note, so the record stays valid if ranges are corrected.

## Undecided
None. [unk] No lane file was absent and no query blocked.

Scope: executed=python3, awk, wc, ls, find, grep, git log, git log -L, git show, git -C mori-shokunin show
