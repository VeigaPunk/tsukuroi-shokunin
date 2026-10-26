VERDICT: supports

Item C1-11 (no-harm for C1, milestone `r39/r40 counters no-regression`). Lane
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, base `0e5805a1f149bd2ed9fe0db2e0a832afb034a835`,
lane tip at dispatch `71851d636ab1bffaf8fee5016617c88878a666f1` (`git -C <lane> rev-parse HEAD` =
71851d63; working tree otherwise already dirty from other seats: `M tools/check-self-assessment.py`
plus untracked `.ufo/waves/round-41/*` — I touched nothing in the lane except this report and my
seat dir).

Two claims checked, both hold: (a) the round-39 and round-40 C1 counters still PASS at the round-41
tip; (b) the round-41 census change is confined to lines inside `run_selftest` and `probe_storage_arm`
is byte-identical.

## 1. Round-40 literals counter at tip: PASS (exit 0)

Command (run once, `--jobs 4`, `TMPDIR` in scratch; full output kept at
`.ufo/waves/round-41/w1/C1ExecPriorCounters/r40-literals-counter-tip.log`):

    python3 tools/score-selftest-literals-r40.py \
      --revision 71851d636ab1bffaf8fee5016617c88878a666f1 \
      --scratch /fast/scratch/hyaku/tsukuroi-r41/C1ExecPriorCounters/a --jobs 4

Observed receipt fields (exit 0, wall 185.34 s):

    "predicate": "baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5"
    "baseline_pass": 1
    "baseline": {"exit": 0, "last": "TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)", "pass": true}
    "neutral_pass": 3            # N1-rename-counter, N2-double-bracket, N3-awk-field all exit 0, 128/128
    "mutants_applied": 9         # M1..M9, each "occurrences": 1
    "survivors": 0, "survivor_names": []
    "selfref": 5
    "result": "PASS", "exit": 0

All nine mutants were killed with a nonzero exit and a `TSUKUROI_CENSUS_SELFTEST: FAIL (128 cases,
…)` last line (e.g. M3-VC-substring-btrfs / M5-a-grep-count / M6-b-fstype-casefold /
M7-e-guard-drops-blocked each 127 passed 1 failed; M1 122/6, M2 and M4 and M8 123/5, M9 126/2).

Predicate source: `tools/score-selftest-literals-r40.py:161` (`ok = (baseline_pass == 1 and
neutral_pass == len(NEUTRAL) and m_applied == len(MUTANTS) …`), `:164`, `:170`.

This is a no-regression statement, not a new claim: the same counter PASSed at the round-40 closure
revision — `grep -n '"counter": "score-selftest-literals-r40"' -A3
.ufo/waves/round-40/after/c1-final-aad0113.jsonl` gives `"revision": "aad01138d5…"` and line 128
`"result": "PASS"`.

## 2. Round-39 storage-hidden counter at tip: PASS (exit 0)

Command (run once; output kept at
`.ufo/waves/round-41/w1/C1ExecPriorCounters/r39-storage-hidden-counter-tip.log`):

    python3 tools/score-storage-hidden-r39.py \
      --revision 71851d636ab1bffaf8fee5016617c88878a666f1 \
      --scratch /fast/scratch/hyaku/tsukuroi-r41/C1ExecPriorCounters/b

Observed receipt fields (exit 0, wall 58.13 s):

    "hidden_matched": 2   # H1-hidden-empty, H2-hidden-absent -> state=BLOCKED … detail=mounts:btrfs-without-sysfs
    "views_matched": 3    # views 0/1/2 -> HEALTHY 2/3/0, DEGRADED 1/1/2, DEGRADED 2/3/9
    "fixtures_matched": 5 # F1 HEALTHY 0/0/0; F2 BLOCKED mounts:btrfs-without-sysfs; F3 BLOCKED mounts:unreadable;
                          # F4 HEALTHY 1/1/0; F5 BLOCKED mounts:btrfs-without-sysfs
    "live_match": 1       # live read of /sys/fs/btrfs -> HEALTHY 1/1/0
    "six_planes_all": 1
    "result": "PASS", "exit": 0

