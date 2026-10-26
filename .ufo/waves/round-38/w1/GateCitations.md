VERDICT: defect-found

# G-3 — lane citation/notice/adjacency gates at round-38 master vs base

Item: run `tools/check-section-citations.py`, `tools/check-appended-notices.py`,
`tools/check-adjacency-anchors.py` at the current lane master and at base
`8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`; name the round-38 cause of any new red.

Scope actually run: all three tools at both revisions, plus `--selftest` for each tool
(hermetic, in-memory + mktemp sandbox), plus a per-commit bisect of the failing tool over the
five round-38 commits. Read-only throughout: no lane file was edited, no git/jj mutation, no
host mutation, no sudo, no package transaction. Nothing was written outside
`.ufo/waves/round-38/w1/GateCitations{,.md}` except one mis-pathed first write of this report,
corrected in the same turn and fully removed (see "Self-disclosure" below).

Environment: lane `HEAD = 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (master);
`git rev-parse refs/remotes/origin/master` = `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (exit 0),
so both the local and the origin-side ancestor binding the tools enforce were satisfied for the
base and the master runs. Python 3.14.8, git 2.56.0.
`TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/GateCitations` on every invocation.

Tool identity (so the delta is content, not tool version): the three scripts and
`tools/_revision.py` are byte-identical at base and at HEAD —
`git rev-parse 8bd001f:<f>` == `git rev-parse 5edb6c2:<f>` for each, e.g.
`tools/check-adjacency-anchors.py` = blob `83a80e886804` at both revisions,
sha256 `a4f500ef680d92132400b1b7…`.

## Results (summary + exit code)

| tool | @ 8bd001f (base) | @ 5edb6c2 (master) |
|---|---|---|
| check-section-citations.py | PASS, exit 0, `correction_count: 2`, `findings: []` | PASS, exit 0, `correction_count: 2`, `findings: []` |
| check-appended-notices.py | PASS, exit 0, `record_count: 97`, `resolved_records: 97`, `distinct_paths: 17`, `findings: []` | PASS, exit 0, `record_count: 97`, `resolved_records: 97`, `distinct_paths: 17`, `findings: []` |
| check-adjacency-anchors.py | **PASS, exit 0**, `inbound_by_class {DRIFTED 17, RESOLVES 96, UNRESOLVABLE 1}`, `inbound_classified 114/114`, `outbound_portable 10/10`, `live_object_match 10/10`, `findings: []` | **FAIL, exit 1**, `inbound_by_class {DRIFTED 16, RESOLVES 96, UNRESOLVABLE 1}`, `inbound_classified 113/114`, same outbound/live counts, one finding |

Raw stdout/stderr for all six runs plus the three selftests:
`.ufo/waves/round-38/w1/GateCitations/check-*-<rev>.out|.err`, `check-*-selftest.out`.
Selftests: section-citations `PASS (68 cases, 68 passed, 0 failed)` exit 0;
appended-notices `PASS (47 cases, 47 passed, 0 failed)` exit 0;
adjacency-anchors `PASS (25 cases, 25 passed, 0 failed)` exit 0 — so the red is not a tool defect.

The single finding at master, verbatim:

```
{"detail": "classification DRIFTED is inconsistent: found_line is not an occurrence of
 evidence_quote (or empty quote requires line 0)",
 "id": "INBOUND-CLASSIFICATION-WRONG",
 "site": "corpus/knowledge/adjacency-anchors-r19.json:inbound[108]"}
```

## New red: round-38 cause

`inbound[108]` is record `IN-109` (`corpus/knowledge/adjacency-anchors-r19.json`, verified by
`git show 5edb6c2:corpus/knowledge/adjacency-anchors-r19.json`):

- `target_path: "tools/tsukuroi-census.sh"`, `classification: "DRIFTED"`,
  `evidence_quote: "check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED"`,
  `found_line: 2346`.

That quote sat at line 2346 at base and at the freeze commit:

```
$ git show 8bd001f:tools/tsukuroi-census.sh | sed -n '2346p'
  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
$ git show 7cbaeb6:tools/tsukuroi-census.sh | sed -n '2346p'
  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
```

