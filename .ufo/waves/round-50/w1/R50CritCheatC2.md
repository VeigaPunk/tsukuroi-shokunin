VERDICT: falsifies — the C2 counter (`tools/check-selftest-matcher-r50.py`) is cheatable: a 12-line census that runs no case at all scores `PASS` under `--runs 1` **and** under the counted `--runs 2`, with a JSON record identical to the real freeze census except `census_sha256`. A second, independent cheat keeps the exact round-49 `printf | grep -q` defect in the arms (brace-renamed to `"${out}"`) and also scores `PASS`.

Seat: R50CritCheatC2 (item C2-B4, cheat the C2 counter). Lane read-only; freeze `8029cdba1049df25632c91a23c8db4eefb54be5f`; base `b866a1d3d26616119a089f1a69b080136becc17b`. All work in `/fast/scratch/hyaku/tsukuroi-r50/R50CritCheatC2`, receipts in `.ufo/waves/round-50/w1/R50CritCheatC2/`.

## Axes (godspeed)
- **A1 cheat cost** — lines/skill needed to reach `verdict: PASS`.
- **A2 counter discrimination** — can a reader tell a cheat from the real fix by the counter's own output?
- **A3 defect coverage** — does `PASS` imply the SIGPIPE defect class is actually gone?
- **A4 provenance** — does the record bind the census bytes to the named revision?

## Fixtures and results (all `--census-file <fixture> --scratch /fast/scratch/.../ctr`)

| # | census | cost | `idiom_sites` | `cases` | `case_ok` | `pass_runs` | verdict | leg that decides |
|---|---|---|---|---|---|---|---|---|
| real | freeze census | — | 0 | 168 | 1 | 1 (`--runs 1`) | **PASS** (`freeze-baseline.json`) | all |
| (a) | base, `pkgline=$out`, 3 arms → `elif false`, 2 arms → `:` | 7 line edits | **0** | 167 | 0 | 0 | FAIL | `cases`, `case_ok`; the mutant's own selftest also FAILs 151/167 (`a-run.out`, first FAILs are the field-boundary assertion) |
| (a2) | base, arms vacuous as in (a) but `pkgline` via full-read awk | 6 line edits | **0** | 167 | 0 | 1 | FAIL | `cases`, `case_ok` only — selftest itself PASSes `167 cases, 167 passed, 0 failed` |
| (b) | base + `(R50-C2)` case, arms still on the pipe idiom | append 13 lines | **7** | 168 | 0 | 0 | FAIL | `idiom_sites` (7); the case itself false-missed `20/20` at 200 KB |
| (c) | **12-line liar**: prints 3 `PASS` lines incl. a `(R50-C2)` PASS and a fabricated summary; runs nothing | 12 lines, 0 skill | **0** | 168 | 1 | 2 | **PASS** (`c-result.json`, `c-result-runs2.json`) | none — all six legs satisfied |
| (d) | freeze census with the `(R50-C2)` case deleted (honest mutant) | delete 20 lines | 0 | 167 | 0 | 1 | FAIL | `cases`, `case_ok` — the counter *does* catch the honest mutant |
| (e) | freeze census, arms reverted to the pipe idiom written as `"${out}"` / `"${pkgline}"` | 5 line edits | **0** | 168 | 1 | 1 | **PASS** (`e-result.json`) | none — defect present, counter green |

### (a)/(a2) — the item's question
`idiom_sites == 0` **does** pass once the arms stop asserting anything: the leg is a literal-spelling counter, not an assertion checker. The selftest does **not** print 168 cases — base has 167 (`a2-result.json`: `TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)`), so the mutant fails only on `cases`/`case_ok`. The crude variant (a) additionally broke the census's own field-boundary assertion (`pkgline=$out` feeds the whole output to a check written for the single packages line, 151/167 FAIL in `a-run.out`); (a2) removes that noise and isolates the answer.

### (b) — case present, arms on the pipe idiom
Fails on `idiom_sites == 7` (this is the limit the counter docstring itself names, lines 29–32). Its `(R50-C2)` line also self-reports `FAIL ... (20/20 false misses)`, so two legs fire.

### (d) — honest mutant
Caught: `cases 167`, `case_ok 0`, `pass_runs 1`, verdict FAIL. The counter is not blind to a *deleted* case.

## Counterexample 1 — the liar (c) is indistinguishable
`c-census.sh` (12 lines, listed in the receipts) ignores its argument, prints
`PASS ... (R50-C2)`, `PASS ...`, `PASS ...`, then
`TSUKUROI_CENSUS_SELFTEST: PASS (168 cases, 168 passed, 0 failed)` and exits 0.

Observed (`c-result-runs2.json`, the counted `--runs 2` form):
`{"case_ok": 1, "cases": 168, "census_sha256": "d066939e…", "full_misses": 0, "idiom_sites": 0, "pass_runs": 2, "verdict": "PASS"}` — rc 0.

Side by side with the real fix (`freeze-baseline.json`): `{"case_ok": 1, "cases": 168, "census_sha256": "aeda2cbc…", "full_misses": 0, "idiom_sites": 0, "pass_runs": 1, "verdict": "PASS"}`. The only differing field is `census_sha256`, which the counter itself prints and never compares to anything. **A reader cannot tell them apart from the counter's output**, and no leg of the predicate (`idiom_sites`, `base_misses`, `full_misses`, `cases`, `pass_runs`, `case_ok`) touches the census's behaviour: `base_misses`/`full_misses` are measured by the counter's own probe (counter lines 56–67, 105–107), the other four are regexes over stdout (lines 100–101, 116–128).

