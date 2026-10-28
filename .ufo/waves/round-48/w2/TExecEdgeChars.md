VERDICT: defect-found

Scope (item C1-X3): edge-case matrix for `selftest_base_dir()` at freeze
ae99f021b76f8eb1c8805d32d80644464afb1ff6. Bytes under test extracted read-only from the frozen
commit and hashed before any run:

    $ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show \
        ae99f021b76f8eb1c8805d32d80644464afb1ff6:tools/tsukuroi-census.sh > .../census.sh
    $ sha256sum census.sh
    375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426  census.sh   (= frozen blob)

Method: one directory per value under scratch, then one selftest at a time, inheriting nothing:

    env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=<value> bash <scratch>/census.sh --selftest

Recorded per run: rc, last stdout line, whether a `tsukuroi-r3-2-selftest.*` fixture existed
INSIDE the value directory, and `/tmp` attribution. `/tmp` counts taken with a marker file are
sibling-contaminated in this wave (40+ concurrent seats create the same fixture names — I saw
1–10 new dirs per run), so attribution was done by three non-counting methods instead: (a) the
fixture tree observed live inside the value dir, (b) a private-mount-namespace run with an empty
`/tmp`, (c) an `strace -f -e trace=mkdir,mkdirat` trace of one full run. Details in "no /tmp use".

## Matrix (14 required values + 1 control)

| # | TMPDIR value (escaped) | rc | last line | fixture inside TMPDIR |
|---|---|---|---|---|
|1|`…/e1tab<TAB>x` (absolute)|0|PASS (166, 166 passed, 0 failed)|yes during run, removed after|
|2|`…/e2nl<LF>x` (absolute)|0|PASS (166/166)|yes|
|3|`…/e3sq'uote`|0|PASS|removed after|
|4|`…/e4dq"uote`|0|PASS|removed after|
|5|`…/e5$HOME` (literal `$HOME`)|0|PASS|removed after|
|6|``…/e6`bt`` (backtick)|0|PASS|removed after|
|7|`…/e7st*ar` (glob star)|0|PASS|removed after|
|8|`…/e8/-x` (leading-dash component, absolute)|0|PASS|removed after|
|9|`…/e9eq=1`|0|PASS|removed after|
|10|`…/e10slash/` (trailing slash)|0|PASS|removed after|
|11|`…/e11link` → `…/e11 real dir` (symlink to dir with space)|0|PASS|removed after|
|12|`e12 rel dir` (relative, with space)|0|PASS|removed after|
|13|`…/e13<200×a>` (200-char component)|0|PASS|removed after|
|14|`…/e14üñí` (unicode)|0|PASS|removed after|
|15|`e13relclean` (control: relative, NO space)|1|**FAIL (166 cases, 14 passed, 152 failed)**|removed after|

Raw lines: `receipts/matrix-summary.txt`; full stdout of every run: `receipts/out.*.log`.

Resolver-level values (no full selftest) were also read directly from the extracted function
(`receipts/resolver-probe.out`): every dirty value resolves `ST_BASE_DIR=/proc/self/fd/240`,
`ST_BASE_FD=240`, and `readlink -f` of the alias equals the real TMPDIR; clean values resolve
`ST_BASE_DIR=<value>`, `ST_BASE_FD=` empty. Verified line by line for all 14 values and 3
injection payloads.

## F1 — defect: a CLEAN relative TMPDIR bypasses the absolute-safe path (item #15)

Mechanism, all at ae99f02 in tools/tsukuroi-census.sh:
- `census.sh:2075` `case "$base" in` → dirty branch (`*[!A-Za-z0-9._/+-]*`) secures a
  whitespace-free absolute alias; the clean branch at `census.sh:2088` `*) ST_BASE_DIR=$base ;;`
  hands the value through unchecked, including when it is not absolute.
- `census.sh:2106` `work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")` then builds a
  RELATIVE work dir; every fixture override path is relative, and `root_locator_class`
  (`census.sh:851-867`) classifies anything not starting with `/` as `relative`, so the census
  refuses the override and the packages plane blocks.

