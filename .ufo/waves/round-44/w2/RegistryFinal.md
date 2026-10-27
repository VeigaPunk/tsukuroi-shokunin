VERDICT: defect-found

# RegistryFinal — R-1 registry coverage (round 44, wave 2)

Seat: RegistryFinal (roster id `RegistryFinal-2`). Leaf; no lane writes other than this report and
its receipts. Scratch `/fast/scratch/hyaku/tsukuroi-r44/RegistryFinal-2` (TMPDIR set there, /tmp
unused), removed at exit. Checker used: `tools/check-registry-coverage.py` sha256
`6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` with `tools/_revision.py`
sha256 `fc861ec8a4f2539ac3f16d1a04af8335a974c17c8ffba0a41f6dad972cad36de` (lane HEAD `3a1c6b5c`).
No pacman/sudo, no scrub, no service/sysfs/mount outside a private namespace, no lane git mutation.

## What was asked and what was measured

Assignment: run `check-registry-coverage.py --revision 8eee79db608b5815c325a5af7cbfdeac50eda9f4`;
expect 70/70 once the round-44 registry table is integrated, otherwise report 68/70 and the two
missing tools.

At the declared integrated tip the check is **red**, and it is red for the whole round except its
last commit:

```
python3 tools/check-registry-coverage.py --revision 8eee79db608b5815c325a5af7cbfdeac50eda9f4
{"branch":"master","branch_tip":"3a1c6b5c...","counts":{"findings":2,"missing":2,
 "registered":68,"rows_total":68,"tools_total":70},
 "findings":[{"detail":"no operative row names this regular tools/ file",
              "id":"REGISTRY-ROW-MISSING","site":"tools/check-scrub-record-r44.py"},
             {"detail":"no operative row names this regular tools/ file",
              "id":"REGISTRY-ROW-MISSING","site":"tools/score-scrub-arm-r44.py"}],
 "revision":"8eee79db608b5815c325a5af7cbfdeac50eda9f4","status":"FAIL"}      exit 1
```

**68/70. Missing rows: `tools/score-scrub-arm-r44.py` (C1 counter) and
`tools/check-scrub-record-r44.py` (C2 counter).** Both were introduced by `1d2afffe` (declaration,
frozen counters); at that commit `tools_total` goes 68 -> 70 while the operative table stays the
round-43 68-row table, so the registry gate is red from the declaration onward.

At lane HEAD, HEAD's pushed tip `3a1c6b5c` (== `origin/master`), the gate is green:

```
python3 tools/check-registry-coverage.py --revision 3a1c6b5c958c4f289a8b12551f96d843877b700e
{"counts":{"findings":0,"missing":0,"registered":70,"rows_total":70,"tools_total":70},
 "findings":[],"revision":"3a1c6b5c...","status":"PASS"}                     exit 0
```

So the "70/70 after the round-44 table is integrated" expectation holds only at `3a1c6b5c`, four
commits after the pinned `8eee79db`. Nothing in the frozen C1/C2 declarations is touched by this
finding: C2's "the registry" in the round-44 declaration (`SCORECARD.md:2787`, "the C2 counter reads
the entry, the registry, the snapshots and the wave-2 records at REV") is `corpus/SOURCES.md`
(`check-scrub-record-r44.py:266`), not this SKILL.md gate table.

This is a repeat of a named, previously repaired harm class: round 27 recorded "the
registry-coverage gate read FAIL (2 missing rows) at `099c7b3f` because the two new counters had no
registry row ... the round-27 registry table in `SKILL.md` restores it" (`SCORECARD.md:1049`).
Round 44 reproduced it in the same shape — two new counters, two missing rows — and repaired it
in the round-44 table at `3a1c6b5c`.

## Full red line across the round-44 series

`tools/check-registry-coverage.py --revision <REV>`, one line per commit
(receipts `sweep-round44.jsonl`):

| revision | commit | status | registered | rows |
|---|---|---|---|---|
| `98020ece` | round-43 base | PASS | 68/68 | 68 |
| `1d2afffe` | declaration, frozen counters | FAIL | 68/70 | 68 |
| `ab8aae16` | C1 arm + 9 selftest cases | FAIL | 68/70 | 68 |
| `7e081698` | SR7 narrowed | FAIL | 68/70 | 68 |
| `071ab0d1` | wave-1 integration (141 -> 148) | FAIL | 68/70 | 68 |
| `9608ebc3` | timers branch fix | FAIL | 68/70 | 68 |
| `8eee79db` | **declared integrated tip** | **FAIL** | **68/70** | **68** |
| `0f8c07a5` | w2 spec/dispatch (32 seats) | FAIL | 68/70 | 68 |
| `8728e8bc` | SKILL sections + r44 registry table | CANNOT_EVALUATE (exit 2) | – | – |
| `efbffe08` | r43 section heading restored | FAIL | 2/70 | 2 |
| `3a1c6b5c` | r44 table carries all 70 rows | PASS | 70/70 | 70 |

Two intermediate states are worth naming because they are where a lenient checker would have
produced a false green:

