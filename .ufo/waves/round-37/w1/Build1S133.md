# Build1S133 — S1 repair control design (round 37 w1, design item 1/12)

seat: executor Build1S133 · axis: C1 operability (probe V8) · milestone: Independent runnable design
date: 2026-10-25 · lane HEAD: `ee36f9e829f640def6b3c6ab3e31c4ed7186c6eb`
scope: read-only on lane content; artifacts and report only in this seat area.

## Deliverable

An isolated, runnable repair control for the C1 S1 defect (probe `one_run`
clone/branch crash): `s1-repair-control.py` (executable, stdlib-only, sandboxed
to mktemp fixtures) plus a precise patch proposal `s1-repair.patch.proposal`.
Run: `./s1-repair-control.py all --live` → exit 0, VERDICT PASS (receipt
`s1-repair-control.run.out.txt`).

## Baseline (unchanged) — how the check fails

The frozen counter is byte-identical at HEAD to the freeze record (sha256
`a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a`, verified by
`sha256sum` this round). Baseline reproduction, live, this round:

```
python3 tools/probe-child-env-allowlist-r36.py --lane <lane> --revision c052bb7d… \
  --set livefive --only tools/check-revision-binding.py --scratch <mktemp>
```

→ exit 1, stdout 0 bytes, stderr traceback ends at probe line 499
`RuntimeError: cannot create local master branch` (2.62 s wall; receipts
`livefive-baseline.single-target.{err,out,meta}`). The fixture-level replay of the
frozen sequence (probe lines 490-497) fails identically at the git level: rc 128,
`fatal: a branch named 'master' already exists`. So on unchanged baseline the
check's baseline arm FAILS (the scenario under test is still present), exactly as
W2RevCounter S1 and the round-36 closure recorded. Root cause: the worktree clone
already carries `refs/heads/master`; `git branch master <tip>` (lines 496-497)
cannot create it; `git()` (lines 347-348) discards stderr, so the probe dies with
a bare RuntimeError before any summary line.

## After state the check measures

Two proposed repair shapes, both verified by the control on identical fixtures
(fresh mktemp repo, default branch `master`, two commits; top-level verified equal
to fixture root before the first commit):

- Shape A (primary proposal): `git checkout --quiet -B master <tip>` instead of
  `git branch master <tip>` (+ fold `git()` stderr into the RuntimeError).
- Shape B (alternative): delete the whole master block (lines 493-499) — verified
  dead: `grep -n master` shows no other use; the run executes on `probe-target`
  (line 500).

Measured after-state per shape: every git step rc 0; worktree `HEAD` =
`probe-target`; target tree present; shape A additionally keeps `refs/heads/master`
at the source tip. Production after-state contract for V8 once the patch lands:
livefive no longer crashes on target 1, the summary JSON line exists (`targets: 5`),
and the previously unmeasurable `check-revision-binding.py` target yields channel
rows instead of a traceback.

## Sources opened this round (2026-10-25, located quotes)

- `tools/probe-child-env-allowlist-r36.py:493-499` — "p = git(penv, '-C', wtree, 'branch', 'master', …)" / "raise RuntimeError('cannot create local master branch')".
- `.ufo/waves/round-36/w2/W2RevCounter/W2RevCounter.md:94-99` — "one_run (r36 lines 483–499) clones a worktree and then creates master, which the clone has already created from the bare clone's HEAD"; "Unconditional for any lane with a master default branch, i.e. always."
- `.ufo/waves/round-36/w2/W2RevCounter/livefive-crash.err:1-13` — traceback ending "RuntimeError: cannot create local master branch".
- `corpus/lessons/round-36-verifier-spotcheck.md:36` — "RuntimeError: cannot create local master branch (probe line 499) before any summary. Probe bug S1 reproduced by the closure."
- `tools/probe-child-env-allowlist-r36.py:347-348` — "def git(env, *args, timeout=120): return subprocess.run([SYSTEM_GIT, *args], env=env, capture_output=True, timeout=timeout)" (stderr discarded).

## Tooling

No installs/updates performed (RULES.md read first; no pacman; python3 and git
already present). No lane/fleet/sibling writes; fixture git confined to mktemp
(rule: top-level == fixture root verified before commits). No subagents/delegation.

## Risks / blockers

- The production after-state is a contract until the V8 patch lands (this wave is
  the design stage); today the control validates the repair shape at fixture level
  and the baseline failure at production level.
- The live probe run clones the lane read-only into scratch; no lane state touched
  (verified `git status --porcelain` unchanged apart from this wave's untracked
  seat/wave files).
