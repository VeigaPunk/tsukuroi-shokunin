VERDICT: defect-found

Item C1-M1 — mutation test of the C1 fix (`selftest_base_dir` fd-alias, r48 lines 2058-2090)
and its two new selftest cases (lines 3538-3555). Subject: the frozen blob
`tools/tsukuroi-census.sh` at ae99f021b76f8eb1c8805d32d80644464afb1ff6, sha256
375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426 (verified on the scratch
copy before mutation). All scratch copies restored to that exact hash after the probes
(restoration evidence below); no lane file touched.

## Detector and baseline

Detector: `bash census-<mutant>.sh --selftest` under `TMPDIR=<scratch>/spaced tmp`
(a real, writable, space-bearing scratch TMPDIR at
`/fast/scratch/hyaku/tsukuroi-r48/TMutFixA/spaced tmp`). Runs sequential, one at a time.
FAIL labels printed by `bad()` (line 2197) go to stderr.

Baseline (pristine, spaced TMPDIR): rc 0, 68.6 s,
`TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` — receipt
`TMutFixA/pristine.log`. Baseline pass confirmed; every failure below is mutant-caused.

## Mutants and verdicts

### M1 — dirty branch returns the plain path, no fd alias — KILLED by the selftest

Diff (`TMutFixA/diff-m1.txt`): replaced lines 2079-2086 (the 240-249 scan, `exec ${fdn}<`,
`ST_BASE_DIR=/proc/self/fd/$fdn`) with `ST_BASE_DIR=$base`; kept `[ -d "$base" ] || return 1`.

`TMPDIR="<scratch>/spaced tmp" bash census-m1.sh --selftest` → rc 1, 86.1 s,
`TSUKUROI_CENSUS_SELFTEST: FAIL (166 cases, 15 passed, 151 failed)` — receipt
`TMutFixA/m1.log` (151 `FAIL ` lines). Kill cases include:

- `FAIL selftest: dirty TMPDIR must resolve to a /proc/self/fd alias inside TMPDIR (R48-C2)`
  — the NEW case A (line 3545/3547): `root_locator_class("$work/../spaced tmp/...")`
  returns 'unsafe', not 'absolute' → `bad`.
- `FAIL selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)`
  — the older line-3526 case.
- ~149 fixture cases, e.g. `FAIL blocked: pacman db.lck: configured root not asserted at a
  field boundary (wanted root_dir=/fast/scratch/.../spaced tmp/.../fx/blocked-lck/root;
  possible live-root read)` and dozens of `exit 2 wanted 0/1` census cases: every
  space-bearing root override was refused 'unsafe' by `root_locator_class`, so probes fell
  back to the live root. The mutation is massively over-killed — the new case is one of
  three independent detectors.

### M2 — alias fd taken as the lowest free fd (240-249 loop dropped) — KILLED by the selftest