* `8728e8bc`: the round-43 heading was consumed, so the round-44 section contains **two**
  `| Name | Kind | ...` header blocks (lines 4040 and 4051 of `SKILL.md`) and no
  `## ... round43 ...` heading. The checker refuses: `E-REGISTRY-TABLE` "operative section must
  contain exactly one required registry header", exit 2. A naive row count over that section finds
  70 rows for 70 tools — i.e. a lenient counter would have reported 70/70 at a structurally broken
  revision. This is the round-19 contract holding ("a missing/duplicate highest table is
  could-not-evaluate, never fallback").
* `efbffe08`: the same section correctly holds only the two new rows while 68 rows sit under the
  restored round-43 heading -> FAIL 2/70 with 68 `REGISTRY-ROW-MISSING` findings, never a silent
  "highest table wins, older rows still count".

## Independent cross-check (not the checker's own code path)

A separate census script (own table splitter, own `git ls-tree`/`git show`, no import of the
checker; receipt `independent-census.txt`) reproduces the same numbers and both endpoint states:

* `8eee79db`: highest heading `round43`, 68 rows, 70 regular `tools/` blobs,
  uncovered = [`tools/check-scrub-record-r44.py`, `tools/score-scrub-arm-r44.py`], orphan rows = [].
* `3a1c6b5c`: highest heading `round44`, 70 rows (8 cells each), 70 tools, uncovered = [], orphan
  rows = [], carried rows = 68 and **byte-identical to the round-43 table**
  (`carried_equals_r43: True`), new rows = `scrub-arm-r44`, `scrub-record-r44` — matching the
  commit message "68 verbatim + scrub-arm-r44, scrub-record-r44".

## Operability and calibration of the gate itself

* Selftest: `python3 tools/check-registry-coverage.py --selftest` -> `PASS (23 cases, 23 passed,
  0 failed)`, exit 0 (receipt `check-registry-coverage-selftest.txt`). The 23 cases include the
  negatives that matter here: `missing-row`, `duplicate-row`, `ambiguous-row`, `orphan-row`,
  `invalid-kind`, `unresolved-selftest`, `incomplete-verdict`, `unique-highest-table`,
  `duplicate-highest`, `no-table`, `bad-revision`, `baseline-split`, audit-live-map cases.
* Independent negative control at table scale (not a 1-row fixture). A `--shared` clone of the lane
  in scratch (toplevel asserted == clone dir, fixture identity commit allowed) with exactly the
  `| scrub-arm-r44 |` row deleted, commit `22d62626b63ad296f8f463677e98ee64c26b200d`
  (receipt `fixture-negative-control.txt`):
  - pristine tip `3a1c6b5c` through the clone's own tool: PASS 70/70, exit 0;
  - row dropped: `FAIL registered=69/70 rows=69`, one `REGISTRY-ROW-MISSING` naming
    `tools/score-scrub-arm-r44.py`, exit 1.
  So the 70/70 PASS is not vacuous on a large table and the finding names the right tool.
* The clone also exposed the `_revision.py` rule-6 push guard: the same fixture commit measured
  while `refs/remotes/origin/master` still pointed at `3a1c6b5c` returns
  `CANNOT_EVALUATE / E-REVISION-NOT-PUSHED` (exit 2) instead of a verdict. In the lane,
  `origin/master == 3a1c6b5c == HEAD`, so both measured revisions are ancestors of the pushed tip
  and the guard is satisfied rather than inert.
* Determinism: two runs per revision are byte-identical with stable exits (1 at `8eee79db`,
  0 at `3a1c6b5c`; receipt `determinism.txt`).
* Row truth for the two rows that were missing at the pinned tip: entry commands match the real
  CLIs (`--revision/--scratch/--lane` for the C1 arm, `--revision/--lane/--sessions` for the C2
  counter; neither tool has a `--self-test` flag, consistent with both rows' "none" self-test
  cells); the pinned digests in the rows equal the committed tool bytes at HEAD **and** at the
  freeze commit `1d2afffe` (`1409a5fd…` for the arm, `c96aeda9…` for the record counter); the
  control scripts named by the rows/declaration hash to `f30f5fd9…` (c1) and `ad7845c4…` (c2)
  (receipt `pinned-values-crosscheck.txt`).

## Limits

* Only committed blobs are read; the working tree (this report included) is irrelevant to the
  result. The gate measures registration and shape only: it checks that a row names each regular
  `tools/` file, one row per tool, kind and verdict-code shape — never that a row's pin is true.
  The pin truth above was checked by hand for the two round-44 rows only.
* `counts.branch_tip` in the JSON is the branch tip, not the measured revision (`8eee79db` run
  prints `branch_tip: 3a1c6b5c`). A skim reader can mistake it for the measured tip; a consumer
  must read `revision`. Not a pass/fail defect, recorded as an operability observation.
* This seat does not judge whether a red registry at `8eee79db` should have blocked wave 1; it
  reports the measured state and the repair commit.

## Proposed text for the L1 (not applied — this seat writes no lane file)

Round note, e.g. appended to the round-44 integration notes: "Registry coverage at the wave-2
close: `check-registry-coverage.py --revision 8eee79db…` exits 1 with 68/70 and two
REGISTRY-ROW-MISSING findings (`tools/score-scrub-arm-r44.py`, `tools/check-scrub-record-r44.py`);
the declaration's pinned integrated tip therefore predates the registry table. `3a1c6b5c` carries
the 70-row table (68 verbatim + the two round-44 rows) and passes 70/70, exit 0. Intermediate
`8728e8bc` is E-REGISTRY-TABLE (two header blocks in the operative section) and `efbffe08` is 2/70;
both are honest refusals, not passes. C1/C2 are unaffected: their counters do not read this table."

## Receipts

Under `.ufo/waves/round-44/w2/RegistryFinal/`:
`check-registry-coverage-pinned-8eee79db.json`, `check-registry-coverage-head-3a1c6b5c.json`,
`check-registry-coverage-8728e8bc.json`, `check-registry-coverage-efbffe08.json`,
`exit-codes.txt`, `sweep-round44.jsonl`, `check-registry-coverage-selftest.txt`,
`independent-census.txt`, `fixture-negative-control.txt`, `determinism.txt`,
`pinned-values-crosscheck.txt`, `duplicate-header-8728e8bc.txt`, `new-rows-at-head.txt`.
