VERDICT: defect-found

Item C1-11 — security/scope review of `tools/score-selftest-literals-r40.py` at
c707e356c2911646f7304d706eb77d118e510610. The assigned write-scope property HOLDS: the counter created,
truncated, renamed or unlinked nothing outside `--scratch` and its census copies reached no host path.
Two low-severity defects and one scope note are recorded below, plus one unreproduced control flake.
Receipts: `.ufo/waves/round-40/w1/C1SentScratch/` (`counter-out.json`, `evidence.txt`). Scratch
`/fast/scratch/hyaku/tsukuroi-r40/C1SentScratch/` was removed after the receipts were copied. `strace 7.2`
was already installed at `/usr/bin/strace`; nothing was installed or upgraded, so no channel entry applies.

## 1. Provenance and the run I traced

- Counter sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159` == the declaration's
  frozen hash (command and output in `evidence.txt` §1). The reviewed artifact is the declared one.
- Census at the implementation commit: `git show c707e35:tools/tsukuroi-census.sh`, 3149 lines, sha256
  `032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733`.
- Run (exactly the assigned shape, plus the `*at`/`unlinkat` variants of the same operations):
  `strace -f -e trace=openat,mkdir,unlink,rename,execve,unlinkat,renameat,renameat2 -o trace --
  python3 tools/score-selftest-literals-r40.py --revision c707e35… --scratch <S>/work --jobs 2`
  → `exit=0`; 4,924,626 trace lines / 454 MB; 412,781 `execve`. Receipt: baseline
  `TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)`, `neutral_pass 3`,
  `mutants_applied 9`, `survivors 0`, `selfref 5`, `result PASS` (`counter-out.json`).

## 2. Every path written outside `--scratch`: none

From the 13-variant trace (`evidence.txt` §3):

- `openat` with `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC|O_APPEND` whose path is not under the scratch root and that
  succeeded: only `/dev/null` (20,770 `O_RDWR`, 8 `O_RDWR|O_CLOEXEC`). **Zero** `O_CREAT`/`O_TRUNC` opens of a
  real file outside scratch.
- Absolute `mkdir` outside scratch: none that succeeded — the only hits are the component-walk probes of
  `mkdir -p` (`mkdir("/fast", 0777) = -1 EEXIST`) before `chdir` into the target under scratch; all following
  components are cwd-relative.
- Absolute `unlink`, `unlinkat(AT_FDCWD, …)` outside scratch: 0. `rename`/`renameat`/`renameat2`: 0 total.
- Cross-checked with a second trace of one complete selftest that also records `chdir`, `symlinkat`, `linkat`,
  `rmdir`, `creat` (`trace3`, 406,909 lines, `LC_ALL=C`, `/usr/bin/bash`, cwd `/`): every creating op resolves
  under `…/st4/tmp/tsukuroi-r3-2-selftest.*`; all 12 `symlinkat` links land in `<work>/bin/<cmd>`; every
  host-tool path argument (`mkdir -p`, `ln -s`, `chmod`, `touch`, `mv`, `mkfifo`, `find`, `sha256sum`) is under
  scratch, e.g. `mkdir -p <S>/st4/tmp/tsukuroi-r3-2-selftest.Psg84r/{bin,fx}`.
- One embedded host-absolute string exists but creates nothing outside: `ln -s /nonexistent-r35
  "$FX/etc/a/l.pacnew"` (`tools/tsukuroi-census.sh:2887` at c707e35). The link is created inside the fixture;
  `/nonexistent-r35` is a dangling target that is never created and never followed.
- Success cleanup: after `exit=0`, `find <S>/work` is empty (the `r40c1.*` dir is gone) and the census's own
  `tsukuroi-r3-2-selftest.*` dirs under `TMPDIR` are gone.

## 3. Every `execve` (13-variant run)

All out-of-scratch executables are `/usr/bin` tools; counts in `evidence.txt` §5: awk 45856, bash 49777,
cat 84145, chmod 1768, comm 52, cut 4628, date 3107, env 3159, find 11011, **git 9**, grep 52637, head 24713,
id 104, ln 156, mkdir 6578, mkfifo 13, mktemp 13, mv 26, paste 3250, python3 1, rm 52, sed 19630,
sha256sum 6292, sort 7865, stat 10530, tail 5986, touch 26, tr 18500, **vercmp 26**, wc 4719.
`pacman`, `pacman-conf`, `systemctl`, `dmesg`, `journalctl`, `nvidia-smi`, `lsmod`, `expac` are executed only
from their scratch stubs (104 distinct scratch paths). `git` is read-only — `rev-parse`, `cat-file`,
`merge-base`, `show`, `check-ref-format` — and no `O_CREAT` occurred under the lane's `.git`. `vercmp` is
called with argv `("1.0-1","1.1-1")` only (no file argument), so it reads nothing.

## 4. Mutated census copies cannot reach host paths

- Both traces: **0** opens of `/proc/self/mounts`, `/proc/mounts`, `/sys/fs/btrfs`, `/var/lib/pacman`,
  `/etc/pacman.conf`, `/var/log/pacman.log` (`evidence.txt` §6).
- The reads that do occur belong to stock runtime, not to a census arm: `/etc/ld.so.cache`, `/etc/passwd`,
  `/etc/nsswitch.conf`, `/etc/localtime`, `/proc/self/maps` (52,638), `/proc/self/cgroup` and
  `/sys/fs/cgroup/…/cpu.max` (7,865 each; attributed to `/usr/bin/sort`'s thread-pool sizing),
  `/proc/sys/vm/overcommit_memory` ×1.
- No `TSUKUROI_*` override escapes. The child environment is a literal dict —
  `tools/score-selftest-literals-r40.py:98` `env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(d),
  'TMPDIR': str(tmp)}` — passed to `subprocess.run(..., cwd='/', env=env, …)` at `:100`. Probe (direct call of
  `run_selftest` with a census that dumps its own env, with ambient `TSUKUROI_PROC_MOUNTS=/etc/passwd`,
  `TSUKUROI_BTRFS_SYSFS=/sys/fs/btrfs`, `TSUKUROI_ROOT_DIR=/` set in the parent): child env = 7 vars
  (PATH, LC_ALL, HOME, TMPDIR + bash's PWD/SHLVL/_), zero `TSUKUROI_*`, poisoned values absent.
- Inside the selftest, `check()` pins 27 `TSUKUROI_*` to fixture paths
  (`tools/tsukuroi-census.sh:2141-2167`); the only arms admitted without them are `check_cli`'s three cases
  (unknown argument, `--sample 0`, `--help`), which exit before any probe — consistent with §4's zero
  host-path opens.

## 5. Defect 1 (low, diagnostics): `first_fails` is structurally always empty

`run_selftest` reads only stdout (`…r40.py:100` `capture_output=True`; `:105-108` builds `first_fails` from
`p.stdout`), while the census prints failures to stderr: `tools/tsukuroi-census.sh:2019`
`bad() { FAIL=$((FAIL + 1)); printf 'FAIL %s\n' "$*" >&2; }`. Consequence: all nine killed mutants in the
committed receipt carry `"first_fails": []` (`counter-out.json`), so the receipt cannot say *why* a mutant died —
the reader must re-run to see the failing case. Smallest remediation (two lines):

```python
    fails = [l for l in (p.stdout + p.stderr).decode('utf-8', 'replace').splitlines()
             if l.startswith('FAIL ')][:3]
