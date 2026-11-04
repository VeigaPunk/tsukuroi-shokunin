# E1Harness — round 71 w1 (C2 per-case timeout harness, independent alternative)

Milestone: C2 harness draft + hermetic cases. Not applied to the lane; the L1 landed an
equivalent at `db58e7c9`, so this seat delivers the independent alternative plus a diff.

Draft base: `db58e7c9^` (`tools/tsukuroi-census.sh` sha256 `042c6b4b…1efe518c`, 4676 lines),
byte-identical to the copy taken before the landing.

## Delivered

- `.ufo/waves/round-71/probes/E1Harness/harness.patch` — 235-line unified diff on the
  pre-landing base (`patch -p1`, dry-run OK).
- `.ufo/waves/round-71/probes/E1Harness/harness-vs-landed.diff` — landed `db58e7c9` → draft.
- `.ufo/waves/round-71/probes/E1Harness/harness-on-landed.patch` — 67-line minimal patch on the
  landed bytes closing the `arm_run` hole and the zombie-blind poll; suite re-ran PASS 217/217.
- `.ufo/waves/round-71/probes/E1Harness/cases.txt` — the three `R71-C2` case bodies.
- `.ufo/waves/round-71/probes/E1Harness/census-r71-c2.patched.sh` and
  `census-on-landed-patched.sh` — runnable patched copies (read-only exercise).
- `.ufo/waves/round-71/probes/E1Harness/E1Harness.md` — full report (touched functions, line
  ranges, guarantee matrix, risks).
- `.ufo/waves/round-71/probes/E1Harness/scorecard-round71-declaration.md` — Round-71 section of
  `SCORECARD.md` at `0fcfca31`, copied read-only for reviewers.

## Behavior

One bounded runner (`case_bound_run`) used by `check`, `check_cli` and `arm_run`: child in its
own session/process group under `setsid`, output to a file under `$work`, 0.1 s poll to
`TSUKUROI_SELFTEST_CASE_TIMEOUT` (default 60), TERM the group, up to 2 s grace, KILL the group,
child rc or 124 returned. Liveness reads `/proc/PID/stat` state so an unreaped zombie reads dead.
A timeout is always `FAIL <label>: case timeout after <N>s (…)` — never a skip, never a suite
crash. The bound is parsed fail-closed.

## Evidence (scratch; tree deleted at yield)

- draft, default bound: `PASS (217 cases, 217 passed, 0 failed)` rc 0, 59.7 s.
- red proof (draft + 3 s sleeper case, `TSUKUROI_SELFTEST_CASE_TIMEOUT=1`): `FAIL R71-C2 RED a 3 s
  child under a 1 s bound: case timeout after 1s (…)`, suite rc **1**.
- draft at bound 2: `FAIL (217 cases, 216 passed, 1 failed)` — `R45-C1` genuinely needs > 2 s, so
  the 60 s default is load-bearing.
- landed `db58e7c9`: PASS 217/217 rc 0, 56.5 s. Landed + minimal patch: PASS 217/217 rc 0, 58.5 s.
- No leftover case child after any run (`ps | grep -c r71-c2` → 0).

## Guarantees the landed version lacked at `db58e7c9` (all since adopted — see below)

`arm_run` unbounded (two A/B neutrality cases can still hang the suite — contradicts "bounds every
selftest case"); zombie-blind `kill -0` poll; 0.2 s grace instead of 2 s; fail-open bound parsing;
no distinct timeout rc; group kill assumes `setsid` execs directly. Reverse: the landed version
uses `mktemp` per call, reports elapsed ms, and its no-false-positive arm slows the real probe.

## Post-adoption (L1 adopted the diff; observed landed blob `a641bcf6…3948fb9`)

Adopted: `arm_run` bounded, `id_run` over all six `--identity` children, `/proc`-state liveness
with `kill -0` fallback, 2 s TERM→KILL grace, `BOUND_RC=124`, unconditional group KILL after
`wait`, and a fourth `R71-C2` case asserting a daemonizing child leaves no descendant.

Remaining **landed-only** guarantees (not in this draft): `mktemp` per call; elapsed ms in the
FAIL line; the no-false-positive arm slows the real probe instead of a fake census; the
daemonizing-child case and its post-`wait` group KILL; `id_run` over the identity children (the
draft left them raw); and bound **normalization to 60 s** where the draft fails closed — a
deliberate policy split, both keeping the guard on.

## Risks

`harness-vs-landed.diff` replaces the landed structure and must not be applied on top of it.
Tightening the default bound below ~5 s false-positives on `R45-C1` (measured at 2 s and 1 s).

## Tooling

No installs or upgrades; no pacman transaction; no host write.

PATCH_LINES=235
CASES=3
BOUND_DEFAULT=60
ESCALATION=yes
NOFALSEPOS=yes
