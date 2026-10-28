VERDICT: supports

# R50ExecMatcher — C2-B1: the matcher fix and its (R50-C2) case

Seat: R50ExecMatcher (EXEC-AUTHORIZED, item C2-B1). Freeze under test:
`8029cdba1049df25632c91a23c8db4eefb54be5f:tools/tsukuroi-census.sh`
sha256 `aeda2cbcdcc4b08b09fefcddc237da7c0d8ee903aaf063a1578452081e0245dc`, 3824 lines.
Base for the base-vs-freeze comparison: `b866a1d3d26616119a089f1a69b080136becc17b:tools/tsukuroi-census.sh`
(3791 lines, sha256 in receipt `census-base.sh` extraction — see command block below).
Both blobs were extracted with `git show <rev>:tools/tsukuroi-census.sh > <file>` and hashed; the
freeze extraction re-hashes to the same digest as the blob read straight from the object store:
`git show 8029cdba…:tools/tsukuroi-census.sh | sha256sum` → `aeda2cbc…0245dc` (matches the extracted copy).
Host: bash `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)`.

## (a) The base idiom is gone; `buf_has`/`out_has` are defined once and carry every former must-match site

### Definitions — exactly one each (freeze)

```
census-freeze.sh:2236:  buf_has() { # buf_has BUFFER ERE — true when any line of BUFFER matches ERE (full read, no early exit)
census-freeze.sh:2239:  out_has() { buf_has "$out" "$1"; }
```

`grep -n 'buf_has()\|out_has()' census-freeze.sh` returns only those two lines — no second definition,
no shadowing copy elsewhere in the file. `buf_has` body is
`printf '%s\n' "$1" | RE="$2" awk '$0 ~ ENVIRON["RE"] { f = 1 } END { exit(f ? 0 : 1) }'`: the awk
program has an unconditional `END` block, so it drains stdin on every call and the upstream `printf`
never takes SIGPIPE.

### Former sites, base → freeze (must-match arms)

| # | base b866a1d3 | base text | freeze 8029cdba | freeze text |
|---|---|---|---|---|
| 1 | 2381 | `pkgline=$(printf '%s\n' "$out" \| grep '^PLANE packages:' \| head -n1 \|\| true)` | 2393 | `pkgline=$(printf '%s\n' "$out" \| awk '/^PLANE packages:/ && !p { print; p = 1 }')` (full-read awk; comment names the SIGPIPE assignment) |
| 2 | 2384 | `elif ! printf '%s\n' "$out" \| grep -q 'host=fixture-host'; then` | 2396 | `elif ! out_has 'host=fixture-host'; then` |
| 3 | 2386 | `elif ! printf '%s\n' "$pkgline" \| grep -qE '^PLANE packages: [A-Z]+ \(…'; then` | 2398 | `elif ! buf_has "$pkgline" '^PLANE packages: [A-Z]+ \(…'; then` |
| 4 | 2390 | `elif ! printf '%s\n' "$out" \| grep -qE "^TSUKUROI_CENSUS: ${wverdict} \("; then` | 2402 | `elif ! out_has "^TSUKUROI_CENSUS: ${wverdict} \("; then` |
| 5 | 2391 | `bad "…: $(printf '%s\n' "$out" \| grep '^TSUKUROI_CENSUS:' \| head -n1)"` | 2403 | `bad "…: $(printf '%s\n' "$out" \| awk '/^TSUKUROI_CENSUS:/ && !p { print; p = 1 }')"` |
| 6 | 2401 | `printf '%s\n' "$out" \| grep -qE -- "$re" \|\| miss="$miss '$re'"` (plane-evidence loop) | 2413 | `out_has "$re" \|\| miss="$miss '$re'"` |
| 7 | 2432 | `printf '%s\n' "$out" \| grep -qE -- "$re" \|\| miss="$miss '$re'"` (check_cli) | 2444 | `out_has "$re" \|\| miss="$miss '$re'"` |

New call sites introduced by the case: `3653` `buf_has "$r50_probe" '^TSUKUROI_CENSUS: R50 marker'`
and `3657` `buf_has "$r50_probe" '^TSUKUROI_CENSUS: absent marker'`.

**No `printf '%s\n' "$out" | grep -q` and no `printf '%s\n' "$out" | grep … | head -n1` remains.**
Full enumeration of every `printf '%s\n' "$out" |` pipe in the freeze file (`grep -n 'printf .%s.n. "\$out" |'`):

