VERDICT: defect-found

# C1-20 — safety review of tools/score-census-readers-r45.py and the six R45 cases

Seat C1SentSafety, round 45 / wave a2w1, attempt 2. Read-only review plus measurement in
`/fast/scratch/hyaku/tsukuroi-r45/C1SentSafety/` (removed at exit; receipts under
`.ufo/waves/round-45/a2w1/C1SentSafety/`). No tracked file in the lane, the fleet repo or the host was
modified; my one untracked lane footprint (a generated `tools/__pycache__/*.pyc` from an importlib call) was
removed again and is disclosed in the last section.

Subject under review: `tools/score-census-readers-r45.py`
sha256 `fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50` — matches the declaration
(`sha256sum` run 2026-10-27 00:24; the frozen file is what I reviewed).
Scored bytes used: census at REV `18389f44…` = `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`
(202,665 B) and at BASE `5bbd5ff5…` = `17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35`
(198,992 B), both via `git -C <lane> show <rev>:tools/tsukuroi-census.sh`.

Host: Linux 7.2.11-arch1-1, python 3.14.8, bash 5.x, strace 6.x; the measurements below ran under the
normal 60-seat load of this wave, so wall times are upper bounds of a quiet host.

## 1. Can it leave files or processes behind? (SIGKILL, ENOSPC, mutant-selftest timeout)

| Scenario (all exercised) | exit | stdout | files left under `--scratch` | processes left |
|---|---|---|---|---|
| normal completion (`--revision 18389f4`, killed nothing) | — | JSON line | none after `cleanup()`; TMPDIR empty (`ls -A t-rev` → empty) | none |
| ENOSPC (192 KiB tmpfs as `--scratch`, private `unshare -rm` mount) | **1** | **0 bytes** | none (`leftover_count=0`) | none |
| SIGTERM at 20 s (mid-run) | 143 | 0 bytes | `r45c1-2188885/` + `r45c1-2188885/tmp/` (2 empty dirs) | none at t+0.2 s |
| SIGKILL at 45 s (mid-selftest) | killed | 0 bytes | 964 KB, 19 entries (eq-S1..S5, census.sh, mut-S1.sh, tmp) | none sampled at t+0.0…2.5 s |
| `run()` timeout (2 s) on a hanging bash + background `sleep` grandchild | 124 | — | — | none (`hang.sh` scan of `/proc`: 0) |

Receipts: `sigterm-residue.txt`, `sigkill-residue.txt`, `enospc.err`, `cost.json`.

Observations behind the table:

- **SIGTERM deliberately does not signal the in-flight child.** `on_signal` (`:100-103`) calls `cleanup()`
  and exits 143; only `run()`'s timeout path calls `os.killpg` (`:119-125`). The live child (own session,
  `start_new_session=True` at `:115`) therefore keeps running while its TMPDIR is unlinked; it dies only on
  its next write to the closed stdout pipe (SIGPIPE), which is why the survivor scan at t+0.2 s was empty.
  The residue is the empty `WORK`/`tmp` pair: `shutil.rmtree(..., ignore_errors=True)` (`:97`) hit ENOTEMPTY
  on `tmp` while the child still had its `tsukuroi-r3-2-selftest.XXXXXX` dir there.
- **SIGKILL leaves the work tree** (`cleanup()` cannot run). Bound is the selftest peak measured in §4:
  **34.7 MB** (`du -sk` of TMPDIR, peak over a full 154-case selftest). The docstring only claims removal on
  "exit, SIGINT and SIGTERM" (`:45`), so SIGKILL residue is not a contradiction of the stated contract, but
  it is the only way to accumulate garbage in `--scratch` on this counter.
- **The timeout path is correct and reaps**: `killpg` + re-`communicate()` returned in 2.0 s, the bash child
  *and* the background grandchild were gone. Boundary worth knowing: `communicate()` after the kill has no
  second timeout (`:124`), so a grandchild that detached into its own session would hang the counter
  forever. `tools/tsukuroi-census.sh` contains no `setsid`, `nohup` or `disown`
  (`grep -n "setsid\|nohup\|disown" tools/tsukuroi-census.sh` → no output), so today's mutant selftests
  cannot reach that state; the guard is structural, not enforced.
