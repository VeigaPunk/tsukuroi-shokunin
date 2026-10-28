VERDICT: defect-found

# TRevCounterB — C1-R6: flakiness/race review of tools/score-selftest-tmpdir-r48.py @ ae99f021

All reproductions ran against the frozen counter (`git show ae99f021:tools/score-selftest-tmpdir-r48.py`) and the frozen census blob (sha256 375aa737… per controls) in scratch `/fast/scratch/hyaku/tsukuroi-r48/TRevCounterB/`. Host load during review: 22 → 64 on 32 cores — exactly the fleet-load regime the item asks about. Receipts in this directory (`A.out`, `B.out`, `term.py`, `stub-census.sh`, `counter.py`).

## F1 — CONFIRMED fleet-scale flake: concurrent counter invocations with the same `--work` destroy each other (HIGH)

`--work` defaults to the fixed path `$HYAKU_SCRATCH/tsukuroi-r48/counter-c1` (line 169-170). Two invocations sharing that dir collide at line 205 (`os.makedirs(wrapdir)` — no `exist_ok`):

- Demonstrated: ran counter A (stub census that sleeps) with `--work shared-work`; ran counter B 3 s later with the same `--work`.
- B output (receipt `B.out`): `{"counter": "score-selftest-tmpdir-r48", "error": "FileExistsError: [Errno 17] File exists: '.../shared-work/wrap'", "verdict": "FAIL"}`, rc=2.
- B's `finally: shutil.rmtree(work)` (line 182) then deleted A's work dir mid-run; A subsequently emitted `{"error": "FileNotFoundError: [Errno 2] ... 'shared-work'", "verdict": "FAIL"}` (receipt `A.out`).
- Net effect: two overlapping counter runs with the default or same `--work` produce two FAIL verdicts and zero counted evidence — a genuine fleet flake (the fleet runs ~90 seats; any second seat running this counter with the default `--work` collides, and distinct `--work` values are not enforced anywhere).
- Second-order: a crashed/killed run that left `work` behind also leaves stale `<name>.mktemp.log` files (makedirs is `exist_ok=True` at line 172), and `read_log` then sees >1 rows → `loc_ok=0`/`failfast_ok=0`. Same fix covers it.
- Exact fix (one line + import):
  ```python
  work = os.path.abspath(a.work or os.path.join(root, 'tsukuroi-r48', f'counter-c1.{os.getpid()}'))
  ```
  or `work = tempfile.mkdtemp(prefix='counter-c1.', dir=os.path.join(root,'tsukuroi-r48'))` when `a.work` is unset. (If `--work` is explicitly given, either honor it as the leaf dir or `mktemp`-suffixed — the collision is in the default path.)

## F2 — CONFIRMED race: SIGTERM in the log→trap window returns −15 and leaks the fixture (MEDIUM)

`term_leg` detects the fixture via the wrapper log then `time.sleep(1.5)` + `send_signal(SIGTERM)` (lines 121-130). The log line is written the moment `mktemp` returns; the census installs `trap 'exit 143' TERM` only *after* `mktemp` returns (census.sh ae99f021 lines 2106-2111). A TERM delivered in that window kills bash with default disposition (Python sees rc −15, not 143) and, worse, the EXIT trap's `rm -rf $work` races the kill — the fixture leaks.

- Demonstrated: fired SIGTERM immediately upon log appearance (no sleep), 12/12 runs: `rc -15`, `fixture_gone False` (leaked `tsukuroi-r3-2-selftest.*` dirs under the spaced TMPDIR). With the counter's 1.5 s sleep, 9/9 runs at delays 1.5–50 s gave rc 143 + fixture removed — so the current margin is normally sufficient, but a scheduler stall >1.5 s between the two trap lines (observed load-64 host) lands in the same window.
- Exact fix, verified working 6/6 (`rc 143 lat ~0.00-0.01s gone True`, no sleep needed): gate on bash's caught-signal mask before signalling —
  ```python
  TERM_BIT = 1 << (signal.SIGTERM - 1)
  while time.time() < deadline and p.poll() is None:
      rows = read_log(log)
      if rows:
          try:
              with open(f'/proc/{p.pid}/status') as f:
                  if int(re.search(r'SigCgt:\s*([0-9a-f]+)', f.read()).group(1), 16) & TERM_BIT:
                      break
          except (FileNotFoundError, AttributeError):
              pass
          time.sleep(0.05)
  ```
  then `send_signal` immediately. This also removes the fixed 1.5 s from every run.