Observed (receipts/out.e15relclean.log:1, run with `TMPDIR=e13relclean`, cwd the scratch dir):

    FAIL healthy: all planes pass: exit 2 wanted 0; output: … TSUKUROI_CENSUS: BLOCKED
      (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
    TSUKUROI_CENSUS_SELFTEST: FAIL (166 cases, 14 passed, 152 failed)

This also falsifies the harness's own invariant, which the file pins for the space case only
(`census.sh:3525-3527`: "the fixture base classifies absolute even when TMPDIR contains a space
(R47-C2)"). Same class, minimal form: `TMPDIR=-x` (relative, dash) with a `-x` directory present
→ `mktemp` treats the template as an option and exits 1 (`Try 'mktemp --help' for more
information.`), no fixture, no /tmp.

Severity: low for the declared contract — C1's four scenarios (unset, `/tmp`, absolute writable
scratch, absolute with space) are unaffected and PASS here; POSIX TMPDIR is expected absolute.
But the resolver *accepts* a relative base (rc=0) and then produces 152 case failures, so
"the fixture base is always classifiable" holds only for the dirty branch. Two candidate fixes
(L1's call, not applied): require an absolute `base` and return 1 through the existing
`census.sh:2102` fail-fast message, or route a relative base through the same
`/proc/self/fd/<n>` alias so `$work` is absolute.

## F2 — one unreproduced selftest failure (risk to the 4-pass C1 predicate)

First run of value #6 (backtick TMPDIR) ended rc=1 in 67 s:

    FAIL degraded: a repo-side behind row joins the candidate class (R9):
      hostname override not honoured — possible host read
    TSUKUROI_CENSUS_SELFTEST: FAIL (166 cases, 165 passed, 1 failed)

That case is `census.sh:2813-2814` checked at `census.sh:2355-2356`; the only host source in that
branch is the header read `host=$(head -n1 "$HOSTNAME_FILE" 2>/dev/null | tr -d '\r' || true)`
(`census.sh:3647`), which degrades to `host=unknown` on any environment hiccup. Rerun of the same
value: PASS; 3 further repeats with unique logs: PASS (receipts/repeat.e6btick.{1,2,3}.log); 2
plain absolute clean-TMPDIR controls: PASS (receipts/out.plain{1,2}.log). So 1 failure in 19
full selftests, not tied to the backtick and not reproduced.

Honest limitation: the failing run's log was overwritten by the rerun before I preserved it
(`matrix.sh` reuses `out.<name>.log`); the FAIL text above is quoted from the live output, no
file receipt exists. Not claimed as a resolver defect; flagged because C1's frozen predicate
needs `pass_ok == 4` and one spontaneous case failure would sink it. Unproven hypothesis
(environmental fork/exec pressure from 40+ concurrent seats) — I did not reproduce it.

## F3 — descriptor behaviour (observation, not a defect)

- The alias fd is not close-on-exec: a child of the census sees it
  (`receipts/fdprobe.out`: `240 -> …/e1tab<TAB>x`). It is needed for the whole run and is closed
  at process exit; a child re-pointing 240 affects only itself. No cross-run leak observed.
- Occupying 240–249 in the caller makes the resolver fail fast deterministically: rc=1,
  `selftest: TMPDIR <…> cannot host the fixture tree (no /tmp fallback, R48-C2)`, no fixture,
  no /tmp write.

## F4 — clean non-directory TMPDIR (observation, cosmetic)

`TMPDIR=<scratch>/plainfile` (regular file, clean charset) passes the clean branch and fails in
`mktemp` with `Not a directory`, rc=1, no fixture, no /tmp — correct outcome, but the message is
mktemp's rather than the resolver's `census.sh:2102` text, because `[ -d "$base" ]`
(`census.sh:2078`) exists only in the dirty branch.

## Injection: none

`census.sh:2083` `eval "exec ${fdn}<\"\$base\""` expands `$base` once, inside double quotes and
apostrophes, so the path is redirection data, never re-parsed. Three payloads as TMPDIR (existing
directories literally named for the payload): `inj-a"; touch <scratch>/PWNED-A; echo "`,
`inj-b$(touch <scratch>/PWNED-B)`, `` inj-c`touch <scratch>/PWNED-C` ``. All returned rc=0 with
`ST_BASE_DIR=/proc/self/fd/240` and a `readlink -f` equal to the payload directory itself; no
`PWNED-*` file was created (`receipts/resolver-probe.out`, last line
`no PWNED files: no injection`). `$HOME`, backtick, `*` and `=` values likewise resolve to the
correct alias target, never a substituted path.

## No silent /tmp use (the item's "silent /tmp" flag: clean)

1. Namespace run, private empty `/tmp` (`unshare -rm`, tmpfs on /tmp; script
   `receipts/ns.sh`). Positive control, TMPDIR unset — fixture correctly in /tmp:
   `root_dir=/tmp/tsukuroi-r3-2-selftest.VrBoEV/fx/drift-unreadable/root`, 5 such lines
   (receipts/out.ns-unset.log). Dirty tab TMPDIR — fixture in the alias only:
   `root_dir=/proc/self/fd/240/tsukuroi-r3-2-selftest.5F9XBF/fx/drift-unreadable/root`, 5 alias
   lines and **0** `/tmp` lines (receipts/out.ns-tab.log).
   (Both namespace runs show 5 FAILs — the EACCES/unreadable-fixture cases, because userns root
   bypasses DAC; the same reason the normal run SKIPs `census.sh:2991` "uid 0 bypasses DAC".
   Those failures are namespace artifacts, not findings.)
2. `strace -f -e trace=mkdir,mkdirat` over a full tab-TMPDIR run: 72,423 traced lines, **0**
   containing `/tmp`, exactly one creation of the fixture root, under the alias:
   `1649265 mkdir("/proc/self/fd/240/tsukuroi-r3-2-selftest.zTVnsM", 0700) = 0`
   (receipts/trace-summary.txt, receipts/trace.e1tab.log.gz). Run itself: 166/166 PASS.
3. Every dirty-value run left `remain=0` in its value directory (fixture cleaned by the trap) and
   no value directory gained a stray fixture.

## Not done / boundaries

- Did not run the frozen C1 counter `tools/score-selftest-tmpdir-r48.py` (owned by the C1 counted
  seats); my runs are the single-scenario form of its four.
- Did not test `TMPDIR=/` (a clean absolute base that would create the fixture on the live root
  filesystem) — writing outside my scratch is outside the host guard.
- Did not retest §C1's SIGTERM/exit-143 or nonexistent-TMPDIR rows beyond the cheap fail-fast
  probes (nonexistent dirty → rc=1 resolver message; nonexistent tab-suffixed → same).
- No tools installed or upgraded; no lane/fleet file touched except this report and
  `.ufo/waves/round-48/w2/TExecEdgeChars/` receipts; scratch removed with
  `trap … rm -rf` after receipts were copied.

## Receipts

`.ufo/waves/round-48/w2/TExecEdgeChars/`: census.sha256, matrix-summary.txt, resolver-probe.out,
fdprobe.out, out.e1tab…out.e14uni.log, out.e15relclean.log, out.plain1.log, out.plain2.log,
out.ns-unset.log, out.ns-tab.log, repeat.e6btick.{1,2,3}.log, trace-summary.txt,
trace.e1tab.log.gz, values.sh, matrix.sh, probe.sh, ns.sh.
