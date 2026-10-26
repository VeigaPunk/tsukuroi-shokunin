VERDICT: defect-found

Scope: security/scope review of `tools/score-selftest-mounts-r41.py` at 568c397da11339aed65181be598414f268835555
(counter sha256 8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c — matches the declaration;
receipts/hashes.txt). Two counter runs, both required by the item:

* run 1, strace: `cd <lane> && TMPDIR=<scratch> strace -f -e trace=openat,mkdir,unlink,rename,execve -o <scratch>/trace
  python3 tools/score-selftest-mounts-r41.py --revision 568c397… --scratch <scratch>/scratch --jobs 4`
  — 1314 s wall, exit 1 (record: receipts/counter-run1-record.json, summary: receipts/counter-run1-summary.txt).
  Census at the revision: `git show 568c397…:tools/tsukuroi-census.sh | sha256sum` =
  646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95.
* run 2, SIGINT: same command without strace, `kill -INT <counter pid>` 30 s after start
  (receipts/sigint-cleanup.txt).

The write-scope claim holds; the defects are in cleanup ordering, in SIGINT latency, and in the record's
diagnosability — plus an observed spurious FAIL of the frozen predicate under load (§5).

1. Writes outside `--scratch`: none.
   Full-trace classification (`trace` = 13,348,196 lines, receipts/write-scope.txt): 521,343 successful
   write-mode `openat`s inside `--scratch`, and outside it only
     /dev/null (269,004 opens, O_WRONLY) and /dev/tty (25,809 opens, O_RDWR; 104,904 further /dev/tty opens
     failed with ENXIO — bash probing a controlling terminal).
   Zero absolute non-scratch target paths appear; distinct outside non-device paths = 0.
   The 223 distinct outside *relative* `mkdir` names (`scratch`, `fx`, `pacmandb`, `tmp`, `r41c1.*`, …) are
   coreutils `mkdir -p` component walks: `mkdir("scratch")` succeeded 9,319 times while `/scratch` does not exist
   (`ls: cannot access '/scratch'`). The only absolute path outside `--scratch` ever named in a `mkdir` is the
   pre-existing `/fast` (38,016 calls: 32,759 `EEXIST`, 5,257 printed `<unfinished ...>` on the call line and
   resumed later; 0 creations). End-state check
   after the run: `/fx`, `/pacmandb`, `/bin/.dispatch`, `/scratch` absent; `find /tmp -name 'tsukuroi-r3-2-selftest.*'`
   = 0. Deletions are not enumerated: the traced set has no `unlinkat`, which glibc/coreutils/Python use, so the
   end state (not the syscall list) carries the cleanup evidence.
   The counter itself creates `--scratch` (`tools/score-selftest-mounts-r41.py:217`) and never removes it; the
   `r41c1.*` work dir is created by `mkdtemp` inside it (`:218`).

