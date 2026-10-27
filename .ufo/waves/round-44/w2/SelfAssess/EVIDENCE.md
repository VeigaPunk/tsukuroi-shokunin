# SelfAssess — retained evidence (round 44 w2, R-5)

Seat: SelfAssess. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only; `git` queries only).
Scratch: `/fast/scratch/hyaku/tsukuroi-r44/SelfAssess` (TMPDIR there). No fixture mutations, no lane writes
except this directory and `../SelfAssess.md`.

## 1. The assigned measurement

    $ python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py \
        --revision 8eee79db608b5815c325a5af7cbfdeac50eda9f4
    exit 1
    checked: 27    mismatches: 4    status: FAIL

Receipt: `self-assessment-tip-8eee79db.json` (full JSON), `self-assessment-tip-8eee79db.err` (empty).

Mismatches (verbatim `stated -> observed`):

| id | stated | observed | stated_line | reason tail |
|---|---|---|---|---|
| K07 | 64 notes | 65 `.md` | SCORECARD.md:2720 | `corpus/knowledge holds 65 .md files` |
| K10 | 62 lesson files | 63 files | SCORECARD.md:2720 | `corpus/lessons holds 63 files` |
| K13 | 132 cases | 148 cases | SCORECARD.md:2722 | `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)` |
| K17 | 132 cases | 148 cases | SCORECARD.md:2732 | `host-census-gate row states 132 cases; the census selftest at this revision prints 148 cases` |

K01-K06 (ordinals) and K08, K09, K11, K12, K14-K16, K18-K27 all `match` at this revision.

## 2. Controls — is the requirement, the table, or the tool at fault?

(a) Checker bytes unchanged base -> tip:

    $ git -C <lane> diff --stat 98020ece 8eee79db -- tools/check-self-assessment.py
    (empty)

    $ git -C <lane> show 8eee79db:tools/check-self-assessment.py | sha256sum
    44b474fb5401559d9a4052f04f03145cd165a688a78455694d7dd25dba5838e6

(b) Checker self-test: `--selftest` exit 0, `cases 19`, `failures 0`.
Receipt: `check-self-assessment-selftest.json`.

(c) Checker at the commit that LANDS the round-43 axes table
(`a87249c7 round-43: measured outcome ... axes and capabilities tables`):

    exit 0, checked 27, mismatches 0, status PASS
Receipt: `self-assessment-r43-outcome-a87249c7.json`.

This is the revision the axes table itself names ("re-derived ... at the round-43 outcome commit",
SCORECARD.md:2716) and the revision the calibration row names ("mismatches 0 required at the
round-43 outcome commit", SCORECARD.md:2724). The 27/0 claim holds there, exactly.

(d) Checker at the round-44 base `98020ece`:

    exit 1, checked 27, mismatches 1 (K10 only: 62 -> 63)
Receipt: `self-assessment-base-98020ece.json`.

(e) Census selftest at the tip, run from a clean `git archive 8eee79db` tree (independent of the checker):

    TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)
Receipt: `census-selftest-tip.txt`.

Combined with (d): base measured 132 (K13 matched at base), tip measures 148 — the declaration's
"132 -> 148 after w1 hardening" clause is corroborated exactly.

(f) Context, outside the assigned revision: lane HEAD while this seat ran was `3a1c6b5c`
(downstream of the assigned tip; the axes heading is still the round-43 table).
`--revision 3a1c6b5c` gives checked 27, mismatches 7 (K07, K08, K09, K10, K11, K13, K17) -> exit 1.
Receipt: `self-assessment-head-3a1c6b5c.json`. This shows the drift widens as w2 lands SKILL/README/lesson
bytes, i.e. the table must be re-derived wholesale at the outcome commit, not patched incrementally.

## 3. Attribution of each mismatch

- K07 (64 -> 65 notes): `corpus/knowledge/btrfs-scrub-record-r44.md` added at `ab8aae16` (round-44 C2 draft
  entry). Round-44 surface change, declared.
- K13, K17 (132 -> 148 cases): round 44 census arm `ab8aae16` (+9 cases) and wave-1 integration `071ab0d1`
  ("141 -> 148" per its message). Round-44 surface change, declared in the C1 claim. Both the operability
  row (`:2722`) and the host-census-gate capability row (`:2732`) still state 132.
- K10 (62 -> 63 lessons): added at `98020ece` — the round-44 BASE commit, "round-43 verifier spot-check",
  which added `corpus/lessons/round-43-verifier-spotcheck.md` one commit after the axes table landed
  (`git show --stat 98020ece` -> `1 file changed, 159 insertions(+)`). Inherited from the round-43 tail, not
  produced by round 44. At `a87249c7` the lessons count was 62, matching the table.

## 4. Not shown by this evidence

- No C1/C2 counter defect: the self-assessment checker is a separate tool (unchanged, self-test green) and
  reads SCORECARD rows, not the census entry or the C2 rows.
- No ordinal drift: K01-K06 match at every revision measured (tip, base, `a87249c7`, HEAD).
- No claim about the round-44 outcome committing a re-derived table: that commit does not exist yet.
