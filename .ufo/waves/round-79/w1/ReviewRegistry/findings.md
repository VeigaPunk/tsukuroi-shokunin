# ReviewRegistry — findings (claim C2)

Independent reviewer. Every statement below is from a run recorded in `receipts.json`
(argv, rc, stdout). Nothing is copied from `ExecRegistry.md`, `ExecInstrument.md` or any
executor receipt. Scratch: `/fast/scratch/hyaku/tsukuroi-r79/ReviewRegistry/`.

## What was reproduced

| # | measurement | result |
|---|---|---|
| 1 | `check-gate-standard-r79.py --root <lane worktree>` | **rc 0**, `duplicates=0 shape_ok=2/2 met=1` |
| 2 | same tool `--revision afe1f261…` (freeze) | **rc 1**, `duplicates=6 shape_ok=0/2 met=0 revision=afe1f261… branch=master`; the six named rows are exactly the declared six |
| 2b | same tool `--revision 9086589a…` (base) | rc 1, `duplicates=6 shape_ok=0/2 met=0` — same six |
| 3 | `check-registry-coverage.py --revision afe1f261…` | **rc 1, FAIL** — see F3; base `9086589a…` is PASS 117/117 |
| 4 | `check-gate-standard-r79.py --selftest` | rc 0, `SELFTEST total=8 passed=8 failed=0` |
| 4b | `measure-unit-deps-r79.py --selftest` | rc 0, `SELFTEST total=32 passed=32 failed=0` |
| 4c | `check-r71-routed-r72.py --selftest` | rc 0, `SELFTEST: PASS (8 cases, 8 passed, 0 failed)` |
| 4d | `count-md-rows-r72.py --selftest` | rc 0, `SELFTEST: PASS (23 cases, 23 passed, 0 failed)` |
| 5 | independent reimplementation of the frozen duplicate/shape clauses | before: duplicates **6** (same six paths); after: **0**; operative rows 117 → 119 |

## Structural inspection of SKILL.md (against the freeze blob)

- Four `> NON-OPERATIVE — carried for history; the round-71 table is the sole operative
  registry.` lines, each the immediate next line under its heading (strict adjacency, no
  intervening blank): Round 72 `selftest-tally` continuation, Round 73 continuation (the
  literal covers both tables under that heading), Round-76 continuation, round-77 addition.
  The instrument's own parser classifies all four tables `marked=True`; the round-71 table
  stays `operative UNMARKED` with 119 rows.
- Exactly two replaced lines: `check-r71-routed-r72` and `count-md-rows-r72`. Cell-wise
  comparison against the freeze shows **only cells 3 (Verdict map) and 4 (Self-test)** differ.
  Both new self-test cells name the row's own tool and `--selftest`; both verdict maps now
  carry a standalone `3` and the words `self-test`; code 2 and code 128 text is preserved.
- Exactly two appended rows: `measure-unit-deps-r79` and `check-gate-standard-r79`, inside
  the operative table (contiguous, no blank line), 8 columns, `gate`, 0/1/2/3 maps.
- Historical preservation: line-multiset diff vs the freeze removes exactly the two old row
  lines and adds exactly 8 line instances (2 replaced rows + 4 markers + 2 new rows).
  SKILL.md 6144 → 6150 lines; `git diff --numstat` `8 2` (SKILL.md), `148 2` and `263 2`
  for the two tools; continuation tables' rows are row-for-row identical to the freeze.
- `check-line-endings-r64.py --check`: PASS (395 files, 0 violations).
- Frozen checker identity: `tools/check-gate-standard-r79.py` sha256 `0b32ddbc…72cfda`
  and `tools/measure-unit-deps-r79.py` sha256 `132be669…82d1d` are byte-identical to the
  freeze blobs; `before/expected.json` `0c09c7a4…dd21` and the snapshot `eb9479be…14c6`
  match the frozen values.

## Findings

