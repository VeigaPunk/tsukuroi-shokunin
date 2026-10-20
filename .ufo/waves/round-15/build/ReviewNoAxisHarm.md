# ReviewNoAxisHarm — round 15 scope / history / ordinal invariants

Baseline `0db618a` = HEAD. Snapshot is the in-progress tree at review time; it moves.
No ordinal in any in-tree text is raised by round 15. Findings are documentation and history defects.

## Findings (severity order)

**F1 (medium) Plan contradicts itself on R14 pair writes.** ScribeClaims.md E4 says "R15 must not edit the R14 pair". The LocatorGate predicate and ActiveRefs task require notices in r14 MD/JSON. Working tree now has additive-only edits to `corpus/knowledge/source-scope-correction-r14.{md,json}`: JSON `]`→`],` plus new `r15_supersession` key; MD appended `## R15 supersession`. Additive matches the r13→r14 precedent, but the writer is not the C1 owner and the change is uncommitted. Fix: amend E4; make the preservation check strip `r15_supersession` before comparing to HEAD.

**F2 (medium) Calibration overclaim in in-progress LOG.** LOG.md:766 "C1/depth resolves these"; :770 "C1 works depth". No "author-side, pending non-author closure" qualifier. The round-14 entry (LOG.md:751) carries that qualifier; rounds 12–13 were rejected for overclaimed depth. LOG.md:770-771 also attaches "Depth8 and adjacency8 remain tied lowest" to the C2 sentence. Fix both.

**F3 (medium) "Clean" census overclaim.** LOG.md:775 "clean entry/census context". `.ufo/waves/round-15/build/start.json` census: exit 0 with five W04 warnings (S038, S041, S042, S043, S044). Round-14 lesson: "not a warning-free pass". Fix: "exit 0 with five disclosed W04 duplicate-URL warnings"; expect a sixth for S046 (ScribeClaims E5).

**F4 (medium) Ordinal governance text is dangling.** `AXES.md` is cited 14× outside `.ufo` (SCORECARD.md:3, :165, :173; plans/*; adjacency-handoffs-fleet-r1.md). `LEARNING.md` is cited in calibration-synthesis.md, package-state-plane.md, plans/*. Neither file exists in the tree; `git log --all -- AXES.md LEARNING.md` is empty. So the saturation line 9 / window 3, the stagnation nudge, the six-axis vocabulary and the capability-row admission rule have no committed text. Round-15 artifacts must cite SCORECARD prose, not AXES.md. Record the dangling reference by append-only erratum. Do not create AXES.md: that would invent rules.

**F5 (low-medium) Stale SCORECARD table without inline pointer.** SCORECARD.md:45-52 ("final self-assessment") still reads coverage 8, freshness 8, adjacency 7. Current values are at SCORECARD.md:273-274 and :294-296 (coverage 9, freshness 9, adjacency 8). The table has no inline superseded marker. Fix: append a pointer; do not rewrite row values.

**F6 (low-medium) Census count pin conflict (not executed here).** SKILL.md:1534 and :1593 and SCORECARD.md:99 pin `PASS (80 cases)` as current. HEAD census blob sha256 `d17d32a3…` equals the round-12 blob (`70fede2`), whose record (SCORECARD.md:257-258) claims 97/97 with 2 skips. The 80-case script (`0ecf3ff`, sha `10452443…`) is the one SCORECARD.md:77 calls "unchanged". Fix: report both as dated history; state no current count until L1's single post-integration run.

**F7 (low) Checker false-positive risk.** R15 notices quote the superseded phrase "documents no further values for this option" (r14 MD R15 section; r14 JSON `r15_supersession.notices[1].superseded_text`), and QUALITY22 forbids appending it. A negative-phrase predicate must exempt quotes inside a named supersession block, or the gate fails on the correction itself. The exemption must not mask a restored unqualified claim. AttackNegativeRestore should test both sides.

**F8 (low-medium) Unlisted scope and capability surface.** The spec names two pairs. Dispatch adds `tools/check-locator-clarification.py` (LocatorGate), `tools/measure-update-recheck.py` (IncidentMeasure), SKILL and corpus README routing (ActiveRefs), and a gate-registry row. SCORECARD.md:165 admits capability rows only when a round demonstrates the capability running. Fix: LOG declares the checkers as checker/probe; no Capabilities row; no ordinal basis.

**F9 (low) Freshness adverse-evidence rule is unstated.** The operator-reported partial upgrade is adverse evidence. Precedent: SCORECARD.md:1 round-12 "recorded as drift, not smoothed". C2 must state "freshness 9 unchanged, no uplift; state BLOCKED; drift recorded". Do not claim re-verification as freshness gain. Do not propose a drop either: no rule exists while AXES.md is missing (F4).

## Invariants that hold (evidence)

- S-IDs: `corpus/SOURCES.md` has 45 rows at HEAD and now (S001–S045). No S046–S048 anywhere in the tree yet: no ID collision.
- R14 JSON: R14-VALUE-DOMAIN and R14-COMMENT-ATTRIBUTION unchanged. Working-tree diff removes only `  ]` (comma added).
- QUALITY.md: +3 lines, 0 removed (QUALITY21/22).
- Ordinal statements agree: depth 8 unchanged (LOG.md:751, SCORECARD.md:294-296); coverage 9, operability 9, freshness 9, calibration 9, adjacency 8. LOG.md:770 "All ordinal scores stay unchanged." ScribeClaims "ordinal deltas0" matches.
- Seats: `dispatch.json` counts spawn 64; `task-result.json` lists 64 names.
- Not yet present at check: `corpus/knowledge/source-locator-clarification-r15.*`, `partial-upgrade-recheck-r15.*`.

## Recommendations (ranked)

1. Amend ScribeClaims E4 to "additive notices only in R14 pair"; strip `r15_supersession` in the preservation check (F1).
2. LOG: add "author-side, pending non-author closure"; remove "clean"; split C1/C2 sentences (F2, F3).
3. Append an erratum for AXES.md/LEARNING.md absence; cite SCORECARD prose only (F4).
4. Append pointers in SCORECARD table and census-pin chain; one post-integration run by L1 only (F5, F6).
5. Declare new checkers and probes as non-capability; no Capabilities row (F8).
6. C2 wording: "freshness 9 unchanged, no uplift, BLOCKED, drift recorded" (F9).

## Limits and tools

- Read-only. No tests, selftests, census, checkers, probes, or host commands run. Git used only for `show`, `log`, `status`, `cat-file`, `merge-base`, `rev-parse`, and `sha256sum` on committed blobs.
- Snapshot-bound: tree was mid-write; re-check before quoting.
- Census count (F6) unresolved: no execution by design.
- Tools installed or updated: none.
