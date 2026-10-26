VERDICT: defect-found

Seat: C1RevSharedState — Item C1-16, line-by-line bash review of `probe_storage_arm` and its six
selftest cases in `tools/tsukuroi-census.sh` at 52ffd65f868431f021b8615ab281efd87195eac6, under the
script's `set -euo pipefail`. One minor defect found (silent pass on an unreadable sysfs root);
every concern class named in the item otherwise checks clean. All line numbers below are the
commit's file (extract verified byte-identical to the worktree file: `git diff --stat
52ffd65f868431f021b8615ab281efd87195eac6 -- tools/tsukuroi-census.sh` → empty).

# Method

- Extracted the commit's script via `git show 52ffd65…:tools/tsukuroi-census.sh` (3029 lines; the
  file's last line `main "$@"` has no trailing newline — see Observations). Scratch:
  /fast/scratch/hyaku/tsukuroi-r38/C1RevSharedState/ (removed at end; receipts copied to the seat
  dir first).
- Built a verbatim harness: lines 1847–1887 of the commit (the function exactly as committed)
  prepended with `set -euo pipefail` and the production default `BTRFS_SYSFS=${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs}`
  (census.sh:446), driven by 15 fixtures (T1–T15 below). The function's only external inputs are
  `$BTRFS_SYSFS` and its output `$STORAGE_LINE`, so the harness is faithful.
- Ran the committed selftest as baseline: `TMPDIR=<scratch> bash tools/tsukuroi-census.sh --selftest`
  → `TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)`, rc=0; all six R38-C1
  storage cases PASS (receipt selftest-baseline.out).
- Ran the live census once (read-only): `STORAGE btrfs-device-stats state=HEALTHY filesystems=1
  devices=1 nonzero=0` — matches manual inspection of the real sysfs
  (/sys/fs/btrfs/1d02a454-…/devinfo/1/error_stats carries exactly the five counters, space-separated,
  trailing newline), so the parser matches real kernel bytes.

# The named concern classes — all clean

1. `set -euo pipefail` confirmed: census.sh:407 is the only `set -` in code (`grep -n 'set -'` →
   407 plus `cap()`'s internal `set -e` at 567 and comment prose). `umask 077` at 408.
2. Unset-variable aborts: none.
   - `local root=$BTRFS_SYSFS …` (1849) cannot abort: `BTRFS_SYSFS=${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs}`
     (446) is always set.
   - Counters initialized in the `local` list (1849: `fsn=0 devn=0 nz=0 blocked=0 … detail=''`);
     per-device state assigned before use (`seen=' ' nk=0 dnz=0 ddet=''`, 1865); `nd=0` per fs (1856).
   - `read` targets are guarded everywhere they are tested: `${k:-}`, `${v:-}`, `${extra:-}` (1867–1872).
   - Empirical: the full selftest (111 cases) and harness T1–T15 ran the function under
     `set -euo pipefail` with no abort.
3. `read` at EOF without a newline: handled correctly.
   - The loop is `while IFS=' ' read -r k v extra || [ -n "${k:-}" ]` (1866). At EOF-without-delimiter
     bash's `read` populates the variables but returns 1 — reproduced standalone:
     `printf 'a 1' | { IFS=' ' read -r k v extra; … }` under `set -e` kills the group at the first
     `read` (rc=1, no output) — i.e. rc=1 **with** k/v populated, which is exactly why the `||` guard
     exists. With the guard: T1 (five counters, last line without `\n`) → `state=HEALTHY
     filesystems=1 devices=2 nonzero=0` — the partial final line is counted, not dropped, not
     duplicated; T9 (three-var loop over `printf 'a 1'`) → exactly 1 iteration, `k` cleared on the
     next EOF read, no runaway.
   - T5 (five counters + duplicate `read_errs 0` as a final partial line) → BLOCKED malformed — the
     guard path feeds the duplicate detector normally.
4. IFS handling: sound. `IFS=' '` (1866) makes space the only delimiter: multiple/leading/trailing
   spaces collapse (bash IFS-whitespace rule); tabs and CR are **not** IFS chars, so tab- or
   CRLF-separated lines fail the `^[0-9]+$` value test → malformed (T8: CRLF → BLOCKED) — strict in
   the fail-closed direction; real sysfs uses single spaces (verified against the live file above).
   A blank line yields k='' → `" ${k:-} "` not in `$keys` → malformed (T6 → BLOCKED).
5. Glob with nullglob off: guarded. No `shopt`/`nullglob` anywhere in the script (grep → 0 hits).
   Both globs — `for fsd in "$root"/*` (1853) and `for dev in "$fsd"/devinfo/*` (1857) — are guarded
   by `[ -e "$fsd" ] || continue` (1854) / `[ -e "$dev" ] || continue` (1858), so a non-matching glob
   degrades to the literal pattern and is skipped. At the fsid and devinfo levels the skip is
   fail-closed: T2 (fsid dir mode 000 → glob literal) → `state=BLOCKED … detail=11111111:-:no-devinfo`;
   T12 (devinfo dir mode 000) → `state=BLOCKED … no-devinfo`. **The root level is the exception — see
   the defect below.**
6. `st_write()` local leakage: the leak is real, the effect is nil.
   - `st_write() { … }` is defined inside `run_selftest` (2885) without `local -f`; bash semantics
     confirmed: `bash -c 'outer(){ inner(){ :; }; }; outer; declare -F inner'` → inner still defined.
     `work` is likewise not in run_selftest's `local bin fx` list (1891 vs assignment 1892).
   - Effect: none. `grep -n st_write` → definition 2885 and calls 2894–2914 only (the six storage
     cases); `run_selftest` is called only from main's `--selftest` branch (2955–2957) which
     `return`s immediately after; no later code defines or calls `st_write`, and each census run in
     `check()` is a subprocess (`"$BASH" "$SELF"`, 2128) so nothing crosses. The `EXIT INT TERM` trap
     (1895) is the script's only trap (grep → 1895 alone), so it clobbers no pre-existing trap, and
     it guards `"${work:-}"`. Benign as committed; would become a hazard only if a later edit added a
     global `st_write`/`work` or code after `run_selftest` in the same process.
7. EXTRA_ENV reset side effects on later cases: none.
   - `check()` resets `EXTRA_ENV=()` and `ROOT_EXPECT=''` unconditionally after every run
     (2164–2165, after the if/elif chain and the no-mutation assert). Every case assignment
     `EXTRA_ENV=(…)` (24 sites: 2249, 2273, 2298, 2347, 2386, 2415, 2469, 2474, 2479, 2519, 2531,
     2558, 2596, 2638, 2643, 2735, 2742, 2749, 2756, 2762, 2768, 2777, 2820, 2878) is immediately
     followed by its `check` call — verified by adjacency grep (`grep -n -A2 'EXTRA_ENV=('` → 25
     `check` hits = 24 cases + the `check()` definition line caught by 2089's window) and by reading
     every case. The storage block adds a defensive `EXTRA_ENV=()` at 2883. Later assignments
     override the base env because they come after it in `env`'s argument order (2127 after
     2109–2126). No path sets EXTRA_ENV and skips `check`.

# Defect (minor): present-but-unsearchable btrfs sysfs root silently reads HEALTHY 0/0/0

- Reproduction (harness, verbatim function under `set -euo pipefail`):
  - T2b — `$TSUKUROI_BTRFS_SYSFS` is a directory containing a real fsid tree with
    `write_errs 1`, but the root itself is chmod 000:
    → `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0`
  - T3 — `$TSUKUROI_BTRFS_SYSFS` is a regular file:
    → `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0`
  Both outputs are byte-identical to the absent-root case the selftest pins (storage-absent,
  census.sh:2889–2892), so a census consumer cannot distinguish "no btrfs mounted" from "btrfs
  sysfs present but unreadable". Mechanism: `[ -d "$root" ]` (1852) is true for a mode-000 dir
  (stat needs only search on the parent), the glob at 1853 then fails with EACCES, degrades to the
  literal `$root/*`, and `[ -e ]` (1854) skips it — fsn stays 0 and no `blocked` is ever set.
- Why it is a defect and not just an uncovered case: the arm fails closed at every other level —
  unreadable error_stats file → BLOCKED (1860–1862; T13 confirms), unreadable fsid dir → BLOCKED
  no-devinfo (T2), unreadable devinfo dir → BLOCKED no-devinfo (T12) — and the script's own
  convention is to name unreadability, never to pass silently (drift arm `unreadable=$unr`,
  census.sh:1844; PCI inventory unreadable → BLOCKED, case D19; PSI unreadable → `unknown=[C6-psi]`).
  The header contract pins only the absent case ("An absent TSUKUROI_BTRFS_SYSFS means no btrfs
  filesystem is mounted: HEALTHY 0/0/0", census.sh:363); a present unreadable root prints the same
  bytes, which is a false clean bill at the one level the arm cannot see past.
- Reachability on the measured host: nil today. `/sys/fs/btrfs` is `drwxr-xr-x root root`
  (verified `ls -ld`), the census runs unprivileged, and the q82 namespace run (`unshare -rm`,
  per the pre-seat amendment) maps euid 0, which bypasses DAC — so neither live mode nor the
  QUALITY-82 gate can hit it. Severity: minor (verdict-neutral line; robustness/coverage gap, not a
  live misread). It still deserves a fix because the arm's fail-closed lattice has a hole at
  exactly its top level, and the selftest has no case for it.
- Proposed hardening (draft, for the implementer's decision — insert after 1852's `[ -d "$root" ]`
  check, before the fsid loop):
  ```bash
  if [ -d "$root" ] && [ ! -r "$root" ]; then
    blocked=1; detail+="${root##*/}:root-unreadable,"
  fi
  ```
  and a covering selftest case asserting `state=BLOCKED … detail=btrfs:root-unreadable` for a
  chmod-000 fixture root (the selftest can build it: the 000-parent skip rationale at the root arm,
  census.sh:2725–2727, does not apply — the residue is removed by the run_selftest trap's
  `chmod -R u+rwx`, 1895).

# Observations (no action needed)

- `010` and `007` are handled as strings, never octal: values only ever pass `^[0-9]+$` and the
  all-zero test `^0+$` (1871–1873); T14 (`write_errs 007`) → `state=DEGRADED nonzero=1
  detail=11111111:1:write_errs=007`. The storage-nonzero case's label ("010 is ten, not octal",
  census.sh:2901–2903) is accurate.
- Malformed devices' nonzero pairs are excluded from `nonzero` by design ("its nonzero pairs count
  only then", comment 1863–1864; the storage-malformed case, 2906–2911, pins `nonzero=1` from the
  healthy sibling only). Consistent comment/code/tests.
- Uppercase-hex fsid dirs are skipped silently (T7 → HEALTHY 0/0/0) — per contract, which pins
  "lowercase UUID" (census.sh:356); the kernel prints fsids lowercase, so unreachable.
- The reviewed file itself ends without a trailing newline (`main "$@"` with no final 0a; `wc -l`
  says 3028, `grep -n` reaches 3029). Bash executes it fine — the 111-case selftest and the live
  run both prove it — but it is the same EOF-without-newline class this item scrutinizes, and
  `git show`-based tooling that counts lines will be off by one at the tail.
- The selftest's `EXIT INT TERM` trap (1895) does not exit on INT/TERM; after the handler runs,
  execution resumes and the next `$work`-relative command fails under `set -e`, stopping the run.
  Cosmetic.

# What I did not do

- No tool installs or upgrades (none needed; bash/git present) — nothing to record under the
  2026-10-19 tooling authorization.
- Reviewed only `probe_storage_arm` (1848–1887), its six selftest cases (2883–2921), and the
  selftest machinery they run through (`run_selftest`/`check`/`check_cli`, 1890–2186). Other arms'
  functions were read only where the named concern classes required it (traps, EXTRA_ENV, env
  plumbing at 405–450).
- Did not run the q82 counter or any lane campaign tool; did not mutate the host (the two census
  runs and the selftest are the script's own read-only paths, writing only under my TMPDIR).

# Receipts

Copied to .ufo/waves/round-38/w1/C1RevSharedState/:
- census-52ffd65.sh — the commit's file as extracted (`git show 52ffd65…:tools/tsukuroi-census.sh`)
- probe_harness.sh — verbatim function + `set -euo pipefail` + production default
- run_probe_cases.sh, run_probe_cases2.sh — fixtures T1–T16 with observed outputs
- selftest-baseline.out — committed selftest, 111/111 PASS
