# CritAdjBoundary — C1 adjacency boundary falsification

Model: devin/swe-2. Attack on C1's adjacency claim; defects are fixable, none blocks the axis.

1. **Pinned commits are stale-by-design; need explicit limit text.** [obs] `corpus/knowledge/adjacency-recheck-2026-10-19.md:76-87` shows pin decay 5/8→1/8 matches in ~50 min (2026-10-19). Round-19 anchors pin capture-time `sibling_commit`/`sibling_blob_sha256` (`adjacency-pointers-r19.json` OUT-001..010); they pre-date any later sibling commit. The existing disclaimer "the table does not freeze another lane's authority" (PROVINCE.md:70-73) covers only the line-range table. The appended section MUST carry its own point-in-time/non-authority line, else verbatim sibling text plus pinned hashes reads as frozen authority — what PROVINCE forbids.

2. **Quoted sibling text risks false provenance.** [inf] Copying sibling sentences into tsukuroi's PROVINCE makes this lane's document assert sibling declarations. Minimum correction: label every anchor "point-in-time quote of sibling-declared text at pinned commit; sibling HEAD remains authoritative; tsukuroi claims no ownership or correctness over it."

3. **Drift handoffs must be report-only.** [obs] PROVINCE.md:38 "a recipient is an analysis/report owner, not permission to repair"; :60-61 "if no row fits, report to the integrator". Pointer-drift is none of the seven classes. Handoffs must report observed pointer + relied-on quote only. Auto-computing a replacement range (e.g. ranged cites IN-068 `oom-event-plane.md:231-257,279-281,301,344-367`) could deliver a wrong "correction" — tsukuroi effectively editing sibling content.

4. **Scope predicate over-triggers.** [obs] `operative` = path lacks `.ufo/`, but `souji census/round-12/connector.md` and `tameshi plans/round-9.plan.md` (IN-090, IN-114) are dated records; stale lines there are correct-by-construction. DRIFTED handoffs for them are false positives.

5. **Live counterexample confirmed.** [obs] IN-072: mori SKILL.md:327 cites `tsukuroi-shokunin/PROVINCE.md:19` "never restarts services…"; the quote is verbatim but now at PROVINCE.md:28 (line 19 is a table rule). Genuine drift; safe handoff presents the quote, prescribes no edit.

6. **Blank range defect.** [obs] OUT-003 range 54-54 is an empty line in `siblings/kagi/c2cab35bc92e/PROVINCE.md:54`; no <=25-word quote exists — needs gate exclusion or a widened kagi range.

Impacted axis: adjacency (C1).

Scope: executed=ls, python3, grep, sed
