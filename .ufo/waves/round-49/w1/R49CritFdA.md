VERDICT: defect-found

# C3-B5 — attack the diagnostic design: is a named `fd band … exhausted` the right repair, and does `SELFTEST_FD_BAND` widen the census's trust surface?

Bytes under test: `tools/tsukuroi-census.sh` at FREEZE `55c07cd3f8bff2e12117c34d57b4c618de74d85c`
(`git rev-parse <rev>:tools/tsukuroi-census.sh` = `61f9f6348981e3d4b37076afb24e1d554441fdeb`;
the scratch copy used for every line reference and every run hashes to the same git blob and to
sha256 `c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75`, 3765 lines —
receipt `R49CritFdA/sha256.txt`, `R49CritFdA/census.sh` bytes were only ever read, the lane tree was not).
The lane working tree was never read; only `git show <rev>:…` and a scratch copy were used.

Judged axes: **operability (C3)** — does the new diagnostic actually name the failures an operator
hits; **C3 claim integrity** — is the frozen `cases == 167 / band_ok` evidence environment-stable;
**design** — is the new override a safe test hook.

Answer in one line: the *direction* is right (fail loud, name a class, keep the no-`/tmp` rule), but
the repair names the **least likely** failure class, leaves the likely ones misattributed to
`TMPDIR`, ships an **unvalidated** env override that can re-create the documented R46-C1 regression
and can abort the selftest with no summary line, and the new case itself is **not hermetic** against
caller-held descriptors. Concrete failing scenarios below, all observed.

---

## 1. Does an inherited `SELFTEST_FD_BAND` change a normal `--selftest` run? Yes — three distinct ways

The override is read at `census.sh:2082` (`band=${SELFTEST_FD_BAND:-240 241 … 249}`) and is
unvalidated. It is referenced only at 2082, 2116 (the diagnostic), 3584 and 3594 (save/restore in the
new case), so the **live census is untouched** — `run_selftest` is reachable only from
`census.sh:3688-3690` (`if [ "$selftest" -eq 1 ]; then run_selftest; return; fi`) and
`selftest_base_dir` is called only from `run_selftest` (2112) and the two cases (3558, 3568, 3587).
So the trust surface widens **only on the diagnostic path**, not on the verdict/exit path. That
concession made, the widening is not benign:

**Scenario S1 (observed, run 1) — an inherited band re-creates R46-C1 and kills the run.**
`TMPDIR='<dir with one space>' SELFTEST_FD_BAND=10 bash census.sh --selftest` →
`rc=1`; stderr:

```
FAIL identity: a parent-held descriptor on a relinked decoy is never hashed (R46-C1): exit 126 wanted 0;
output: /usr/bin/bash: /proc/self/fd/10/tsukuroi-r3-2-selftest.L39kUz/identity/held.sh: Not a directory
```