## Questions posed by the item, answered

1. **Selftest already finished before SIGTERM?** Impossible in practice: fixture log appears ~0.02 s after spawn; SIGTERM goes at ~1.5 s; a selftest runs tens of seconds (leg at delay 50 s was still mid-run, 152 output lines). Even on a fast host, completion in <1.5 s is infeasible. If it ever did, `send_signal` on a reaped Popen is a guarded no-op (verified on Python 3.14: `Popen(['true']).wait(); p.send_signal(SIGTERM)` returns `None`, no exception), and `communicate` returns rc 0 → `ok=0` — a correct FAIL, not a flake.
2. **Deferred trap behind a foreground child?** SIGTERM to the bash pid does not reach the in-flight child; bash runs the TERM trap after that child exits. Measured latency from send_signal to exit: 0.04–0.21 s at delays 1.5–35 s, **6.17 s at delay 50 s** (deferred behind the current case's child; output grew to 152 lines before SIGTERM, so the leg ran a full case between signal and trap). Worst-case deferral ≈ one fixture/census child duration — far inside the 180 s `communicate` window. Residual (theoretical, not demonstrated): if bash's in-flight child spawned a grandchild that outlives bash while holding the stdout pipe, the second `communicate()` at line 135 has **no timeout** and hangs forever; grep of census.sh found no `&`/coproc/wait background children (only the summary printf at :3558), so this needs a future census that backgrounds a pipe-holder — not reachable with the frozen blob.
3. **Log appended before fixture exists?** No — WRAPPER (lines 48-54) runs `/usr/bin/mktemp` first and appends the log only on success; the fixture is created before the log row exists. Torn-read theoretical: `read_log` would split a partial line into <3 fields and `len(rows)==1` could pass on a half-written row — never observed across ~20 runs; O_APPEND writes are single syscall, sub-microsecond window. No fix proposed.
4. **Shared wrapper log between scenarios?** No — verified: each scenario/failfast/term leg uses `f'{name}.mktemp.log'`/`term.mktemp.log`/`{name}.mktemp.log` inside `work` (lines 87, 107, 116); distinct files within one invocation. Cross-invocation sharing is F1.
5. **Worst-case runtime vs RUN_TIMEOUT?** `timeout=RUN_TIMEOUT` (900 s) bounds each `subprocess.run` *individually* (line 77), not the run. Six selftest invocations + polling/term phase → ceiling ≈ 6×900 + 60 + 1.5 + 180 ≈ **91.5 min**. At ~60 s nominal per selftest the whole counter is ~6 min nominal, ~20-30 min at load factor 3-4 — inside typical seat budgets but far above the "5-10 minutes" in the round notes; if a seat wall-clock limit kills the counter, `finally: rmtree(work)` still cleans on SIGTERM but the seat gets no JSON line. Optional honesty fix: compute a total deadline and report `verdict: FAIL, error: 'counter wall-clock exceeded'` rather than dying silent — not required for the predicate.

## Not defects
- `run_selftest` TimeoutExpired propagates to `main`'s in-band handler → FAIL JSON, rc 2, work cleaned (lines 76-78, 177-182). Honest timeout → counted FAIL, correct semantics.
- `p.poll()`-missed-exit in `term_leg` line 126-128: also `p.communicate()` with no timeout — only reachable if the census hung before writing any fixture; bounded by the same theoretical-grandchild caveat in (2); the 60 s loop itself is fine.
- `send_signal` races a just-exited pid: guarded by Python's `_sendsignal` returncode check + pid-reuse waitpid sentinel (subprocess.py:2217ff); verified no-op.
- `clean_ok`/`loc_ok` row parsing (`len(rows)==1 and len(rows[0])==3`) fails safe.

## What I did not do
- Did not run the frozen counter end-to-end on the frozen revision (one invocation ≈ 6 selftests ≈ 6 CPU-min; other seats hold that receipt — controls `battery-summary-r48-c1.jsonl` K-pass already shows PASS at sha 375aa737).
- Did not test the spaced-TMPDIR alias path for F1/F2 beyond the real census runs above (all term legs ran under `TMPDIR=$PWD/tmpd/a b`, i.e. the spaced path).
