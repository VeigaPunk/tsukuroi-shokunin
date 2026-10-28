VERDICT: defect-found

Seat R49ExecFdA (C3-B1, EXEC-AUTHORIZED) — fd-band behaviour matrix at the round-49 freeze bytes.
Everything below is measured at `55c07cd3f8bff2e12117c34d57b4c618de74d85c` unless stated. Nothing in
the lane was written; the census was read with `git -C ... show <rev>:tools/tsukuroi-census.sh`.

## 1. Bytes under test

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/tsukuroi-census.sh > census.sh
3765 lines
c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75  census.sh
```
The same file cloned at the same revision (`mktemp -d $S/fx.XXXXXX`, `git clone -q --shared`,
`git checkout -q --detach 55c07cd...`, `git rev-parse HEAD` = 55c07cd…, `rev-parse --show-toplevel` =
the fixture dir) hashes identically: `c66144d7…59a2e75` (receipt `R49ExecFdA/census.sha256`).

## 2. Probe construction (hand copy, as instructed)

`probe.sh` carries `selftest_base_dir()` copied BY HAND from census lines 2063-2101; nothing is
sourced from the census (the `source <(sed -n …)` form is fragile and was deliberately not used).
The copy is verified code-identical, not eyeballed:

```
$ sed -n '2063,2101p' census.sh > fn_ref.sh
$ sed -n '/^selftest_base_dir()/,/^}/p' probe.sh > fn_probe.sh
$ grep -v '^\s*#' fn_ref.sh | sed '/^$/d' > a.txt; grep -v '^\s*#' fn_probe.sh | sed '/^$/d' > b.txt
$ diff -u a.txt b.txt && echo CODE-IDENTICAL
CODE-IDENTICAL (24 lines)
```
(The plain `diff` of the two ranges differs only in comment lines; the stripped diff is empty.)
`diag.sh` likewise carries a hand copy of the `run_selftest` prologue (census 2103-2122, the
`selftest_base_dir || { case … }` diagnostic block) and the same resolver copy.

## 3. Required matrix — all six cases behave as specified

Run: `TMPDIR=/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdA bash probe.sh` (receipt `R49ExecFdA/matrix.txt`):

```
CASE=(a) band-free                      RC=0 DIR=/proc/self/fd/240 FD=240 ERR=<empty> BAND=default
CASE=(b) fd-240-held                    RC=0 DIR=/proc/self/fd/241 FD=241 ERR=<empty> BAND=default
CASE=(c) all-ten-held                   RC=1 DIR=<empty> FD=<empty> ERR=fd-band BAND=default
CASE=(d) custom-band-2-held             RC=1 DIR=<empty> FD=<empty> ERR=fd-band BAND='240 241'
CASE=(d2) custom-band-free              RC=0 DIR=/proc/self/fd/240 FD=240 ERR=<empty> BAND='240 241'
CASE=(e) tmpdir-missing                 RC=1 DIR=<empty> FD=<empty> ERR=dirty-missing BAND=default
CASE=(f) clean-tmpdir                   RC=0 DIR=/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdA/cleanbase FD=<empty> ERR=<empty> BAND=default
CASE=(f) DIR-identity OK
CASE=(g) fd240 free after probes
CASE=(g) fd241 free after probes
```

| case | requirement | observed |
|---|---|---|
| (a) band free, spaced TMPDIR | rc 0, FD 240, ERR empty | rc 0, FD 240, ERR empty ✔ |
| (b) 240 held | fd 241 | fd 241 ✔ |
| (c) all ten held | rc 1, ERR=fd-band, DIR empty | rc 1, ERR=fd-band, DIR empty ✔ |
| (d) `SELFTEST_FD_BAND='240 241'`, both held | ERR=fd-band | ERR=fd-band ✔ (the case's own path) |
| (e) nonexistent spaced TMPDIR | ERR=dirty-missing | ERR=dirty-missing ✔ |
| (f) clean TMPDIR | no alias, ERR empty | FD empty, DIR==TMPDIR, ERR empty ✔ |

Extra: (d2) shows the band override is honoured on the success path (alias 240, not the default-band
first free); (g) shows no descriptor leak from (a)/(b). The `exec {r48_fd}<&-` close form used by the
census was also checked on this host's bash 5.3.20: 240 open → closed, 241 untouched
(`R49ExecFdA/varclose.txt`).

## 4. `run_selftest` diagnostic branch (hand-copied prologue, `diag.sh`)

Receipt `R49ExecFdA/diag.txt` — the named diagnostic prints once, on stderr, and the function returns 1
without ever reaching `mktemp`:

```
(h) band '240 241' both held -> "selftest: fd band 240 241 exhausted (every descriptor already open), cannot alias TMPDIR </…/band dir>; no /tmp fallback (R49-C3)" RC=1
(i) all ten held, default   -> "selftest: fd band 240 241 242 243 244 245 246 247 248 249 exhausted … (R49-C3)" RC=1
(j) nonexistent spaced TMPDIR -> "selftest: TMPDIR </…/no such dir> cannot host the fixture tree (dirty-missing; no /tmp fallback, R48-C2)" RC=1
(k) clean TMPDIR            -> REACHED-WORK-PATH base=/…/cleanbase RC=0
```

## 5. Required full `--selftest` with a spaced TMPDIR — it does NOT print the (R49-C3) PASS line

```
$ cd <fixture clone at 55c07cd…> && TMPDIR="/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdA/selftest tmpdir" \
    bash tools/tsukuroi-census.sh --selftest > selftest.out 2> selftest.err
