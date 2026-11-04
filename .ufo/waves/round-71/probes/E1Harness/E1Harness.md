# E1Harness — C2 per-case timeout harness (round 71, w1)

Independent alternative to the harness the L1 landed at `db58e7c9`. Drafted on the
pre-landing base `db58e7c9^` (blob sha256 `042c6b4b…1efe518c`, 4676 lines — byte-identical to
the copy taken before the landing). Nothing here was applied to the lane tree; the L1 owns it.

## Artifacts

| path | what |
|---|---|
| `harness.patch` | the draft as a unified diff on `db58e7c9^` (`patch -p1`, dry-run OK) |
| `harness-vs-landed.diff` | landed `db58e7c9` → the draft, for guarantee-by-guarantee review |
| `harness-on-landed.patch` | minimal patch **on the landed bytes** closing the two gaps below; suite re-run PASS 217/217 |
| `census-r71-c2.patched.sh` | the draft applied, runnable read-only (`TMPDIR=<scratch> bash <file> --selftest`) |
| `census-on-landed-patched.sh` | landed + `harness-on-landed.patch`, runnable the same way |
| `cases.txt` | the three hermetic case bodies, verbatim from the draft |
| `scorecard-round71-declaration.md` | `git show 0fcfca31:SCORECARD.md` Round-71 section (read-only copy for review) |

## The draft (`harness.patch`, 235 lines, 5 hunks)

One runner, `case_bound_run LABEL OUTFILE BOUND CMD...` (patched `tools/tsukuroi-census.sh`
2648–2739), used by every case driver:

- starts the child under `setsid` through a wrapper that publishes **its own** pid before it
  runs the command, so that pid is the new session's leader and `kill -- -PID` addresses exactly
  this case's group whether `setsid` execs directly or forks;
- output to `$work/case-out.*` (never a command substitution that a killed child can strand);
- polls at 0.1 s to `CASE_BOUND` (env `TSUKUROI_SELFTEST_CASE_TIMEOUT`, default **60**), then
  TERM the group, up to a 2 s grace, KILL the group; returns the child rc or **124**;
- liveness is `/proc/PID/stat` state (a zombie reads dead), falling back to `kill -0` off `/proc`;
- the bound is parsed fail-closed: a non-integer or `< 1` value makes `run_selftest` refuse to
  run (rc 1) instead of silently disabling the guard.

Touched call sites and ranges (patched file):

| function | lines | change |
|---|---|---|
| `run_selftest` (harness block after `skip()`) | 2648–2739 | `case_bound_value`, `case_alive`, `case_bound_run`, `case_timeout_line/fail`, `CASE_BOUND` resolution |
| `check` | 2915–2966 | child run through `case_bound_run`; timeout branch first, before the exit-code branch |
| `check_cli` | 2968–2994 | same |
| `arm_run` | 4263–4271 | same (the two A/B neutrality cases) |
| `run_selftest` tail | 4603–4679 | three `R71-C2` hermetic cases |

The three cases (`cases.txt`) each drive the **real** `check` path in a subshell whose `ok`/`bad`
append to files, so a deliberate FAIL cannot leak into the suite's counters: (a) FIFO-blocked
child at a 2 s bound → killed, FAIL names the case and `timeout`; (b) 1 s child at the same 2 s
bound → passes; (c) `trap '' TERM` child → escalated, gone inside the bound.

## Measured evidence (raw outputs retained under `receipts/`)

| run | result |
|---|---|
| draft, default bound | `PASS (217 cases, 217 passed, 0 failed)` rc 0, 59.7 s |
| draft, `TSUKUROI_SELFTEST_CASE_TIMEOUT=2` | `FAIL (217 cases, 216 passed, 1 failed)` rc 1 — `R45-C1` (foreign baseline past the pipe buffer) legitimately needs > 2 s |
| **red proof**: draft + a 3 s sleeper case, bound 1 | `FAIL R71-C2 RED a 3 s child under a 1 s bound: case timeout after 1s (TSUKUROI_SELFTEST_CASE_TIMEOUT; child killed TERM then KILL)`, rc **1** |
| landed `db58e7c9`, default bound | `PASS (217 cases, 217 passed, 0 failed)` rc 0, 56.5 s |
| landed + `harness-on-landed.patch` | `PASS (217 cases, 217 passed, 0 failed)` rc 0, 58.5 s; arms 2052/1239/2050 ms |

