VERDICT: supports

C1-9 (determinism matrix of the frozen C1 counter at `c707e356c2911646f7304d706eb77d118e510610`).

# Scope actually run

Reproduced the frozen counter `tools/score-selftest-literals-r40.py` (sha256
`8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`, matching the declaration at
`SCORECARD.md:2303`) at revision `c707e356c2911646f7304d706eb77d118e510610`
(`git cat-file -t` = commit, `git merge-base --is-ancestor … master` succeeded, commit subject
"round-40: C1 census selftest varies mount-table literals (R39-FIXTURE-MONOCULTURE)").

Nine matrix cells (caller `cwd` × caller `LC_ALL` × `--jobs`) plus one repeat cell, all with `TMPDIR`
unset in the caller and `--scratch /fast/scratch/hyaku/tsukuroi-r40/C1ExecEnvMatrix/s`, driven by
`run_matrix.sh` (receipts dir, copied verbatim). Cell = one full counter run = 13 census selftests.

| cell | caller cwd | caller LC_ALL | --jobs | exit | wall s | result |
|---|---|---|---|---|---|---|
| cwd_root_C_j1 | `/` | C | 1 | 0 | 380 | PASS |
| cwd_root_C_j6 | `/` | C | 6 | 0 | 121 | PASS |
| cwd_root_enUS_j1 | `/` | en_US.UTF-8 | 1 | 0 | 298 | PASS |
| cwd_root_enUS_j6 | `/` | en_US.UTF-8 | 6 | 0 | 64 | PASS |
| cwd_scratch_C_j1 | `…/C1ExecEnvMatrix` | C | 1 | 0 | 258 | PASS |
| cwd_scratch_C_j6 | `…/C1ExecEnvMatrix` | C | 6 | 0 | 74 | PASS |
| cwd_scratch_enUS_j1 | `…/C1ExecEnvMatrix` | en_US.UTF-8 | 1 | 0 | 267 | PASS |
| cwd_scratch_enUS_j6 | `…/C1ExecEnvMatrix` | en_US.UTF-8 | 6 | 0 | 81 | PASS |
| repeat_cwd_root_C_j6 | `/` | C | 6 | 0 | 112 | PASS |

Every cell: `baseline_pass 1`, `neutral_pass 3`, `mutants_applied 9`, `survivors 0`,
`survivor_names []`, `selfref 5`, `exit 0`, and baseline last line

    TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)