real 1m36.469s, RC=1
TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)
stderr: FAIL selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)
```
The case count is right (167), but the new case FAILS: the summary is `FAIL (167 cases, 166 passed,
1 failed)` and the `(R49-C3)` line is `FAIL`, not `PASS` (receipts `R49ExecFdA/selftest.out`,
`R49ExecFdA/selftest.err`). This is the deviation from the item's expectation.

Control, same bytes, same clone, clean (space-free) TMPDIR:

```
$ TMPDIR="/…/clean-tmpdir" bash tools/tsukuroi-census.sh --selftest   # real 1m25.588s, RC=0
PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)
TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)
```
(receipt `R49ExecFdA/selftest-clean.out`, 167 PASS lines vs 166 in the dirty run.) A line-by-line diff
of the two runs, with the `PASS `/`FAIL ` prefixes stripped, differs in exactly one place — the
(R49-C3) line and the summary:

```
169c169,170
< TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)
---
> selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)
> TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)
```
No other case is affected by TMPDIR shape.

## 6. Root cause (path:line at the freeze revision)

`tools/tsukuroi-census.sh`:
- `2112-2123` — `run_selftest` calls `selftest_base_dir` once at the top. With a space-bearing TMPDIR
  the resolver opens the alias at the FIRST band descriptor, 240 (`2091-2094`), and `2123`
  (`st_base=$ST_BASE_DIR`) keeps it: `work=$(mktemp -d "$st_base/…")` (`2124`) builds the whole
  fixture tree through `/proc/self/fd/240`. The descriptor is never closed — the EXIT trap at
  `2127` only chmods/rm -rf's `$work`; grepping every close in the file returns only the case-local
  closes at `2096`, `3567`, `3569`, `3596`, `3597`.
- `3580` — the new case's guard is `if [ ! -e /proc/self/fd/240 ] && [ ! -e /proc/self/fd/241 ]; then`.
  Under a dirty TMPDIR, fd 240 IS the harness's own alias, so the guard is false, `r49_held` stays 0
  and control falls to `3599`:
  `bad 'selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)'`.

So the case proves `fd-band` only in the configuration where no alias exists (clean TMPDIR). In the
configuration the resolver was written for — TMPDIR containing whitespace, the R48-C2 surface — the
case can never pass, because the harness already occupies the first probe descriptor.

Deterministic reproduction without a full run (hand copies of the same bodies; receipt
`R49ExecFdA/harness-clash.txt`):

```
harness st_base=/proc/self/fd/240  alias_fd=240  fd240=open
work=/proc/self/fd/240/tsukuroi-r3-2-selftest.1LKbai
R48 resolve fd=241                       # the R48-C2 case still passes, on 241
R49-C3: BAD-path -> selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)
fd240=open fd241=free
```
(The same shell with a clean TMPDIR reserves 240/241 and takes the PASS path — probe case (d).)

## 7. Why the C3 counter still passes (inference from the counter source, not run by me)

`tools/check-fd-band-r49.py:96` runs the selftest with
`env = {'PATH': …, 'LC_ALL': 'C', 'TMPDIR': rundir, 'HOME': work}` where `rundir = work/run`,
`work = tempfile.mkdtemp(prefix='fd-band-', dir=<HYAKU_SCRATCH>/tsukuroi-r49/counter-c3)` — a
space-free path, i.e. the clean-TMPDIR configuration. That is exactly the configuration in which the
new case does pass (section 5 control), so `band_ok`/`case_pass` are satisfied and the frozen
predicate holds while the case is dead under a dirty TMPDIR. `band_ok` is therefore
configuration-dependent, not a property of the case. [INFERENCE: I did not run
`check-fd-band-r49.py` — that is the C3 counter seat's measurement, outside this item.]

## 8. Proposed fix (exact text; measured in both configurations)

Replace the hard-coded pair at `3580-3581` with the first two FREE descriptors of the band, and drive
`SELFTEST_FD_BAND` from that pair (leaving `3586` to use `$r49_pair` instead of the literal):

```sh
  r49_pair=''
  for r49_f in 240 241 242 243 244 245 246 247 248 249; do
    [ -e "/proc/self/fd/$r49_f" ] && continue
    r49_pair="${r49_pair:+$r49_pair }$r49_f"
    case "$r49_pair" in *" "*) break;; esac
  done
  if [ -n "$r49_pair" ]; then
    r49_ok=1
    for r49_f in $r49_pair; do eval "exec ${r49_f}<&0" 2>/dev/null || r49_ok=0; done
    [ "$r49_ok" -eq 1 ] && r49_held=1
  fi