stdout stops after 165 lines at the R47-C2 case (`PASS selftest: a space in a root override stays
unsafe by design (R47-C2)`) and **contains no `TSUKUROI_CENSUS_SELFTEST:` summary line at all**
(`grep -c` = 0). Receipts `R49CritFdA/run1.out`, `run1.err`. The alias itself resolves at fd 10
(`FD=10 DIR=/proc/self/fd/10`), so a child that opens fd 10 — which the selftest's own R46-C1 case
does at 3531 (`exec 10<"$1"`) — makes `$work` unreachable; direct demonstration in
`scenario-matrix.txt` line L: `mkdir /proc/self/fd/10/zz: Not a directory`. That is *exactly* the
failure the 240-249 comment at 2070-2075 exists to prevent ("observed 2026-10-28: R46-C1 … Not a
directory"), re-opened by one exported variable.

**Scenario S2 (observed) — the diagnostic can lie.** `SELFTEST_FD_BAND=' '` with a dirty `TMPDIR` →
`RC=1 ERR=<fd-band>` and

```
selftest: fd band   exhausted (every descriptor already open), cannot alias TMPDIR <…/dirty tmpdir>; no /tmp fallback (R49-C3)
```

The band is whitespace, so `for fdn in $band` (2088) iterates **zero** times, `fdn` stays empty, and
`[ -e "/proc/self/fd/" ]` (2091) is true because that is a directory — `ST_BASE_ERR=fd-band` is
assigned without a single descriptor being tried, and the message asserts "every descriptor already
open" about an empty set. A monitor gets a band field of two spaces (receipt `scenario-matrix.txt` C).

**Scenario S3 (observed) — malformed bands are blamed on `TMPDIR`.** `SELFTEST_FD_BAND='240-249'`
(the spelling the usage text at 608 itself uses) → `exec: 240-249: not found`, `ERR=<alias-open>`, and
the generic message `selftest: TMPDIR <…> cannot host the fixture tree (alias-open; no /tmp fallback,
R48-C2)`. Same for `abc` (`exec: abc: not found`), `-1` (`exec: -1: invalid option`), `999999`
(`999999: Bad file descriptor`) — four caller-side errors, one message that points the operator at
`TMPDIR` (receipt `scenario-matrix.txt` D, E, J, K).

Is an overridable band acceptable *because the census is a diagnostic, not a security boundary*?
Partly: a hostile caller is out of scope. But the realistic caller is a wrapper/harness with a stale
export, and this repo's own history shows callers run the selftest with unusual fd state
(`.ufo/waves/round-48/w2/TRevPortable/envmatrix.txt:11`, and round-48 `Rc2` pre-held fds 10, 11, 12).
S1 is not a security argument; it is an operator-visible false failure from a one-word environment
difference, and the selftest's purpose is to be the instrument that is trustworthy when everything
else is suspect.

## 2. Is a named diagnostic the right repair? Yes in direction, wrong in target

The named `fd band … exhausted` class fires only when **all ten** of 240-249 are occupied
(`census.sh:2088-2091`). The observed, far more common failure of this resolver on a constrained
host is *not* exhaustion but the band lying outside `RLIMIT_NOFILE`:

- `ulimit -n 128` + dirty `TMPDIR` → `240: Bad file descriptor`, `ERR=<alias-open>`, and the
  **generic** message blaming `TMPDIR` (receipt `scenario-matrix.txt` F). fd feasibility measured:
  under `ulimit -n 128` fds 16, 100, 120, 127 all open, fd 240 fails (line M).
- This is not new: round-48 already recorded it as "fail-closed" without a named class
  (`.ufo/waves/round-48/w2/TRevPortable/envmatrix.txt:11`: `J ulimit -n 100 (< fd band)
  "240: Bad file descriptor", rc=1 fail-closed`). Round 49 named the exhaustion case and left this
  one naming `TMPDIR` as the culprit. So the repair is attached to the rarer cause.

Consequence: an operator who sees `alias-open`/`cannot host the fixture tree` will inspect `TMPDIR`
permissions/path, which is the wrong object. In a container (the usual place `ulimit -n` is small)
the diagnostic actively misdirects.

## 3. Alternatives, judged

- **Retry with an auto-allocated fd after the band** — reject. Auto-allocation starts at 10
  (measured: `exec {n}<…` assigns `n=10` every time; `scenario-matrix.txt` line M context), which is
  the documented collision (2070-2075) and S1's mechanism. A post-band retry only helps if it is a
  *descending* scan below the band (e.g. 253 → 16), which is the same thing as the next item and
  should be done instead of, not after, a fixed band.
- **`{var}` allocation** — reject, same reason: it lands on 10. It is strictly worse than the
  current fixed band because the allocated number varies with the caller's opened fds, making `$work`
  paths depend on unrelated state.
- **Derive the band from `ulimit -n`** — recommend. `lim=$(ulimit -n)`; keep 240-249 when
  `lim > 250` (bit-identical to today on normal hosts), else use the ten highest numbers below
  `min(lim, 254)`, floored at 16. Measured: fd 127 opens under `ulimit -n 128`, fd 240 does not. This
  deletes the `alias-open`-blames-`TMPDIR` class for the limit case entirely, for ~3 lines, and keeps
  the R46-C1 contract (band stays far above fixture auto-allocations). Cap at 253, not 254: round-48
  `Rc1` recorded bash moving its script descriptor to 254 when 255 is taken.

## 4. Diagnostic wording: count and `TMPDIR`

Current text (2115-2116) prints the **band token list** and `TMPDIR`, no descriptor count, no
`ulimit -n`, and re-reads `${SELFTEST_FD_BAND:-…}` rather than the band the resolver actually used —
so under any override the printed band can differ from the tried band. The usage text (608) prints a
different shape, `fd band 240-249 exhausted` (hyphen range, hard-coded to the default band); a monitor
matching the documented string can never match the runtime string, and the runtime string for a
whitespace band (`fd band   exhausted`) is unmatchable by any fixed pattern.

Frozen-counter constraint (verified in `tools/check-fd-band-r49.py:93`): `diag_ok` requires the
**contiguous literal** `fd band %s exhausted`. Any new field must go *after* `exhausted`, not between
the `%s` and `exhausted`.

## 5. Should `ST_BASE_ERR` be machine output? Yes — as its own prefix

Observed: on resolver failure the run exits 1 and prints **no machine line at all** (S1: `grep -c
TSUKUROI_CENSUS_SELFTEST` = 0 on 165 lines of stdout; the only class information is one English
sentence on stderr). On a case-level failure the summary *is* printed (`run2.out`). So a monitor
watching the documented summary grammar sees silence for the resolver class, and the census exit map
(0/1/2) carries no class either.

The summary line is a de facto consumer contract (round-12
`.ufo/waves/round-12/resumed/FixtureReviewR.md:91`: "Keep the summary line format unchanged … so
consumers of `TSUKUROI_CENSUS_SELFTEST:` do not break"), and the frozen counter's regex anchors
`… (\d+) failed\)$` (`check-fd-band-r49.py:47`). Therefore put the class on a **separate prefix**, not
inside the summary:

```
TSUKUROI_CENSUS_SELFTEST_ERR: err=fd-band band="240 241 242 243 244 245 246 247 248 249" ulimit_n=1024 tmpdir="/path"
```

This is inert for the frozen counter (it only parses `SUMMARY`-shaped lines) and gives a monitor a
single stable key. Do not append `err=` to the summary line itself.

## 6. The new case is not hermetic against caller-held descriptors (claim-integrity defect)

Observed run 2: clean `TMPDIR`, caller holds **fd 241 only** → `rc=1`,

```
FAIL selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)
TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)
```

Receipts `R49CritFdA/run2.out:169`, `run2.err:1`. Cause: the case requires **both** 240 and 241 to be
absent before claiming them (3580-3582) and otherwise calls `bad` (3599) — a failure of the test, not
of the resolver, and the message advertises a resolver defect that is not there.

Scope of the damage, stated precisely: the frozen counter is **not** affected — it runs
`env={PATH,LC_ALL,TMPDIR,HOME}` and Python's `subprocess` closes fds ≥3 by default
(`check-fd-band-r49.py:96-98`), so the frozen `PASS (167 …)` is reproducible. The defect hits any
human/harness run from a shell that holds 240 or 241 (this repo's round-48 `Rc2` pre-held 10/11/12;
holding a high fd is not exotic under `ulimit`-tight or instrumentation-heavy runners), and it makes
the selftest's own PASS/FAIL depend on caller state — the opposite of the instrument property C3 is
claiming.

## 7. Minor, pre-existing but now reachable: `set -e` abort inside the R48-C2 case

`census.sh:3558` calls the resolver **unguarded** under `set -euo pipefail` (454):
`TMPDIR="$r48_dir" selftest_base_dir; r48_rc=$?`. The `r48_rc=$?` capture on 3558 is dead code on the
failure path — the shell exits first, which is why run 1 ends mid-file with no summary. The round-49
override is what made this path reachable from the outside; a poison band therefore degrades from
"one case fails" to "no machine output".

---

## Smallest safe correction (ranked; all keep the frozen predicate at `167`)

1. **Delete the env surface; pass the band as a parameter** (removes the whole class S1/S2/S3):
   - 2082 → `local band=${1:-240 241 242 243 244 245 246 247 248 249}`; record
     `ST_BASE_BAND=$band` after the clean check at 2099 (and in every failure arm) so the printer
     shows the band actually tried.
   - 3587 → `if selftest_base_dir '240 241'; then`.
   - 2116 → print `${ST_BASE_BAND:-…}` instead of `${SELFTEST_FD_BAND:-…}`.
   Counter legs survive unchanged: `diag_ok` still finds `ST_BASE_ERR=fd-band` (2091),
   `fd band %s exhausted` (2115) and ≥2 `fd band` (2115, 608, 3577, 3588-3592); `cases` stays 167.
2. **If the override is kept, validate it**: `case "${SELFTEST_FD_BAND:-}" in ''|*[!0-9\ ]*)
   ST_BASE_ERR=band-invalid; return 1;; esac`, at least one token, every token in 10..253. A new
   `band-invalid` class makes the generic branch (2118) name the cause instead of blaming `TMPDIR`.
3. **Derive the default band from `ulimit -n`** as in §3; print `ulimit -n` in the class line.
4. **Wording** (keeps the frozen literal):
   `selftest: fd band %s exhausted (%d descriptors, ulimit -n=%s; every descriptor already open), cannot alias TMPDIR <%s>; no /tmp fallback (R49-C3)`
   and make usage 608 match the runtime shape (or state "the band printed at run time").
5. **Machine line** before the `return 1` at 2121: `TSUKUROI_CENSUS_SELFTEST_ERR: err=%s band=%s
   ulimit_n=%s tmpdir=%s` (separate prefix, stderr).
6. **Harden the case**: pick the two probe descriptors dynamically (first two free numbers scanning
   240..249), then hold exactly those and pass them as the resolver argument; if fewer than two are
   free the host is pathological — print a `SKIP`-style `ok` line rather than `bad`, so caller fd
   state can never turn the frozen PASS into a FAIL.
7. **Guard 3558**: `if ! TMPDIR="$r48_dir" selftest_base_dir; then bad …; else …; fi` (or `set +e`),
   so a resolver failure is reported, not an abort.

---

## What I did not do

- Did not run the frozen counter `check-fd-band-r49.py` (C3 counter seat owns it) and did not re-run
  the pristine control at the freeze revision: the frozen PASS 167 is taken from the claim and the
  counter's own env discipline, not re-measured by me.
- Did not test the live (non-`--selftest`) census path: reachability was established statically
  (only 3688-3690 calls `run_selftest`; `SELFTEST_FD_BAND` occurs only at 2082/2116/3584/3594).
- Did not mutate the lane or any fixture git repo; no commits were made anywhere (no fixture repo was
  needed). No tools were installed or upgraded.
- Two selftest-bearing runs only, one at a time (95.8 s and 69.1 s), no retries needed.

## Receipts (all under `tsukuroi-shokunin/.ufo/waves/round-49/w1/R49CritFdA/`)

| file | content |
|---|---|
| `census.sh` | the freeze blob bytes (git blob `61f9f63…`, sha256 `c66144d7…`, 3765 lines) |
| `resolver.sh` | lines 2063-2101 of that blob (the resolver under test) |
| `sha256.txt` | sha256 of `census.sh`, `resolver.sh`, `drive.sh`, plus the freeze-blob equality proof (`git hash-object census.sh` = `61f9f63…` = `git rev-parse <rev>:tools/tsukuroi-census.sh`) |
| `run1.out`, `run1.err` | S1: dirty TMPDIR + `SELFTEST_FD_BAND=10` → rc 1, R46-C1 false FAIL, 165 lines, no summary |
| `run2.out`, `run2.err` | §6: clean TMPDIR + caller holds fd 241 → `FAIL (167 cases, 166 passed, 1 failed)`, rc 1 |
| `scenario-matrix.txt` | resolver unit matrix A-M: inert clean-path override, false `fd-band` on whitespace band, four malformed bands blaming `TMPDIR`, `ulimit -n 128` → `alias-open`, fd-10 collision, fd/limit feasibility |
| `drive.sh` | the harness that sources `resolver.sh` and reproduces the run_selftest diagnostic block verbatim (2112-2121) |

Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49CritFdA/` is removed after the receipts are copied.
