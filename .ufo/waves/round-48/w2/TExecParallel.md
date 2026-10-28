VERDICT: supports

# C1-X11 — concurrency of the `selftest_base_dir` /proc/self/fd alias

**Answer.** Concurrent `--selftest` runs do not interfere through the alias: the fd is
per-process, so three runs under three different space-bearing TMPDIRs each opened their own
`fd 240`, each created exactly one fixture inside **its own** TMPDIR, and each removed it. Two
runs sharing **one** spaced TMPDIR also passed with distinct fixture trees and no collision.
Across 9 concurrent-run samples there was **zero alias cross-talk**; one run (A3) failed a
single *host-source read* assertion, which is not on the alias path and did not reproduce when
the same TMPDIR was re-run solo.

## 1. Bytes under test (identity)

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show \
    ae99f021b76f8eb1c8805d32d80644464afb1ff6:tools/tsukuroi-census.sh > census.sh
375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426  census.sh
3718 census.sh
```

Matches the frozen blob in the round declaration
(`375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`). All runs used this
extracted copy; the lane working tree was never read for bytes and never written.

Mechanism under test (`census.sh`, frozen blob):

- `census.sh:2058` `selftest_base_dir()`; `:2074` `base=${TMPDIR:-/tmp}`;
  `:2079-2086` picks the first free fd in 240..249 and `eval "exec ${fdn}<\"\$base\""`,
  sets `ST_BASE_DIR=/proc/self/fd/$fdn`;
- `census.sh:2106` `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")`;
- `census.sh:2109-2111` EXIT/INT/TERM traps removing `$work`.
- `TMPDIR` has **no other behavioural use** in the file:

```
$ grep -n 'TMPDIR' census.sh | grep -v '^[0-9]*: *#'
2074:  base=${TMPDIR:-/tmp}
2102:    printf 'selftest: TMPDIR <%s> cannot host the fixture tree (no /tmp fallback, R48-C2)\n' ...
3540:  TMPDIR="$r48_dir" selftest_base_dir; r48_rc=$?        # per-run $work/fx/dirty tmpdir
3550:  if TMPDIR="$work/fx/definitely missing dir" selftest_base_dir; then
```
(lines 3526/3527/3545/3547/3552/3554 are `ok`/`bad` message strings and comments)

No live code scans TMPDIR, so the only shared thing two concurrent runs can touch is the
*directory* itself, never a name inside it (mktemp `XXXXXX` is `O_EXCL`).

Nested-call safety: the selftest calls `selftest_base_dir` again at `:3540` while 240 is
already held by the outer alias; the probe loop breaks on the first *free* fd, so the nested
call lands on 241, and no assertion pins a specific fd number — only `[ -n "$r48_fd" ]` and a
`readlink -f` match (`:3542-3548`). Confirmed by the very fact that all 166 cases pass under a
spaced TMPDIR in the runs below.

## 2. Harness

Fixture location is read from **what the harness did** — a PATH-shadowing `mktemp` wrapper that
logs `"$*"`, the result and `readlink -f` of the result — exactly the counter's method
(`tools/score-selftest-tmpdir-r48.py`, `WRAPPER`/`scenario()`), not from census text. Each run:
`env -i`-equivalent dict `PATH=<own wrap dir>:/usr/bin:/bin LC_ALL=C TMPDIR=<dir>
MKTEMP_LOG=<own log>`, `bash census.sh --selftest`, distinct output files. Wrapper inheritance
smoke (before the real runs; proves fd 240 survives `exec` into the wrapper child):

```
ST_BASE_DIR=/proc/self/fd/240
-d /proc/self/fd/240/tsukuroi-r3-2-selftest.XXXXXX  /proc/self/fd/240/tsukuroi-r3-2-selftest.5XnOgI  /fast/scratch/.../p one/tsukuroi-r3-2-selftest.5XnOgI
```

TMPDIRs: `<S>/p one`, `<S>/p two`, `<S>/p three` (`<S>` =
`/fast/scratch/hyaku/tsukuroi-r48/TExecParallel`, removed at end). Host context at launch
(`host-at-launch.txt`): `08:59:23 up 1 day 20:50, load average: 31.42, 27.77, 30.66`,
30 GiB RAM with 12 GiB available, 32 CPUs, 5661 processes — i.e. the whole fleet was loaded.