No `r71-c2` or `sleep 30` process survived any run (`ps -eo pid,stat,args | grep -c` → 0).

## Guarantees the landed version lacked at `db58e7c9` (all since adopted — see post-adoption)

Landed lacks:

1. **`arm_run` is unbounded.** The initramfs-neutral and xfs-neutral A/B cases call
   `env … "$BASH" "$SELF"` directly (`db58e7c9` line 4233). A hang there still ends the suite at
   an external bound — the exact pre-fix failure mode — so "bounds **every** selftest case" is
   not yet literally true. `harness-on-landed.patch` fixes only this and re-verifies green.
2. **Zombie-blind liveness.** `while kill -0 "$pid"` succeeds on an unreaped zombie; it works on
   this bash (measured), but the guarantee is the shell's reaping behaviour, not the harness's.
3. **0.2 s grace**, not the 2 s the seat spec names, between TERM and KILL.
4. **Fail-open bound parsing**: a malformed `TSUKUROI_SELFTEST_CASE_TIMEOUT` silently becomes 60.
5. **No distinct timeout rc**: callers see the wait status (143/137) plus a flag; the draft
   returns 124.
6. **Group kill assumes `setsid` execs directly** (true for a non-interactive background child);
   the draft's wrapper-pid form is correct either way.

Landed has, and the draft does not: `mktemp` per call instead of one fixed capture file per call
site (safe here only because calls are sequential); elapsed ms in the FAIL line; and its
no-false-positive arm slows the **real** census probe rather than a fake census, which is the
stronger form of that proof.

## Post-adoption status (L1 adopted the diff; observed blob `a641bcf6…3948fb9`)

Adopted into the landed harness: `arm_run` bounded, an `id_run` wrapper bounding all six
`--identity` children, `/proc`-state liveness with a `kill -0` fallback, a 2 s TERM→KILL grace,
`BOUND_RC=124` on timeout, an unconditional group KILL after `wait`, and a fourth `R71-C2` case
asserting a daemonizing child leaves no descendant.

**Guarantees that remain landed-only** (present in the landed harness, absent from this draft):

1. `mktemp` per call — the draft reuses one fixed capture file per call site (safe only because
   the calls are sequential).
2. Elapsed milliseconds in the timeout FAIL line (`BOUND_ELAPSED`); the draft prints the bound in
   whole seconds only.
3. The no-false-positive arm slows the **real** census probe (a slow `pacman` stub inside a real
   run) rather than the draft's fake census script — the stronger form of that proof.
4. The daemonizing-child case and the unconditional post-`wait` group KILL that backs it.
5. `id_run` over the `--identity` children; the draft left them raw on the judgement that they
   carry no probe surface. The landed version is stricter.
6. Bound **normalization to 60 s** where the draft fails closed. Deliberate policy difference: the
   draft refuses to run on a malformed value (loud, but no harness at all), the landed version
   keeps the guard on and the suite running. Both keep a bound; neither disables it.

## Risks

- `harness-vs-landed.diff` replaces the landed structure wholesale; it is a comparison artifact,
  not something to apply on top of `db58e7c9`.
- A 1 s bound false-positives on `R45-C1` (measured), so the 60 s default is load-bearing; do not
  tighten it in the suite.
- Both harnesses poll at 0.1 s, so the bound is accurate to about ±0.1 s plus the child's own
  startup; the arms allow 5–8 s of slack accordingly.

## Tooling

No installs, no upgrades, no pacman transactions.