```
2230:  # comment quoting the banned idiom
2393:  pkgline=$(printf '%s\n' "$out" | awk '/^PLANE packages:/ && !p { print; p = 1 }')
2403:  bad "... $(printf '%s\n' "$out" | awk '/^TSUKUROI_CENSUS:/ && !p { print; p = 1 }')"
2418:  bad "... $(printf '%s\n' "$out" | grep '^PLANE ' | tr '\n' '|')"      # failure diagnostic only
2420:  bad "... $(printf '%s\n' "$out" | grep -E '^HANDOFF ' | tr '\n' '|')" # failure diagnostic only
3498:  elif [ "$(printf '%s\n' "$out" | grep -c .)" -ne 1 ]; then            # grep -c consumes all input
```

The two surviving `grep` consumers (2418/2420) sit inside `bad "…"` messages that only execute on an
already-failing case, and both pipe into `tr` which reads to EOF — no early exit, no SIGPIPE. `3498`
uses `grep -c`, which also reads to EOF. None of them is a must-match arm.

Remaining `grep -q` in executable lines (2, both unrelated to `$out` pipes):

```
1898:  [ -n "$host" ] && grep -qxF -- "$t" <<< "$host" && continue          # here-string, no writer process
2408:  if grep -qE -- "${re#ABSENT:}" <<<"$out"; then                       # ABSENT arm, here-string, no writer process
```

Both read a here-string, so there is no upstream `printf` to be killed; the round-42 fail-open hazard
they guard against is structural, not the SIGPIPE one C2 names.

### The counter's own idiom leg agrees

Running the counter's `IDIOM_RE` (`tools/check-selftest-matcher-r50.py`, comment lines excluded, exactly
as the counter computes `idiom_sites`) over the three extractions:

```
census-freeze.sh idiom_sites= 0 []
census-mut2.sh   idiom_sites= 1 [(2413, 'printf \'%s\n\' "$out" | grep -qE -- "$re" || miss="$miss \'$re\'"')]
```

Freeze scores `idiom_sites == 0`; the single textual match at 2230 is a comment and is filtered by the
counter's `not ln.lstrip().startswith('#')` guard, which I reproduced.

## (b) What `(R50-C2)` asserts, and how many trials

Freeze `tools/tsukuroi-census.sh:3645-3665` (case body, comments included):

```sh
  # (R50-C2) The must-match arm must find a mid-stream line in a buffer far past the 64 KiB pipe
  # buffer on every trial. … 20 trials, because the old idiom false-missed 11/20 at this size —
  # one trial would not discriminate.
  r50_big=$(printf '%*s' 100000 '' | tr ' ' x)
  r50_probe=$(printf '%s\n' "$r50_big" 'TSUKUROI_CENSUS: R50 marker' "$r50_big")
  r50_miss=0 r50_t=0
  while [ "$r50_t" -lt 20 ]; do
    r50_t=$((r50_t + 1))
    buf_has "$r50_probe" '^TSUKUROI_CENSUS: R50 marker' || r50_miss=$((r50_miss + 1))
  done
  if [ "$r50_miss" -ne 0 ]; then
    bad "selftest: mid-stream match lost in a 200 KB buffer ($r50_miss/20 false misses) (R50-C2)"
  elif buf_has "$r50_probe" '^TSUKUROI_CENSUS: absent marker'; then
    bad 'selftest: an absent pattern matched a 200 KB buffer (R50-C2)'
  else
    ok 'selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)'
  fi
```

Assertions, exactly:

1. **Sensitivity arm.** `buf_has "$r50_probe" '^TSUKUROI_CENSUS: R50 marker'` must return true on
   **20/20 trials** (`r50_miss == 0`). The probe is 100 000 `x` chars, then the marker line, then
   100 000 `x` chars; `printf '%s\n' … | wc -c` measures **200 030 bytes** — the marker starts at byte
   100 001, i.e. past the 64 KiB (65 536 B) pipe buffer, so an early-exiting reader in the matcher is
   guaranteed to be hit with a still-writing `printf`.
2. **Specificity arm.** `buf_has "$r50_probe" '^TSUKUROI_CENSUS: absent marker'` must return **false**
   (else `bad`), so a matcher that always returned 0 would not pass the case.
3. It runs **20 trials** on the sensitivity arm and **1** on the specificity arm, against a **200 030-byte**
   buffer, with the pattern anchored (`^…`) and matched mid-stream.

What it would catch: any regression of the *matcher definition* back to an early-exit reader. Measured
directly (mutant below): replacing the `buf_has` body with the base idiom makes this case print
`FAIL … (19/20 false misses)` and the whole selftest exit 1. It would not catch a *reuse* of the base
idiom at a call site while `buf_has` stays intact (see Findings F2) — that is the counter's
`idiom_sites` leg.

