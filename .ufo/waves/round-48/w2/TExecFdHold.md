VERDICT: defect-found

# C1-X4 — attack the descriptor choice (`selftest_base_dir`, fixed fd band 240-249)

Bytes under test: `tools/tsukuroi-census.sh` at FROZEN `ae99f021b76f8eb1c8805d32d80644464afb1ff6`
(extracted with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <rev>:tools/tsukuroi-census.sh`;
sha256 `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`, matching the frozen blob).
All runs used a `git clone --shared` of the lane pinned at that rev
(`git -C <clone> rev-parse HEAD` = `ae99f021…ff6`), so the mutable working tree was never read.
Line numbers below are lines of that blob (receipt copy: `TExecFdHold/census-frozen.sh`).

One defect found: **the band-exhaustion and low-`RLIMIT_NOFILE` failure paths are undiagnosed — the
selftest aborts mid-run with rc 1, zero `FAIL` lines, no summary line and empty stderr.** The four
documented behaviours of the descriptor choice themselves hold (including the ones my own two
sharpest hypotheses predicted would break).

## Method

Every selftest run: `env -i PATH=<stub>:/usr/bin:/bin LC_ALL=C [TMPDIR='<spaced dir>'] bash -c '<pre-opens>; exec bash tools/tsukuroi-census.sh --selftest'`.
The spaced TMPDIR is `/fast/scratch/hyaku/tsukuroi-r48/TExecFdHold/dirty tmpdir` (one space).
A PATH-first stub `mktemp` logged `ls -l /proc/$PPID/fd` before `exec /usr/bin/mktemp "$@"`, which
names the alias descriptor and its target exactly (source: `TExecFdHold/stub-mktemp.sh`; driver:
`TExecFdHold/run.sh`; raw log: `TExecFdHold/logs/mktemp.log`). One selftest at a
time; 13 selftest runs, 41-92 s each. No counter run, no tool installs, no labrat.

## Observed runs (all receipts in `TExecFdHold/logs/`)

| run | caller pre-held (TMPDIR) | rc | last stdout line | stderr | alias fd (mktemp log) |
|---|---|---|---|---|---|
| R0 baseline | none (spaced) | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` | empty | 240 -> dirty tmpdir |
| Ra (a) | 240,241,242,243 (spaced) | 0 | PASS 166/166 | empty | **244** -> dirty tmpdir; 240-243 stay `/dev/null` |
| Rj (control) | 240..247 (spaced) | 0 | PASS 166/166 | empty | **248**; the in-selftest R48-C2 probe took 249 and PASSed |
| Ri (a+1) | 240..248 (spaced) | **1** | `PASS selftest: a space in a root override stays unsafe by design (R47-C2)` (164 PASS, **0 FAIL**, no summary) | **empty** | 249 -> dirty tmpdir, then abort |
| Rb (b) | 240..249 (spaced) | **1** | (no stdout at all) | `selftest: TMPDIR </fast/…/dirty tmpdir> cannot host the fixture tree (no /tmp fallback, R48-C2)` | none (mktemp log empty) |
| Rc1 (c) | 255 (spaced) | 0 | PASS 166/166 | empty | 240; bash moved the script fd to **254** (CLOEXEC, flags `02100000`) |
| Rc2 (c) | 10,11,12 (spaced) | 0 | PASS 166/166 | empty | 240 |
| Rd (d) | 240 open with `FD_CLOEXEC` (spaced) | 0 | PASS 166/166 | empty | 240 (the fd is gone at exec; nothing to reserve) |
| Re | 240 = live pipe (spaced) | 1 | `FAIL (166 cases, 165 passed, 1 failed)` | `FAIL blocked: nvidia hardware, driver offline: hostname override not honoured — possible host read` | 241 (pipe at 240 untouched) |
| Re2 | 240 = live pipe, repeat | 0 | PASS 166/166 | empty | 241 |
| Rf | 240..249 (TMPDIR unset) | **1** | `PASS … unsafe by design (R47-C2)` (164 PASS, 0 FAIL, no summary) | empty | n/a |
| Rg | none, `ulimit -n 200` (TMPDIR unset) | **1** | `PASS … unsafe by design (R47-C2)` (164 PASS, 0 FAIL, no summary) | `…/tools/tsukuroi-census.sh: line 2083: 240: Bad file descriptor` | none |
| Rh | none, `ulimit -n 200` (spaced) | **1** | (no stdout) | 2 lines: the `line 2083: 240: Bad file descriptor` diagnostic **then** the documented `selftest: TMPDIR <…> cannot host the fixture tree …` | none |

Unit-level sweep of the resolver alone (`fdef.sh` = frozen lines 2058-2089, receipt `logs/fd-matrix.txt`):

```
held=0  outer rc=0 alias=240 | second-call rc=0 fd=241
held=4  outer rc=0 alias=244 | second-call rc=0 fd=245
held=8  outer rc=0 alias=248 | second-call rc=0 fd=249
held=9  outer rc=0 alias=249 | second-call rc=1 (band exhausted)
held=10 outer rc=1 (band exhausted)
pipe@240 -e=TRUE rc=0 alias=241 ; deleted-file@240 -e=TRUE rc=0 alias=241 ; socket@240 -e=TRUE rc=0 alias=241
ulimit -n 249/241 -> rc=0 alias=240 ; ulimit -n 240/200 -> rc=1 + "line 26: 240: Bad file descriptor"
```

## Findings

**F1 — (a) pre-held 240..243: PASS, alias 244 (supports the mechanism).** `Ra`: rc 0, 166/166,
and the stub's `/proc/$PPID/fd` listing shows `240-243 -> /dev/null` while `244 -> …/dirty tmpdir`.
The "first free slot" scan (lines 2079-2081) skips occupied numbers exactly as documented.
Control `Rj` (8 held) also PASSed with alias 248, so the scan has 10 usable slots for its *first* call.

**F2 — (b) all of 240..249 pre-held: documented fail-fast, nothing built (supports).** `Rb`: rc 1,
zero stdout, exactly the one documented stderr line (line 2102), `mktemp` never ran
(`logs/mktemp.log` empty for that run), `ls -A …/dirty tmpdir` = 0 entries after the run. Nothing
landed under /tmp either: the /tmp `tsukuroi-r3-2-selftest.*` directories present were pre-existing
(8 at check time) and `find /tmp -maxdepth 1 -name 'tsukuroi-r3-2-selftest.*' -newermt '-40 minutes'`
returned 0. So it is fail-fast, not silent, and not a /tmp fallback.

**F3 — (c) fd 255 and fd 10-12 held: PASS, alias 240 (supports).** `Rc1`: the caller's 255 stays
`/dev/null`; bash moved the script to 254 with `flags: 02100000` (O_CLOEXEC), i.e. the 240-249 band
really is below the script descriptor band and does not collide with it. `Rc2`: 10,11,12 pre-held do
not disturb the alias (`240 -> dirty tmpdir`) — the auto-allocation-collision rationale in the
comment at lines 2064-2070 holds: a fixture `exec 10<…` cannot re-point the alias.

**F4 — (d) a caller fd 240 with `FD_CLOEXEC`: PASS; the reservation is not observable (supports).**
`Rd` (python: `fcntl(F_SETFD, FD_CLOEXEC)` on 240, confirmed `01`, then exec): rc 0, 166/166, alias
240. A close-on-exec descriptor is gone before `selftest_base_dir` runs, so the resolver legitimately
reuses the number. There is no way for a caller to reserve a band number across exec; that is a
property of exec, not a defect here. Same result for pipes/sockets (F6).

**F5 — DEFECT: band exhaustion after the first alias aborts the selftest with no diagnostic.**
`set -euo pipefail` is global (line 452). The in-selftest R48-C2 probe is
`TMPDIR="$r48_dir" selftest_base_dir; r48_rc=$?` (line 3540) — a bare failing command, so under
`set -e` a resolver failure **terminates the shell at that line** and the intended
`else bad 'selftest: dirty TMPDIR must resolve to a /proc/self/fd alias inside TMPDIR (R48-C2)'`
(line 3547) is unreachable. Measured on three independent runs:
* `Ri` (spaced TMPDIR, 240..248 held): outer alias took 249, then the probe found no free slot ->
  rc 1, 164 PASS, **0 FAIL, no `TSUKUROI_CENSUS_SELFTEST:` summary line, empty stderr**. A run that
  otherwise passes 164 cases dies looking like a truncated report.
* `Rf` (TMPDIR unset, 240..249 held): identical shape — rc 1, 164 PASS, no FAIL, no summary, empty stderr.
* `Rg` (TMPDIR unset, `ulimit -n 200`): identical shape with one stderr line, a bare bash
  `line 2083: 240: Bad file descriptor` (line 2083 is `eval "exec ${fdn}<\"\$base\""`) — the
  diagnostic points at the resolver, not at the case, and no `FAIL` case is named.
Consequence: the band has **two** consumers per spaced-TMPDIR run (the outer alias plus the
in-selftest probe), so caller headroom is 8, not 10 — confirmed by the control `Rj` (8 held, PASS)
against `Ri` (9 held, abort). With TMPDIR unset/`/tmp` the headroom is 9 (F2 `Rb` vs `Rf`).
Any tooling that counts on `PASS (166 cases, ...)` gets an unattributable rc 1 instead.
A counter run that hit this would simply record FAIL for a reason no case names.

**F6 — DEFECT (small): `RLIMIT_NOFILE` <= 240 makes the alias impossible, with a misleading and
(latently) double-line error.** `exec {fdn}<` at line 2083 cannot open fd 240 when the limit excludes
it: `ulimit -n 240` and `-n 200` both return rc 1 with bash's own `240: Bad file descriptor` (unit
sweep; `ulimit -n 241` and above succeed). With a spaced TMPDIR (`Rh`) stderr carries **two** lines —
the bash diagnostic *then* the documented `selftest: TMPDIR <…> cannot host the fixture tree (no /tmp
fallback, R48-C2)` — which is false: the TMPDIR is fine, the process limit is not. With TMPDIR unset
(`Rg`) only the bash line appears and the run aborts per F5. Descriptor choice 240-249 is what creates
this coupling; no preconditions on `RLIMIT_NOFILE` are stated in the code comment or the claim.