```
(replace the `p.stdout`-only construction at `:105-108`; the predicate is unaffected).

## 6. Defect 2 (low, robustness): Ctrl-C does not stop the batch; scratch outlives the signal

The executor is wrapped by `with` inside `try`, and cleanup is the `finally`
(`…r40.py:143-148`), so `ThreadPoolExecutor.__exit__ → shutdown(wait=True)` drains **every queued future**
before `shutil.rmtree(work, …)` runs. `cancel_futures` is not used and child processes are not signalled.

Measured (receipt `evidence.txt` §8): `timeout -s INT -k 240 8 python3 … --scratch <S>/kt2/work --jobs 2` →
`timeout_rc=124`, harness wall **238.50 s** for a run interrupted at t=8 s (≈230 s of post-Ctrl-C work), exit
via `KeyboardInterrupt` at `…r40.py:145` (`for f in concurrent.futures.as_completed(futs)`). With `--jobs 1`
the same test did not finish inside 240 s. Answer to the assigned question: **the scratch is removed on success
and on KeyboardInterrupt**, but on interrupt only after the whole 13-variant batch drains; no orphan process and
no leftover directory remained afterwards (`find <S>/kt2/work` shows no `r40c1.*`; `pgrep` by my scratch path
empty). Direction is safe (it over-waits, it does not leak) and with the default `--jobs 4` the drain is ~13/4
selftests; worst case it is bounded by `--timeout 900` per queued variant.

Smallest remediation — keep the executor out of the `with` so the interrupt path can cancel:

```python
    ex = concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs))
    try:
        futs = {ex.submit(run_selftest, t, work / n, a.timeout): n for n, t in jobs.items()}
        for f in concurrent.futures.as_completed(futs):
            res[futs[f]] = f.result()
    finally:
        ex.shutdown(wait=False, cancel_futures=True)
        shutil.rmtree(work, ignore_errors=True)