- Worst-case service time is bounded only per child: 40 equivalence draws × 30 s + 7 selftest runs × 900 s
  + 600 s adjacency ≈ 8,100 s ≈ 2 h 15 min. No total deadline exists.

## 2. Does any write escape `--scratch`?

No, on every path I could observe. Static write sites are all inside `WORK = --scratch/r45c1-<pid>`
(`:196` draw input, `:202` unlink of `out`, `:231-237` WORK/tmp, `:268` `eq-<site>` dirs, `:305` `mut-<site>.sh`);
the only write outside WORK is `os.makedirs(--scratch)` itself (`:230`).

- Children get `TMPDIR=WORK/tmp` and every `TSUKUROI_*`/`UFO_*` variable is stripped (`child_env`, `:105-110`),
  so a stray fixture env cannot steer a child census; the selftest and every mutant run with `cwd=WORK/tmp`
  (`:209`), and the census's own `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX"` therefore lands
  in scratch. The selftest copy is `WORK/census.sh` (`:284-286`), so child censuses never execute the lane file.
- **Full census selftest at REV under `strace -f`** (`-e trace=openat,mkdir,mkdirat,unlink,unlinkat,rename,renameat`,
  TMPDIR and cwd inside scratch): 376,707 trace lines, `PASS (154 cases, 154 passed, 0 failed)`, and the
  write-mode opens split **11,703 under `--scratch`** vs **12,008 `/dev/null`**, with **0** anywhere else.
  Non-scratch absolute targets of `mkdir`/`unlink`/`rename`: **0**. TMPDIR empty after the run.
  Receipt `selftest-writes.txt`.
- The 184 distinct *relative* `mkdir("name")` calls in that log are not escapes: GNU `mkdir -p` walks its
  absolute template by successive `chdir` + relative `mkdir`, starting at `/` and descending the scratch path.
  Direct evidence in `mkdir-p-chdir.txt` (execve of `mkdir -p /fast/scratch/…/tsukuroi-r3-2-selftest.CDsF3b/{bin,fx}`
  followed by `chdir("/fast") … chdir("t-probe") … chdir("tsukuroi-r3-2-selftest.CDsF3b")`, then `mkdir("bin")`).
- `git()` (`:128-130`) runs `git -C <lane> show/cat-file`; a straced `git show REV:tools/tsukuroi-census.sh`
  shows 25 traced calls, no write-mode open, no mkdir/unlink/rename (`git.strace`).

## 3. Does the adjacency checker write anything?

**No.** `tools/check-adjacency-anchors.py --revision 18389f4` run under
`strace -f -e trace=openat,mkdir,mkdirat,unlink,unlinkat,rename,renameat,symlink,link` with `TMPDIR` in
scratch and cwd in scratch: exit 0, `"status": "PASS"`, 2,207 trace lines, **148 write-mode opens, all
`/dev/null`**, **0** `mkdir`/`unlink`/`rename`/`symlink`/`link`, **0** write-mode opens under
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; `TMPDIR` and cwd empty after the run.
Receipts `adj.strace`, `adjacency-writes.txt`.

Why that holds: `check-adjacency-anchors.py` sets `sys.dont_write_bytecode = True` before
`from _revision import …` (line 12-18), its only file writes are inside
`tempfile.TemporaryDirectory(prefix="check-adjacency-anchors-")` in its own selftest mode (line 968-981), and
`_revision.bind()` uses only `rev-parse`/`cat-file`/`merge-base`/`check-ref-format` (`tools/_revision.py:172-195`).
Note `:321` invokes it with `cwd=None`, i.e. the caller's cwd is inherited — harmless today because the tool
writes nothing relative, but it is the one path a future edit could turn into a cwd write.

## 4. Cost of the six `(R45-C1)` cases

Measured by re-running the scored census bytes with a timing line injected into a scratch copy of `check()`
(the lane copy untouched); REV vs BASE, same host, same load:

| | cases | first case → summary | peak `du` of TMPDIR |
|---|---|---|---|
| `18389f4` (REV) | 154 PASS | **58.34 s** | **34,672 KB** |
| `5bbd5ff5` (BASE) | 148 PASS | **45.82 s** | 32,384 KB |
| delta | +6 cases | **+12.51 s** | +2.3 MB (+7 %) |

Per-case duration (REV, start→next start):

- `degraded: a large is-system-running…` 0.342 s
- `degraded: a large timer Result…` 0.319 s
- `healthy: a large nvidia-smi…` 0.332 s
- `blocked: a large is-active…` 0.294 s
- `degraded: a large timer ActiveState…` 0.319 s
- `degraded: a foreign baseline past the pipe buffer…` **8.205 s** (last start → summary line)

The foreign-baseline case carries almost all of it, and its cost is the 2016-awk lookup ladder, not the
150 KB padding: the case's live `CAP_OUT` has 2016 rows and `probe_packages` spawns one
`printf … | awk -v n="$nm" …` per row, each scanning the whole 2016-row baseline
(`tools/tsukuroi-census.sh:777`). Standalone reproduction with the case's exact shapes:
2016 lookups over an 88,384-byte baseline = **6.381 s**, `known=2015 drift=1`
(`awk2016/`, `cost.json`). The five padding cases are as cheap as an average case (0.29–0.34 s), so the
"150 KB × cases" worry is a non-issue; the quadratic-ish lookup ladder is the cost.

Counter-level impact: the counter runs **7** selftest invocations (1 REV + 6 revert mutants, `:287` and `:296`),
each paying the full case list → **≈ +88 s per counter run** (upper bound: the S6 mutant's early-exit lookup
ladder aborts the 2016-row loop sooner), i.e. **≈ +21 %** on the declared 6–7 min, and up to **14,112** extra
process spawns. Disk is immaterial (+2.3 MB peak, 595 GB free on `/fast`).

## Findings

### F1 — ENOSPC (or any write/read `OSError`) exits 1 with a traceback and no JSON line, against the tool's own contract (severity: low-medium)

**Exploit path.** Disk full (or a full/vanished `--scratch`) while `eval_stmt` opens a draw file (`:196`,
`:201`) or while writing `mut-*.sh` (`:305`). `score()` raises `OSError`, `main`'s `finally: cleanup()` runs
(`:238-240`), and the traceback reaches the interpreter: **exit 1, 0 bytes on stdout**.
Contract at `:45`: "exit 0 PASS, 1 FAIL, 2 usage/read/harness error".

**Evidence.** `unshare -rm` + 192 KiB tmpfs as `--scratch`, counter at `18389f4`:
`counter_rc=1 elapsed_ms=261`, `stdout_bytes=0`, stderr ends
`File ".../score-census-readers-r45.py", line 196, in eval_stmt … OSError: [Errno 28] No space left on device`,
work tree removed (`leftover_count=0`). Receipt `enospc.err`, `enospc.out` (empty).

**Impact.** A host I/O fault is indistinguishable from a genuine FAIL by exit code, and the caller has no
machine-readable line to see why. This is not theoretical for the wave: the pre-data battery treats a
non-JSON stdout as `json.dumps({'error': stderr[-300:]})` (`.ufo/waves/round-45/controls/run_controls_c1.py:129-130`)
and then `res.setdefault('verdict', 'FAIL')` (`:157`), while the accept counters only compare
`res.get('verdict')` with the expected verdict (`:166-168`). An ENOSPC during a control that is *supposed* to
FAIL therefore lands as `verdict: FAIL` and increments `should_fail_accepted` — a host problem recorded as a
control pass. (`error` is written into `C1-<k>.jsonl`, so the fault is recoverable by a careful reader, but the
accept/fail arithmetic does not look at it.)

**Smallest remediation (counter, no behavioural change on a healthy host).** Turn the harness fault into the
documented exit code, keeping `cleanup()`:

```python
    try:
        return score(a, rev, tmp)
    except OSError as exc:
        print(json.dumps({'error': f'harness I/O failure: {exc}'}))
        return 2
    finally:
        cleanup()
```
Optional second line of defence in the battery: treat `res.get('error')` or `exit == 2` as a harness error,
not as an accepted FAIL.

