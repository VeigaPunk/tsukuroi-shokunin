VERDICT: defect-found

Seat R49MutFd (mutation-tester, w1, item C3-B7). Bytes under test: freeze
55c07cd3f8bff2e12117c34d57b4c618de74d85c (`tools/tsukuroi-census.sh` blob sha256
c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75; counter
`tools/check-fd-band-r49.py` blob sha256 852621ebea420636b7d3bccc7dcb2d44c6ed8104db4ead747cd5d5261f11f2d8).
All mutants were built from copies in `/fast/scratch/hyaku/tsukuroi-r49/R49MutFd/` and run
through the frozen counter with `--census-file`; the lane was never written.

Axes: (1) does each C3 leg (stale / diag / band / cases) actually kill a defect of the class
it names, (2) does the verdict depend on the mutation alone or on host noise, (3) is the
case-count leg independent of the census's own self-report.

## Headline

| Mutant | Edit (freeze census) | Counter | Verdict |
|---|---|---|---|
| M0 pristine | none | rc 0, PASS | baseline (matches control K-pass) |
| M1 message removed | named-diagnostic branch made unreachable | **rc 0, PASS** (diag_ok 1) | **SURVIVED — real gap** |
| M2 producer renamed | `ST_BASE_ERR=fd-band` -> `fd-band2` | rc 1, FAIL, `band_ok 0` | KILLED (band_ok, R49-C3 case line) |
| M3 stale comment | inert comment `builds a /tmp fixture tree` re-added | rc 1, FAIL, `stale_ok 0` | KILLED (stale leg) |
| M4 count doctored | probe deleted, PASS line kept -> printed 167 / exercised 166 | **rc 0, PASS** | **SURVIVED — the named limit** |

Two of four mutants survive: the `diag_ok` leg is purely lexical and no case ever asserts the
*printed* `fd band ... exhausted` line, and the `cases` leg is satisfied by the census's own
self-reported summary. Neither survival contradicts C3's literal predicate; both are coverage
limits of it.

## Runs (counter, `--revision 55c07cd…`, `--census-file <scratch mutant>`)

```
=== RUN freeze rc=0 elapsed=77s
{"band_ok": 1, "cases": 167, "case_line": "PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)", "diag_ok": 1, "selftest_rc": 0, "stale_ok": 1, "summary": "TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)", "verdict": "PASS"}
=== RUN m1 rc=1 elapsed=56s
{"band_ok": 0, "cases": 167, "case_line": "PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)", "diag_ok": 1, "selftest_rc": 1, "stale_ok": 1, "summary": "TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)", "verdict": "FAIL"}
=== RUN m2 rc=1 elapsed=95s
{"band_ok": 0, "cases": 167, "case_line": "FAIL selftest: exhausted fd band must name err=fd-band (got 'fd-band2') (R49-C3)", "diag_ok": 1, "selftest_rc": 1, "stale_ok": 1, "summary": "TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 166 passed, 1 failed)", "verdict": "FAIL"}
=== RUN m3 rc=1 elapsed=110s
{"band_ok": 0, "cases": 167, "case_line": "PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)", "diag_ok": 1, "selftest_rc": 1, "stale_ok": 0, "summary": "TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 165 passed, 2 failed)", "verdict": "FAIL"}
=== RUN m4 rc=0 elapsed=104s
{"band_ok": 1, "cases": 167, "case_line": "PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)", "diag_ok": 1, "selftest_rc": 0, "stale_ok": 1, "summary": "TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)", "verdict": "PASS"}
```
Raw JSON: `.ufo/waves/round-49/w1/R49MutFd/out-{freeze,m1,m2,m3,m4}.json`.

**The M1 counter row is not attributable to the mutation.** Its single failure is the
host-dependent case described under "Host flake" below: a re-run of the same M1 bytes under
the counter's exact environment gives `PASS (167 cases, 167 passed, 0 failed)`, and the
`R49-C3` line is a PASS (`.ufo/waves/round-49/w1/R49MutFd/diag-m1.out:169`). Taken together —
diag_ok 1 (from the counter run), rc 0 / summary PASS / cases 167 / PASS `R49-C3` line (from
the direct env-identical run) — the frozen predicate is satisfied by M1.

## M1 — SURVIVED (the diag leg is lexical, nothing exercises the printed line)

Mutant (`m1.diff`, 498 B): `tools/tsukuroi-census.sh:2114` `      fd-band)` ->
`      fd-band-disabled)`, so the named-diagnostic arm of `run_selftest`
(`:2113-2119`) is never taken while its `printf 'selftest: fd band %s exhausted …'` text stays
in the file.

