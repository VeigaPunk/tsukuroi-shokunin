VERDICT: defect-found

Item C1-M2 (seat TMutFixB): mutants M5-M8, one at a time, against a private copy of the
FREEZE blob `tools/tsukuroi-census.sh` @ ae99f021b76f8eb1c8805d32d80644464afb1ff6
(sha256 375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426 — re-verified
at extraction and again after all runs). All work under /fast/scratch/hyaku/tsukuroi-r48/TMutFixB
(scratch removed on exit). No lane file was ever modified; every detector ran on mutant copies.

## Mutants (line numbers in the frozen blob)

- M5  delete line 2111 `trap 'exit 143' TERM` → census-m5.sh sha d0745f5ef6686d183669a8a09fc502c3be5ebdc4b0b5794716d15319d083d39c
- M6  line 2110 `trap 'exit 130' INT` → `trap '' INT` → census-m6.sh sha 2e23bb9553e301681f373787f2def942e3bcfab5b3503bfef9f8676b6a826ff8
- M7  line 2109 EXIT trap: drop `chmod -R u+rwx` → `trap 'rm -rf -- "${work:-}" 2>/dev/null || true' EXIT` → census-m7.sh sha 9aacbe3af78c107c68efaaca8c68a809ce45c0f7f1851e6333df6e21ec20dd39
- M8  delete line 3549 `[ -n "$r48_fd" ] && exec {r48_fd}<&-` → census-m8.sh sha f6723d474df1979ddc6e648fa988d0ea9cd82581bda1966d83706dbd5c442b84

## Baselines (pre-data + in-seat)

- Control receipt (frozen, pre-data): controls/battery-summary-r48-c1.jsonl K-pass on the frozen
  blob sha 375aa7… = PASS with all legs (pass_ok 4, loc_ok 4, clean_ok 4, failfast_ok 2, term_ok 1, static_ok 1).
  Related pre-data kill: K3 "fix with the INT/TERM exit traps reverted" = FAIL (term_ok 0), as_expected true.
- In-seat pristine selftest (TMPDIR=$S/plain): `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)`, rc=0, 73 s — receipt pristine-selftest.log.
- In-seat pristine SIGINT probe: SIGINT at t≈25 s mid-run → rc=130, run aborted (int-probe-pristine.log).

## Results

### M5 — drop `trap 'exit 143' TERM` — KILLED by frozen counter, leg `term`
`python3 counter.py --census census-m5.sh` → rc=1, verdict FAIL.
term leg: `{"rc": -15, "stdout_has_pass": false, "fixture_removed": true, "ok": 0}`.
Untrapped SIGTERM kills bash with signal 15 (rc=-15, not 143) → term_ok=0 → predicate fails.
All other legs green (pass 4/4, loc 4/4, clean 4/4, failfast 2/2, static 1). Receipt m5-counter.json.
Note: bash still ran the EXIT trap before re-raising SIGTERM, so the fixture was removed —
the kill is on the exit-status half of the leg, not the cleanup half.

### M6 — `trap '' INT` — SURVIVED. Real defect, no detector leg.
- Frozen counter: `python3 counter.py --census census-m6.sh` → rc=0, verdict PASS —
  all legs green incl. term (`rc: 143, fixture_removed: true, ok: 1`). Receipt m6-counter.json.
- Direct SIGINT probe proves the defect is real: M6 mid-run SIGINT → process still alive 2 s
  post-signal, runs to `PASS (166 cases…)`, rc=0 (int-probe-m6.log) vs pristine rc=130.
- Coverage gap: nothing in the counter (counter.py: only term_leg sends a signal, SIGTERM,
  counter.py:115-141) or the 166 selftest cases ever delivers SIGINT. The frozen mechanism text
  ("INT/TERM traps exit 130/143", census :2110-2111 and counter docstring :8) asserts a 130-on-INT
  contract that no leg measures. A coverage finding, not a contract change — recommend the L1
  note an `int_leg` (mirror of term_leg, SIGINT, expect 130) as untested surface on the C1 mechanism.

