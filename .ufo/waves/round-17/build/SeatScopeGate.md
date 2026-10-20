# SeatScopeGate — QUALITY24 red demonstration

[obs] `tools/check-seat-scope.py` (651 lines) is new. `--revision <7-64 hex>` reads `swarm-registry.json`/`spec.json` and `<Name>.md` reports from git objects; `--worktree` reads disk; `--selftest` is hermetic (line 360). Seats = registry members ∪ spec items, spec role/prompt winning (line 89). The last `^Scope: executed=(.+)$` line decides (lines 37, 52); findings are `SCOPE-REPORT-MISSING`, `SCOPE-UNDECLARED`, `SCOPE-EXEC-UNAUTHORIZED` (line 58); JSON carries `counts` per finding id plus `revision`, `branch`, `branch_tip`, `wave`, `seat_count` (line 137); exit 0/1/2.

[obs] Revision binding (line 202): non-hex, `HEAD`, `@`, `refs/…` → `E-REVISION-INVALID`; `merge-base --is-ancestor refs/heads/<branch>` failure → `E-REVISION-NOT-LANDED`; an existing `refs/remotes/origin/<branch>` adds `E-REVISION-NOT-PUSHED`; a wave with no seats is `E-NO-SEATS`, never a pass.

[obs] `--selftest`: 42/42 cases PASS, exit 0 — in-memory fixtures plus a mktemp git sandbox covering landed/unlanded/pushed/not-pushed/missing-branch/unknown-hex and two end-to-end `collect` reads of a committed wave tree.

[obs] At `f871697aa0a8ed180771e62d99e3b9559fd5efd1`, `.ufo/waves/round-16/build` holds 64 reports, 64 registry members, 64 spec items and 0 `^Scope: executed=` lines (two reports carry non-matching `Scope:` prose).

[inf] The demonstration therefore yields `{"SCOPE-UNDECLARED": 64}` at exit 1; I did not execute it — authorization covered `--selftest` only. L1 runs it.

[obs] That commit is an ancestor of `refs/heads/master` and `refs/remotes/origin/master`.

[unk] Round-17's own wave (74 registry members, two without spec prompts).

Tools installed: none.

Scope: executed=python3 tools/check-seat-scope.py --selftest; python3 -c JSON/tree inspections; git ls-tree/show/rev-parse/for-each-ref/merge-base reads; sed -n/grep/wc reads