## 3. Phase A — three concurrent, three different spaced TMPDIRs

Three started together, wall 58.7 s each (`result.json`):

| run | TMPDIR | rc | last line | fd | fixture resolved | parent = own TMPDIR | removed | dir after |
|---|---|---|---|---|---|---|---|---|
| A1 | `p one` | 0 | `PASS (166 cases, 166 passed, 0 failed)` | 240 | `.../p one/tsukuroi-r3-2-selftest.RGw7BH` | yes | yes | empty |
| A2 | `p two` | 0 | `PASS (166 cases, 166 passed, 0 failed)` | 240 | `.../p two/tsukuroi-r3-2-selftest.Jvi2SN` | yes | yes | empty |
| A3 | `p three` | **1** | `FAIL (166 cases, 165 passed, 1 failed)` | 240 | `.../p three/tsukuroi-r3-2-selftest.C1GK8o` | yes | yes | empty |

Every run logged **exactly one** creation (`creations=1`), no run's log contains another run's
path, and the three resolved paths are pairwise distinct. A3's alias behaviour was identical to
the passing runs (fd 240, own directory, one fixture, removed).

A3's one failure, verbatim (`logs/run-A3/stderr.txt`):

```
FAIL blocked: C1 root arm — dangling symlink is unavailable, not a pass (R12-C1): hostname override not honoured — possible host read
```

That is `census.sh:2356`, reached because the census output for case
`blocked-root-dangling` (`census.sh:3010`) did not contain `host=fixture-host`; `rc` and the
`PLANE packages:` line still matched, so the census ran to completion. The asserted value comes
from `census.sh:3647-3649`:

```
host=$(head -n1 "$HOSTNAME_FILE" 2>/dev/null | tr -d '\r' || true)
host=${host:-unknown}
```

which is printed *before* any probe; `TSUKUROI_HOSTNAME_FILE="$FX/hostname"` is passed by the
harness at `:2333` and the fixture writes `fixture-host` at `:2245`. Nothing in that path reads
TMPDIR, the alias, or any shared file — it is a read of a per-run fixture through `/proc/self/fd/240`.

### Attribution of A3 (what I measured)

- **Same directory, solo** (`logs/run-solo`): `rc=0`, `PASS (166 cases, 166 passed, 0 failed)`,
  fd 240, `.../p three/tsukuroi-r3-2-selftest.AHK3tq`, removed, dir empty. So neither `p three`
  nor the alias state is at fault.
- **3-concurrent, second sample** (A1b/A2b/A3b, wall 88.5 s): 3/3 `PASS (166 cases, 166 passed,
  0 failed)`, all TMPDIRs empty afterwards. This sample's wrapper directory was not created, so
  it carries no location log; it is pass/cleanup evidence only.
- **3-concurrent, third sample** with logging (A1c/A2c/A3c, wall 59.5 s): 3/3 `PASS`, each
  `fd=240`, `creations=1`, `parent_is_own_tmpdir=true`, `fixture_removed=true`, distinct paths.
- **Fork/exec failure probe**: the only way the `:3647` line can lose `fixture-host` is a failed
  or empty `head`/`tr`. Three workers × 2000 iterations of the exact pipeline under the same
  load: `worker1/2/3 total=2000 empty=0`, captured stderr 0 bytes — no fork/exec failure
  observed in 6000 invocations (`probe-fork.log`).

Conclusion on attribution: the failure is **not** alias cross-talk (A3's alias state and fixture
location were correct, and the same directory passed solo), and it is **not** reproducible by me
in 8 further concurrent runs or in a 6000-call fork probe. I did not capture the census's actual
`host=` value for that case: the `bad` branch discards `$out`. A behaviour-neutral diagnostic
copy is deposited for the L1 — `census-diag.sh`, sha256
`4e8c5e5e1ce90133cf3448023fb932f30ae2fd23cb0cfc7bce8c1e51a4b3df59`, identical to the frozen
blob except for three lines added inside that failure branch (`:2356-2358`) that append `$out`
to `$TSUKUROI_SELFTEST_DIAG`; it never triggered in my runs. **It is an instrument, not the
bytes under test — never cite it as the blob.**