```
Residual after this change: a census copy already running finishes on its own and then unlinks a
now-removed `TMPDIR` (no-op, no writes outside scratch).

## 7. Note (low, scope): `--scratch` is not validated against `--repo`

`os.makedirs(a.scratch, exist_ok=True)` and `tempfile.mkdtemp(prefix='r40c1.', dir=a.scratch)` (`…r40.py:127-128`)
accept any writable path. The module docstring's "Read-only on the lane" therefore holds only because the
seats pass a `/fast/scratch/...` path; a caller who passed `--scratch` inside the lane would create (and later
delete) files there. The scratch itself is safe from sibling interference (`mkdtemp` is `O_EXCL`, 0700, and the
census copy is written inside it). Smallest remediation: refuse when `realpath(scratch)` is inside
`realpath(repo)` and require an absolute path — three lines in `main()` before `:127`.

## 8. Control noise observed, not reproduced

One direct selftest run (ambient `LANG=en_US.UTF-8`, no `LC_ALL`, under `strace -s 512`) returned
`TSUKUROI_CENSUS_SELFTEST: FAIL (124 cases, 123 passed, 1 failed)` on
`healthy: memory-pressure arm quiet (S7-2)`: "plane evidence missing: `guards=max/max oom\.group=0; r6 vocab:
oom-event-plane\.md §8`" — while the same run's captured evidence line visibly contains
`…; guards=max/max oom.group=0; r6 vocab: oom-event-plane.md §8)` (full line in
`C1SentScratch/evidence.txt` §10). Not reproduced in 8 further direct runs of the same census copy (3 ambient
UTF-8, 1 under `strace` with `LC_ALL=C`, 3 ambient UTF-8, 1 clean `env -i`), all 124/124; the counter's own 13
runs show no such noise. I therefore treat it as an unexplained one-off rather than a counter defect (direction
is fail-closed: a flake can only change PASS into FAIL), but if it recurs the suspect is the multibyte `§` token
in the evidence regex at `tools/tsukuroi-census.sh:2473` matched under a non-C locale.

## 9. What I did not do

Did not run the counter at the base revision (`before`) — pre-data controls were already scored; did not
attempt any out-of-scratch write as a test; did not mutate the host, the lane, the fleet repo or any sibling
lane; ran no `git` write command; installed nothing; spawned no agents. All reads of the lane were
`git show`/`git log`/`git status`/`git diff` (read-only) plus the frozen counter and census under review.
