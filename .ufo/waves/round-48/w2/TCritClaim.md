VERDICT: defect-found

C1-R4 counter-as-cheat attack on `tools/score-selftest-tmpdir-r48.py` (frozen at ae99f021). Two cheats PASS the frozen predicate; two fail as designed. All four runs used `--work /fast/scratch/hyaku/tsukuroi-r48/TCritClaim/w<k>`; receipts: ./m{1,2,3,4}.json and mutant bytes ./m{1,2,3,4}-*.sh; M2's 3-line diff from the frozen blob (sha 375aa73…) is ./m2.diff.

## Mutants and results

- **M1 do-nothing — PASS** (m1.json, verdict PASS, all legs 4/4/4/2/1/1). 8-line census: resolves `base=${TMPDIR:-/tmp}`, `[ -d ]` fail-fast, ONE `mktemp -d "$base/tsukuroi-r3-2-selftest.XXXXXX"`, EXIT/INT/TERM traps, 3 s stub "work", prints `PASS (166 cases, 166 passed, 0 failed)`. Runs zero cases in ~3 s (vs ~60 s real). Leg that should have caught it: **pass_ok checks only `rc == 0` and the last stdout line; the counter cannot distinguish 166 executed cases from 0** — the count string is trusted verbatim from the blob under test.
- **M2 decoy — PASS** (m2.json, verdict PASS). The FROZEN census with a 2-line patch (m2.diff): a decoy `mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX"` logs an honest in-TMPDIR creation through the PATH wrapper, while `work=$(/usr/bin/mktemp -d /tmp/r48cheat.XXXXXX)` does ALL real fixture work under /tmp via an absolute path the wrapper never sees. All 166 real cases ran and passed in /tmp. Leg that should have caught it: **loc_ok/clean_ok inspect only the single logged wrapper row; absolute-path mktemp calls and any second creation are invisible** (failfast_ok likewise demands only "no *logged* creation").
- **M3 absolute-path only — FAIL as designed** (m3.json, loc_ok=0, clean_ok=0, term_ok=0). Confirms the seat item's prediction: when nothing matching `tsukuroi-r3-2-selftest` goes through PATH, 0 creations are logged → `len(rows)==1` fails → loc/clean 0, and the TERM leg reports `no fixture appeared before exit`. The shadowed-PATH observation channel works — but only when the subject chooses to use bare `mktemp`; M2 shows the same channel is trivially satisfied by a decoy.
- **M4 TERM-leaves-fixture — FAIL as designed** (m4.json, term_ok=0, `fixture_removed: false`). TERM trap `trap - EXIT; exit 143` ends 143 with the fixture left behind; the leg catches it.

## Second cheats that pass for free (no run needed, same legs)

- **Mechanism not claimed by the counter**: C1's stated mechanism ("reaches a dirty TMPDIR through a /proc/self/fd/24x alias") is never asserted. M1 builds `mktemp -d "$base/…"` with the space INSIDE the quoted template — works fine under bash — and scores loc_ok=4 with zero /proc/self/fd involvement. The counter verifies the outcome, not the claimed mechanism.
- **failfast "no fixture anywhere" is not checked**: failfast_ok requires only `rc!=0`, no PASS line, and no *logged* row. A census doing `/usr/bin/mktemp -d /tmp/ff.XXXXXX` on missing TMPDIR still scores failfast_ok=2.
- **static_leg evasions**: `BASE_ASSIGN = r'(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])'` — `base=${TMPDIR:-/tmp}` (the /tmp fallback in disguise), `base="/tmp"`, `base=/tmp/$(x)` all miss (verified locally against the regex). `stbase= /tmp` is a syntax error anyway.

## Universals the counter does not enumerate

- "fixture lands in /tmp ONLY for unset and /tmp" → counter checks **one** creation per scenario; creations beyond the first, or via other channels (absolute paths, `mkdir` without mktemp), are unenumerated (M2 proof).
- "no fixture anywhere" on missing TMPDIR → only the wrapper log is "anywhere" (noted above).
- `selftest_base_dir`'s `/proc/self/fd` mechanism, the INT→130 path (only TERM is exercised; INT claimed in C1 text), read-only vs nonexistent TMPDIR, and TMPDIR-as-file vs -as-dir are all untested legs.

## Smallest safe corrections (for the L1)

1. Require the logged row to be the census's ONLY creation channel: after each scenario, glob `<work>/tmp-*`, the real TMPDIR and /tmp for `tsukuroi-r3-2-selftest.*`/`r48cheat`-shaped orphans; or intercept at the syscall layer (the counter already runs bash under `env -i`, so `strace -f -e mkdir` on the whole run, then assert every mkdir lands under the expected base).
2. Neutralize absolute-path evasion: prepend a `mktemp`-logging `env`/`bash` hook is fragile — better, run the subject with `BASH_ENV` or a preload shim, or simply audit the blob for `mktemp` calls with `/` in argv position 0 (static leg).
3. Make pass_ok count cases from output lines, not the self-reported total (or at minimum require `>= CASES` distinct `ok`/`check` lines before the summary).

## Cost / method notes

4 counter runs total (within the 4-run cap): M1/M3/M4 ~15 s wall each (do-nothing subject), M2 ~225 s (full 166-case work under /tmp + 7 invocations). Static-leg evasions tested locally against the regex, no run consumed. No lane bytes modified; scratch $S removed on… actually retained only m/* copies already moved to this dir — scratch cleaned below.