(`matrix.log` in the receipts dir is the driver's transcript; the ten full JSON records are there too.)
Per-mutant killed-case counts are identical in all nine cells, read from each mutant's last line —
M1 2, M2 2, M3 1, M4 2, M5 1, M6 1, M7 1, M8 2, M9 2 failed cases — and N1/N2/N3 each exit 0 with
124/124. All nine `.err` files are 0 bytes.

Supplemental cell (not part of the requested matrix; tests the two environment knobs the counter is
supposed to neutralise): caller `TMPDIR=/tmp`, `TZ` unset, `--jobs 2`, cwd `/` → exit 0, PASS,
132 s, survivors 0, baseline 124/124. So a caller `TMPDIR` of `/tmp` neither moves nor perturbs any
write (see write locality below): the counter's child environment is a fixed dict
(`tools/score-selftest-literals-r40.py:98` `{'PATH','LC_ALL':'C','HOME','TMPDIR':<scratch>/tmp>`), the
child cwd is hard-coded `/` (`:100`), and the only directory the counter creates is
`tempfile.mkdtemp(prefix='r40c1.', dir=a.scratch)` (`:128`).

# Determinism result

The judged signature — `(result, survivors, neutral_pass, mutants_applied, selfref, baseline.last,
per-mutant occurrences/exit/last, per-neutral occurrences/exit/last)` — hashes to the same value,
`0ad7e8feeab6a5ba`, in all nine matrix cells, in the repeat cell, in the supplemental cell, **and in
the author receipt** `.ufo/waves/round-40/after/c1-after-c707e35.jsonl`. Nothing in the predicate
varied with cwd, caller locale or `--jobs`.

Byte level: the nine cell JSONs are 3249 bytes each; seven hash `a55161dc5f3c8f53…` and two
(`cwd_scratch_enUS_j6`, `repeat_cwd_root_C_j6`) hash `f70671a6bdee028c…`. A field diff of the two
variants shows exactly one differing line:

    4c4
    <     "branch_tip": "f951f288483c1af0cef4afd458488b84cf7a2165"
    ---
    >     "branch_tip": "d84e2aab555557606b2cf5a999929be45f1d4f44"

`branch_tip` is the informational `refs/heads/master` read at run time (`tools/_revision.py`,
`branch_tip`), not part of the predicate; the lane tip advanced `f951f288…` → `d84e2aab…` between cells 7 and 8 because a peer landed
work (`git log -1 d84e2aab` = 2026-10-26 04:39:30 -0300, "round-40: final self-assessment, sources
census and C2 receipts at e3bc934"). That is repo state, not counter nondeterminism — the
revision under test stayed bound to `c707e35…` (`bind()` refuses an unlanded revision, and no cell
took the `exit 2` could-not-evaluate path).

# Write locality (nothing outside the scratch)

From `matrix.log`, per cell: `leftover_workdirs=0` (the counter's `shutil.rmtree(work)` leaves no
`r40c1.*` behind) and `scratch_paths` constant at 4 before/after each cell; the only growth inside my
scratch was my own `logs/` (pruned from the count) and `census-c707e35.sh`, which I extracted myself
with `git show` ×1, mid-matrix — so the before/after counts differ by exactly that one file (3 → 4),
not by anything a run wrote.

`/tmp`: `find /tmp -maxdepth 2 -name 'r40c1.*'` was empty before and after the matrix (and after the
supplemental cell, where the same `find` returned no match but surfaced `Permission denied` on
root-owned `systemd-private-*` directories); `ls -1 /tmp` name diffs over both windows contain only
other seats' traffic (`base170.*`, `c3added.txt`, `manifest_table.md`, `p`, `revaddenda_*`, peers'
dotfiles appearing), and one *deletion* of a pre-existing `tsukuroi-r3-2-selftest.sjpAGd` — a
directory whose name matches the census's own `mktemp` template, so [INFERENCE] it was another seat's
`--selftest` that defaulted its `TMPDIR` to `/tmp` and cleaned up; no such directory was created during
my runs,
because the census writes only under `"${TMPDIR:-/tmp}"` (census line 1930) and the counter always
sets `TMPDIR` inside the scratch (`…-r40.py:98`). The raw `ls -la /tmp | wc -l` counter drifted
185→187 over the matrix window for that peer traffic, which is why the name diff, not the count, is
the evidence.

Lane: no lane file was written by me. Tracked content of the surface under test is unchanged —
`git show HEAD:tools/tsukuroi-census.sh`, `…:tools/score-selftest-literals-r40.py` and
`…:tools/check-exec-environment-r40.py` each hash to the same value as the worktree file
(`032faa8f…`, `8b06de18…`, `d4a2bb94…`). `find … -newermt` over my window shows 385 paths under
`.ufo/waves/round-40/w1/<seat>/` (peers' own reports), one `corpus/`/`SCORECARD.md`/`LOG.md` set whose
mtime moved inside the window (content not verified by me; [INFERENCE] the lane owner's jj operations
rewrite worktree files), and two **untracked** `.pyc` files dated 04:15
(`tools/__pycache__/score-selftest-literals-r40.cpython-314.pyc`,
`check-exec-environment-r40.cpython-314.pyc`) whose mtime predates my first matrix cell, and which
running a counter as `__main__` does not produce — [INFERENCE] a peer imported those counters; my
runs refreshed nothing (`_revision.cpython-314.pyc` is dated 01:11, before my work). I record these as
ambient, not as my writes.

# Nondeterminism found — in the census selftest's assertion idiom, not reachable by the matrix knobs

A real flake exists one level below the counter, and I hit it only by making the machine far slower
than any cell: an artificial heavy ptrace trace (`strace -f -y` over openat/creat/mkdir/unlink/rename/
symlink/link) of the census `--selftest`.

| run (census at `c707e35`, env identical to the counter's child env) | wall | last line | FAIL messages |
|---|---|---|---|
| `strace -f -qq -y -e trace=openat,creat,mkdir,mkdirat,unlink,unlinkat,rename,renameat2,symlink,link` | 181 s | `FAIL (124 cases, 121 passed, 3 failed)` | 3 × "hostname override not honoured" |
| same trace set, instrumented copy (`diag2`) | 44 s | `FAIL (124 cases, 123 passed, 1 failed)` | "blocked: pacman db.lck: hostname override not honoured" |
| same trace set + 8 CPU hogs, instrumented copy (`diag3`) | 880 s | `FAIL (124 cases, 123 passed, 1 failed)` | "healthy: privilege artifacts counted, not drift (D05): hostname override not honoured" |
| **untraced**, `env -i PATH=/usr/bin:/bin LC_ALL=C HOME TMPDIR=<scratch>/tmp`, cwd `/` | 40 s | `PASS (124 cases, 124 passed, 0 failed)` | none — 4/4 runs |

Mechanism, with receipts:

1. The census runs its selftest under `set -uo pipefail` (census `c707e35` line 1940) and every
   assertion is the pipeline `printf '%s\n' "$out" | grep -q PATTERN` (e.g. line 2175 for the
   hostname assertion).
2. `printf` emits a multi-line argument in several `write(1, …)` calls — traced for a 2453-byte
   argument: `write(1,…,34)`, `write(1,…,2401)`, `write(1,"host=fixture-host\n",18)` (`write_test.txt`).
3. The hostname assertion's pattern matches the **first** chunk, because the census header prints
   `host=` on line 1 (`census:3084-3085`, `printf 'tsukuroi-census %s — host=%s — %s — read-only\n'`).
   `grep -q` therefore exits while later chunks are still unwritten; the next `write` gets EPIPE,
   `printf` dies of SIGPIPE (141), and `pipefail` makes the whole pipeline 141 — which `elif ! …`
   reads as "assertion failed".
4. Direct evidence of step 3, from the instrumented copy that reports the status of the *same*
   pipeline (`diag3.out`): `HOSTCOND label=healthy: privilege artifacts counted, not drift (D05)
   pipeline_rc=141 bytes=2471`, against 120 sibling assertions with `pipeline_rc=0`. The dumped `$out`
   for the failing case **did contain** `host=fixture-host` (`diag2.out`), which is why the message is
   false.
5. Deterministic trigger for the same race: a 100 018-byte output (> pipe buffer) false-fails 3/3 with
   `pipefail` on and 0/3 with it off. At the real size (≈2.0-2.5 kB) it is a scheduling race: 0/3000
   false failures idle and 0/3000 under 8-CPU load in my micro-test, 0 in 14 508 case evaluations
   (9 cells × 13 selftests × 124 cases) across the nine matrix cells, but 1-3 per 124-case run once
   ptrace stretches each fork/exec.

Attribution: this is **not** counter nondeterminism and **not** reachable through caller `cwd`,
`LC_ALL`, `TMPDIR` or `--jobs` — the counter's child env and cwd are fixed (`…-r40.py:98,100`). It is
a latent flake in `run_selftest` (a surface this claim explicitly does not change), direction
**false FAIL only**: a flake on the baseline or on a neutral rewrite turns the counter's predicate
`baseline_pass == 1 … neutral_pass == 3` into FAIL; a flake inside a mutant's own assertion is still
recorded as killed, so it cannot manufacture a PASS or hide a survivor. At observed ambient load the
counter was stable 10/10. A one-line hardening the arm's owner could apply (not mine to edit):
replace `printf '%s\n' "$out" | grep -q PAT` with `[[ $out == *PAT* ]]` (or a here-string), which
removes the second process, the pipe and the SIGPIPE/`pipefail` interaction.

# Not done

- Did not run the counter at its default `--jobs 4` (the author receipt already records that), nor at
  any locale other than `C` and `en_US.UTF-8`. Caller `TZ` was pinned to `UTC` in the nine matrix
  cells and left unset in the supplemental cell; both states produced the same judged signature, but
  `TZ` was never varied independently of the other knobs.
- Did not trace a full counter run end to end (the 13-selftest trace is ~37 MB and was discarded; only
  the one-selftest trace receipt lines are kept).
- No file in the lane was modified, no tool was installed or upgraded, no host state touched; all
  clones/copies/mutants lived in `/fast/scratch/hyaku/tsukuroi-r40/C1ExecEnvMatrix/` and were removed
  after the receipts were copied here.
