VERDICT: defect-found

# C1-3 — held-out literal/position mutants of the STORAGE mount-table read (seat C1HeldOutMutants)

Item: write at least six NEW mutants of the mount-table read in `probe_storage_arm`, none in the
frozen MUTANTS list, each keyed on a literal or position the round-40 fixtures might still share;
apply each in a scratch copy of the census, run `bash <copy> --selftest` (TMPDIR in scratch),
record KILLED/SURVIVED and the killing case label; for survivors give a separating mount table
and the exact selftest case (bash) that kills it. Result: 9 held-out mutants, 6 KILLED,
3 SURVIVED; each survivor is killed by a separating table that was exercised in both directions
(pristine+table PASS, mutant+table FAIL).

## Target and method

Target: `tools/tsukuroi-census.sh` at f951f288483c1af0cef4afd458488b84cf7a2165 (lane tip at
dispatch — `git rev-parse HEAD` → `f951f288483c1af0cef4afd458488b84cf7a2165`; `git diff --stat
f951f288483c… -- tools/tsukuroi-census.sh tools/score-selftest-literals-r40.py` → empty, so the
pinned bytes are the working bytes). The mutated block is the mount-table read inside
`probe_storage_arm`: guard `if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]` at
tools/tsukuroi-census.sh:1906, table read at :1910-1918; the counted block ("LOOP",
tools/tsukuroi-census.sh:1912-1915) is:

```bash
      while read -r _src _mp fst _rest; do
        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
      done <<< "$mtab"
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
```

Method mirrors the frozen counter (tools/score-selftest-literals-r40.py:11-16 method paragraph,
:57-66 LOOP constant, :68-81 MUTANTS, run env :98): census text from `git -C <lane> show
f951f288…:tools/tsukuroi-census.sh` (read-only; 176385 bytes, sha256
`032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733`); each mutant an exact
substring replacement of LOOP, applied because `text.count(LOOP) == 1` (driver output: "LOOP
occurrences=1 / LOOP starts at line 1912"); each variant run as `bash <copy> --selftest` with
`PATH=/usr/bin:/bin`, `LC_ALL=C`, `HOME=<run dir>`, `TMPDIR=<run dir>/tmp`, cwd `/`. KILLED =
exit != 0 or the last stdout line is not `TSUKUROI_CENSUS_SELFTEST: PASS (…, 0 failed)`.

Novelty: none of the nine replacement strings equals any frozen M1-M9/N1-N3 replacement —
checked by importing tools/score-selftest-literals-r40.py read-only and comparing strings
(output: `H1…H9: duplicate_of_frozen=False` for all nine; `my LOOP identical to counter LOOP:
True`). The frozen list is M1-VA-device-literal, M2-VB-root-mountpoint, M3-VC-substring-btrfs,
M4-VG-subvolid-256, M5-a-grep-count, M6-b-fstype-casefold, M7-e-guard-drops-blocked,
M8-subvol-at-literal, M9-last-line-only (tools/score-selftest-literals-r40.py:68-81).

## Baseline

Command: `bash <pristine copy> --selftest` (env as above). Observed: exit 0,
`TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)` — same case count as the
frozen receipt's baseline (`.ufo/waves/round-40/after/c1-after-c707e35.jsonl`, `"baseline"`
`"last": "TSUKUROI_CENSUS_SELFTEST: PASS (124 cases, 124 passed, 0 failed)"`).

## Results — nine held-out mutants

| mutant | key (literal / position) | verdict | killing case(s) — label from the run's FAIL lines |
|---|---|---|---|
| H1-btrfstrw-adjacency | whole-table `case $mtab in *' btrfs rw'*` | KILLED | storage-mounts-varied-multi (1 case failed) |
| H2-relatime-option | whole-table `*relatime*` | KILLED | storage-absent, storage-hidden-absent, storage-hidden-empty, storage-mounts-btrfs-in-path, storage-mounts-fstype-case (5 failed) |
| H3-dumppass-fields | whole-table `*' 0 0'*` | KILLED | storage-absent, storage-mounts-btrfs-in-path, storage-mounts-fstype-case (3 failed) |
| H4-first-line-only | first line only: `IFS=' ' read -r _src _mp fst _rest <<< "$mtab"` | KILLED | storage-hidden-absent, storage-mounts-varied-home, storage-mounts-varied-multi (3 failed) |
| H5-mountpoint-absolute | counts only when `[[ ${_mp:-} == /* ]]` | **SURVIVED** | — |
| H6-source-devonly | counts only when `[[ ${_src:-} == /dev/* ]]` | **SURVIVED** | — |
| H7-threshold-two | `if [ "$mt" -gt 1 ]` | KILLED | storage-hidden-absent, storage-hidden-empty, storage-mounts-varied-home, storage-mounts-varied-multi (4 failed) |
| H8-options-ro-only | counts only when `[[ ${_rest:-} == ro,* ]]` | KILLED | storage-hidden-absent, storage-hidden-empty, storage-mounts-varied-home (3 failed) |
| H9-subvolkey-option | whole-table `*'subvol='*` | **SURVIVED** | — |

