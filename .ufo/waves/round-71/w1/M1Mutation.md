# M1Mutation — C2 harness and its three cases, mutation-tested (round 71, w1)

Probe: `.ufo/waves/round-71/probes/M1Mutation/{mutants.txt,score.md}`.

## Target

E1Harness's C2 harness did not publish a `harness.patch` while this seat ran, so the probe
scored two targets with the same eight mutations:

* **A** a reference implementation of the frozen C2 predicate (`harness.sh`, 5 cases:
  3 self-check + 2 ordinary; baseline PASS rc 0, 3.2 s);
* **B** the per-case bound block copied **verbatim** from E1Harness's live prototype
  (`…/E1Harness/census.sh` sha256 `ebe3ab2d…f46c`, lines 2648–2738), with only the census
  `check` path shimmed (baseline PASS 3/3 rc 0, 5.2 s). The (a)/(b)/(c) case bodies are the
  prototype's own, so B is the real design under test.

Detector: the three R71-C2 cases, run as a suite under `timeout -k 5 120`; killed = a case
FAILs or the suite hangs. Each run in a fresh `WORK`.

## Result

| mutant (one guarantee removed) | A | B |
|---|---|---|
| no process-group kill (kill `$pid`, not `-$pid`) | killed by (c) | killed by (c) |
| TERM only, no KILL escalation | killed by (c) | killed by (c) |
| bound ignored (no deadline) | killed by (a) | **killed by hang** (rc 124, 0 verdict lines) |
| bound cached at startup | killed by (a) | **survived** (equivalent mutant) |
| timeout reported as PASS | killed by (a) | killed by (a)+(c) |
| timeout line without the case label | killed by (a) | killed by (a) |
| no output capture (verdict falls back to rc) | killed by (b) | killed by (b) |
| capture file under `/tmp`, not `$work` | **survived** | **survived** |

`MUTANTS=8 KILLED=7 SURVIVORS=1` (A); `KILLED=6 SURVIVORS=2` (B).

## Survivors and the class that beat the case

* **m8 — hermeticity/location.** No case asserts *where* the capture lives; the cases read
  verdicts and pids only. Reader-consistent `/tmp` move passes 3/3 in B. The variant that only
  moves the writer is caught — by writer/reader divergence, a different defect.
* **m4 — equivalent mutant in B.** The real design computes `CASE_BOUND` once and passes the
  bound **by argument**, so caching the env knob is unobservable. In A (bound read per call) the
  same edit is real and (a) kills it. Consequence: the real suite cannot honour a mid-suite
  per-case override — not required by the frozen predicate, but it is why this mutant is free.

## Attribution and self-coverage

Each guarantee has exactly **one** behavioural detector: (a) owns the deadline + the timeout
line, (b) owns the capture, (c) owns group kill + KILL escalation. (c) also greps the timeout
line, so a reporting defect costs two cases (m5/m6) — attribution is not 1:1.

**Can the self-check catch its own removal? No.** With the three R71-C2 cases deleted
(`--suite-noself`), all eight mutants return `PASS (2 cases, 2 passed, 0 failed)` rc 0 —
**8/8 invisible**. The removal is noticed only by the frozen arithmetic target `N >= 217`
(214 + 3), never behaviourally; a future round that "repairs" the count would erase the last
trace of the guarantee.

## Restoration

Lane tree never written; `tools/tsukuroi-census.sh` sha256
`487feeb6caa687daf586d4b7577746e5f1ed22ca336e9c0e0194d13995bd4b3c` before and after.
Pristine A re-run after all mutants: same sha256, `PASS (5 cases, 5 passed, 0 failed)` rc 0.
E1Harness's prototype read only. No tool installed. All trees under
`S=/fast/scratch/hyaku/tsukuroi-r71/M1Mutation`, deleted at exit.