## (c) Freeze census selftest — observed run

Command, run from the scratch dir holding the extracted freeze bytes at `tools/tsukuroi-census.sh`
(so the relative path is the item's path), TMPDIR inside the seat scratch:

```
cd /fast/scratch/hyaku/tsukuroi-r50/R50ExecMatcher/t
env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=/fast/scratch/hyaku/tsukuroi-r50/R50ExecMatcher/t \
  bash tools/tsukuroi-census.sh --selftest
```

Observed (`selftest-freeze.out`, `selftest-freeze.rc`):

```
170:PASS selftest: mid-stream match held 20/20 in a 200 KB buffer and an absent pattern was rejected (R50-C2)
171:TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)
rc=0
```

- Summary line: `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` — **168 cases**, so
  the `167 -> 168` half of the claim holds (the case is counted).
- `(R50-C2)` line: the `PASS … 20/20 … absent pattern was rejected` line above, i.e. `case_ok == 1`.
- rc: **0**. Tallies: `grep -c '^PASS '` → 168, `grep -c '^FAIL '` → 0, `grep -c '^SKIP '` → 2 (the two
  pre-existing C1 root arms at output lines 89-90, `non-root-owned fixture` and `EACCES metadata case`,
  both unrelated to C2 and uncounted in the 168).
- Wall time 28.6 s. One run only — the counter's `pass_runs == 2` needs two runs; I ran the single
  selftest this item authorises, so I corroborate `cases == 168`, `case_ok == 1` and one of the two
  `pass_runs`, and did **not** re-measure the second run (the C2 counter seat owns that leg).
- No TMPDIR residue after the run: `find t -type f ! -path 't/tools/*' | wc -l` → 0, consistent with
  the no-write contract for this case.

## (d) Attack: is 20 trials on 200 KB enough to catch the base idiom?

### Base idiom reproduced verbatim under the same shell options

`base-idiom.sh` (receipt) is the base arm 2384/2390 text, `set -euo pipefail`, marker mid-stream:

```sh
big=$(printf '%*s' "$1" '' | tr ' ' x)
probe=$(printf '%s\n' "$big" 'TSUKUROI_CENSUS: R50 marker' "$big")
if printf '%s\n' "$probe" | grep -q '^TSUKUROI_CENSUS: R50 marker'; then return 0; else return 1; fi
```

Observed (`base-idiom.out`):

```
base idiom size=50000  bytes(total~100040) false_misses=1/20
base idiom size=100000 bytes(total~200040) false_misses=20/20
base idiom size=200000 bytes(total~400040) false_misses=20/20
```

So at the case's own size the base idiom false-misses **20/20** — the 20-trial budget is not merely
enough, it is saturated: P(20/20 misses) = 1 as observed, and even the least favourable observation
(1/20 at 100 KB) would already trip `r50_miss != 0` on a single trial. At half the case's size (100 KB
total) the race only fires 1/20, which is exactly why the case is sized at 200 KB rather than 96 KB.

### The replacement matcher at and beyond the case's size

`new-idiom.sh` uses the freeze `buf_has` body verbatim, same `set -euo pipefail`:

```
buf_has size=50000   bytes(total~100040)  false_misses=0/20
buf_has size=100000  bytes(total~200040)  false_misses=0/20
buf_has size=200000  bytes(total~400040)  false_misses=0/20
buf_has size=1000000 bytes(total~2000040) false_misses=0/20
absent-arm: rejected (rc=1) as expected
```

0/20 false misses at 4× the case's size, and the specificity direction holds (absent pattern rejected
with rc 1). The full-read matcher is not size-sensitive up to 2 MB.

### Mutation of the census itself (the discriminating test the case exists for)

- **M1 — matcher definition reverted** (`census-mut.sh`: `buf_has` body replaced with
  `printf '%s\n' "$1" | grep -qE -- "$2"`, everything else at freeze):
  `FAIL selftest: mid-stream match lost in a 200 KB buffer (19/20 false misses) (R50-C2)` and
  `TSUKUROI_CENSUS_SELFTEST: FAIL (168 cases, 167 passed, 1 failed)`, **rc=1**. The case discriminates.
- **M2 — one call site reverted** (`census-mut2.sh`: freeze line 2413 put back to
  `printf '%s\n' "$out" | grep -qE -- "$re" || miss=…`, `buf_has`/`out_has` untouched):
  `PASS selftest: mid-stream match held 20/20 … (R50-C2)` and
  `TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)`, **rc=0** — the case alone does
  **not** see a partial revert (fixture `$out` values are far under 64 KiB). The counter's static leg
  does: `idiom_sites(mut2) = 1` (line 2413), so the conjunction
  `idiom_sites == 0 and case_ok == 1` fails M2 even though `case_ok == 1`.