## 4. Phase B — two concurrent sharing ONE spaced TMPDIR

Both under `<S>/p one`, started together, wall 56.6 s each:

| run | rc | last line | fd | fixture resolved real path | removed | dir after |
|---|---|---|---|---|---|---|
| B1 | 0 | `PASS (166 cases, 166 passed, 0 failed)` | 240 | `.../p one/tsukuroi-r3-2-selftest.Mxj2ee` | yes | empty |
| B2 | 0 | `PASS (166 cases, 166 passed, 0 failed)` | 240 | `.../p one/tsukuroi-r3-2-selftest.y6aZ7U` | yes | empty |

Distinct fixture names, exactly one creation each, both trees removed, no collision; `readlink -f`
shows both aliases resolved into the same shared directory while naming disjoint subtrees.
Both runs independently binding `fd 240` onto the same directory is the direct demonstration that
the descriptor is per-process state: had it been host-global, the second bind would have failed
(`selftest_base_dir` returns 1 only when *its own* 240-249 band is occupied).

## 5. Cross-talk summary

- 0 of 9 concurrent runs' logs contained another run's fixture path.
- 0 runs observed more or one fewer than one fixture creation.
- All TMPDIRs (`p one`, `p two`, `p three`) were empty after every phase
  (`ENV.txt`: `p one -> 0 entries`, `p two -> 0`, `p three -> 0`).
- `/tmp`: I did not attribute anything to `/tmp`. `result.json` `tmp_pre` had 6
  `tsukuroi-r3-2-selftest.*` entries and `tmp_post` 4 (a different set): those are other seats'
  runs on this host (the host carried 100 background jobs / load 31). **None of my runs wrote
  `/tmp`** — every logged creation resolved under `/fast/scratch/...`, and my TMPDIRs were the
  spaced directories. The pre/post delta is fleet noise, not evidence of a `/tmp` fallback and not
  evidence of a leak by my runs.

## 6. Explicitly NOT done

- Did not run the frozen C1 counter (`tools/score-selftest-tmpdir-r48.py`) — other seats own the
  counted C1 verdict; my runs are observational samples, not counter legs.
- Did not exercise the `SIGTERM`/fail-fast legs concurrently.
- Did not test more than three simultaneous selftests (the item's one allowance), nor a
  shared-TMPDIR pair under TERM.
- Did not reproduce A3's host-read failure, and did not capture its `host=` value (see §3).

## 7. Risk / finding for the L1

A3 is an honest negative on **repeatability under 3-way concurrency**: 1 of 9 concurrent full
selftests failed one assertion, non-alias, non-reproducible in isolation, and its failure message
discards the evidence needed to classify it. If C1's `pass_ok == 4` predicate is ever executed
under comparable host load, this is a plausible source of a spurious FAIL whose text
("hostname override not honoured — possible host read") would be misread as a real host-read
defect. Minimal hardening worth considering (not implemented here — lane is read-only for me):
make `:2355` report the observed `host=` value, as the neighbouring branches already do
(`:2360`, `:2362` print their `got:` tail).

## 8. Scratch / tooling

Scratch `/fast/scratch/hyaku/tsukuroi-r48/TExecParallel` removed after receipts were copied
(`ls` → No such file or directory). No tool installed or upgraded; `pacman` untouched. Nothing
written outside the wave directory and the scratch dir.

Receipts: `.ufo/waves/round-48/w2/TExecParallel/` — `result.json` (phase A+B), `result-repeat.json`
(sample 3), `logs/run-{A1,A2,A3,B1,B2,A1c,A2c,A3c,solo}/{stdout,stderr,mktemp}.…`,
`host-at-launch.txt`, `smoke.log`, `probe-fork.log`, `ENV.txt`, `driver.py`, `driver2.py`,
`census-diag.sh` (instrument, distinct sha256).