Every killed mutant: exit 1, last line `TSUKUROI_CENSUS_SELFTEST: FAIL (124 cases, N passed, M
failed)`; every survivor: exit 0, `… PASS (124 cases, 124 passed, 0 failed)`. Full FAIL lines
(with the harness "got:" text) and per-run exits: receipts `runs-log.txt`, `results.json`;
per-mutant unified diffs: receipts `<name>.diff`.

Killing-label notes worth keeping:

- H1 is killed by exactly one case — storage-mounts-varied-multi, whose btrfs line is the only
  `ro` one (tools/tsukuroi-census.sh:3021). Every other must-block table has `btrfs rw`
  adjacency (:2980, :2985, :3013). Drop that one ro fixture and a ` btrfs rw` adjacency arm
  passes 124/124.
- H4 is NOT killed by storage-hidden-empty: its table's only line is the btrfs line
  (tools/tsukuroi-census.sh:2985), so first-line-only still counts it. The other three
  must-block tables all have btrfs off line 1.
- H2 and H3 are killed partly through non-btrfs lines carrying the literal (the fx_default
  table's ext4 line `rw,relatime … 0 0`, tools/tsukuroi-census.sh:2035; the ext4/BTRFS lines of
  the two must-stay-healthy R40 cases, :3028, :3033) — option/field literals leak across lines.

## Survivors — three counter-sufficiency defects

The four must-block btrfs tables (storage-hidden-absent :2980, storage-hidden-empty :2985,
storage-mounts-varied-home :3012-3014, storage-mounts-varied-multi :3019-3022) still share four
shapes that the round-40 variation did not vary: mountpoint always absolute, source always
`/dev/*`, every btrfs line carries a `subvol=` option key, and exactly one btrfs line per table.
An arm keyed on any of those shapes passes the selftest 124/124.

### H5-mountpoint-absolute (SURVIVED)

Mutant (receipts `H5-mountpoint-absolute.diff`): counts only when the mountpoint is absolute —

```bash
        if [ "${fst:-}" = btrfs ] && [[ ${_mp:-} == /* ]]; then mt=$((mt + 1)); fi
```

Separating mount table (fstype field still `btrfs`, mountpoint `btrfs` is not absolute):

```
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
devtmpfs btrfs btrfs rw 0 0
```

Exact selftest case (bash) that kills it — proposed addition after tools/tsukuroi-census.sh:3035:

```bash
  case_home='storage-mounts-mp-relative'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    'devtmpfs btrfs btrfs rw 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs line counts by fstype alone, mountpoint need not be absolute (held-out H5)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'
```

Exercised (as a patch of the storage-mounts-varied-home fixture table, receipts
`H5-mountpoint-absolute.separating.diff`): pristine+table → exit 0, `PASS (124 cases, 124
passed, 0 failed)`; mutant+table → exit 1, `FAIL (124 cases, 123 passed, 1 failed)`, FAIL label
`healthy rollup: a btrfs /home on another device and options, not last, is BLOCKED (R40-C1)`.

### H6-source-devonly (SURVIVED)

Mutant (receipts `H6-source-devonly.diff`): counts only when the source starts with `/dev/` —

```bash
        if [ "${fst:-}" = btrfs ] && [[ ${_src:-} == /dev/* ]]; then mt=$((mt + 1)); fi
```

Separating mount table (btrfs source not under /dev):

```
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw 0 0
```

Exact selftest case (bash):

```bash
  case_home='storage-mounts-src-uuid'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    'UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs line counts by fstype alone, source need not be /dev/* (held-out H6)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'
```

Exercised (receipts `H6-source-devonly.separating.diff`): pristine+table → exit 0, `PASS (124
cases, 124 passed, 0 failed)`; mutant+table → exit 1, `FAIL (124 cases, 123 passed, 1 failed)`,
same FAIL label as H5.

### H9-subvolkey-option (SURVIVED)

Mutant (receipts `H9-subvolkey-option.diff`): whole-table option-key literal —

```bash
      case $mtab in *'subvol='*) blocked=1; detail+='mounts:btrfs-without-sysfs,' ;; esac
```

Round 40 varied the subvol VALUES (`subvol=/@` :2980/:2985, `subvol=/` :3013,
`subvol=/machines` :3021) but every btrfs line still carries the `subvol=` KEY, and no
non-btrfs fixture line does, so the mutant agrees with the correct arm on all 124 cases.