**F7 — hypothesis falsified: `[ -e /proc/self/fd/N ]` is not a broken occupancy test.** I predicted
that a pipe, a unix socket or a descriptor on a deleted file would stat-false and be silently
re-pointed over by `exec ${fdn}<"$base"`. Measured (`fd-matrix.txt`, and `Re`/`Re2` end-to-end):
`-e` is TRUE in all three cases (the magic symlink resolves to a statable anonymous inode), the
resolver therefore takes the *next* slot (`alias=241`) and the caller's pipe at 240 survives
(`240 -> pipe:[…]` before and after; `Re2` PASS 166/166 with `241 -> dirty tmpdir`). No silent
re-pointing on Linux. This is an honest negative on the sharpest attack I had on the occupancy test.

**F8 — one non-reproducible case failure, not attributable to descriptors (reported, not scored).**
`Re` (pipe at 240) failed the `check` case that runs a census child for
`blocked: nvidia hardware, driver offline (exit 2, BLOCKED)`; stderr carried
`FAIL blocked: nvidia hardware, driver offline: hostname override not honoured — possible host read`
from `bad "$label: hostname override not honoured — possible host read"` (line 2356, guarded at 2355
by `grep -q 'host=fixture-host'`). `diff logs/R0-baseline-spaced.txt logs/Re-240pipe.txt` shows exactly that one line
missing; the identical pipe-at-240 rerun `Re2` PASSed 166/166, and 8 other runs passed. So the failure
is a load-sensitive case (≈24 concurrent seats were running selftests on this host), not a
descriptor-band effect — but it is relevant to C1's `pass_ok == 4`: one of 9 spaced-TMPDIR runs
produced 165/1 without any descriptor pressure being reproducible.

