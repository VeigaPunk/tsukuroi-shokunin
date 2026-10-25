# Build2S334 — S3 nonvacuity mutation

**Axes:** operability; build:S3 nonvacuity mutation. **Deliverable:** runnable isolated counterexample/control at `s3_nonvacuity.py`; no lane/source files changed, no tools installed, no Git/jj or host changes.

## Check and retained evidence

The fixture uses a tiny deterministic model of the livefive evidence policy and the non-vacuity invariant; it does not import or execute lane code. It encodes the observed implementation seam from `tools/probe-child-env-allowlist-r36.py:1256-1257`: parity differences become evidence only when the set is not `livefive`. Given control `git_execs=1`, injected run `git_execs=0, child_execs=0, rc=0`, baseline scoring records a git-count parity diff but outputs `leak=false`, empty evidence. That is the unchanged-baseline false clean S3 result. Its guarded after state rejects zero-child execution with `RuntimeError("instrumented channel executed no child")`. A third control (`child_execs=1`, parity drift retained) remains admitted and does not call parity drift a leak, preserving the live-journal variance exception.

Run command: `python3 tsukuroi-shokunin/.ufo/waves/round-37/w1/Build2S334/s3_nonvacuity.py`. This was not executed here (the wave forbids verification); expected deterministic JSON is encoded by assertions in the fixture, not claimed as observed output.

## Integration criterion / risk

For the real probe, enforce `child_execs >= 1` after each injected livefive channel run, treating zero as a harness error (and therefore preventing a green empty-leak summary). Do not make livefive parity drift leak evidence: the mutation's measured after-state is rejection of do-nothing runs while allowing a child-running live-counter drift. Current fixture is a focused policy regression, not an end-to-end test of `one_run`, trace parsing, or JSON summary plumbing; integrate the guard and adapt the fixture to call that code in the parent-owned integration gate.

## Sources opened this round

- Local source, `tools/probe-child-env-allowlist-r36.py`, opened 2026-10-25: lines 1152–1157 require a child only for control; lines 1256–1260 waive parity diffs for livefive. No external sources cited.
