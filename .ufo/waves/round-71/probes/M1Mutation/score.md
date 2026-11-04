# M1Mutation — score: C2 harness mutants against the three R71-C2 cases

## Method

Two targets, the same eight single-guarantee mutations, the same detector.

* **A — reference model** (`harness.sh`, sha256 `43f9d5af…d64799`): the frozen C2 predicate
  implemented directly — `run_case` starts each child in its own process group (`set -m`,
  `$!` is the PGID), polls `/proc/$pid/stat` state to the per-case bound
  (`TSUKUROI_SELFTEST_CASE_TIMEOUT`, default 60 s, read on every call), kills the group TERM,
  gives 20 × 0.05 s grace, kills the group KILL, emits `FAIL <label> timeout after <n>s`,
  captures child output under `$WORK`. Baseline **PASS (5 cases, 5 passed, 0 failed) rc 0, 3.2 s**.
* **B — real-design replica** (`real-harness.sh`): the per-case bound block copied **verbatim**
  from the E1Harness prototype (`/fast/scratch/hyaku/tsukuroi-r71/E1Harness/census.sh`,
  sha256 `ebe3ab2d…f46c`, lines 2648–2738; block sha256 `7db90195…41bd0`) — `case_bound_run`
  with the `setsid` wrapper + pidfile authority, `case_alive`, `CASE_TICK 0.1`,
  `CASE_GRACE_TICKS 20`, unconditional group KILL, rc file, `case_timeout_line`/`case_timeout_fail`.
  Only the census `check` path is a shim (runs `$SELF`, requires the expected rc and the
  `TSUKUROI_CENSUS: <verdict>` line). The three (a)/(b)/(c) case bodies are the prototype's own.
  Baseline **PASS (3 cases, 3 passed, 0 failed) rc 0, 5.2 s**.

Detector: each mutant suite runs under `timeout -k 5 120`. **Killed** = a case FAILs, or the
suite does not finish inside the external 120 s bound. Every run used a fresh `WORK` dir.

## Scores

| guarantee removed | A verdict | A rc | A (a/b/c) | B verdict | B rc | B (a/b/c) |
|---|---|---|---|---|---|---|
| m1 no process-group kill | killed | 1 | P P F | killed | 1 | P P F |
| m2 TERM only, no KILL | killed | 1 | P P F | killed | 1 | P P F |
| m3 bound ignored | killed | 1 | F P F | killed (hang) | 124 | – – – |
| m4 bound cached at startup | killed | 1 | F P F | **survived** | 0 | P P P |
| m5 timeout reported as PASS | killed | 1 | F P F | killed | 1 | F P F |
| m6 timeout line without label | killed | 1 | F P F | killed | 1 | F P P |
| m7 no output capture | killed | 1 | P F P | killed | 1 | P F P |
| m8 capture under /tmp, not $work | **survived** | 0 | P P P | **survived** | 0 | P P P |

A: **MUTANTS=8 KILLED=7 SURVIVORS=1**. B: **MUTANTS=8 KILLED=6 SURVIVORS=2** (one equivalent).

## Attribution — which case owns which guarantee

* **(a) FIFO-blocked child bounded** owns: the deadline itself (m3), the timeout FAIL line
  naming the case and `timeout` (m6), and timeout-counted-as-failure (m5). It also fires on m4
  in model A because the per-case override is the only way to shorten the bound there.
* **(b) child that finishes inside the bound** owns: capture integrity (m7). In model A the
  probe is a child that prints `FAIL …` and exits 0 — the census `bad()` shape, which prints
  and returns 0 — so removing the capture turns a real FAIL into a PASS.
* **(c) TERM-ignoring child killed** owns: group kill (m1) and KILL escalation (m2). In model B
  the published pid is the *descendant* (`$$` of the stubborn script), which is exactly why a
  pid-only kill is visible there.

Overlap findings:

1. **(c) is not independent of the timeout-line contract.** m5 and m6 also fail (c) in model A
   and m5 fails (c) in model B, because (c) greps the same `timeout` line. A defect in the
   reporting channel costs two cases, not one — attribution is not one-case-per-guarantee.
2. **(b) is the only detector of capture loss.** No other case observes the capture.
3. **(a) is the only detector of the label** (model B): m6 leaves (b) and (c) green.
4. Every guarantee has exactly **one** behavioural detector. There is no redundancy: a single
   case regression blinds a whole guarantee class, and nothing else in the suite notices.

## Survivors and the classes that beat the cases

* **m8 — hermeticity/location (both models).** Moving the case capture from `$work` to `/tmp`
  changes nothing the three cases assert: they read verdicts and pids, never the path of the
  capture file. Model B survives with a reader-consistent move (`check` writes and reads
  `/tmp/out.$$.$RANDOM`): `PASS (3 cases, 3 passed, 0 failed)`. The only way this mutation
  surfaces is writer/reader divergence (variant `B*`, rc 1) — i.e. a *different* defect.
  The frozen predicate says output goes "under `$work`"; no case checks it.
  Class: **unasserted location / no hermeticity probe**.
* **m4 — equivalent mutant (model B only).** The real design computes `CASE_BOUND` once at
  startup and passes the bound to `case_bound_run` **by argument**; caching the env knob in
  `case_bound_value` is therefore unobservable. In model A the bound is read per call, so the
  same edit is a real defect and (a) kills it. Class: **unreachable-by-construction**, not a
  coverage gap — but it means the real suite cannot honour a mid-suite per-case override, which
  the frozen predicate does not require.

## Can the harness's own self-check catch its own removal?

Measured, model A: with the three R71-C2 cases deleted from the suite (`--suite-noself`, two
ordinary cases left), **all eight mutants return `PASS (2 cases, 2 passed, 0 failed)` rc 0 —
8/8 invisible**. Model B without the three cases has no cases at all, so 8/8 invisible by
construction.

So the self-check is the **sole** detector for every guarantee in the list; deleting it is
behaviourally silent. The only thing that notices its removal is arithmetic: the frozen target
`N >= 217` (baseline 214 + 3) fails if the three cases disappear. That is a count assertion,
not a behavioural one — and it is exactly the kind of target a future round could "repair" by
lowering the number.

## Restoration evidence

* Lane tree never written: `tools/tsukuroi-census.sh` sha256 before and after
  `487feeb6caa687daf586d4b7577746e5f1ed22ca336e9c0e0194d13995bd4b3c` (identical).
* E1Harness prototype read only; sha256 `ebe3ab2d4bfb2e8470dc63403112c4e72642e904e1726f5578997cab73fef46c`.
* Pristine `harness.sh` sha256 `43f9d5af0de24ded426cccafa4370642aa69e689169d53573bf7de79ced64799`
  re-run after all mutants: `PASS (5 cases, 5 passed, 0 failed)` rc 0.
* All trees under `S=/fast/scratch/hyaku/tsukuroi-r71/M1Mutation`, deleted at exit.