**F9 — by-design observation (not a defect): the alias fd is never closed and is inherited by every
fixture child.** Only the in-selftest probe closes its own descriptor (line 3551); the outer alias
taken at line 2084 is not closed after `mktemp` (line 2106). That is required, not a leak: the
fixture paths handed to children are `/proc/self/fd/<n>/…`, so each child must inherit the descriptor
(`Rd`/`Ra` stub listings show the alias present in the `mktemp` child). Side effect worth knowing:
a caller's own fds 240-249 are inherited by all fixture children too.

## Proposed text (non-binding; my item asks for no draft)

Minimal fix for F5, in the R48-C2 self-check block, so the diagnostic survives `set -e`:

```
  r48_rc=0
  TMPDIR="$r48_dir" selftest_base_dir || r48_rc=$?
  r48_base=$ST_BASE_DIR; r48_fd=$ST_BASE_FD
```

(`r48_base`/`r48_fd` reads stay safe because `selftest_base_dir` sets `ST_BASE_DIR=`/`ST_BASE_FD=`
before every return — lines 2072-2073.) For F6, the same band's precondition should be stated where
the band is justified (comment at lines 2064-2070): the alias needs `RLIMIT_NOFILE` > 249 and a free
number in 240-249, and the in-selftest probe consumes a second number, so the contract is
"<= 8 caller-held descriptors in 240-248 for a spaced-TMPDIR pass".

## What I did not do

No run of the frozen counter `tools/score-selftest-tmpdir-r48.py` (5-10 min, six selftests; owned
elsewhere) — so F5/F6 are edges of the mechanism, **not** a falsification of the frozen predicate
`pass_ok == 4 and loc_ok == 4 …` as the counter runs it (the counter's own environment holds no band
descriptors and no `ulimit`). No SIGTERM/INT run (not my item), no test of the `TMPDIR=/tmp` and
"writable scratch" modes under descriptor pressure (I fixed the matrix to TMPDIR unset and the spaced
dir), no `--identity` interleaving with a held 255 (the 254 fallback was observed only via the stub).
No agents spawned; no tools installed; no pacman; nothing written outside my scratch and this wave dir.

Rule deviation to disclose: during one `ulimit` sweep I captured a stub's stderr in `/tmp/x.<pid>`
(two 0-byte files, removed immediately). The receipt was regenerated with scratch-local capture, so
no `/tmp` path is depended on; no fixture tree was ever created under `/tmp` by my runs.

Scratch `/fast/scratch/hyaku/tsukuroi-r48/TExecFdHold/` removed after the receipts above were copied
here (pre-removal `df -h /fast`: 546 G available).
