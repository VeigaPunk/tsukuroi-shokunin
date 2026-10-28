VERDICT: defect-found

# R49CritFdB — cheat the C3 counter (`check-fd-band-r49.py`)

Seat item C3-B6. Claim under test: C3 (operability). Counter:
`tools/check-fd-band-r49.py` at freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c`.
Predicate: `stale_ok == 1 and diag_ok == 1 and band_ok == 1 and cases == 167`.

Two of the three cheats PASS the counter. The third is caught. **No claim byte at the freeze is
dishonest** — `tools/tsukuroi-census.sh:3577-3600` really does hold descriptors 240/241, narrow the
band and call `selftest_base_dir` — but the counter cannot distinguish that work from a 19-line
script that prints two lines. This is a discriminating-power defect in the instrumentation, not a
falsification of the C3 bytes.

## Results

| Cheat | Counter verdict | Legs | Caught by |
|---|---|---|---|
| **A** 19-line liar at the census path | **PASS** (`rc 0`) | stale_ok 1, diag_ok 1, band_ok 1, cases 167 | **no leg** |
| **B** freeze census, `(R49-C3)` case replaced by a bare `ok` | **PASS** (`rc 0`) | stale_ok 1, diag_ok 1, band_ok 1, cases 167 | **no leg** |
| **C** freeze census, resolver returns 0 on an exhausted band | **FAIL** (`rc 1`) | stale_ok 1, diag_ok 1, **band_ok 0**, cases 167 | **band_ok**, through the case's `bad` branch |

Cheat A also passes on the *real measurement path* (`--revision`, no `--census-file`), proved by
committing it at `tools/tsukuroi-census.sh` in a throwaway `--shared` clone.

## Cheat A — a 19-line liar PASSes; nothing catches it

Content (`R49CritFdB/cheat-a.sh`, 13 inserted lines): three comment lines carrying
`ST_BASE_ERR=fd-band`, `fd band %s exhausted` and one more `fd band`, then two `printf`s and
`exit 0`. No `selftest_base_dir`, no `--selftest`, no fixture tree.

```
$ python3 tools/check-fd-band-r49.py --revision 55c07cd... --census-file .../cheat-a.sh
{"band_ok": 1, ..., "case_line": "PASS selftest: exhausted fd band fails the base resolver and
 names err=fd-band (R49-C3)", "cases": 167, "diag_ok": 1, "selftest_rc": 0, "stale_ok": 1,
 "summary": "TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)", "verdict": "PASS"}
RC=0
```

Why every leg is satisfied: `stale_ok` is `STALE not in text` (counter:91) — the liar just never
writes the phrase. `diag_ok` is a **substring census** (counter:92-93) — comments count. `band_ok`
is the child's own `printf` (counter:104-106) — `case_pass` only asks that some line contain
`R49-C3` and start with `PASS`, and `cases` is parsed from the same self-printed summary
(counter:101-102). The counter never inspects size, structure, shebang behaviour, or the census's
own `--identity` facility (`tools/tsukuroi-census.sh:3462-3520`), which exists precisely to name
executed bytes.

Equivalent on the measurement path — throwaway clone, verified
`git rev-parse --show-toplevel == $D` and base `6256760` present before the first commit:

```
$ git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -m 'cheat-a: 19-line liar'
f94e8dec  tools/tsukuroi-census.sh | 3777 +----------------  1 file changed, 13 insertions(+)
$ python3 tools/check-fd-band-r49.py --lane "$D" --revision f94e8dec... 
{"band_ok": 1, ..., "revision": "f94e8decc202500acbcb490e1c88f042834678da", "verdict": "PASS"}
RC_REVA=0
```

The `--revision` branch differs from `--census-file` only in how `src` is obtained
(counter:79-80); the legs are identical. So committing the liar is enough — no `--census-file`
needed to cheat the claim measurement.

Note on a first attempt: an earlier `cheat-a.sh` of mine carried the forbidden phrase inside a
comment explaining that it was absent, and the counter correctly returned `stale_ok 0, FAIL`. That
is the whole strength of `stale_ok`: a plain substring test, defeated by not typing the string.

## Cheat B — a neutered case PASSes; nothing catches it

The only difference from the freeze census is the 30-line `(R49-C3)` block
(`tools/tsukuroi-census.sh:3573-3602`) replaced by:

```bash
  # (R49-C3) fd-band exhaustion is named, not silent (asserts nothing).
  ok 'selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)'
```

No descriptor is ever opened, no resolver is ever called, and the printed diagnostic
(`tools/tsukuroi-census.sh:2113-2120`) becomes unreachable dead code while `diag_ok` still reads 1.

```
$ time python3 tools/check-fd-band-r49.py --revision 55c07cd... --census-file .../cheat-b.sh
{"band_ok": 1, ..., "case_line": "PASS selftest: exhausted fd band fails the base resolver and
 names err=fd-band (R49-C3)", "cases": 167, "diag_ok": 1, "selftest_rc": 0, "stale_ok": 1,
 "summary": "TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)", "verdict": "PASS"}
