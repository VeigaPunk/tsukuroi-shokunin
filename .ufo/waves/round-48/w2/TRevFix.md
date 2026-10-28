VERDICT: supports

# TRevFix — non-author correctness review of the C1 fix (diff 5fdf062f → ae99f021, tools/tsukuroi-census.sh)

Lines below refer to blob ae99f021 (sha256 375aa737…, verified by `git show`). All runtime checks ran against an extracted copy of that blob under /fast/scratch/hyaku/tsukuroi-r48/TRevFix/ (scratch removed after receipts copied).

## Q1 — does the /proc/self/fd alias stay inside TMPDIR (cd / fork / exec)?

Yes. `/proc/self/fd/<n>` is an inode reference, not a name lookup:

- cd elsewhere: `bash -c 'exec 240<inh; (cd /; ls -d /proc/self/fd/240/.)'` → resolves. Observed 2026-10-28.
- rename of TMPDIR after the fd is bound: `exec 240<inh; mv inh inh2; touch /proc/self/fd/240/newfile` → `newfile` lands in `inh2`, i.e. still inside the real TMPDIR inode (readlink -f tracks the rename).
- fork/exec of children: `env -i /bin/ls -d /proc/self/fd/240/.`, `setsid ls -d /proc/self/fd/240/.`, nested `bash -c` → all resolve; bash does not set close-on-exec on `exec N<file` redirections (only on its internal temp fds), so fixture children inherit the alias.
- Fixed high descriptor 240-249: correct choice — fixture code auto-allocates `exec 10<...` (line 3513) and bash's internal copy band tops at 255; the `for fdn in 240…249` loop picks the first unoccupied slot and returns 1 if all ten are held (verified: occupied 240-249 → `selftest_base_dir` rc=1). `eval` is required: `exec $n<file` does not re-parse the fd number (verified 127 'not found' without eval).

## Q2 — `exec ${fdn}<"$base"` under set -e / set -u

File has `set -euo pipefail` at c.sh:452. Inside `selftest_base_dir` the exec is `eval "exec ${fdn}<\"\$base\"" || return 1` (c.sh:2083) — explicit `||` keeps a failed open as rc 1 instead of aborting the function mid-way (bash returns status 1 on redirection failure, does not exit, in non-POSIX mode). The function is also always invoked under `||` (c.sh:2101, 3540, 3550), which exempts its interior from `set -e` anyway; `set -u` is satisfied (`$base` is assigned at 2074). Verified live: spaced-but-unreadable TMPDIR (`chmod 311`) → `exec` fails, friendly message `selftest: TMPDIR <…> cannot host the fixture tree (no /tmp fallback, R48-C2)` on stderr, rc=1, nothing created anywhere.

## Q3 — unchecked `work=$(mktemp -d ...)` under mktemp failure

Safe. `work=$(mktemp -d …)` at c.sh:2106 is a command-substitution assignment: its exit status is mktemp's, and with `set -e` active (the function is called from `main` at c.sh:3642, not under `||`/command-substitution) the script exits 1 immediately — before the EXIT trap at 2109 is even installed, so there is nothing to clean and no path where `$work` stays empty while the run continues. Verified: `TMPDIR=/proc bash c.sh --selftest` → `mktemp: failed to create directory via template '…'` rc=1; spaced-TMPDIR on a readonly dir (`chmod 555 "ro dir"`) → `mktemp: failed to create directory … Permission denied` rc=1. Fail-fast in both, never a /tmp fallback. Cosmetic note: this path prints mktemp's own stderr, not the friendly `cannot host` message — acceptable.

## Q4 — INT/TERM/EXIT traps: cleanup once, exit status preserved

- EXIT trap (c.sh:2109) does `chmod -R u+rwx` + `rm -rf` on `$work` with `|| true`, so it cannot mask an already-chosen exit status.
- `trap 'exit 130' INT` / `trap 'exit 143' TERM` (2110-2111): signal → `exit` → EXIT trap runs once → process exits with the trap's code. Bash runs the EXIT trap once even under re-entrant signals, and `rm -rf` through the alias works since it is inode-bound.
- Observed: SIGTERM at ~12 s into a dirty-TMPDIR run → rc 143, fixture dir gone (fixture-before 1, after 0), nothing in /tmp. SIGINT same → rc 130. TMPDIR-unset + SIGTERM → rc 143, fixture under /tmp removed (my dir removed, strays in /tmp were other seats' concurrent counter runs — 4 sibling `score-selftest-tmpdir-r48.py` processes were live; not my writes).
- Trap install order: INT/TERM arms land *after* mktemp (a TERM in that millisecond window kills by default disposition, but no fixture exists yet — nothing to clean; the counter's term leg waits for fixture creation, so the claim's scenario is unaffected).

## Q5 — can the two new cases FAIL? (mutants run against the frozen blob)

- Case 1 (c.sh:3539-3548) FAILed under M1 (corrupted readlink comparison — sanity that `bad` fires) and under M2 (`ST_BASE_DIR=/tmp` — the classic silent /tmp fallback): `FAIL selftest: dirty TMPDIR must resolve to a /proc/self/fd alias inside TMPDIR (R48-C2)`, case 2 still PASS, summary `FAIL (166 cases, 165 passed, 1 failed)`. It pins the alias-resolves-inside-TMPDIR contract.
- Case 2 (c.sh:3550-3556) FAILed under M5 (`[ -d "$base" ] || base=/tmp` — a /tmp fallback *inside* the resolver for missing TMPDIR): `FAIL selftest: nonexistent dirty TMPDIR must fail the base resolver`, case 1 still PASS. It pins the must-fail contract. (Naive removal of the `-d` guard alone does NOT get caught — `exec` still fails on a missing dir; that is correct behaviour, not a gap.)
- Both cases execute unconditionally in every selftest (their `$work`-local fixtures are always dirty paths regardless of the run's own TMPDIR) and the script exits non-zero on FAIL, so each is load-bearing.

## Minor observations (not defects)

- c.sh:415 still reads "builds a /tmp fixture tree" — stale for the scratch/spaced-TMPDIR scenarios (fixture lands under TMPDIR there). Doc drift only.
- The removed comment's sentence "Secrets are never read: only public package/system unit/driver/journal state is queried" (present at 5fdf062f:413) was dropped in the edit; no corresponding guarantee remains in the comment block. Unrelated to the fix; flag for the author to restore or justify.
- `/proc` unmounted: `[ -e /proc/self/fd/240 ]` false → picks 240, `exec` binds the real dir, then `[ -d "$ST_BASE_DIR" ]` fails → fd closed, rc 1, fail-fast — graceful by code reading (not executed: no /proc-less environment available).
- Static-claim check against the frozen counter: `BASE_ASSIGN = r'(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])'` does not match `base=${TMPDIR:-/tmp}` (c.sh:2074) or my notes — consistent with the claim "the file holds no `...base...=/tmp` fallback assignment": only the mktemp-default `${TMPDIR:-/tmp}` and the alias remain (grep of the blob: no other `=/tmp`).

## What I did not run

- Full unmutated `bash c.sh --selftest` end-to-end (mutant runs show 165/166 PASS elsewhere; the PASS side is the counter's and other seats' job — I verified the failing side and the mechanism directly).
- The 6-arm counter predicate itself (R44C1Counter/TExecCounterA/B territory).

Conclusion: the fix is correct — alias is inode-bound inside TMPDIR, fd discipline is sound, fail-fast covers every refusal path, signals clean once with 130/143, and both new pins provably fail under the regressions they name.
