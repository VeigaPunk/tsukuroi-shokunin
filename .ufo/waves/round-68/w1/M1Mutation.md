2026-11-03T22:40:00Z

# M1Mutation — round 68 receipt (C1 RW-row predicate, independent mutation test)

Seat: M1Mutation (mutation-tester), lane tsukuroi-shokunin, round 68 wave w1 (hyaku run 15).
Lane base `42400ec6`; declaration read from `SCORECARD.md` §"Round 68 — declaration"; HEAD at
report time `3f6edcc9` (read-only). Scratch: `/fast/scratch/hyaku/tsukuroi-r68/M1Mutation`
(created, used, removed at exit; every kept receipt was written into the lane first).

## What ran

An independent strict counter (`mycount.py`, sha256
`3ad6e99a929bc7e5273400e22345dc66afe7fc51283ed9457cf0b9f8a6646cc9`) was written from the declaration
text only: rows `^| RW<n> |`, outside ``` fences, 3rd cell non-empty, distinct ids. It was run over
eight mutants built to the item's shapes, then six single-point mutants of the counter itself were
run over the same fixtures, then the C1/E2 counter was executed over the same fixtures and over four
clause probes. `drafts/c1/count-rw-r68.py` was read only after the kill matrix was written; the M1
counter was not edited afterwards.

## Results

1. Fixture matrix (item-literal verdicts): m0 6, m1 1, m2 3, m3 0, m4 5, m5 0, m6 0, m7 6 —
   observed equals the declared oracle on 8/8, control 6, so red_killed = 0/7 under the definition
   `KILLED ⇔ observed != expected`. The fixtures are not inert: the frozen literal
   `grep -cE '^\| RW[0-9]+ \| '` deviates on m1 (6/1), m2 (6/3) and m4 (6/5), so the distinct-id,
   fence and evidence clauses are each behaviour-bearing.
2. Counter mutants (milestone: mutate the strict counter): c1 distinct-ids, c2 fence guard, c4
   id regex, c5 evidence cell, c6 repeated header are all KILLED (5/6). c3 (drop leading-pipe guard)
   SURVIVES and is *equivalent* for the declared m3 shape — a line starting `RW1 |` puts the id in
   `cells[0]`, and the guard only matters for a non-pipe-led line carrying the id in its second
   field (scratch diagnostic: pristine 0, c3 1). Routed shape, not applied to the declared eight.
3. Cross-counter: on the declared 3-cell fixtures the two counters agree on 3/8 (m3, m5, m6); the
   five disagreements are E2's 8/9-cell row-shape clause, which measures 0 on every fixture holding
   a counted row. Rebuilt as 8-column rows (same defects), they agree on 7/8 — the exception is
   m8/m4, where M1 counts a blank-evidence row (6) and E2 equals the oracle (5). That isolates a
   real defect in M1: its evidence check is positional (`cells[3]`), and its "last non-empty cell"
   clause is vacuous as specified, so in the note's 8-column layout it has no evidence guard.
4. Clause probes (8-column, one clause each): numeric-vs-string id equality (M1 2 / E2 1 for
   RW1+RW01), placeholder evidence (2/1 for `-`), `~~~` fences (6/3), table membership without a
   separator (1/0). These four readings are open in the frozen text and each changes a count.
5. Live C1 draft note (`drafts/c1/note.md`, sha256
   `30d3b2fd2ff0e75ad01b146f2abc0fc09bbbd8a03f820150aeeba766d124c6ea`): literal grep 6, M1 6,
   E2 5 with `LAYOUT=mixed` and `REJECT line=34 id=RW5 reason=SHAPE detail=11 data cells, 13 raw
   fields (need 8)`. Header line 28 has 8 data cells; RW1–RW4 are 9 cells (unescaped `|` inside the
   literal `awk -F'|' on the S… row, field 7`), RW5 is 11 cells (a second unescaped pipe in
   `grep -n '^| S185 ' corpus/SOURCES.md`), RW6 matches the header. E2's 9-cell tolerance admits
   RW1–RW4 and rejects RW5. The C1 row floor is therefore 6 under the frozen literal predicate and 5
   under an arity-binding strict counter on the same bytes — a predicate-scope decision for the L1,
   and the rows as written break the `awk -F'|'` addressing the note itself uses.

## Files

- `probes/m1-kill-matrix.txt` — fixture matrix, literal-grep calibration, six counter mutants, c3 diagnosis, before/after counter sha.
- `probes/m1-vs-e2-counter.txt` — required comparison, arity-matched set, clause probes, live-note numbers, freeze evidence.
- `drafts/c1/M1-report.md` — survivors and why they survive.

Addendum (2026-11-03T22:45:12Z, after E2Battery's IRC): re-measured on the current bytes —
`count-rw-r68.py` sha `b93f5912…` (the message's `fa0d866d…` is not the state measured), fixtures
rebuilt from the kill matrix and sha-verified byte-identical. Declared eight still 0 under the strict
counter (3/8 unchanged); the live note `1d2a4d8d…` now has 8 data cells per row and reads 6 under both
the literal grep and the strict counter with no REJECT (the RW5 malformed-row finding is resolved);
the 9-cell tolerance is gone; numeric-id equality (1 vs 2) and placeholder evidence (1 vs 2) remain
open. M1's own m8/m4 over-count stands; its counter stays frozen. Addendum appended to both receipts.

No tracked file, no sibling repo, no E2 draft was modified. No installs.

RED_KILLED=0/7 CONTROL=6 SURVIVORS=fixtures:m1,m2,m3,m4,m5,m6,m7;counter:c3 COUNTERS_AGREE=3/8