RC=0        real 1m21.6s
```

This is the sharpest result: the counter's `(R49-C3)` leg is satisfied by a **name and a PASS
token**, not by the assertion. The frozen control set does not cover it — C3-K1 removes the case
(`controls/battery-summary-r49-c3.jsonl`, K1 note: "the R49-C3 case removed" → `cases 166`,
FAIL), which changing the count to 167 here repairs. No control neuters the case in place.

Side finding: because the other 166 cases ran genuinely in cheat B and all passed, the freeze
census's remaining 166 cases are confirmed green at the freeze bytes; only the 167th was replaced.

## Cheat C — caught, by `band_ok` alone

Freeze census with one line changed (`tools/tsukuroi-census.sh:2091`):

```
-      if [ -e "/proc/self/fd/$fdn" ]; then ST_BASE_ERR=fd-band; return 1; fi
+      if [ -e "/proc/self/fd/$fdn" ]; then ST_BASE_ERR=fd-band; ST_BASE_DIR=$base; return 0; fi
```

The diagnostic strings stay in the text, so `stale_ok 1` and `diag_ok 1`; the R49-C3 case then
takes the `if selftest_base_dir; then bad ...` branch (`tools/tsukuroi-census.sh:3587-3589`):

```
$ time python3 tools/check-fd-band-r49.py --revision 55c07cd... --census-file .../cheat-c.sh
{"band_ok": 0, ..., "case_line": "FAIL selftest: an exhausted fd band must fail the base resolver
 (R49-C3)", "cases": 167, "diag_ok": 1, "selftest_rc": 1, "stale_ok": 1,
 "summary": "TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)", "verdict": "FAIL"}
RC_C=1      real 1m5.8s
```

Which leg catches it: **`band_ok`**, and only because the case body actually calls the resolver and
checks its return code. `diag_ok` does **not** catch it — it stayed 1 while the diagnostic became
unreachable. So `diag_ok` proves the diagnostic is *written down*, never that it is *emitted*.

## What the four legs actually measure

All four are self-reports about the script under test:

- `stale_ok` — absence of a literal (counter:44,91).
- `diag_ok` — presence of two literals plus `text.count('fd band') >= 2`, comments included
  (counter:92-93).
- `band_ok`/`cases` — the child's own stdout/stderr and exit code (counter:95-106), with no
  independent oracle and no comparison against the expected bytes.
- The one structural check that would bind execution to the extracted bytes — `--identity`
  (`tools/tsukuroi-census.sh:3462-3520`, `verified=yes`, digests re-derived from the descriptor bash
  holds) — is never invoked by the counter (`grep identity tools/check-fd-band-r49.py` → no hit).

Hence A and B pass because printing is cheaper than doing; C fails because it broke a *behaviour*
that one case still observes.

## Recommended hardening (one, not implemented)

Make the counter an **independent oracle for the exhausted-band path** instead of trusting a
self-printed case line: the counter itself constructs the input and asserts the census's observable
behaviour on it.

Concretely, as a fifth leg evaluated before/instead of the `(R49-C3)` PASS token:

1. `os.makedirs(os.path.join(work, 'tmdir with a space'))` — space-bearing, so the census takes the
   dirty-`TMPDIR` branch (`tools/tsukuroi-census.sh:2084-2085`).
2. Open two descriptors in the counter, dup them to 240 and 241, keep them inheritable.
3. Run `['/bin/bash', src, '--selftest']` with `TMPDIR=<that dir>`, `SELFTEST_FD_BAND='240 241'`,
   `pass_fds=(240, 241)`.
4. Require **`rc == 1`**, **`selftest: fd band 240 241 exhausted`** on stderr, and **no fixture tree
   created** — the resolver fails before `mktemp` (`tools/tsukuroi-census.sh:2124`), so this costs
   about a second, not another 80-second selftest.

Cost/benefit: cheat A (`rc 0`, no diagnostic) and cheat B (never enters the resolver) both fail this
leg; the honest freeze census passes it. Residual: a census could special-case that exact
invocation, but then it must implement the failing resolver path for an input it did not choose —
i.e. do the work. If the round also wants protection against a targeted special-case, the only
non-mimickable defence is provenance (require the `--identity` sha256 to equal the sha256 of the
extracted file, or freeze the census digest in the counter); that is a different axis and it would
also preclude the `--census-file` control path, so it should be a deliberate separate decision, not
folded into this hardening.

(NB: this is a recommendation only — no counter or census byte was modified by this seat.)

## What I did not do

- I did **not** run the unmodified freeze census through the counter; the `K-pass` control receipt
  (`controls/battery-summary-r49-c3.jsonl`) records that PASS, and cheat B's run exercised the other
  166 cases green, but the honest 167th case was not executed by this seat.
- I did **not** run the claim measurement on the live lane revision (not this seat's assignment, and
  the lane is read-only for me).
- I did **not** modify or install any tool. No `pacman`. Free space at start: `/fast` 528G avail,
  `/home` 557G avail.
- No tracked lane/fleet file was written; the only lane writes are this report and its receipts.

## Receipts (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-49/w1/R49CritFdB/`)

`cheat-a.sh` · `cheat-b.sh` · `cheat-c.sh` · `cheat-b.diff` · `cheat-c.diff` ·
`cheat-a-censusfile.json` · `cheat-b-censusfile.json` · `cheat-c-censusfile.json` ·
`cheat-a-revision-clone.json` · `fixture-commit.txt`

Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49CritFdB/` (census copy, mutant copies, clone
`fx.AP6JhB`, counter work dirs) was removed after the receipts were copied.
