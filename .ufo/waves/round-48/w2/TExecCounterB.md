VERDICT: defect-found

# C1-X2 — replicate B of the frozen C1 counter under a poisoned ambient (TExecCounterB)

**Result.** One run of the frozen command, exactly as the item spells it. The counter returned
**FAIL, rc 1, `pass_ok = 2` of 4** where replicate A (`w2/TExecCounterA/counter.json`) returned
**PASS, `pass_ok = 4`** on the *same* census bytes (`census_sha256` identical) inside the same
host window. Every other leg matched A: `loc_ok 4`, `clean_ok 4`, `failfast_ok 2`, `term_ok 1`,
`static_ok 1`.

So, split precisely:

- The **C1 mechanism itself was confirmed by this replicate**: the dirty-TMPDIR `/proc/self/fd/240`
  alias resolves *inside* TMPDIR (spaced leg `real_parent` = `…/w/tmp with space`, log line
  `-d /proc/self/fd/240/tsukuroi-r3-2-selftest.XXXXXX … /fast/scratch/…/w/tmp with space/tsukuroi-r3-2-selftest.r88iyL`),
  the fixture never lands outside its base, both fail-fast legs fail fast with zero fixture
  creations, SIGTERM ends 143 with the fixture removed, and the static `/tmp` scan is clean.
- The **counter's PASS predicate did not reproduce**: two of four scenario legs returned
  `TSUKUROI_CENSUS_SELFTEST: FAIL` at the same census hash. That is a defect in the measuring
  instrument (see §5), not evidence that TMPDIR handling is broken — but it means the frozen
  counter cannot certify C1 as a stable counted verdict while the fleet runs concurrently.

- The **poisoned ambient was not the cause and had no effect**: the counter built each child env
  from scratch (`tools/score-selftest-tmpdir-r48.py:68-73` — only `PATH`, `LC_ALL`, `MKTEMP_LOG`
  and per-scenario `TMPDIR`), the ambient `TMPDIR="$S/amb space"` and `HYAKU_SCRATCH="$S/hs"`
  were never touched (`amb space` empty afterwards; `$S/hs` never created), and the failure class reproduced
  later from a **plain** outer environment (the `diag` replay, no ambient poisoning), while every
  rerun whose outer env *was* poisoned ran clean. Ambient sensitivity: absent.

## 1. Command, bytes, timing

```
S=/fast/scratch/hyaku/tsukuroi-r48/TExecCounterB
env TMPDIR="$S/amb space" HYAKU_SCRATCH="$S/hs" nice -n 10 \
  python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-selftest-tmpdir-r48.py \
  --revision ae99f021b76f8eb1c8805d32d80644464afb1ff6 --work "$S/w"
```
(`run-b.sh`; the only difference from the item's line is `/usr/bin/time`, absent on this host —
the first driver attempt died `rc=127` *before* python started, so exactly **one** counter run
was executed, `run-status.txt`: `rc=1 start=1793188743 end=1793188971 dur=228`.)

- Counter blob under which it ran: `tools/score-selftest-tmpdir-r48.py` sha256
  `8eead161e990e9e6f5155984797396d79fe7a3e6524a1a0c3087758658625640`, identical to the frozen
  record (`.ufo/waves/round-48/frozen/FROZEN.md`, C1 counter row).
- Census bytes read by the counter itself from the freeze revision (counter `:186-192` does
  `git -C <lane> show <rev>:tools/tsukuroi-census.sh` into `$work`): **`census_sha256 =
  375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`** — expected value, matches
  the item and `FROZEN.md`.
- Output: `.ufo/waves/round-48/w2/TExecCounterB/counter.json` (verbatim, single JSON line),
  `verdict: FAIL`, empty stderr (`counter.stderr`, 0 bytes).

## 2. Legs (this run vs replicate A)

| leg | A (`w2/TExecCounterA/counter.json`) | B (this seat) |
|---|---|---|
| pass_ok | 4 | **2** |
| loc_ok | 4 | 4 |
| clean_ok | 4 | 4 |
| failfast_ok | 2 | 2 |
| term_ok | 1 | 1 |
| static_ok | 1 | 1 |
| verdict | PASS | **FAIL** |
| census_sha256 | 375aa737…e2426 | 375aa737…e2426 |

Per-scenario, from `counter.json` (`scenarios[]`):