Both mutants live only in seat scratch and the wave receipt dir; no lane byte was touched.

## Findings

**F1 (supports, the item's question).** C2's bytes are as claimed: zero `printf '%s\n' "$out" | grep -q`
and zero `printf '%s\n' "$out" | grep … | head -n1` remain in the selftest harness; `buf_has`/`out_has`
are defined once (2236/2239) and every former must-match site routes through them (mapping table in (a));
the `(R50-C2)` case asserts a 20/20 mid-stream match on a 200 030-byte buffer plus rejection of an absent
pattern; the freeze selftest prints `PASS (168 cases, 168 passed, 0 failed)`, `(R50-C2)` PASS, rc 0. The
base idiom false-misses 20/20 at that size, so the case's trial count and buffer size are adequate, and
a definition-level revert is caught (M1, rc 1).

**F2 (coverage observation — no defect in the frozen predicate).** `(R50-C2)` pins the matcher
*definition*; it cannot see a *call-site* revert, because the fixture buffers are small (M2 passes the
whole selftest 168/168). The guarantee against call-site reverts rests entirely on the counter's
`idiom_sites` regex, which is textual: it matches only `$out`/`$pkgline` as the piped buffer, so a
future arm written as `printf '%s\n' "$CAP_OUT" | grep -q …` (or `grep -m1`, `sed '/x/q'`) would evade
both legs. The conjunction `idiom_sites == 0 and case_ok == 1` is exactly complementary on M1/M2 —
measured, not assumed — so the frozen predicate is sound as written; this is a residual risk for future
edits, not a falsification.

**F3 (minor doc inaccuracy in the frozen counter).** `tools/check-selftest-matcher-r50.py` docstring
states `idiom_sites … (target 0; 6 at base b866a1d3)`. The counter's own `IDIOM_RE`, applied to
`b866a1d3:tools/tsukuroi-census.sh` with the counter's own comment filter, counts **7** executable
sites: base lines 2381, 2384, 2386, 2390, 2391, 2401, 2432 (listed in (a)). The number is prose only —
the predicate never reads it and `idiom_sites == 0` at REV is unaffected — but the docstring should say
7. Exact proposed text for the next touch of that docstring:

```
  idiom_sites    lines of the extracted census that still pipe `$out`/`$pkgline` into `grep -q*` or
                 `head -n1` inside the selftest harness (target 0; 7 at base b866a1d3)
```

**F4 (observation, pre-existing, not part of C2).** The `buf_has` comment (freeze 2233-2235) says "a
here-string is not used because over 64 KiB it is a temporary file and would break the no-write
contract", yet freeze 2408 (the `ABSENT:` arm) still matches with `grep -qE -- "$re" <<<"$out"`. That
arm has no upstream writer, so it carries no SIGPIPE hazard and the round-42 comment there is accurate;
but if a fixture `$out` ever exceeded 64 KiB, bash would spill that here-string to a TMPDIR file. The
selftest's TMPDIR stayed empty on my run (0 files) because fixture outputs are small, so nothing is
broken today; it is a latent inconsistency with the stated rationale, not a C2 failure.

## What I did not do

- Did not run `tools/check-selftest-matcher-r50.py` (not a command named in this item; the C2 counter
  seat owns the full predicate) — so `pass_runs == 2` is not independently re-measured here; I observed
  one PASS run and reproduced the counter's `idiom_sites` regex statically.
- Did not run the base census selftest (167 cases) — the 167 figure is taken from the counter's
  docstring and my line-level base/freeze comparison, not from a base run.
- Did not mutate or write any lane file, index or jj state; both mutants were built from the extracted
  blob inside seat scratch.
- No tool installs were needed (bash 5.3.20, coreutils, python3, git all present).

## Receipts

`.ufo/waves/round-50/w1/R50ExecMatcher/` — `base-idiom.sh`, `base-idiom.out`, `new-idiom.sh`,
`new-idiom.out`, `selftest-freeze.out`, `selftest-freeze.rc`, `selftest-mut.out` (M1),
`selftest-mut2.out` (M2), `census-mut.sh`, `census-mut2.sh` (508 KB total, each under 2 MB).
Seat scratch `/fast/scratch/hyaku/tsukuroi-r50/R50ExecMatcher/` removed at close (545 G free on /fast
at start; no ENOSPC).