```
with `SELFTEST_FD_BAND="$r49_pair"` in place of `SELFTEST_FD_BAND='240 241'` (`3586`), the same
`$r49_pair` used for the release at `3596-3597`, `unset r49_pair r49_f r49_ok` added to the `unset`
list at `3601`, and
the failure text at `3599` left as-is (it then means genuinely fewer than two free descriptors).

Alternative, minimal-diff: capture the harness alias (`r49_harness_fd=$ST_BASE_FD` at `2123`, before
`ST_BASE_FD` is reset by the later resolver calls at `2078`/`3568`) and skip that descriptor in
the `3580` guard — but the first-free-pair form needs no new global and works when a *caller* holds
240 too. Note `ST_BASE_FD` cannot be consulted at `3580` directly: the resolver zeroes it on entry
(`2078`), and the `3568` call has already cleared it.

Measured effect of the first-free-pair form, hand-copied into the same simulation (receipt
`R49ExecFdA/fix-check.txt`):

```
[dirty-TMPDIR] harness_alias_fd=240 probes=241 242
[dirty-TMPDIR] RESULT=PASS-path err=fd-band
[clean-TMPDIR] harness_alias_fd=none probes=240 241
[clean-TMPDIR] RESULT=PASS-path err=fd-band
```
Both configurations reach `ST_BASE_ERR=fd-band` with an empty base/fd. The full selftest was NOT
re-run against the patched census (the patch is proposed text, not applied anywhere).

## 9. Scope, cost, limits

- Ran exactly one full `--selftest` with the spaced TMPDIR as instructed (96 s, RC 1), plus one
  clean-TMPDIR control run (86 s) because the required line came back FAIL and the control is what
  isolates the defect to the dirty-TMPDIR configuration. One selftest-bearing command at a time;
  no timeouts occurred and no retries were needed.
- Not run by me: `tools/check-fd-band-r49.py` (C3 counter), the C1/C2 counters, any full selftest
  against a patched census.
- No lane file was created, edited or deleted; no git/jj mutation outside the scratch fixture clone;
  nothing written under /tmp; scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdA/` removed at exit
  (receipts copied first). No tool installs, no pacman.
- Host load during the runs: load average 40.9 / 45.5 / 45.4 on 32 CPUs.

## 10. Receipts

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-49/w1/R49ExecFdA/`
`census.sha256`, `probe.sh`, `matrix.txt`, `diag.sh`, `diag.txt`, `varclose.txt`,
`harness-clash.txt`, `fix-check.txt`, `selftest.out`, `selftest.err`, `selftest-clean.out`,
`selftest-clean.err` (empty).