Round-38 C1 commit `52ffd65f868431f021b8615ab281efd87195eac6` ("C1 storage-integrity census
arm") inserted 65 net lines above that case — `git diff -U0 7cbaeb6 52ffd65 --
tools/tsukuroi-census.sh` gives `115 insertions(+), 4 deletions(-)` with per-hunk net deltas
above old line 2346 of +19 (old 349), +1 (372), +1 (425), +1 (529), +42 (1824), +1 (2060)
= **+65**. The case therefore moved 2346 → 2411:

```
$ git show 5edb6c2:tools/tsukuroi-census.sh | sed -n '2411p'
  check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \
$ git show 5edb6c2:tools/tsukuroi-census.sh | sed -n '2346p'
  case_home='blocked-journal-missing'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
```

The registry's `found_line` was not refreshed in `52ffd65` or in any later round-38 commit, so
the DRIFTED record's citation no longer resolves and the gate reddens. Bisect receipt
(`.ufo/waves/round-38/w1/GateCitations/bisect-adjacency.txt`), same tool blob at every step:

```
8bd001f EXIT=0   7cbaeb6 EXIT=0   52ffd65 EXIT=1   1fe28e7 EXIT=1   9c9bb64 EXIT=1   5edb6c2 EXIT=1
```

Cause is isolated to `52ffd65` (first red commit = the C1 census-arm implementation); the C2
commit `1fe28e7`, the pre-seat amendment `9c9bb64` and the registry commit `5edb6c2` inherit it
without changing it. Line-shift receipt: `.ufo/waves/round-38/w1/GateCitations/in-109-line-shift.txt`.

Blast radius is exactly one record: `IN-109` is the only inbound record whose
`target_path` is `tools/tsukuroi-census.sh` (scripted scan of all 114 inbound records), and the
checker reports exactly one finding. Both other gates are unchanged PASS at both revisions, so
this is a lane-gate regression, not a C1/C2 predicate failure: the C1 arm's own content is not
implicated, only its citation bookkeeping.

## Proposed remedy (draft only — NOT applied; this seat is read-only on lane content)

In `corpus/knowledge/adjacency-anchors-r19.json`, record `IN-109`, replace

```
"found_line": 2346,
```

with

```
"found_line": 2411,
```

and append to its `note` (exact proposed text):

```
 Round 38: the C1 storage-arm census change (52ffd65) inserted 65 lines above the case, moving
 it from line 2346 to line 2411 (found_line updated; wave-1 GateCitations).
```

`target_ranges` `[915,970]` and the `DRIFTED` classification stay as-is — DRIFTED does not
require the range to resolve, and the existing note already explains the drift. Whichever seat
owns registry maintenance must make this edit; G-3 does not edit it.

## Axes

- Operability: three gates evaluated at two revisions with exact exit codes; the red is named,
  bisected to one commit, and quantified (+65 lines), with a one-field remedy.
- No-harm: read-only on lane content; only this report and its receipts directory were written
  there; scratch removed; one mis-pathed fleet-root write was detected and fully reverted
  (disclosure below).

## Not done / limits

- `refs/remotes/origin/master` exists in this lane and equals HEAD, so the tools' origin-side
  ancestor binding was exercised, not vacuous; every run reports `branch_tip` = lane HEAD.
- I did not run any other lane gate, any counter, or any build/test/lint; those belong to the
  parent's post-integration gate.
- No tools installed or upgraded; no package or service action attempted.

## Files changed

- Added `.ufo/waves/round-38/w1/GateCitations.md` (this report).
- Added receipts under `.ufo/waves/round-38/w1/GateCitations/`: 6 run outputs + 3 selftest
  outputs, `bisect-adjacency.txt`, `in-109-line-shift.txt`.
- No tracked lane file modified (`git status --porcelain corpus/knowledge/adjacency-anchors-r19.json tools/` → empty).

## Self-disclosure: one corrected mis-write outside the lane

The first write of this report used a path relative to the session cwd
(`/home/vgpnk/Projects/shokunin`), so it landed at
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-38/w1/GateCitations.md` — i.e. under the fleet
root, which this seat must not write. Corrected immediately in the same turn: the file was copied
to the lane path above, the fleet-root copy deleted, the empty `w1/` and then the empty
`.ufo/waves/round-38/` directory removed (`find .ufo/waves/round-38 -mindepth 1` was empty before
`rmdir`), and `find .ufo -maxdepth 4 -name 'GateCitations*'` in the fleet root now returns nothing.
No fleet-root tracked file was touched; `git status --porcelain` in the fleet repo shows only
pre-existing modifications that this seat did not make. Disclosed here rather than omitted.