Predicate source: `tools/score-storage-hidden-r39.py:265-269`. Note the six-plane/fixture legs read
the census arms directly (no `--selftest`), so the round-41 selftest insertion is not on their path;
the PASS at tip is therefore positive evidence that the *arms* were not disturbed, which is the
stronger reading of "no harm".

## 3. Locality of the round-41 census change

    $ git -C <lane> diff --stat 0e5805a1… 71851d63… -- tools/tsukuroi-census.sh
     tools/tsukuroi-census.sh | 27 +++++++++++++++++++++++++++
     1 file changed, 27 insertions(+)

Zero deletions; a single hunk. `-U0` hunk header, printed verbatim:

    --- a/tools/tsukuroi-census.sh
    +++ b/tools/tsukuroi-census.sh
    @@ -3036,0 +3037,27 @@ STUB

Hunk table (one hunk ⇒ one enclosing function):

| hunk header (git) | base lines | tip lines added | enclosing function |
|---|---|---|---|
| `@@ -3036,0 +3037,27 @@ STUB` | insertion after base line 3036 | 3037–3063 (27) | `run_selftest` |

Caveat on the header text: git's bash `funcname` heuristic names the hunk `STUB`, which is *not* the
enclosing function. I attributed the hunk by brace-matched function extents over the census at each
revision (`^[A-Za-z_][A-Za-z0-9_]*\s*\(\)\s*\{` … matching `}`, 28 functions at both revisions):

    base: run_selftest 1928–3055, probe_storage_arm 1865–1925
    tip : run_selftest 1928–3082, probe_storage_arm 1865–1925

    inserted tip lines 3037–3063; enclosing function(s): [('run_selftest', 1928, 3082)]
    other functions overlapping 3037–3063: []
    functions matched by the regex with a start line between 1900 and 3100:
        [('run_selftest', 1928, 3082), ('rc_of', 1944, 1944), ('out_of', 1945, 1945), ('main', 3085, 3175)]

`rc_of`/`out_of` are the two one-line helpers nested inside `run_selftest`
(`rc_of() { local f="$fix/$1.rc"; … }`, `census:1944–1945` at tip), so they neither sit in 3037–3063
nor own any changed line; `main` starts at tip:3085, after the insertion.

`run_selftest` grew by exactly the 27 inserted lines (3055→3082); every one of the four new fixture
ids lives inside that range: `storage-mounts-mp-relative` tip:3039, `storage-mounts-src-uuid`
tip:3045, `storage-mounts-no-subvol-opt` tip:3051, `storage-mounts-two-btrfs` tip:3057.
All four new cases sit between two pre-existing ones: the context line just above the insertion is
base:3036 (`'^STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0$'`, the
R40-C1 exact-fstype case) and the line just below is base:3037 =
`case_home='storage-root-unreadable-mounted'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"`
(`git show 0e5805a1…:tools/tsukuroi-census.sh | sed -n '3034,3040p'`), so the insertion lands inside
`run_selftest`'s case sequence, which closes at base:3055 / tip:3082.

## 4. `probe_storage_arm` byte-identical at base and tip

awk-extraction (from the `probe_storage_arm() {` line through its closing `}` at column 0), 61 lines
at both revisions:

    0e5805a1f149bd2ed9fe0db2e0a832afb034a835  71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56  -
    71851d636ab1bffaf8fee5016617c88878a666f1  71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56  -

Whole-file digests differ exactly because of the insertion (recorded for completeness):

    base 032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733
    tip  646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95

(`--branch master` in both counters; the receipts' `branch_tip` equals the requested revision in both
runs, so the revision argument — not the working tree — is what was scored.)

## 5. Support checks that keep the two PASSes interpretable