| scenario | A | B | B last_line |
|---|---|---|---|
| unset | pass 1, rc 0 | **pass 0, rc 1** | `TSUKUROI_CENSUS_SELFTEST: FAIL (166 cases, 164 passed, 2 failed)` |
| tmp | pass 1, rc 0 | pass 1, rc 0 | `PASS (166 cases, 166 passed, 0 failed)` |
| scratch | pass 1, rc 0 | pass 1, rc 0 | `PASS (166 cases, 166 passed, 0 failed)` |
| spaced | pass 1, rc 0 | **pass 0, rc 1** | `TSUKUROI_CENSUS_SELFTEST: FAIL (166 cases, 165 passed, 1 failed)` |

Location and cleanup were green in all four legs of the failing run (`loc_ok 4`, `clean_ok 4`);
the failures are case failures inside the census selftest, not TMPDIR placement failures.

## 3. Hostile ambient: insensitive, and no ambient write

- The counter passes a *constructed* env to each child (`score-selftest-tmpdir-r48.py:68-73`):
  `PATH=<wrapdir>:/usr/bin:/bin`, `LC_ALL=C`, `MKTEMP_LOG=<work>/<scenario>.mktemp.log`, plus
  `TMPDIR` only for the `tmp`/`scratch`/`spaced`/failfast legs. Ambient variables cannot reach a
  child except through inherited fds and cwd (`subprocess.run`, `close_fds=True`, cwd=`work`).
- `"$S/amb space"` after the run: empty (`ls -a` → `. ..`). Nothing was written there.
- `"$S/hs"` (ambient `HYAKU_SCRATCH`) never came into existence: `ls -d "$S/hs"` →
  `No such file or directory`; `--work` was explicit, so the counter never fell back to it
  (`:175-177` `root = os.environ.get('HYAKU_SCRATCH', ...)`, overridden by `--work`).
- The ambient TMPDIR **did** carry a space, and the selftest still built only under the counter's
  own per-scenario dirs — i.e. the ambient spelling did not leak into any fixture path.

## 4. /tmp and fixture hygiene (kill-rule observation)

Attribution is by the counter's own `mktemp` wrapper log (same technique the counter uses,
`WRAPPER` at `:48-57`), copied while the run was live (`mktemplogs/`):

| scenario | wrapper log (args → out → realpath) |
|---|---|
| unset | `-d /tmp/tsukuroi-r3-2-selftest.XXXXXX` → `/tmp/tsukuroi-r3-2-selftest.aUXWf6` → same |
| tmp | `-d /tmp/tsukuroi-r3-2-selftest.XXXXXX` → `/tmp/tsukuroi-r3-2-selftest.iK8UzB` → same |
| scratch | `…/w/tmp-plain/tsukuroi-r3-2-selftest.XXXXXX` → `…/tmp-plain/tsukuroi-r3-2-selftest.bJGHjC` |
| spaced | `-d /proc/self/fd/240/tsukuroi-r3-2-selftest.XXXXXX` → `/proc/self/fd/240/tsukuroi-r3-2-selftest.r88iyL` → **`…/w/tmp with space/tsukuroi-r3-2-selftest.r88iyL`** |

- `/tmp` fixture alive mid-run (`tmp` leg, 09:00:03): `/tmp/tsukuroi-r3-2-selftest.iK8UzB`
  containing `bin fx` — legitimate for `unset`/`tmp` (the `unset` leg's
  `/tmp/tsukuroi-r3-2-selftest.aUXWf6` had already been created and removed by then).
- After the run: **`aUXWf6`, `iK8UzB`, `bJGHjC`, `r88iyL` all gone** (checked by exact name,
  nothing left behind), the spaced fixture was inside `$S/w/tmp with space` and vanished with
  `$S/w` (`shutil.rmtree(work)`, counter `:182`).
- Other `/tmp/tsukuroi-r3-2-selftest.*` entries seen during and after my window are **not mine**
  and are not attributable to my run: `qMuipK` (mtime 1793186906 = 08:28:26) and `BkCWTl`
  (1793188661 = 08:57:41) pre-date my start (1793188743 = 08:59:03) — both present in the
  pre-run listing `tmp-listing-pre-run.txt`; `aQr5Cf`, `uBW26g`, `CZGS6O`, `EXXxw6`, `iCjBC4`,
  `MPSXpR`, `SmtiKT`, `lY448E`, `w5t6JY` appear only from concurrently running sibling seats
  (their names never appear in my wrapper logs; siblings ran their own selftests in parallel).
- No `/tmp` fixture outside `unset`/`tmp`, no write to `/var/tmp`, no ambient-dir write.

