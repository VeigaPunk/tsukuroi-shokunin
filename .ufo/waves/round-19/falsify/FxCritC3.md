## Attack
C3 separability: test whether a discovered-tool row can make a baseline tool count as covered after that baseline tool’s own row is removed. This is falsifiable because the gate appears to count tool-path mentions, rather than bind each row to exactly one tool. Impacted axis: C3 calibration (one-to-one registry/tool agreement and the meaning of `baseline_tools_missing`). The attack targets detector separability, not the accuracy of the current pinned registry count.

## Method
Ran the requested target gate:

```sh
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
```

Read `tools/check-registry-coverage.py` at the target commit, especially `build_parser` (lines 259–270), `_coverage` (198–241), and the baseline split (293–308). There is no `--registry` CLI option; the registry is read from committed `SKILL.md`. To exercise the actual table semantics, used fresh scratch clones under `/tmp/fxc3` and committed mutations only there.

1. In clone `/tmp/fxc3/m2`, removed the `revision-binder` row and appended `(tools/_revision.py)` to the Entry cell of the existing `registry-coverage` discovered-gate row. Scratch commit: `31cedd7c5195814346b3943ad4a31c03fab2b54b`. Ran:

```sh
python3 /tmp/fxc3/m2/tools/check-registry-coverage.py --revision 31cedd7c5195814346b3943ad4a31c03fab2b --branch m2 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
```

2. In clone `/tmp/fxc3/m3`, removed `revision-binder` and added a second `adjacency-anchors` row without adding a reference to `_revision.py`. Scratch commit: `08a147b162ef02bd9225ac332231c0a96988e309`. Ran:

```sh
python3 /tmp/fxc3/m3/tools/check-registry-coverage.py --revision 08a147b162ef02bd9225ac332231c0a969 --branch m3 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac
```

Compared `tools/` regular-blob entries at the baseline and target with `git ls-tree -r -l --full-tree <REV> -- tools/`.

## Verdict
**REFUTE — C3 separability.** The current target’s observed 0-missing/14-baseline result is reproducible, and the three discovered tools are correctly reported. But the detector accepts a missing baseline row masked by a discovered row that merely mentions the baseline path. A duplicate discovered row alone does not mask it; that mutation fails with both duplicate and missing findings.

## Evidence
- The requested target invocation exited 0 and emitted `status=PASS`, `baseline_tools_total=14`, `baseline_tools_missing=0`, `discovered_tools=[tools/check-adjacency-anchors.py, tools/check-boot-writers.py, tools/check-registry-coverage.py]`, `tools_total=17`, `rows_total=17`, and no findings.
- `git ls-tree -r -l --full-tree 452a054677f6b18284917d7c08c45361f91c25ac -- tools/` lists 14 regular files. The corresponding target tree lists those same 14 paths plus exactly `tools/check-adjacency-anchors.py`, `tools/check-boot-writers.py`, and `tools/check-registry-coverage.py`; no baseline path is absent. The independent tree comparison found no changed baseline blobs.
- Target source `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/check-registry-coverage.py:203-206` unions paths parsed from Entry and Self-test. Lines 218–240 add each row to every referenced tool’s coverage list and build `covered` from any matching row; duplicate detection at 231–238 is per path. Lines 303–307 compute `baseline_tools_missing` as `len(baseline_tools - covered)` and report discovered tools separately. There is no requirement that a row cover only the tool its row describes.
- The original dedicated library row is `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:2079`; the discovered gate row is at `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:2082`. In scratch commit `31cedd7c5195814346b3943ad4a31c03fab2b54b:SKILL.md:2081`, the dedicated row is gone and the discovered row’s Entry cell contains `tools/_revision.py`.
- The gate run on that scratch commit exited 0 with `status=PASS`, `baseline_tools_missing=0`, `baseline_tools_total=14`, `discovered_tools` unchanged, `tools_total=17`, `registered=17`, `rows_total=16`, and no findings. Thus one discovered row covered two tool paths and masked the missing baseline row.
- The duplicate-only scratch gate run on `08a147b162ef02bd9225ac332231c0a96988e309` exited 1 with `baseline_tools_missing=1`, `REGISTRY-ROW-DUPLICATE` for `tools/check-adjacency-anchors.py`, and `REGISTRY-ROW-MISSING` for `tools/_revision.py`. A duplicate does not itself cover an unmentioned baseline path.

## Residual
The strict separability property is refuted, but the current pinned revision’s registry is not miscounted: its 17 rows each name exactly one distinct tool path in Entry/Self-test, and the target run passes cleanly. Smallest safe correction: require each operative row to resolve to exactly one regular `tools/` path across Entry and Self-test (or add an explicit tool-path identity field and validate one-to-one ownership), then retain the existing per-tool missing/duplicate checks. The current rows satisfy the single-path condition, and it rejects the demonstrated cross-row masking attempt. No tools were installed or updated; no host or live boot state was probed.

Scope: executed=python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-registry-coverage.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; python3 /tmp/fxc3/m2/tools/check-registry-coverage.py --revision 31cedd7c5195814346b3943ad4a31c03fab2b54b --branch m2 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; python3 /tmp/fxc3/m3/tools/check-registry-coverage.py --revision 08a147b162ef02bd9225ac332231c0a96988e309 --branch m3 --baseline-tools 452a054677f6b18284917d7c08c45361f91c25ac; scratch-only SKILL.md mutations and fixture commits in `/tmp/fxc3/m2` and `/tmp/fxc3/m3`.