Separating mount table (btrfs line with no `subvol=` option):

```
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0
```

Exact selftest case (bash):

```bash
  case_home='storage-mounts-no-subvol-opt'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    '/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs line counts by fstype alone, options need no subvol= key (held-out H9)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'
```

Exercised (receipts `H9-subvolkey-option.separating.diff`): pristine+table → exit 0, `PASS (124
cases, 124 passed, 0 failed)`; mutant+table → exit 1, `FAIL (124 cases, 123 passed, 1 failed)`,
same FAIL label as H5.

## Reading

The frozen predicate (tools/score-selftest-literals-r40.py:26-28) proves `survivors == 0` over
M1-M9 only — the receipt records exactly that (`.ufo/waves/round-40/after/c1-after-c707e35.jsonl`:
`"survivors": 0`, `"result": "PASS"`). Held out of that set, three of nine same-class mutants
survive, so the round-40 fixtures do not yet pin the arm's contract "count every line whose
third field is exactly `btrfs`, regardless of source shape, mountpoint shape, option keys, or
how many btrfs lines a table has". Residual monoculture, by shape:

1. mountpoint always absolute (H5);
2. source always `/dev/*` (H6);
3. `subvol=` key present on every btrfs line — values were varied, the key was not (H9);
4. exactly one btrfs line per table (H7 is killed only because every table has fewer than two;
   a two-btrfs-line table would additionally pin the count direction);
5. the rw/ro split carries the kill for adjacency literals: H1 (` btrfs rw`) dies only on the
   single ro fixture (:3021); H8 (ro-only) dies only on the three rw tables.

Reachability caveat, stated plainly: on a live `/proc/self/mounts`, mountpoints are absolute and
btrfs sources are `/dev/*`, so H5/H6 arms would agree with the correct arm on the live host, and
current kernels normally display `subvol=` for btrfs (H9 mostly agrees live). But the census
reads an overridable file — `PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}`
(tools/tsukuroi-census.sh:463), served from the fixture at :2166 — so the arm's tested contract
covers arbitrary tables, and the hermetic selftest is where that contract is pinned. These are
counter-sufficiency defects (fixture coverage gaps), not observed live-host bugs.

## Proposed draft text (exact, for the selftest)

Add the three cases above (H5, H6, H9) after the `storage-mounts-fstype-case` block
(tools/tsukuroi-census.sh:3032-3035), before `storage-root-unreadable-mounted` (:3037). They are
the exact `check` calls whose tables and expected regexes were exercised in this item; what was
run patched each separating table into the existing storage-mounts-varied-home case (same
harness, same expected regex, label unchanged), not as new named cases — running them as
standalone cases in the census is the one step this seat did not do (read-only seat; the census
is lane content).

## Bounds, tooling, what I did not do

- Read-only on the lane: the only writes were this report and the seat receipt dir
  `.ufo/waves/round-40/w1/C1HeldOutMutants/`. Git usage limited to `rev-parse`, `cat-file -t`,
  `diff --stat`, `show` (all read-only); no index/jj state touched; no sibling lane, fleet repo,
  or shokuknow access.
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1HeldOutMutants/` held every copy, mutant and
  TMPDIR; receipts were copied out first, then the scratch dir was removed (verified below).
  No /tmp paths were used as evidence.
- No host mutation of any kind: no packages, services, mounts, sysfs, /etc, no sudo, no pacman;
  no processes signalled. No tools were installed (bash, python3, git sufficed).
- Leaf seat: no subagents, no `agent://all` messages.
- Not done: the frozen counter itself was not re-run (its receipt already records the declared
  predicate at c707e356; this item worked at the itemized tip f951f288, which was not
  re-verified against c707e356 beyond the empty diff noted above); the three proposed cases were
  not added to the census (read-only seat); killed mutants were run once each, not repeated.

## Receipts (seat dir `.ufo/waves/round-40/w1/C1HeldOutMutants/`)

- `H1-btrfstrw-adjacency.diff` … `H9-subvolkey-option.diff` — nine unified diffs,
  pristine→mutant, census :1912-1915 region (418-757 bytes each).
- `H5-mountpoint-absolute.separating.diff`, `H6-source-devonly.separating.diff`,
  `H9-subvolkey-option.separating.diff` — the separating-table patches (varied-home fixture).
- `results.json` — all 16 runs: rev, census sha256, exit, last line, verdict, full FAIL lines.
- `proof-results.json` — the six separating-table proof runs.
- `runs-log.txt` — trimmed per-run log (last line + every FAIL line, untrimmed text).
- `driver.py`, `proof.py` — the exact runners (method evidence).
