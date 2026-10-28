VERDICT: supports

# C1-X8 — predecessor gates must not regress (base 5fdf062f → freeze ae99f021)

Kill-rule result: **no PASS→FAIL regression** among the eight predecessor checkers. All
three failing seats fail at base as well; their findings are identical (seat-bindings,
report-receipts) or widen by exactly the two tools the freeze adds (registry-coverage,
FAIL→FAIL — reported below, not a regression).

## Method

- Tool bytes are identical at base, freeze and the (mutable) worktree, so every
  PASS/FAIL difference below is a property of the lane data at the revision, not tool
  drift:
  `check-adjacency-anchors 83a80e886804`, `check-adjacency-overlap 94bafb4e391c`,
  `check-registry-coverage 885b55d40c06`, `check-recheck-commands 055f9b3835c7`,
  `check-knowledge-header e253fd516ee7`, `check-seat-bindings 9b5ef9f2bc58`,
  `check-report-receipts 5ea796e2dc57`, `check-revision-binding 86ef0ad09602`
  (`git rev-parse <base>:tools/<t>.py` == `git rev-parse <freeze>:tools/<t>.py` ==
  `git hash-object tools/<t>.py`, all eight).
- Each tool was run one at a time, `timeout 300`, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r48/TExecAdjSelf`,
  cwd the lane root (read-only invocation; no lane file written). Raw JSON receipts are in
  `.ufo/waves/round-48/w2/TExecAdjSelf/` next to this report.
- Deviation from the item text, stated because it changes the command form:
  `check-revision-binding.py` has **no `--revision`**; its required flag is the full
  40-hex `--tools-revision` (`--help`), which is what was passed at both revisions.
  `check-report-receipts.py` has no standalone `--revision` mode: it requires
  `--report PATH --lane REPO --revision REV`, so the revision's own `SCORECARD.md`
  (`git show <rev>:SCORECARD.md`, copies `SCORECARD.base.md` / `SCORECARD.freeze.md`)
  was supplied as the report at each revision.

## Status table

| tool | base 5fdf062f | freeze ae99f021 | verdict |
|---|---|---|---|
| check-adjacency-anchors | PASS (exit 0, findings 0) | PASS (exit 0, findings 0) | PASS→PASS, counts identical |
| check-adjacency-overlap | PASS (exit 0, anchored_rows 6/6) | PASS (exit 0, anchored_rows 6/6) | PASS→PASS, rows identical |
| check-registry-coverage | FAIL (exit 1, 1 finding) | FAIL (exit 1, 3 findings) | FAIL→FAIL, **findings differ** |
| check-recheck-commands | PASS (exit 0, clean 51/67, flagged 0, invocations 81) | PASS (exit 0, same) | PASS→PASS, counts identical |
| check-knowledge-header | PASS (exit 0, clean 67, notes 67, findings 0) | PASS (exit 0, same) | PASS→PASS, counts identical |
| check-seat-bindings | FAIL (exit 1, 41 findings, 378 requests) | FAIL (exit 1, 41 findings, 378 requests) | FAIL→FAIL, finding set identical |
| check-report-receipts | FAIL (exit 1, cited 2, unreceipted 2) | FAIL (exit 1, cited 2, unreceipted 2) | FAIL→FAIL, stdout byte-identical |
| check-revision-binding | PASS (exit 0, status PASS, consistency PASS, consolidation FAIL) | PASS (exit 0, same sub-statuses) | PASS→PASS, shape identical |

## Kill-rule findings

None. No PASS→FAIL.

## FAIL→FAIL detail (item also asks for differing findings)

### check-registry-coverage — findings differ, not a regression in kind

Base (1 finding, tools_total 75, registered 74):
`REGISTRY-ROW-MISSING` at `tools/check-scrub-admission-r47.py`
(`.ufo/waves/round-48/w2/TExecAdjSelf/check-registry-coverage.base.log`).

Freeze (3 findings, tools_total 77, registered 74):
same r47 row **plus** `REGISTRY-ROW-MISSING` at `tools/check-scrub-admission-r48.py`
and `tools/score-selftest-tmpdir-r48.py`
(`.../check-registry-coverage.freeze.log`).

So the freeze adds two unregistered tools — the round's own C1 counter and its scorer —
to a gate that was already red at base. `registered`/`rows_total` are unchanged (74/74);
only the tool set grew. This is a forward-looking note for the L1: the registry-coverage
gate cannot turn green at the round's final revision unless rows for the r47 file,
the r48 counter and the r48 scorer are added. The checker's own per-tool revision
behaviour stayed FAIL at every valid selector form at both revisions
(`origin-absent`, `short-tip`, `tip`, `landed-parent` all exit 1 / FAIL in
`check-revision-binding.*.log` `per_tool`).

### check-seat-bindings — identical failing set

41 findings at both revisions, sets equal (`SCOPE-PATH-DENIED` 23,
`SCOPE-TOOL-UNKNOWN` 16, `SCOPE-EXEC-DENIED` 2), first finding
`SCOPE-TOOL-UNKNOWN` at `OracleFetchHTTPS:2`; `requests_total` 378,
`incomplete_seats` 0, `missing_seats` 0 at both. Nothing in the freeze moved this gate.

### check-report-receipts — identical unreceipted citations

Both revisions: exit 1, `{"cited": 2, "unreceipted": 2}` with the same two pairs —
`d621b7126e088824fed354e19839a9c1bd4e74f0` / `tools/check-journalctl-v262-corrections.py`
and `29b22df142efb5479333af9d57ecbd069462ba05` / `tools/check-self-assessment.py`
(cited from the historical round-37 table rows, e.g. `SCORECARD.base.md:2064-2066`).
The two logs are byte-identical (sha256 `885cd3e3…` both), so no regression.
Caveat: this verdict depends on the supplied report; it is a pre-existing red gate in
`SCORECARD.md`, not a product of the freeze.

### check-revision-binding sub-gate

`status` PASS both revisions (`status_scope`: original-nine consistency only);
`consolidation_status` is FAIL at both: `consolidated_tools` 8 of `total` 9, with the
single non-consolidated original tool being `check-freshness-r17.py` (`shared` false —
no shared `_revision.bind` import; `consistent` true, `local_rev_regex` 0). The 19
`per_tool` entries include the 10 newly discovered tools, which the source comment
(lines 909-911) keeps outside the grade. `shared_tools` 8, `local_rev_regex_copies` 0,
`legacy_bound` 5/5, `bound_tools` 9, `all_total` 19 — identical at both revisions.
Per-tool records map one-to-one; the only field differences are the revision hashes
(`tip`/`short-tip`/`origin-absent`/`landed-parent` move from the base chain to the freeze
chain, `unlanded` fixture hash changes) with `ok: true` and identical `json_status`
everywhere. Diffing `per_tool` base vs freeze shows no status or `ok` change in any
selector form.

## Receipts (sha256, in `.ufo/waves/round-48/w2/TExecAdjSelf/`)

- check-adjacency-anchors.base.log `f284e466…`, .freeze.log `59ebe21e…`
- check-adjacency-overlap.base.log `fd4ed714…`, .freeze.log `1f448210…`
- check-registry-coverage.base.log `49be70c1…`, .freeze.log `5beac110…`
- check-recheck-commands.base.log `cd228088…`, .freeze.log `7170165f…`
- check-knowledge-header.base.log `7dab9e18…`, .freeze.log `d5dd30f2…`
- check-seat-bindings.base.log `5ed7bd28…`, .freeze.log `a5eb9509…`
- check-report-receipts.base.log and .freeze.log `885cd3e3…` (identical)
- check-revision-binding.base.log `f41fe35f…`, .freeze.log `ee1fe00c…`
- SCORECARD.base.md, SCORECARD.freeze.md — the report inputs, extracted with
  `git show <rev>:SCORECARD.md`.

## Not done / limits

- `check-self-assessment.py` deliberately not run (owned by another seat).
- No `--selftest` runs (not requested; would contend for CPU with the counter seats).
- Scratch `/fast/scratch/hyaku/tsukuroi-r48/TExecAdjSelf` removed after the receipts were
  copied. Lane working tree was not modified (only this wave directory was written).