## 5. Divergence analysis — what failed, and what I could not attribute

The counter keeps only the last stdout line and six booleans (`scenario()` `:86-104`); it never
persists the child's stdout/stderr, and it deletes `work` (`:182`). So the two failing `unset`
cases are **not** recoverable from the frozen artifacts.

**One label was recovered** by replaying the counter's exact child env by hand (my own driver,
census read from the freeze revision, `diag.sh`, work under my scratch, `nice -n 10`):

```
== between runs loadavg=48.19 39.10 34.67 46/7492 3484213 ==
spaced rc=1 last=TSUKUROI_CENSUS_SELFTEST: FAIL (166 cases, 165 passed, 1 failed)
FAIL blocked: C1 root arm survives empty-db early return (R12-C1): plane evidence missing:
  'root_status=ok root_mode=0755 root_uid=[0-9]+ root_gid=[0-9]+'; got: PLANE packages: BLOCKED
  (pacman -Qq listed no packages [local db empty; state not assessable]; root_status=ok
  root_mode=0755 root_uid=1000 root_gid=1000 root_euid=1000 root_owner_write=present
  root_owner_search=present root_src=override
  root_dir=/proc/self/fd/240/tsukuroi-r3-2-selftest.DpwvQR/fx/blocked-root-early-empty-db/root) …
```
(`diag-spaced-fail.txt` and `diag-summary.txt`, verbatim; census frozen lines 3047-3050 = the case,
2372 = the failing pipeline, 2377 = the `got:` rendering.)

That is a **self-contradictory failure record**: the text the check demands is printed in the
same `$out` the check searched (`got:` is rendered from `$out` at census `:2377`).

What I ruled out, by measurement:

- **`pipefail` + `printf | grep -q` SIGPIPE (fail-closed) — real hazard, wrong size class here.**
  The pipeline shape at census `:2372` runs under `set -euo pipefail` (`:452`); an early match
  with a large tail makes `printf` die of SIGPIPE and the pipeline read 141, which the `|| miss=`
  branch logs as a missing pattern *though grep matched* (the file's own round-42 note at `:726`
  records the same trap elsewhere). Measured boundary (`TExecCounterB/tests/pipe-boundary-result.txt`):
  fail 0/10 up to 60 KiB tail, 1/10 at 63 KiB, 7/10 at 64 KiB, 9/10 at 80 KiB, 10/10 at ≥128 KiB.
  But instrumented length tracing of the failing case shows its `$out` is **2 417 bytes** (max
  over all `check` calls in that scenario is 2 732 B; `probe2-len-trace.txt`), so this
  mechanism cannot explain it.
- **Small-input pipeline flakiness under load**: 20 000 consecutive iterations of the exact
  pipeline on a 2.4 KB `$out` at fleet load 18.8 → `nonzero=0` (receipt re-run of the same
  shape; the census-shaped input is in `TExecCounterB/tests/`).
- **Ambient and niceness**: six instrumented reruns over the `spaced`+`unset` envs (probe at
  no-nice load 69.8/73.5, probe+nice at 56.8/46.9, probe2 at 33.6/26.7) all returned `PASS (166
  cases, 166 passed, 0 failed)` (`probe-instrumented-summary.txt`, `probe-nice-summary.txt`,
  `probe2-len-summary.txt`) — two of them under *higher* load than the failing run.
- **MISS hunt**: `hunt.sh` drives the counter's `spaced` child env at nice 10 through the frozen
  census with a copy that records `PIPESTATUS`, a replay rc and dumps `$out` on any miss.
  **6/6 attempts passed** (`hunt-attempts.txt`: `attempt=1..6 rc=0 … PASS (166 cases,
  166 passed, 0 failed)`, MISS count 0, no `$out` dump).

