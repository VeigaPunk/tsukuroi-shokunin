# CritAdjVacuity — first falsifier of C1 (adjacency)

Census: `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` (inbound 114, outbound 10, JSON :88-89).

## Attack 1 — denominator padding. VERDICT: defect, fixable.
[obs] 89/114 inbound `sibling_path` start `.ufo/` (jq count): sealed wave reports that will never be edited — classifying them produces no handoff. Of the 25 "operative", ≥4 are also immutable records (`census/round-12/connector.md` IN-090; `census/round-16/transcripts/...` IN-091 — a tool-call *echo* `read(...)⇒ok`, not a reliance; `plans/round-9.plan.md` IN-114; `corpus/knowledge/closeout-r11.md` IN-102) plus 4 `plans/round-5*` pointers (IN-103..106,108,110,113). ~8 more IDs are duplicate reliance sites (IN-070/071 same file; IN-105/106,113 same row; IN-067–069 same row). Honest headline: **≈15 live reliance sites** (mori PROVINCE/SKILL/corpus×6, tameshi service-optin×4, tameshi fleet-suite/mutation-case×2, kama-advice targets IN-016..018 are `.ufo/`).
Required change: gate emits `operative_classified 0→25` and `historical_drift_evidence 0→89` separately; headline claim counts operative only; per-scope verdicts so 89 easy RESOLVES can't mask an operative miss.

## Attack 2 — RESOLVES vacuity. VERDICT: real counterexample exists.
[obs] IN-001..006 point `PROVINCE.md:42`, but the relied-on ADJ-06 "ownership unresolved" row now sits at `PROVINCE.md:51`; line 42 is prose "protocol integrator, never to whichever lane answered first." (census :106-112). IN-067 (live mori PROVINCE) cites `:21-24` = the owned-surfaces table, not adjacency. A quote picked mechanically inside a cited range certifies nothing — RESOLVES is provable garbage.
[obs] 21/114 pointers cite 2–4 ranges (e.g. IN-023 four lines); schema's single found_line cannot cover multi-range reliance.
Required change: (a) `evidence_quote` must instantiate the sibling's relied-on proposition — classifier writes a binding note; (b) per-range results or PARTIAL class; (c) gate ships a negative-fixture arm (in-range/wrong-proposition quote must be rejected), else the check is vacuous by construction.

## Attack 3 — appended section vs QUALITY criterion 21. VERDICT: improves only if it becomes the authority; currently risks triplication + unanchorable cell.
[obs] `corpus/knowledge/adjacency-recheck-2026-10-19.md:7-36,72-87` already owns the pin/anchor table (commits differ: kaika pins vs census pins). A PROVINCE appendix = third authority unless it names itself superseding for routing.
[obs] OUT-003 cites kagi `:54` which is an **empty line** (snapshot `siblings/kagi/c2cab35bc92e/PROVINCE.md:53-55`) — no exact quote possible; `in_cited_range` will be false or the quote leaves the range.
[obs] mori/kama/tameshi snapshots place cited ranges above the first `##` heading (title-line anchors, not `## Core`); OUT-001/005 overlap mori:3-16 — identical (heading,quote) anchors collapse two pointers.
Required change: anchors keyed per ADJ row adjacent to the table (line ranges demoted to hints); quote unique-per-pointer within snapshot; OUT-003 sub-range `:54` repointed or declared unanchorable (9/10 honest, not a padded 10); section states observed-at + supersedes recheck pins for future routing.

## Attack 4 — separability. VERDICT: not fully separable; ordering defect.
[obs] C1 ships `tools/check-adjacency-anchors.py`; C3's gate counts tools/ vs SKILL.md registry (14 files, 13 rows). C1/C2 landing unregistered tools make C3's `baseline_tools_missing` nonzero — C1 changes C3's target state.
Required change: each claim's draft carries its registry row; C3 recomputed post-integration.

Scope: executed=none