### F1 — MEDIUM (instrument limit, not a repair defect). The shape leg is presence-based.
The leg asks whether the tool blob contains `--selftest` and `SELFTEST`; it cannot see
whether the mode passes. Demonstrated: fixture `red-selftest` (current SKILL.md, both tool
blobs replaced by a stub whose `--selftest` prints `SELFTEST: FAIL (5 cases, 4 passed, 1
failed)` and exits 3) → gate `rc 0`, `duplicates=0 shape_ok=2/2 met=1`; the stub run directly
is `rc 3`. This matches the frozen claim wording ("registry legibility and two truthful
interfaces", presence clauses) but it is the exact class of my F4 observation: a red
self-test does not move the numeric gate. Declared limit; the after-state rows happen to
name modes that are green (4c/4d), so the *current* green is not hollow on this point.

### F1b — MEDIUM (instrument gap; falsifies this item's own acceptance sentence).
The self-test cell is only substring-checked: it must contain `--selftest` and the row name;
the path in it is never validated and the source clause reads the **entry** cell's blob.
Fixture `phantom-selftest` (current SKILL.md; `check-r71-routed-r72` self-test cell replaced
by `` `python3 tools/does-not-exist-r79.py --selftest` check-r71-routed-r72 ``, tool blobs
selftest-bearing stubs): counter **rc 0**, `duplicates=0 shape_ok=2/2 met=1` — a row that
names a `--selftest` its tool does not contain **passes**. The item's sentence "a row that
names a `--selftest` its tool does not contain is a finding, not a pass" is therefore a
requirement the counter does not enforce. In the delivered tree the two cells name their
own tools, and I ran those modes green (4c/4d), so the current green is substantively
backed; the gap is in the instrument, not in the delivered rows. Mitigation outside this
counter: `check-registry-coverage.py` flags the resulting orphan
(`REGISTRY-ROW-ORPHAN` for a path absent from `tools/`), so the pair of gates together
catch this fixture; the C2 counter alone does not.

### F1c — LOW (instrument fragility, no live instance).
`current_rows()` resolves a table's heading with `lines.index(heading)`, so an **exact
duplicate** of a registry heading line earlier in the file makes the real table resolve to
the earlier line, fall before the operative heading, and stop counting. Fixture
`heading-collision` (an exact copy of the Round-72 continuation heading inserted near the
top): counter **rc 0**, `duplicates=0 shape_ok=2/2 met=1`, i.e. the duplicate that the
marker leg is supposed to count disappears. Live SKILL.md has no such collision — all four
target headings and the operative heading occur exactly once as full lines (the only
duplicate heading lines in the file are non-registry `###` headings, and their tables are
not 8-column), so the after value is unaffected. `check-registry-coverage.py` uses
enumerated indices, not `lines.index`, and is immune to this class.

### F2 — LOW (truthfulness of the two replaced verdict cells).
Both rows now say code 2 is "could-not-evaluate (argparse usage error)", but the new
`--selftest` mode also exits 2 on harness refusal: `HARNESS-TMPDIR-REFUSED reason=tmpdir-unset`
and `…reason=tmpdir-under-tmp` for both tools (measured, rc 2). Neighbouring rows
(`check-r72-routed-r73`, `count-ul-rows-r73`) state that second code-2 condition explicitly;
these two do not. Not a false interface (2 is "could-not-evaluate" in both cases), but the
parenthetical is incomplete for a mode the row itself advertises.

### F3 — MEASUREMENT DISCREPANCY (seat text vs frozen bytes), resolved in the repair's favour.
The seat instruction says coverage at the freeze "must stay PASS". Measured at
`afe1f261…`: **FAIL, rc 1**, two `REGISTRY-ROW-MISSING` for the two round-79 tools
(`counts: tools_total=119, rows_total=117, registered=117, missing=2`). At base
`9086589a…`: PASS 117/117. `--baseline-tools 9086589a…` confirms the same two files are
the "discovered" newcomers. The freeze therefore introduced the two instruments before
their rows existed; the repair under review (appended rows) is what restores the
invariant. Worktree projection using the coverage tool's own functions
(`_operative_rows` + `_coverage` over the worktree SKILL.md and the 119 `tools/` files):
**0 findings, 119/119 covered**. The revision-bound after value could not be measured
because the L1 had not committed when this seat measured (`HEAD 883aae61`); it must be
re-run at the integration commit.

### F4 — OBSERVATION (integration-window artifact; not reproducible at final bytes).
At ~16:13:5x–16:14:00 local, while `tools/count-md-rows-r72.py` was being rewritten
(mtime 16:14:00), one run of `count-md-rows-r72.py --selftest` returned **rc 3**:

    SELFTEST map-digest rc=1 FAIL
      expected-but-absent: ['map-digest']
    SELFTEST: FAIL (23 cases, 22 passed, 1 failed)

The digest of the bytes executed in that run was not captured, so it cannot be attributed
to the final artifact. At the final digest `58f7397e…45063c`, five consecutive runs pass
23/23 rc 0, and a sixth capture for `receipts.json` also passes. Recorded because (a) it
proves the declared code-3-on-selftest-failure mapping is real, and (b) it is exactly the
F1 class: during that window the C2 numeric gate would still have been green if the
registry had already named the mode. A transient red during integration is not evidence
of a repaired defect; only the final digest is certified here.

### F5 — Attacks killed (evidence the instrument is not vacuous).
All run against the real counter with `--root` fixtures built from the current SKILL.md:

| fixture | rc | counter output | reading |
|---|---|---|---|
| `good` (current text, selftest-bearing stubs) | 0 | `duplicates=0 shape_ok=2/2 met=1` | positive control |
| `lying` (self-test cell back to "none") | 1 | `shape_ok=1/2`, `GATE-STANDARD-SHAPE check-r71-routed-r72` | a row naming no mode fails |
| `tool-without-selftest` (blob lacks the flag) | 1 | `shape_ok=1/2`, `GATE-STANDARD-SHAPE count-md-rows-r72` | a claimed mode absent from the tool fails |
| `verdict-no-3` (code 3 removed) | 1 | `shape_ok=1/2` | verdict clause is live |
| `unmarked` (one marker removed) | 1 | `duplicates=2` (`check-r72-routed-r73`, `count-ul-rows-r73`) | marker leg is live |
| `forged-source` (row entry borrows the other frozen tool, own tool has no `--selftest`) | 1 | `duplicates=1 shape_ok=2/2 met=0` | borrow is caught by the duplicate leg |
| `forged-borrow` (same, with the borrowed tool's own row removed) | 1 | `duplicates=0 shape_ok=1/2 met=0` | fixture tool set is exactly the two frozen tools, so the source clause cannot resolve a third tool |
| `red-selftest` | 0 | `duplicates=0 shape_ok=2/2 met=1` | F1: presence-only (survives by design) |
| `phantom-selftest` (self-test cell names a nonexistent tool + the row name) | 0 | `duplicates=0 shape_ok=2/2 met=1` | F1b: the self-test path is never validated (survives) |
| `heading-collision` (exact duplicate of a registry heading earlier in the file) | 0 | `duplicates=0 shape_ok=2/2 met=1` | F1c: `lines.index` drops the real table (survives; no live instance) |

### F6 — LOW (interface delta of the two repaired tools).
The edits replace two `ap.add_argument` lines with a mutually exclusive group, so
`--revision X --fixture Y` is now an argparse error: measured freeze copy rc 1 (accepted,
fixture wins) → current rc 2 (`argument --fixture: not allowed with argument --revision`).
The documented single-mode invocations in both registry rows are unchanged, and every
normal-mode run measured here returns the same result before/after (`--revision
afe1f261…`: `ROUTED_STALE=0` rc 0; `MD_TARGET … met=1` rc 0). Recorded as a tightening,
not a regression; neither row advertises combining the two flags.

### F7 — PASS detail (no finding).
`--root` after value and all four markers/rows verified independently; no tool path is
named by more than one current row (independent recount 0); 119 current rows / 119
operative rows; the two new rows do not create coverage findings (projection 0); both
new `--selftest` modes exist and are green at the final digests; both tools' normal
`--revision` forms still exit 0 with their historical summaries.

## Residual verification gaps

1. Revision-bound after-state coverage (the tool's shipped `--revision` form on the
   integrated commit) was **not run**: no integration commit existed at measurement time
   (`HEAD 883aae61` is the dispatch commit). Projection via the tool's own functions is
   PASS; the main agent must run `check-registry-coverage.py --revision <landed REV>` and
   `check-gate-standard-r79.py --revision <landed REV>` after the L1 commit.
2. The transient F4 red cannot be reconstructed; only the final digests are certified.
3. Fixtures are synthetic stubs under my scratch; they test the counter's clause reactions,
   not the real tools' hermeticity. The real tools' selftests were exercised directly
   (4c/4d) and their harness refusals measured (both rc 2).