Diff (`TMutFixA/diff-m2.txt`): lines 2079-2084 replaced by `eval "exec {fdn}<\"\$base\""`
(bash auto-allocation → fd 10, since the selftest shell's fds stop at 9).

`--selftest` under spaced TMPDIR → rc 1, 111.3 s,
`FAIL (166 cases, 165 passed, 1 failed)` — receipt `TMutFixA/m2.log`. The single kill case:

- `FAIL identity: a parent-held descriptor on a relinked decoy is never hashed (R46-C1):
  exit 126 wanted 0; output: /usr/bin/bash: /proc/self/fd/10/tsukuroi-r3-2-selftest.XXXXXX/identity/held.sh: Not a directory`

  Exactly the failure mode the r48 comment at lines 2064-2070 documents (observed
  2026-10-28): the fixture child `exec 10<held.decoy` re-points the inherited fd 10, so
  every `$work`-relative path spelled `/proc/self/fd/10/...` resolves through the decoy
  regular file. The fd-10 alias is inherited harmlessly by children that never re-point
  it, which is why exactly ONE of 166 cases fails — the only fixture child that `exec 10<`.
  Note: the killer is the PRE-EXISTING R46-C1 'held' case, not an R48-C2 case; the new
  dirty-TMPDIR case still passes under M2 because its inner `selftest_base_dir` call
  allocates fd 11 (fd 10 already held by the outer alias). The 240-249 band has no
  dedicated R48 pin — its only regression detector is the incidental R46 case (see
  coverage notes).

### M3 — nonexistent-TMPDIR branch falls through to /tmp — KILLED by the selftest

Diff (`TMutFixA/diff-m3.txt`): line 2078
`[ -d "$base" ] || return 1` → `[ -d "$base" ] || { ST_BASE_DIR=/tmp; ST_BASE_FD=; return 0; }`.
This spelling was chosen deliberately: it resurrects the r47 `/tmp` fallback while dodging
the counter's `static_leg` regex `(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])` — verified: the
regex matches `st_base=/tmp` but NOT `ST_BASE_DIR=/tmp` or `base=/tmp/` — so this mutant
isolates the selftest kill from any static-leg kill.

`--selftest` under spaced TMPDIR → rc 1, 79.9 s,
`FAIL (166 cases, 165 passed, 1 failed)` — receipt `TMutFixA/m3.log`. The single kill case:

- `FAIL selftest: nonexistent dirty TMPDIR must fail the base resolver (R48-C2)` — the NEW
  case B (lines 3550-3554): with the fallback, `TMPDIR="$work/fx/definitely missing dir"
  selftest_base_dir` returns 0 with `ST_BASE_DIR=/tmp` → `bad` fires.

So the second new case DOES fail on a resurrected /tmp fallback — the fix's fail-fast
contract is pinned by the selftest alone. (Counter legs that would also fire on a full
counter run, not run: `failfast` legs would log a mktemp row under /tmp, `spaced` loc_ok
would break. Also of record: a mutant written `st_base=/tmp` — the original r47
lowercase spelling — trips `static_leg` as well; the case-sensitive regex does not cover
uppercase `ST_BASE_DIR=/tmp` or a trailing-slash `base=/tmp/`, a small static-leg gap.)

### M4 — the readlink comparison in the first new case made vacuous — SURVIVED (coverage defect)

Diff (`TMutFixA/diff-m4.txt`): line 3544
`[ "$(readlink -f -- "$r48_base")" = "$(readlink -f -- "$r48_dir")" ]` →
`[ "$(readlink -f -- "$r48_base")" = "$(readlink -f -- "$r48_base")" ]` (tautology; the
only assertion that binds the alias's resolution to inside-TMPDIR is neutralized).

- Selftest under spaced TMPDIR → rc 0, 54.8 s,
  `PASS (166 cases, 166 passed, 0 failed)` — receipt `TMutFixA/m4.log`.
- Frozen counter run: `python3 counter.py --census census-m4.sh --work <scratch>/counter-work-m4`
  → rc 0, 154.6 s, JSON `"verdict": "PASS"` with pass_ok=4 loc_ok=4 clean_ok=4
  failfast_ok=2 term_ok=1 static_ok=1 and `census_sha256` = the mutant hash
  `071b942514c4df8ebd804475786acedb599dc0e440eaebe8021c278df9037f6c` (proving the mutant
  file, not the pristine, was tested) — receipt `TMutFixA/m4-counter.json`.

VERDICT: SURVIVED — neither the selftest nor the frozen counter detects that case A lost
its discriminating assertion. This is a coverage defect in the counter's static leg: the
`in-TMPDIR` property of the fd alias is asserted at exactly ONE text site (line 3544),
and the static leg only greps for `*base*=/tmp` assignments and the phrase "or /tmp
itself" — nothing pins the case's assertion text or an equivalent binding.

Honest qualification: no added RUNTIME case can kill M4 — the real mechanism is
unmutated, so any correct runtime assertion of the same property still passes. What can
kill it:

(a) exact proposed kill — a static binding on the case text, added to
    `static_leg` in tools/score-selftest-tmpdir-r48.py:

        if '"$r48_base")" = "$(readlink -f -- "$r48_dir' not in text:
            bad.append('R48-C2 case lost its in-TMPDIR readlink binding (M4-class mutant)')

    On the M4 file this appends a problem → static_ok=0 → counter FAIL (the mutated line
    compares `$r48_base` to itself, so the needle `"$r48_dir` is absent). Verified by
    inspection against counter.py lines 147-158; the identical code shape works because
    `static_leg` already does full-text substring search for "or /tmp itself".

(b) defense-in-depth runtime double-binding (does NOT kill M4 — the correct mechanism
    still passes it — but re-derives the in-TMPDIR property at a second, mutation-
    independent site so a single edited assertion can never silently carry the contract;
    add after line 3555, inside the same `r48_` block):

        # (R48-C2) second binding of the in-TMPDIR contract: a file created through the
        # resolved base must land inside the dirty TMPDIR itself — never /tmp — and the
        # resolved alias must not equal the raw dirty path either.
        r48_probe=
        if [ -n "$r48_base" ] && : >"$r48_base/.r48-probe" 2>/dev/null; then
          r48_probe="$r48_dir/.r48-probe"
          { [ -f "$r48_probe" ] \
            && [ "$(dirname "$(readlink -f -- "$r48_probe")")" = "$(readlink -f -- "$r48_dir")" ] \
            && [ "$(readlink -f -- "$r48_dir")" != "$(readlink -f -- /tmp)" ]; } \
            && ok 'selftest: a file created via the fd alias lands inside TMPDIR, never /tmp (R48-C2)' \
            || bad 'selftest: the fd alias must write inside TMPDIR, never /tmp (R48-C2)'
        else
          bad 'selftest: the fd alias must be writable inside TMPDIR (R48-C2)'
        fi
        rm -f -- "${r48_probe:-}" 2>/dev/null || true
        unset r48_probe

    This kills the SEMANTIC class M4 proxy-for (an alias not resolving into TMPDIR) even
    where a reviewer-edit had weakened case A, without relying on case A's text.

## Summary table

| mutant | detector | selftest result | counter result | verdict |
|--------|----------|-----------------|----------------|---------|
| M1 plain dirty path | selftest | FAIL 151/166 (new R48-C2 case A + R47-C2 + ~149 fixture cases) | — | KILLED |
| M2 lowest-free-fd alias | selftest | FAIL 1/166 (R46-C1 'held' identity case, `fd/10 Not a directory`) | — | KILLED |
| M3 /tmp fallback (ST_BASE_DIR=/tmp) | selftest | FAIL 1/166 (new R48-C2 nonexistent-TMPDIR case B) | — | KILLED |
| M4 vacuous readlink in case A | selftest + counter | PASS 166/166 | counter PASS (all legs) | SURVIVED |

## Coverage findings

1. SURVIVOR M4: the in-TMPDIR binding exists once; nothing pins it statically. Kill via
   the static_leg needle proposed in (a); belt-and-suspenders runtime double-binding in (b).
2. M2's killer is incidental: the fd-band invariant is pinned only by the R46-C1 'held'
   identity fixture, not by any R48 case. If that identity case ever moves ahead of the
   tmpdir cases or is dropped, an auto-allocated alias regresses silently. An explicit
   `[ "$r48_fd" -ge 240 ] && [ "$r48_fd" -le 249 ]` assertion inside case A would pin the
   band directly. (Noted, not required: M2 is still killed today.)
3. `static_leg`'s BASE_ASSIGN regex is case-sensitive (`\w*base\w*=`): `ST_BASE_DIR=/tmp`
   and `base=/tmp/` both dodge it. Runtime legs still catch the behavior (M3 above), so
   this is a static-depth note, not an unkill hole.

## Restoration evidence

- `sha256sum` of all four mutant files after `cp census-pristine.sh census-<m>.sh`:
  all four read 375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426,
  byte-identical to the frozen blob (pristine copy fetched via
  `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ae99f021…:tools/tsukuroi-census.sh`,
  hash verified pre-mutation).
- Mutant diffs preserved in `TMutFixA/diff-m{1,2,3,4}.txt`; run logs in
  `TMutFixA/{pristine,m1,m2,m3,m4}.log`; counter JSON in `TMutFixA/m4-counter.json`.
- Scratch dir `/fast/scratch/hyaku/tsukuroi-r48/TMutFixA` removed at seat end after
  receipts were copied; the selftest's own fixture dirs were cleaned by its EXIT trap
  (counter clean_ok=4 also confirms fixture removal on the M4 run).

## Cost / environment notes

- 5 sequential selftests (~86/111/80/55/69 s) + 1 counter run (154.6 s, `--census` on the
  M4 mutant only); bash jobs run via a Python subprocess wrapper because the host bash
  job cap was saturated. TMPDIR used: `/fast/scratch/hyaku/tsukuroi-r48/TMutFixA/spaced tmp`.
- No tools installed; python3 + bash + git only. No lane writes outside this report and
  the receipt dir `TMutFixA/`.