### F2 — SIGINT/SIGTERM clean the files but never signal the live child; residue and an orphan window (severity: low)

**Exploit path.** `on_signal` (`:100-103`) → `cleanup()` → `sys.exit(128+n)`. The in-flight child (own
session) is left running; `cleanup()` races it, `rmtree(ignore_errors=True)` hits ENOTEMPTY, and the child
writes into an unlinked TMPDIR until its next stdout/stderr write kills it with SIGPIPE.

**Evidence.** SIGTERM at 20 s into a full run: `counter_rc=143`, stdout 0 bytes, residue
`r45c1-2188885/` + `r45c1-2188885/tmp/` (both empty), no child at t+0.2 s. Receipt `sigterm-residue.txt`.
The SIGKILL run shows the same child-alive-at-kill state (`sigkill-residue.txt`: live
`bash …/census.sh --selftest`, ppid = counter, at the kill instant).

**Impact.** Two empty directories per aborted run, and an orphan that can outlive the counter by up to one
case duration (the foreign-baseline case takes 8.2 s and writes nothing until it completes). Nothing lands
outside `--scratch`; no host state is touched.

**Smallest remediation.** Remember the live child and kill its group before deleting, e.g. a module-level
`ACTIVE = None` set in `run()` after `Popen` and cleared after `communicate()`, then in `on_signal`:
`if ACTIVE: os.killpg(ACTIVE, signal.SIGKILL)` before `cleanup()` (and the same in `cleanup()` so the
`finally` path is covered).

### F3 — SIGKILL leaves up to ~35 MB in `--scratch`, and the work tree is created with default permissions (severity: informational)

`os.makedirs(WORK)` (`:232`) carries no mode; with the host umask 0022 the tree is **0755** and `/fast/scratch`
is 0755, so the extracted candidate census, the six mutants and the draw inputs are world-readable while the
counter runs (single-user host: no exposure). `mktemp`, used by the census for its own work dir, gives 0700 —
the counter could match it with `os.makedirs(WORK, mode=0o700)` plus the `exist_ok` path unchanged. This is
hardening only; it does not affect any verdict.

## What I did not do

- No end-to-end full counter run of my own (other seats own the verdict); my runs were the real counter
  launched and terminated at chosen instants, and the selftest leg exercised standalone on the scored bytes.
- No detached-session (`setsid`) grandchild test: the claim that `communicate()` would then block forever is
  inference from `:129-131`, not an executed check; the census contains no detach (grep above).
- No analysis of the counter's *verdict* correctness (that is C1-13/C1-16/other seats), no root/privilege
  path, no network, no host mutation, no tool installation.

## Related observation (not this seat's surface)

The lane's `tools/__pycache__/` receives `.pyc` files whenever a seat imports a counter by `importlib` (the
chair's suggested pattern for single legs). During this wave:
`check-scrub-grounding-r45.cpython-314.pyc` appeared at 00:31:48 (not mine), and
`score-census-readers-r45.cpython-314.pyc` appeared at 00:25:49 **from my own importlib call**; I removed that
file again (`rm -f tools/__pycache__/score-census-readers-r45.cpython-314.pyc`, directory listing verified) and
report it here as my only footprint in the lane. The directory is gitignored (`.gitignore:2`), so this cannot
reach a commit, but seats that import tools should set `sys.dont_write_bytecode = True` before `exec_module`
(or export `PYTHONDONTWRITEBYTECODE=1`) to keep the lane directory untouched.

## Receipts

`.ufo/waves/round-45/a2w1/C1SentSafety/`: `adj.strace` (197,916 B), `adj.out`, `adjacency-writes.txt`,
`git.strace`, `selftest-writes.txt`, `mkdir-p-chdir.txt`, `rev-selftest.out`, `base-selftest.out`,
`timing-rev.tsv`, `timing-base.tsv`, `cost.json`, `sigterm-residue.txt`, `sigkill-residue.txt`,
`enospc.err`, `enospc.out`. All under 2 MB each; the 36 MB full selftest strace and the 22 MB probe trace
stay in scratch (summarised in the two `.txt` receipts). Scratch removed at exit.