- The previous counters themselves did not move: `git diff --stat 0e5805a1… 71851d63… -- tools/`
  lists only `tools/check-package-anatomy-r41.py` (new, +405), `tools/score-selftest-mounts-r41.py`
  (new, +313) and `tools/tsukuroi-census.sh` (27 insertions). `score-selftest-literals-r40.py` and
  `score-storage-hidden-r39.py` are byte-identical at base and tip, so any change in their verdict
  would have to come from the census.
- `selfref` (the r40 counter's anti-self-read leg, `SELFREF_RE` at
  `tools/score-selftest-literals-r40.py:54`, base count 5) is statically unchanged: my independent
  match over the census gives 5 at base and 5 at tip, on the same five lines — 427
  `SELF=${BASH_SOURCE[0]}`, 1522 `$0 == "__MAP__"`, 2169 `"$BASH" "$SELF"`, 2209 (`check_cli`
  comment), 2216 `out=$("$BASH" "$SELF" "$@" 2>&1)`. The four inserted cases add no self-read, so the
  counter's `selfref == 5` leg is not satisfied by accident of the change.
- The mutant/neutral `old` texts still occur exactly once, which is *why* `mutants_applied == 9`
  rather than a FAIL: the receipt reports `"occurrences": 1` for all 9 mutants and all 3 neutrals, and
  the arm they target hashes identically at both revisions (§4).
- No fixture-id collision: `grep -o "case_home='[^']*'"` over the tip census yields 125 ids, none
  duplicated (`sort | uniq -c | awk '$1>1'` empty), so the four new cases get their own `$work/fx/*`
  directories instead of overwriting an existing fixture.
- The new cases are coherent with the arm they test: `fx_default` (`census:2022-2111` at tip; its only
  `btrfs` mention is the comment at 2034, so it creates no `$d/btrfs` and a btrfs-free mount table,
  2035) and each new case overwrites `$FX/mounts` with a table whose third field is `btrfs`, so
  `fsn==0 && blocked==0` reaches the mounts branch and the expected line
  `state=BLOCKED … detail=mounts:btrfs-without-sysfs` is the one the arm produces (fixture lines
  3039/3045/3051/3057 in the tip diff).

## What I did not do

- No base-revision run of either counter (a PASS at tip is the no-harm condition; a base run would
  only add a comparison point). I likewise did not re-run either counter a second time.
- I did not score the round-41 counter `score-selftest-mounts-r41.py`, did not check its kill
  attribution, decoy, or the 13-mutant/4-param predicate — other seats hold those items; §5 only
  notes that the fixtures its claim relies on are present in `run_selftest`.
- No package/tool installation or upgrade (nothing needed; `python3` 3.14 stock).
- No writes outside this report and `.ufo/waves/round-41/w1/C1ExecPriorCounters/`; scratch
  `/fast/scratch/hyaku/tsukuroi-r41/C1ExecPriorCounters/` removed after copying receipts. No git
  index, jj state, host service, sysfs, mount or /etc change; no sudo.

## Receipts

- `.ufo/waves/round-41/w1/C1ExecPriorCounters/r40-literals-counter-tip.log` — full JSON receipt of §1
- `.ufo/waves/round-41/w1/C1ExecPriorCounters/r39-storage-hidden-counter-tip.log` — full JSON receipt of §2
- `.ufo/waves/round-41/w1/C1ExecPriorCounters/census-locality-evidence.txt` — §3/§4 raw command output
  (diffstat, hunk header, awk-extracted `probe_storage_arm` sha256 at both revisions, whole-file sha256)

## Risks

- Host load was high during both runs (load average 45–60 on 32 CPUs): the literals counter took 185 s
  wall at `--jobs 4` and the storage counter 58 s. Neither run hit its timeout (2700 s / 1800 s
  ceilings I set) and neither showed a retry or a partial receipt, so latency did not affect the
  verdicts — but both counters are load-sensitive, and a queue-wait failure would surface as a
  `survivor`/mismatch rather than an error, which is the one place a loaded host could fake a FAIL.
  Nothing here did.