2. execve: 1,083,416 calls, 295 distinct program paths (receipts/execve-list.txt).
   Outside `--scratch`, only 31 paths, all `/usr/bin/*`: cat 221041, grep 138091, bash 130713, awk 120068,
   head 64845, sed 51546, tr 48573, find 28875, stat 27654, sort 20625, mkdir 17226, sha256sum 16500, tail 15672,
   wc 12375, cut 12144, paste 8514, env 8283, date 8151, chmod 4620, ln 396, id 264, cp 246, rm 132, comm 132,
   touch 66, vercmp 66, mv 66, mktemp 33, mkfifo 33, git 9, python3 1 (the counter).
   Every mirror probe resolved to the run-local stub under `<scratch>/<variant>/tmp/…/bin/` — pacman 31251,
   journalctl 47487, systemctl 27951, dmesg 4191, nvidia-smi 3960, lsmod 3960, expac 3828, pacman-conf 3828;
   no host `/usr/bin/pacman|systemctl|journalctl|dmesg|nvidia-smi|lsmod|expac` was executed.
   All 9 `git` calls are read-only, e.g. `["git","--no-pager","-C","<lane>","rev-parse","--disambiguate=568c…"]`,
   `cat-file -t`, `merge-base --is-ancestor`, `show 568c…:tools/tsukuroi-census.sh`, under
   `_revision.clean_env()` (`GIT_OPTIONAL_LOCKS=0`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`);
   no `fetch`/`update-ref`/`gc`.

3. Scratch removal: yes on both paths, but SIGINT is not prompt and deletes under live children.
   * normal exit (run 1): `--scratch` empty afterwards (`ls -la` → `total 0`, no `r41c1.*`, no
     `tsukuroi-r3-2-selftest.*`).
   * SIGINT at 30 s (run 2): exit 130, `--scratch` empty (r41c1_dirs=0, files=0), no `/tmp` leftovers — but the
     process kept running 82,059 ms after the signal (receipts/sigint-cleanup.txt).
     Mechanism in the code: the handler `_cleanup` rmtrees every work dir and then `sys.exit(130)`
     (`:128-132`); the resulting SystemExit unwinds through `with ThreadPoolExecutor(...)` (`:240-249`, `:265-273`),
     whose `shutdown(wait=True)` waits for queued *and* running futures, so all remaining selftest runs execute
     after the tree was deleted — `run_selftest` then re-creates its dir via `d.mkdir(parents=True, exist_ok=True)`
     (`:136`) inside the tree that was just removed. Worst case is `--timeout` (default 900 s) × queued runs per
     worker slot, not the 82 s measured here. Children whose `TMPDIR` vanished abort at the census's
     `work=$(mktemp -d "${TMPDIR:-/tmp}/…")` under `set -euo pipefail`
     (`git show 568c397…:tools/tsukuroi-census.sh:423,1930`), so no write escapes — but the fixture root would be
     `/bin`, `/fx`, … if the census ever ran past that point with an empty `$work` (it cannot today, `set -e`
     aborts first). SIGTERM shares the same handler and also exits 130 (not 143); SIGHUP/SIGQUIT are unhandled;
     the registration window is two statements after `mkdtemp` (`:222-224`).

4. `R41_CAP` capture cannot write outside the scratch through the counter CLI.
   `run_selftest` passes a *replacement* environment dict (`:141`), so no ambient `TMPDIR/HOME/R41_CAP` leaks;
   `env['R41_CAP'] = str(cap)` is only set for the capture run, with `cap = work/'cap'` created by `cap.mkdir`
   (`:142-144`) inside the `mkdtemp` dir; the census text at the revision contains 0 occurrences of `R41_CAP`
   (the line is injected only into the counter's private copy, `:116-117`); cwd is `/` and `HOME`/`TMPDIR` are
   per-variant dirs. Empirically the capture run wrote 125 `.args` + 123 `.mounts` files, all under
   `--scratch/…/cap` (standalone capture copy, identical env: `rc=0`, PASS 128/128).
   Residual gap (informational, frozen artifact): the injected line has no `${R41_CAP:?}` guard, so an empty
   value expands to `/N.args` — `set -u; R41_CAP=""; echo "$R41_CAP/$((0+0)).args"` → `/0.args`. Unreachable
   through the CLI (the variable is always passed when the capture text is used), and the write is swallowed by
   `2>/dev/null || true`.

5. Observed FAIL of the frozen predicate in run 1, caused by a load flake the single retry did not absorb.
   Run 1: `baseline_pass=1, neutral_pass=3, decoy_pass=1, mutants_applied=13, survivors=0, params=0` → exit 1.
   The whole difference is `capture_pass=0`: the capture run failed, was retried once (`:253-262`), failed again
   (both attempts wrote all 125 capture `.args` files, so all checks ran — it was a verdict mismatch, not an
   abort). Direct evidence of the cause (receipts/flake-probe.txt):
   * 4 capture copies + 1 baseline, plain concurrency, no strace: 5/5 PASS, 26 s total.
   * 4 capture copies under one `strace -f`: 1/4 FAIL — `degraded: the fold never reads off a missing baseline (R9)`
     (receipts/flake-capture-case.txt).
   * 4 *baseline* copies under the same strace: 1/4 FAIL, on a *different* case
     (`boot-0 coredumps route one coredumps handoff (R32-C1)`, receipts/flake-baseline-case.txt).
   So the flake is in the census `--selftest` under slowdown, not in the capture injection, and it hits
   unmutated text too. Causal mechanism not isolated (recorded limit).
   Diagnosability defect (this is the actionable part): the JSON record never carries the capture run's verdict —
   `capture_pass` is an int and `param_cases` is empty when it fails, so an operator seeing `params == 0` cannot
   tell a load flake from a real regression of the parameters gate; the same holds for the retry record of
   baseline/capture (only mutant rows carry `last`/`confirmed` detail, and control rows only get a `retried`
   block when they fail). Nothing in `:274-300` stores `res['capture']`.

6. Lane scope: the traced run wrote nothing into the lane (0 write-mode opens outside `--scratch`, §1), and git
   was read-only (§2). One observation outside the counter's own behaviour, for main: the lane's
   `tools/__pycache__/score-selftest-mounts-r41.cpython-314.pyc` appeared at 15:05:40 (3 s after my run started)
   and was rewritten at 15:08:20 mid-run, i.e. a sibling process compiles the counter inside the lane; my trace
   contains no such write (`__main__` is not cached, `_revision.pyc` was current). Any harness that imports
   counters into the lane should run with `PYTHONDONTWRITEBYTECODE=1`.

Smallest remediation (report only — lane is read-only for this seat; the counter is frozen by the declaration):
 * Remove the rmtree from the signal path and keep only the raise; let the single `finally: _cleanup()`
   (`:276-277`) delete once, after the pool has drained — or, one step further, cancel pending futures and stop
   live children by pid before the first rmtree. Either way the SIGINT latency becomes a documented bound rather
   than 900 s × queued runs.
 * Put the capture run's `last`/`exit`/`fail_count` (and the retry's first verdict) into the record next to
   `capture_pass`, so `params == 0` is self-explaining.
 * Optional hardening: `: "${R41_CAP:?}"` in the injected capture line, if that line is ever reused outside the
   counter.

What I did not do: no second strace run; no SIGKILL/SIGHUP test; `unlinkat`-based deletions not syscall-traced
(end state used instead); the census selftest's load-flake mechanism not root-caused; no counter run beyond the
two the item specifies. Trace parsing limit: with `-f` under load strace prints many calls as `<unfinished ...>`
plus a path-less resumed line, so success/failure attribution of individual calls is approximate; path *sets*
(the basis of §1) are complete because the path is always printed on the call line. No tool installed or upgraded.

Receipts: `.ufo/waves/round-41/w1/C1SentScratch/` — counter-run1-record.json, counter-run1-summary.txt,
write-scope.txt, execve-list.txt, sigint-cleanup.txt, flake-probe.txt, flake-capture-case.txt,
flake-baseline-case.txt, hashes.txt.