Detector, run directly against the diagnostic path (dirty TMPDIR, `SELFTEST_FD_BAND='240 241'`,
descriptors 240/241 held open — the run exits before any case, so it is cheap):

```
=== census-freeze.sh
selftest: fd band 240 241 exhausted (every descriptor already open), cannot alias TMPDIR <…/dirty dir>; no /tmp fallback (R49-C3)
rc=1
=== census-m1.sh
selftest: TMPDIR <…/dirty dir> cannot host the fixture tree (fd-band; no /tmp fallback, R48-C2)
rc=1
```
(`.ufo/waves/round-49/w1/R49MutFd/diag-probe.txt`)

Expected detector: the C3 claim is that the census "names descriptor-band exhaustion …
instead of failing silently". Under M1 the user-visible message degrades to the generic
R48-C2 line that files the cause as an unnamed `(fd-band)`; nothing in the 167-case suite
notices → `diag_ok 1`, `band_ok 1`, `cases 167`, verdict PASS. The full `--selftest`
transcript of M1 is byte-identical to the pristine one
(`sha256 5f346034c87bb2ac06ef14c55ec82cb91a20fbc54e55c2dcd7f404c24bd456aa` for both
`diag-freeze.out` and `diag-m1.out`), i.e. the suite observes nothing at all.

Why it is a real gap, not an artifact of my edit:

- `diag_ok` (`tools/check-fd-band-r49.py:92-93`) matches `DIAG_CODE`/`DIAG_TEXT` in the file
  text plus `text.count('fd band') >= 2`. `ST_BASE_ERR=fd-band` also occurs in the selftest
  comment at `tools/tsukuroi-census.sh:3576`, and `fd band %s exhausted` occurs exactly once,
  at `:2115` — so any edit that keeps the file bytes and makes the arm unreachable passes.
  Deleting the `printf` outright would flip `diag_ok` to 0; that is a lexical kill, not a
  behavioural one.
- The `R49-C3` case (`:3577-3600`) asserts only `selftest_base_dir`'s exit status,
  `ST_BASE_ERR == 'fd-band'`, and empty `ST_BASE_DIR`/`ST_BASE_FD` (`:3587-3592`). It never
  calls `run_selftest` and never greps the printed diagnostic, which is emitted only at
  `:2115-2116`.
- No other case covers the message: the only selftest cases that touch the base resolver are
  the dirty-TMPDIR pair at `tools/tsukuroi-census.sh:3544-3572` (which also call
  `selftest_base_dir` directly) and `R49-C3`; no case re-invokes the script's `--selftest`
  path (`grep -n -- --selftest` finds only the usage text, the `--identity --selftest`
  usage-error case at `:3536`, and the argument parser at `:3669`).

Finding for the L1 (coverage, not a contract change): C3's `diag_ok` proves the strings exist,
not that the exhausted-band path emits them. A case that captures stderr of `--selftest` under
an exhausted band (e.g. re-invoking `"$BASH" "$SELF" --selftest` with `SELFTEST_FD_BAND='240 241'`
and asserting `fd band 240 241 exhausted`) is what M1 shows is missing.

## M2 — KILLED, and killed by band_ok, not by diag_ok

Mutant (`m2.diff`, 514 B): `tools/tsukuroi-census.sh:2091` `ST_BASE_ERR=fd-band` ->
`ST_BASE_ERR=fd-band2`; the R49-C3 case is kept unchanged. Observed: `band_ok 0`, case line
`FAIL selftest: exhausted fd band must name err=fd-band (got 'fd-band2') (R49-C3)`,
summary `FAIL (167 cases, 166 passed, 1 failed)`, counter rc 1 → `band_ok`
(`check-fd-band-r49.py:104-106`) catches it through the failing `R49-C3` line.

Answer to the item's question: yes, `band_ok` catches it — and note `diag_ok` stayed **1**,
because the stale-free comment at `tools/tsukuroi-census.sh:3576` still contains the literal
`ST_BASE_ERR=fd-band`. A rename that also updated that comment would leave the diag leg
blind; the kill here rests on the case line alone. The runtime message also degrades exactly
as in M1 (`diag-probe.txt`: `cannot host the fixture tree (fd-band2; …)`), which the counter
cannot see.

## M3 — KILLED by stale_ok (deterministic, textual)

