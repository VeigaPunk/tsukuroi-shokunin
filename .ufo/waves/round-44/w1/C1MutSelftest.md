VERDICT: defect-found

# Seat C1MutSelftest — item C1-10: the C1-9 mutants (a)-(j), scored by the
# 7e081698d4fc3c4ea944884fd093058de9909de1 census's own `--selftest`

Scope: reuse the C1-9 mutant list (a)-(j) verbatim (w1-spec.json C1MutArm prompt),
score each with the census's own `--selftest` (TMPDIR in scratch), report which of
the nine `(R44-C1)` cases kill which mutant, and for every survivor propose an
extra `check` case that is red on the mutant and green on 7e081698; run both.

## 1. Method

- Pristine census extracted read-only from the lane at the implementation revision:
  `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 7e081698d4fc3c4ea944884fd093058de9909de1:tools/tsukuroi-census.sh`
  -> `/fast/scratch/hyaku/tsukuroi-r44/C1MutSelftest/pristine-census.sh`
  (sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c`; 3396 lines).
- All work under scratch `/fast/scratch/hyaku/tsukuroi-r44/C1MutSelftest/`; `export TMPDIR` there
  (selftest writes only under `$TMPDIR/tsukuroi-r3-2-selftest.*`).
- Baseline: `bash pristine-census.sh --selftest` -> rc=0,
  `TSUKUROI_CENSUS_SELFTEST: PASS (141 cases, 141 passed, 0 failed)` (~35 s).
- Ten single-site mutants built by editing scratch copies (one site each; `diff -u`
  receipts in the seat dir: `ml-<a..j>.diff`). Each mutant was then run as
  `bash m<X>.sh --selftest`; a mutant is KILLED iff at least one of the nine
  `(R44-C1)` cases FAILs (exit 1).

Mutants (exact sites in the pristine probe):

| id | mutation | pristine text -> mutant |
|----|----------|------------------------|
| a | drop `local LC_ALL=C` | line 1968 removed |
| b | records `-r` -> `-e` | `[ -r "$e" ] || unr=$((unr + 1))` (scrub.status.UUID branch only) -> `[ -e "$e" ]` |
| c | orphan test inverted | `[[ $fsids != *" ${BASH_REMATCH[1]} "* ]]` -> `==` |
| d | progress `-S` -> `-e` | `[ ! -S "$e" ]` -> `[ ! -e "$e" ]` (progress branch) |
| e | speed regex `+` -> `*` | `^[0-9]+$` -> `^[0-9]*$` |
| f | bare template counted | `[ "${e##*/}" != 'btrfs-scrub@.timer' ] || continue` removed |
| g | `sysfs:absent` gate dropped | `if [ "$rec" -gt 0 ] && [ "$sysok" -eq 0 ] && [ ! -e "$root" ]; then blocked=1; detail+='sysfs:absent,'; fi` removed |
| h | `^0+$` -> `= 0` | `! [[ $v =~ ^0+$ ]]` -> `[ "$v" != 0 ]` |
| i | RECORDED needs records | `elif [ $((rec + tmp + sock)) -gt 0 ]` -> `elif [ "$rec" -gt 0 ]` |
| j | detail/info join reversed | `detail+=$info` -> `detail=$info$detail` |

## 2. Kill table (`--selftest`, ambient LANG=en_US.UTF-8, TMPDIR in scratch)

| mutant | exit | summary | failing `(R44-C1)` case(s) | verdict |
|--------|------|---------|------------------------------|---------|
| a | 0 | PASS 141/141 | — | SURVIVES |
| b | 1 | FAIL 140/141 | `a 000 record is unreadable, ... a _tmp counts apart` (case 3) | KILLED |
| c | 1 | FAIL 140/141 | `one readable record of a mounted fsid reads RECORDED; other names are ignored` (case 2) | KILLED |
| d | 1 | FAIL 140/141 | `a symlinked or directory record and a non-socket progress name are BLOCKED...` (case 8) | KILLED |
| e | 0 | PASS 141/141 | — | SURVIVES |
| f | 1 | FAIL 140/141 | `enabled scrub timer instances count by link name; the bare template and other timers do not` (case 7) | KILLED |
| g | 1 | FAIL 140/141 | `records with no sysfs root to judge orphans by are BLOCKED` (case 9) | KILLED |
| h | 0 | PASS 141/141 | — | SURVIVES |
| i | 0 | PASS 141/141 | — | SURVIVES |
| j | 0 | PASS 141/141 | — | SURVIVES |

So the nine `(R44-C1)` cases kill 5 of the 10 mutants (b, c, d, f, g) and
survive 5 (a, e, h, i, j). Each survivor is a behaviour-changing mutant (proven by
the red/green demonstrations below), i.e. a selftest coverage gap.

Note on (c): it is killed by case 2 only. Case 3's orphan count is the *total* of
mounted+unmounted records, so the inversion swaps which record is counted and the
total stays 1 — case 3 is immune to (c).

Raw per-mutant evidence: seat-dir receipts `m<X>.out` / `m<X>.err` (each err has
the exact FAIL label; `baseline.out` has the pristine PASS).

## 3. Proposed extra `check` cases for the survivors

Each case below is inserted in `run_selftest` immediately after the existing
`scrub-sysfs-absent` case (before the `check_cli` block), i.e. as the 10th/11th
`(R44-C1)`-family case. Demonstrated: green on 7e081698 (P<X>: PASS 142/142,
rc=0) and red on the mutant (U<X>: FAIL 141/142, rc=1, failing exactly the new
case).

### (a) survivor — locale pinning (drop `local LC_ALL=C`)

The probe's `local LC_ALL=C` pins C-locale regex ranges. Under en_US.UTF-8,
`[a-f]` matches a collation-inflated `á` (verified directly: `LC_ALL=en_US.UTF-8 bash -c '[[ aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaáa =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]]'` -> MATCH; `LC_ALL=C` -> NOMATCH). The fence pins the ambient locale for the census child and uses a name that is a uuid only under UTF-8 collation:

```bash
  case_home='scrub-locale-fsid'; FX="$work/fx/$case_home"; mkdir -p "$FX/btrfs" "$FX/scrub"; fx_default "$FX"
  local lfs=$'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaa\xc3\xa1a'
  mkdir -p "$FX/btrfs/$lfs/devinfo/1"; printf '0\n' > "$FX/btrfs/$lfs/devinfo/1/scrub_speed_max"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.$lfs"; chmod 644 "$FX/scrub/scrub.status.$lfs"
  EXTRA_ENV=(LC_ALL=en_US.UTF-8)
  check 'healthy: the probe pins LC_ALL=C so a collation-inflated name is never a uuid (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'
```

Demonstration: P-a PASS 142/142; U-a FAIL exactly this case. Raw census output
(env LC_ALL=en_US.UTF-8, same fixture):
pristine: `SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`<br>
mutant a: `SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`

Environment caveat: the fence needs `en_US.UTF-8` installed (present on this host;
`locale -a` lists `en_US.utf8`). The `EXTRA_ENV=(LC_ALL=...)` pin makes the fence
independent of the harness's own ambient locale.

### (e) survivor — empty scrub_speed_max line (regex `+` -> `*`)

`^[0-9]*$` matches the empty string, so a file containing a single newline (v='')
is silently accepted instead of normalized malformed:

```bash
  case_home='scrub-speed-empty'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1"; printf '\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  check 'healthy rollup: an empty scrub_speed_max line is malformed, never a silent no-limit (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-malformed$'
```

Demonstration: P-e PASS 142/142; U-e FAIL exactly this case. Raw census output:
pristine: `SCRUB btrfs-scrub-record state=BLOCKED dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-malformed`<br>
mutant e: `SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:1:speed_max=`
(the mutant also counts the empty value as a limit and emits an empty `speed_max=`)

### (h) survivor — zero-padded limit (`^0+$` vs `= 0`)

`000` is 0 (no limit) under the regex, but `"000" != 0` under the string compare:

```bash
  case_home='scrub-speed-zero-padded'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1"; printf '000\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  check 'healthy: a zero-padded scrub_speed_max is still no limit (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'
```

Demonstration: P-h PASS 142/142; U-h FAIL exactly this case. Raw census output:
pristine: `SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`<br>
mutant h: `SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:1:speed_max=000`

### (i) survivor — RECORDED with zero finished records

A `_tmp` record alone (records=0, tmp=1) must still read RECORDED; the mutant only
looks at `rec`:

```bash
  case_home='scrub-tmp-only'; FX="$work/fx/$case_home"; mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/scrub"; fx_default "$FX"
  printf '0\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"
  printf 'scrub status:1\n' > "$FX/scrub/scrub.status.${sfs}_tmp"; chmod 600 "$FX/scrub/scrub.status.${sfs}_tmp"
  check 'healthy: an in-progress _tmp record alone reads RECORDED with zero finished records (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=RECORDED dir=present records=0 tmp=1 sockets=0 unreadable=0 orphan=0 limited=0 timers=0$'
```

Demonstration: P-i PASS 142/142; U-i FAIL exactly this case. Raw census output:
pristine: `SCRUB btrfs-scrub-record state=RECORDED dir=present records=0 tmp=1 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`<br>
mutant i: `SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=1 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`

(A first attempt used `mkfifo` for a "socket"; a FIFO is not a socket and the
pristine probe correctly BLOCKED it (`progress:not-socket`), so that fixture was
rejected — the `_tmp` fixture is the honest red/green one.)

### (j) survivor — detail vs info join order

With both detail evidence (malformed speed) and info (valid nonzero limit) present,
the pristine line lists detail first; the mutant lists info first:

```bash
  case_home='scrub-detail-info-both'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  mkdir -p "$FX/btrfs/$sfs/devinfo/1" "$FX/btrfs/$sfs/devinfo/2"
  printf 'fast\n' > "$FX/btrfs/$sfs/devinfo/1/scrub_speed_max"; printf '104857600\n' > "$FX/btrfs/$sfs/devinfo/2/scrub_speed_max"
  check 'healthy rollup: detail evidence precedes limit info in the detail join (R44-C1)' 0 HEALTHY \
    '^SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:1:speed-malformed,11111111:2:speed_max=104857600$'
```

Demonstration: P-j PASS 142/142; U-j FAIL exactly this case. Raw census output:
pristine: `SCRUB btrfs-scrub-record state=BLOCKED dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:1:speed-malformed,11111111:2:speed_max=104857600`<br>
mutant j: `SCRUB btrfs-scrub-record state=BLOCKED dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:2:speed_max=104857600,11111111:1:speed-malformed`

All five extra cases keep the `(R44-C1)` label and are inserted between the existing
`scrub-sysfs-absent` case and the `check_cli` block; the green variants raise the
selftest to 142 cases.

## 4. Host guard / environment

- No host mutation: no package/service/timer/sysfs/mount/boot changes; no `btrfs
  scrub` commands; no sudo; only read-only queries (the raw-line captures ran the
  census with `TSUKUROI_SCRUB_DIR`/`TSUKUROI_BTRFS_SYSFS`/`TSUKUROI_TIMER_WANTS`
  pointing at scratch fixtures).
- Lane read-only: `git status --porcelain -- tools/tsukuroi-census.sh
  tools/score-scrub-arm-r44.py` and `git diff --stat` both empty (rc 0); no clone
  mutations, no git mutation commands run.
- No tool installs performed (nothing was missing; per RULES.md no install record
  needed).
- Environment: LANG=en_US.UTF-8, LC_ALL unset; `locale -a` contains `C`, `C.utf8`,
  `en_US.utf8`. bash 5.x (host).
- Scratch `/fast/scratch/hyaku/tsukuroi-r44/C1MutSelftest/` removed on finish
  (trap), receipts copied to the seat dir first.

## 5. Receipts (in `.ufo/waves/round-44/w1/C1MutSelftest/`)

- `pristine-census-7e081698.sh` — pristine census at the implementation revision.
- `hashes.txt` — sha256 of pristine + all ten mutants.
- `ml-<a..j>.diff` — unified diff pristine vs each mutant (one site each).
- `baseline.out`/`baseline.err` — pristine selftest run.
- `m<X>.out`/`m<X>.err` — mutant selftest runs (kill table).
- `p<X>.out`/`p<X>.err`, `u<X>.out`/`u<X>.err` — green/red demonstrations for the
  survivor fences (a, e, h, i, j), including the final `scrub-tmp-only` variants.