Why nothing catches it:
- `--census-file` skips the only provenance step: the revision is read only to `git cat-file -e` when *no* census file is given (counter lines 75–83), and the copied file is never compared to `git show <rev>:tools/tsukuroi-census.sh` (lines 88–97). The reported `revision` is an echo.
- The census's exit status is recorded but never used (line 121 `'rc': p.returncode`; line 129's `ok` omits it).
- Nothing cross-checks `cases` against the number of `PASS`/`FAIL` lines actually printed, nor `passed` against them.
- `SUMMARY_RE.search` takes the **first** match (line 54/120), so a real census that echoes a fabricated summary before its own would also win. [INFERENCE from the code path; not run.]

## Counterexample 2 — (e) keeps the defect and scores green
`e-census.sh` restores the round-49 idiom in the three must-match arms and the two evidence loops, spelled with braces:
`printf '%s\n' "${out}" | grep -q …`, `printf '%s\n' "${pkgline}" | grep -qE …` (5 executable sites). `IDIOM_RE` (line 53) requires the literal `"$out"` / `"$pkgline"`, so it scores **0** and the counter returns `verdict: PASS` (`e-result.json`).

The defect is not cosmetic — same probe, same 200 KB buffer, plain vs braced form (`probe-brace.sh`, observed):
```
PLAIN_MISSES 20
BRACED_MISSES 20
```
i.e. the braced spelling false-misses exactly as the banned one does, and `A3` is violated: `PASS` does not imply the defect class is gone. `A2` is violated for the same reason.

## Secondary defects found while cheating
1. Counter docstring line 16 says "6 at base b866a1d3"; `IDIOM_RE` measured over `base-census.sh` gives **7** sites (2381, 2384, 2386, 2390, 2391, 2401, 2432). The frozen claim's "167 -> 168 cases" and `idiom_sites == 0` are unaffected, but the doc's base number is wrong.
2. `--runs 1` prints the literal predicate `pass_runs == 2` while accepting `pass_runs == 1` (line 129 uses `a.runs`). The JSON `predicate` string is then false about its own run. The claim's counted invocation uses `--runs 2`, so this is a reporting defect, not a claim break.
3. `--census-file` mode also disables the `--scratch` requirement (lines 75–79), so the item's own prescription (`--census-file --runs 1`) is the weakest possible invocation — and it is the one that yields PASS for (c).

## Smallest safe correction (three legs; each is cheap and orthogonal)
Add to `run()` after the census text is read (counter line 98), and to the predicate:

```python
        # blob_match: the bytes under test must be the revision's bytes (kills a fabricated
        # --census-file: today the revision is only echoed, lines 75-83/88-97)
        blob = git(lane, 'show', f'{a.revision}:{CENSUS}')
        blob_match = 1 if blob.returncode == 0 and \
            hashlib.sha256(blob.stdout).hexdigest() == hashlib.sha256(open(census, 'rb').read()).hexdigest() else 0
        # pass_lines: the summary must be backed by real case output
        pass_lines = sum(1 for ln in out.split('\n') if ln.startswith('PASS '))
        # per run, alongside pass_runs:
        #   if p.returncode == 0 and pass_lines == cases: pass_runs += 1
```

and replace the spelling-sensitive idiom leg (line 53) with a structural one applied only to the `run_selftest` body:

```python
IDIOM_RE = re.compile(r'\|\s*(?:grep\s+-[A-Za-z]*q|(?:[^|\n]*\|)\s*head\s+-n1)')
```

`blob_match == 1` alone kills (c) and (e) as delivered; the structural regex is what catches a *committed* census whose arms keep the pipe idiom under any variable spelling; `pass_lines == cases` plus `rc == 0` makes the summary non-fabricable and costs nothing. Predicate becomes
`idiom_sites == 0 and blob_match == 1 and base_misses > 0 and full_misses == 0 and cases == 168 and pass_runs == 2 and case_ok == 1`,
with `--runs` required to be 2 for a counted run (exit 2 otherwise).

## Impacted axes
A1 (cheat cost collapses to 12 lines / 5 edits) and A3 (defect survives a green verdict) are the binding ones; A4 is the root cause — the record never binds the census bytes to `8029cdb`. C2's *fix* in the freeze census is genuine (`buf_has`/`out_has` at freeze lines 2236–2239 read to EOF via awk, and the `(R50-C2)` case at 3643–3661 really exercises a 200 KB buffer), but the claim "the counter ... verifies" overstates: the counter verifies stdout shapes, not the census.

## What I did not do
- No committed-mutant test in the lane (read-only): (e) was run through `--census-file`, not as a committed census at a revision.
- No 168-`PASS`-line liar (would defeat `pass_lines` alone; only `blob_match`/structural legs stop it).
- No timing/ENOSPC observations; no tools installed.
- Did not run the counted `--runs 2` form on (a2)/(b)/(d)/(e) — each was `--runs 1` per the item; (c) was run both ways.