Run tally across every scenario run I executed (each row = one `TSUKUROI_CENSUS_SELFTEST`
invocation under the counter's own child env):

| driver | scenario runs | failures | failing legs |
|---|---|---|---|
| counter (the item's one run) | 4 (unset, tmp, scratch, spaced) | **2** | unset (2 cases), spaced (1 case) |
| diag (manual replay, frozen census) | 2 (unset, spaced) | **1** | spaced (1 case) |
| probe (instrumented, no nice) | 2 | 0 | — |
| probe + nice 10 | 2 | 0 | — |
| probe2 (len tracing, nice 10) | 2 | 0 | — |
| hunt (nice 10, 6 attempts) | 6 | 0 | — |
| **total** | **18** | **3** | |

The three failures cluster in 09:00:03-09:06:27 (fleet load 44-56; at 09:03:27 pgrep showed six sibling `tsukuroi-census.sh --selftest`
processes plus four sibling counter drivers); the 15 later runs, at load 12-73, were clean. Failure rate is therefore ~17 % per
scenario run and zero once the fleet's peak concurrency passed — which is the operational risk
below, and also why the one permitted counter run could legitimately come back red.

**Independent corroboration that single-case selftest failures are a class, not my error:**

- `w2/TExecStrace.md:15-17` — one strace-slowed `spaced` run: `FAIL (166 cases, 165 passed, 1
  failed)`, label `hostname override not honoured — possible host read`, while both un-straced
  controls passed 166/166 in the same seat.
- `w2/TExecParallel.md:80` — concurrent run A3: `FAIL (166 cases, 165 passed, 1 failed)` on a
  host-source assertion that did not reproduce when the same TMPDIR was rerun solo.

Both are the same failure *shape* as mine (one or two evidence assertions flip inside an
otherwise 166/166-clean selftest) with a different label, in seats that did not touch my ambient.

## 6. Risks / blockers

- **The frozen C1 counter is load-sensitive as an instrument.** `pass_ok == 4` can read 2 on the
  frozen bytes with no code difference; the predicate therefore cannot certify C1 in one run
  while other seats run selftests. A counted verdict taken from a single counter run is
  coin-flippable; replicate runs disagree (A PASS, B FAIL) inside the same window.
- **The failure is not post-hoc diagnosable from the receipt.** The counter discards child
  stdout/stderr and removes `work`, so a red run cannot be attributed after the fact. Minimal
  instrument fix (not applied — lane bytes are not mine to edit): keep the child's stdout and
  the count of `FAIL` lines in the counter's JSON, and keep `work` on FAIL.
- The remaining unexplained step is mechanical: how a `check` whose `$out` is ~2.4 KB and whose
  demanded text is present can register a miss. Candidates not yet separated: a transient error
  exit from `grep` itself under fork/memory pressure (would also explain the sibling seats'
  `hostname override` variant, since that clause is a sibling pipeline at census `:2357`), and
  mid-line interleaving of the census child's own output. Both need a captured failing `$out`;
  my instrumented copy (`probe2-census.sh`, sha differs deliberately from the frozen blob) is the
  tool for that and is *not* the bytes under test. **[INFERENCE]** for the mechanism; the
  divergence itself is measured, not inferred.

Not done (stated so it is not mistaken for passed): no second counter run (item budget: one);
no lane edits; no removal of the pre-existing `/tmp/tsukuroi-r3-2-selftest.qMuipK` or sibling
fixtures (other seats' state); no verdict on the C2/C3 claims.

## 7. Evidence index

- `.ufo/waves/round-48/w2/TExecCounterB/counter.json` — the run's single JSON line.
- `…/TExecCounterB/run-status.txt` — `rc=1 … dur=228`.
- `…/TExecCounterB/mktemplogs/{unset,tmp,scratch,spaced}.mktemp.log` — fixture paths per leg.
- `…/TExecCounterB/tmp-listing-pre-run.txt` — `/tmp` snapshot (3 287 entries) before the run.
- `…/TExecCounterB/diag-summary.txt`, `diag-spaced-fail.txt` — independent replay, label recovered.
- `…/TExecCounterB/probe-instrumented-summary.txt`, `probe-nice-summary.txt`,
  `probe2-len-summary.txt`, `probe2-len-trace.txt` — reruns and `$out` length distribution.
- `…/TExecCounterB/hunt-attempts.txt` — MISS-hunt attempts.
- `…/TExecCounterB/tests/pipe-boundary-result.txt` — 64 KiB SIGPIPE/pipefail boundary
  measurement, `pipe-boundary-test.sh` beside it (re-runnable; no lane bytes touched).
- `…/TExecCounterB/drivers/` — `run-b.sh` (the item's command, minus `/usr/bin/time`), `diag.sh`,
  `probe.sh`, `probe-nice.sh`, `probe2.sh`, `hunt.sh`. Scratch was removed per the section-7
  directive; these copies plus the frozen blob re-create every run above. `probe2-census.sh` (the
  instrumented census, sha differs from the frozen blob on purpose) was deleted with the scratch
  and is regenerated by adding, after `rc=$?` in `check()`, a length tracer and, in the `*)`
  must-match branch, a `PIPESTATUS` + replay + `$out` dump tracer — it is never the bytes under
  test.
