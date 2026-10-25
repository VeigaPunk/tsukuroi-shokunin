# Build4Source36 — build/check design item 4/12: source AST binding test

- Round/wave: tsukuroi r37 w1, seat Build4Source36 (executor, leaf).
- Axis: operability — `build:source AST binding test` (milestone: Independent runnable design).
- Deliverable: isolated runnable check `Build4Source36/source-ast-binding-test.py`, run
  results `Build4Source36/results-baseline-vs-patched.json`, precise patch proposal
  `Build4Source36/proposal.patch`, and this report. Nothing else written; lane
  read-only.

## What the check is and what it measures

The lane's revision judge `tools/check-revision-binding.py` decides a tool is
"shared" via a static AST census `shared()` (lines 284-314): it parses the tool
source and counts a bind use only when an executing import binds `_revision` /
`bind` and a call site uses it; `local_rev_regex_copies` counts literal `{7,64}`
copies. `item["shared"] = imports and copies == 0` (line 908-909) feeds
`consolidated_tools` (lines 918-919) — the C2 grade. A false positive here
certifies an unbound consumer as shared.

The check loads the judge from a private copy in a `TemporaryDirectory` (never
the lane), runs `shared()` over a labeled matrix of synthetic consumer sources
with ground-truth binding outcomes, and compares. It then applies the proposed
patch to the copy and re-runs the same matrix, measuring the after state.
No git, no commits, no subprocesses beyond python3; no lane/fleet/sibling write.

## How the check fails on unchanged baseline

Baseline run (artifact `results-baseline-vs-patched.json`, exit 0 = red-before +
green-after contract): 12 gating cases; **11 pass, 1 fails**:

| Case | Source shape | Expected `(uses, copies)` | Baseline got |
|---|---|---|---|
| `dead-while-literal-bind` | `while False:\n    import _revision\n    _revision.bind(r, v)` | `(False, 0)` | **`(True, 0)` — FAIL** |

The unchanged census prunes constant-false `if` branches but not constant-false
`while` loops: `visit()` only special-cases `ast.If` with an `ast.Constant`
test (lines 294-298). A dead `while False:` block containing the only
`_revision.bind` mention therefore reports `shared=True` — the consumer would
pass the shared gate although its bind never executes (runtime NameError).
All other gating cases pass on baseline, including the existing live/dead
`if`-literal cases, string-only mentions, unbound attribute call without module
import, local `{7,64}` copy, and syntax-error source.

## After state the check measures

Same matrix against the patched census: **12/12 gating cases pass**; the
`dead-while-literal-bind` case flips to `(False, 0)`. The two additional
`while`-else/True semantics cases (`live-while-else-live-bind` → (True,0),
`live-while-true-body-bind` → (True,0)) pass on both baseline and patched —
proving the patch does not over-prune reachable `while` content. Observed but
non-gating (documented limitation boundary, unchanged by the minimal patch):
`if 1 == 2:` and non-literal-test `if` branches still count their content; the
census remains a static bound, not a reachability proof.

## Precise patch proposal (proposal.patch)

One line in `shared()`/`visit()` (baseline lines 294): extend the constant-test
prune from `ast.If` to `(ast.If, ast.While)`. The branch formula (body iff
truthy, orelse iff falsy) is correct for both node kinds. Recommended selftest
additions: `dead-while-literal-bind` and `live-while-else-bind` in the
`selftest()` `check(...)` block (near lines 1286-1292). Existing selftest
shared-cases (`dead-import-not-shared`, `live-import-call-census`,
`from-import-call-census`, `string-import-not-shared`, `local-copy-census`)
exercise no `while` content and are unaffected.

## Sources opened this round (local files, line-anchored)

- `/home/vgpnk/.omp/agent/RULES.md:1-14` (tooling authorization; no install/update
  needed — python3 and git pre-existing; no pacman use).
- `skill://godspeed` (axis naming: operability/build; iterate cheap, parallel,
  no-harm moves).
- `tools/check-revision-binding.py`: docstring 1-54; imports 55-57; `shared()`
  284-314; per-tool use 908-910; `consolidated_tools` 916-919; STUB/selftest
  1016-1149, 1284-1292.
- `.ufo/waves/round-37/w1-plan.json:940-943` and `w1-spec.json:357-366`
  (assigned item 4/12 definition); `w1-dispatch.json:935-938`.
- SCORECARD.md C2/consolidation history: lines 538, 561, 573 (shared census is
  the C2 grade input; false-positive vector therefore directly gates C2).

## Scope/limits

- Read-only on lane content; the only writes are the seat report and seat-dir
  artifacts. No git/jj writes anywhere; the check creates no git repos and makes
  no commits (no fixture-commit gate needed).
- The check exercises `shared()` directly; it does not run the judge's full
  `--selftest` battery or live probes.
- Observed residual limitations (constant-comparison and non-literal-condition
  branches still counted) are reported, not silently extended; extending them
  would exceed the minimal no-harm patch.
- Tools installed: none (RULES.md consulted; channel N/A).