### M7 — EXIT trap without `chmod -R u+rwx` — SURVIVED selftest (no abort path exercised).
- Selftest (TMPDIR=$S/plain): PASS 166/166, rc=0; TMPDIR empty afterward — zero residue
  (m7-selftest.log). Every `chmod 000` fixture dir is restored to 755 in the same case
  (pairs at :3130/:3133, :3190/:3193, :3285/:3288, :3325/:3328), so at normal exit `rm -rf`
  alone suffices.
- Mechanism demo (scratch, no selftest): `chmod 000 work/sub` → `rm -rf work` fails
  "cannot remove …/sub: Permission denied" and leaves work/ + work/sub/; `chmod -R u+rwx` first →
  clean removal. So the chmod is only load-bearing on abort paths (set -e abort or a signal between
  the `chmod 000` and its `chmod 755`, e.g. TERM landing inside the storage cases :3130-3193 —
  ~50 s into the run, counter sends TERM at ~2 s so its leg never reaches them). Killing M7 would
  need a leg that faults or signals mid-000-window and then checks `os.path.exists(real)` —
  the counter's clean_ok already measures that, only the trigger is missing.

### M8 — drop `exec {r48_fd}<&-` after the R48 dirty-TMPDIR case — SURVIVED selftest.
- Three selftest runs under TMPDIR=$S/plain: run1 PASS 166/166 rc=0; run2 FAIL 165/166 (one
  pre-existing flaky case, `healthy: five zero counters on one device` STORAGE — executes ~line 110
  of output, far *before* the removed close at :3549, cannot be caused by the mutant; coincided with
  an aggressive /proc fd poller I attached — operator-induced noise); run3 PASS 166/166 rc=0
  (m8-selftest.log/3/4; the run2 artifact is m8-selftest3.log).
- Why it survives: `ST_BASE_FD` is read only at :3541 (into `r48_fd`) and :3551 (close on the
  fail branch). With the :3549 close removed, the alias fd (240) stays open until process exit —
  a leak, but inert: the next `selftest_base_dir` call (:3550) fails at its `[ -d "$base" ]`
  guard before the fd loop, `run_selftest` never consults `ST_BASE_FD` again, and the identity
  selftest only counts regular-file O_CLOEXEC script descriptors, not a directory fd.
  No selftest case counts open descriptors, so the hygiene line has no detector.

## Detector accounting (per item rules: counter used only for M5/M6 — 2 runs)

| mutant | selftest verdict | counter verdict | result |
|--------|------------------|-----------------|--------|
| M5     | (not run alone; inside counter: all 4 scenarios PASS) | FAIL, term_ok=0 (rc=-15) | KILLED by leg `term` |
| M6     | PASS under SIGINT probe (that's the defect) | PASS all legs | SURVIVED — no SIGINT leg exists |
| M7     | PASS 166/166, TMPDIR residue-free | not run (not permitted) | SURVIVED — chmod only matters on abort paths no leg reaches |
| M8     | PASS 166/166 (one unrelated flaky STORAGE case under fd-polling load, re-run clean) | not run | SURVIVED — fd leak inert, uncounted |

## Restoration

- Lane blob re-verified after all runs: `git -C …/tsukuroi-shokunin show ae99f021…:tools/tsukuroi-census.sh | sha256sum` = 375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426.
- Scratch pristine copy untouched throughout (mutations only ever applied to census-m5/m6/m7/m8.sh copies); in-seat baseline ran on hash-identical bytes.
- No tracked file of lane or fleet written; only this report + receipts dir. Scratch dir removed on finish.

## Receipts (in .ufo/waves/round-48/w2/TMutFixB/)
m5-counter.json, m6-counter.json, pristine-selftest.log, m7-selftest.log, m8-selftest.log,
m8-selftest3.log (flaky-case artifact), m8-selftest4.log, int-probe-pristine.log, int-probe-m6.log,
mutant-shas.txt.
