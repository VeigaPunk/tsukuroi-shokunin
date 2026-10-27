VERDICT: defect-found
Seat: SelfAssess (L2, tsukuroi r44 w2, hyaku 9) — Item R-5, self-assessment run
Measured revision: 8eee79db608b5815c325a5af7cbfdeac50eda9f4 (`tools/check-self-assessment.py --revision …`).
Requirement: 27 fixed checks, mismatches 0. Scratch `/fast/scratch/hyaku/tsukuroi-r44/SelfAssess`; lane read-only.

# F1 — the self-assessment surface at the assigned revision misses the 0 requirement: 27 checks, 4 mismatches

    $ python3 tools/check-self-assessment.py --revision 8eee79db608b5815c325a5af7cbfdeac50eda9f4
    checked: 27    mismatches: 4    status: FAIL    exit 1

| id | row (SCORECARD.md) | stated | observed | cause |
|---|---|---|---|---|
| K07 | depth `:2720` | 64 notes | 65 | `corpus/knowledge/btrfs-scrub-record-r44.md` added at `ab8aae16` (round-44 C2 draft entry) |
| K10 | depth `:2720` | 62 lessons | 63 | `corpus/lessons/round-43-verifier-spotcheck.md` added at `98020ece` (round-44 **base**) — inherited |
| K13 | operability `:2722` | `PASS (132 cases, …)` | 148 | round-44 census arm `ab8aae16` (+9) and w1 integration `071ab0d1` (141 -> 148) |
| K17 | host-census-gate `:2732` | 132 cases | 148 | same census surface as K13; second row stating the count |

K01-K06 (ordinals) and K08, K09, K11, K12, K14-K16, K18-K27 all match. Receipt:
`.ufo/waves/round-44/w2/SelfAssess/self-assessment-tip-8eee79db.json`.

# Calibration: the 0 requirement holds at the revision it names; the tip is a not-yet-re-derived surface

The axes table is still `## Axes — current self-assessment (round 43 final measured surface)`
(`SCORECARD.md:2714`) and says the counts are "re-derived from the committed lane tree at the round-43
outcome commit" (`:2716`); the calibration row states "mismatches 0 required at the round-43 outcome
commit" (`:2724`). Measured controls, each with a retained receipt:

1. At `a87249c7` ("round-43: measured outcome … axes and capabilities tables", the commit that lands that
   table): **27 checks, 0 mismatches, PASS, exit 0**. The 27/0 claim is exactly true at its own named
   revision — re-derived today, not assumed
   (`self-assessment-r43-outcome-a87249c7.json`).
2. At the round-44 base `98020ece`: **27 checks, 1 mismatch (K10)** — `98020ece` is one commit after
   `a87249c7` and adds `corpus/lessons/round-43-verifier-spotcheck.md` (63rd lesson) without re-deriving the
   depth row (`self-assessment-base-98020ece.json`). K10 is therefore **inherited, not round-44-produced**.
3. The checker itself is intact: bytes unchanged base -> tip (`git diff --stat 98020ece 8eee79db --
   tools/check-self-assessment.py` empty; sha256 `44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6`),
   and `--selftest` exits 0 with 19 cases, 0 failures (`check-self-assessment-selftest.json`).
4. K13/K17's observed 148 is independently reproduced outside the checker: from a clean
   `git archive 8eee79db` tree, `bash tools/tsukuroi-census.sh --selftest` prints
   `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)` (`census-selftest-tip.txt`). With
   control 2, base measured 132 -> tip measures 148: the C1 declaration's "132 -> 148 after w1 hardening"
   clause is corroborated exactly.

So this finding is a **stale self-assessment surface at the assigned revision**, not a counter defect, and
not grounds to falsify C1 or C2. The three round-44 mismatches are the inevitable delta of a round-43-titled
table against round-44 bytes; the fourth (K10) is a round-43-tail drift that a "re-derive only what moved
this round" pass will silently keep.

# F2 — LOW: the drift widens with each w2 integration commit

Context measured outside the assigned revision: lane HEAD during this seat was `3a1c6b5c` (downstream of the
tip; axes heading still round 43). `--revision 3a1c6b5c` gives **7 mismatches** — K07, K10, K13, K17 plus
K08 (4112 -> 4230 SKILL.md lines), K09 (1067 -> 1156 table lines), K11 (425 -> 452 corpus/README.md lines) —
because w2 commits `8728e8bc`/`efbffe08`/`3a1c6b5c` landed SKILL/README/lesson bytes while the table stayed
round 43 (`self-assessment-head-3a1c6b5c.json`). Any outcome-commit re-derivation must recompute all seven
quantities at once, and the numbers in the proposed text below will move again before the outcome commit.
This reframes the requirement: 27/0 at the tip is only reachable when the table and the tree are the same
commit.

# Proposed text (for the round-44 outcome commit)

Depth row (`SCORECARD.md:2720`), re-derived at the outcome commit:

    65 notes (`find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l`); `SKILL.md` <N> `wc -l` /
    <M> table lines (`grep -c '^|' SKILL.md`); `corpus/lessons/` 63+ files (`find corpus/lessons -type f | wc -l`)

Operability row (`:2722`) and host-census-gate row (`:2732`), both to the measured count:

    `bash tools/tsukuroi-census.sh --selftest` prints PASS (148 cases, 148 passed, 0 failed)

Calibration row (`:2724`) keeps its sentence only if the same commit reports 27/0; state the revision
explicitly (`mismatches 0 at <round-44 outcome commit>`) rather than "0 required", which reads as a standing
obligation the mid-round surface cannot meet.

And one line for the round-44 record:

    Self-assessment at the round-44 tip re-derived the axes table: 64 -> 65 notes, 62 -> 63 lessons
    (the lesson landed at base `98020ece`, inherited from the round-43 tail), 132 -> 148 census cases in the
    operability and host-census-gate rows; 27 checks, 0 mismatches at the outcome commit.

# Residual risk

- Landing the table edit in any commit other than the outcome commit re-creates the same drift on the next
  commit; the checker reads the table and the tree at one revision.
- K10 shows the failure mode this seat exists to catch: a count that changed **before** the measured round
  and is invisible to a round-scoped diff. Re-derive from the tree, not from the previous table.
- Nothing here bounds C1/C2: the checker does not read the census entry text or the C2 rows. The 148-case
  figure is corroborated, the arm's semantics are other seats' surface.