Mutant (`m3.diff`, 599 B): one inert comment line `# The gate builds a /tmp fixture tree for
its hermetic selftest.` inserted before `tools/tsukuroi-census.sh:415`. Observed `stale_ok 0`
→ counter FAIL (rc 1). Attribution: `STALE` is matched against the whole file
(`check-fd-band-r49.py:44`, `:91`), so the added comment alone flips it; the comment has no
runtime effect, which is correct for a claim about a comment. The same run also reported
`167 cases, 165 passed, 2 failed` — both failures are the host flake, not the mutation
(`diag-m3.out:34,133`).

## M4 — SURVIVED: the named limit (self-reported case count)

Mutant (`m4.diff`, 1908 B): the whole `R49-C3` probe block
(`tools/tsukuroi-census.sh:3577-3601`) is replaced by an unconditional
`ok 'selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)'`.
Printed count is unchanged at 167 because `ok`/`bad` are the only case counters
(`:2214-2215`, summary at `:3605`), so the suite now exercises 166 cases and reports 167.
Observed: `band_ok 1`, `cases 167`, case line PASS, summary
`PASS (167 cases, 167 passed, 0 failed)`, counter rc 0 → **PASS**. The counter accepts it, as
the item predicted.

Why: `cases` and `case_pass` are both read from the census's own stdout
(`check-fd-band-r49.py:103-106`); `band_ok` folds `cases == TARGET_CASES` into the same
conjunct, so no leg recomputes the number of assertions, and no leg checks that the `R49-C3`
line was produced by a comparison rather than typed. `stale_ok`/`diag_ok` remain satisfied
because the strings survive. This is the limit of the C3 counter: it validates the census's
self-report, not the suite's content. (A distributor of this mutant would need to forge the
PASS line too; the count alone is not the weak point.)

## Host flake contaminating band_ok (operability, incidental to C3)

3 of my 6 selftest-bearing runs reported failures unrelated to the bytes under test, always
the same assertion:

```
diag-m3.out:34:FAIL blocked: empty local db is not a pass (D02): hostname override not honoured — possible host read
diag-m3.out:133:FAIL healthy: one readable record of a mounted fsid reads RECORDED; other names are ignored (R44-C1): hostname override not honoured — possible host read
```
(`.ufo/waves/round-49/w1/R49MutFd/diag-m3.out`; 0 occurrences in `diag-freeze.out` and
`diag-m1.out`.)

Affected runs: counter-m1 (1 failure → false FAIL), counter-m3 (2), direct-m3 (2). Unaffected:
counter-freeze, direct-freeze, direct-m1. The assertion is
`tools/tsukuroi-census.sh:2373-2374` on the identity header composed at `:3694-3696` from
`HOSTNAME_FILE` (`:479`); the two failing checks use the default fixture with no hostname
override (`:2625`, `:3317`). Host at the time: `loadavg 68.36 68.42 59.10`, 14 GB available,
`journalctl -k --since -40min` showed no OOM lines — mechanism not identified, so I make no
causal claim. Consequence for C3: `band_ok` requires `selftest_rc == 0` and `failed == 0`, so
one such flake makes the frozen predicate FAIL on unmodified bytes; the counter has no retry.
Recommend the L1 treat a single `band_ok 0` on the freeze revision as inconclusive (rerun)
rather than as evidence about the claim.

## Restoration / provenance

- No lane, fleet or sibling file was written; the lane was read only via
  `git -C …/tsukuroi-shokunin show 55c07cd…:<path>`. Re-derived after all probes:
  `git show 55c07cd…:tools/tsukuroi-census.sh | sha256sum` =
  `c66144d73da1ac376cfe756eab3a60340e18bce91d60abe24c444408b99a2e75`, identical to my pristine
  copy before the mutants were generated (`hashes.txt`), and the counter blob
  `852621eb…` likewise.
- Mutant bytes: `census-m1.sh 2ef9cb55…b9828c`, `census-m2.sh 0880784c…63d448`,
  `census-m3.sh 5a76d9c5…c1147`, `census-m4.sh 3a095148…cace9`; each is
  reproducible as `git show 55c07cd…:tools/tsukuroi-census.sh` + the matching `m*.diff`
  (498/514/599/1908 B) and each passes `bash -n`.
- Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49MutFd/` removed after copying receipts.
- Not done: no run of the counter at any revision other than 55c07cd…; no C1/C2 probe; no
  attempt to identify the hostname-flake mechanism beyond the load/journal observation above;
  no fifth mutant variant for the M4 "count-only, no forged PASS line" combination (it is
  caught by `case_pass`, `check-fd-band-r49.py:104` — read, not run).
