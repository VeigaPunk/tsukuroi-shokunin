VERDICT: defect-found

# C1-3 — generalisation attack on the round-41 mount-table selftest (seat C1HeldOutMutants)

Target: the mount-table read in `probe_storage_arm`, tools/tsukuroi-census.sh at lane tip
71851d636ab1bffaf8fee5016617c88878a666f1 (HEAD confirmed: `git rev-parse HEAD` = 71851d63…),
lines 1910-1915:

```bash
      while read -r _src _mp fst _rest; do
        if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
      done <<< "$mtab"
      if [ "$mt" -gt 0 ]; then blocked=1; detail+='mounts:btrfs-without-sysfs,'; fi
```

Frozen mutants excluded by construction: the 13 of tools/score-selftest-mounts-r41.py:85-110
(M1-M9, H5, H6, H9, H10 — full list read from the counter; sha256 8306d999… matches the frozen
claim). My nine mutants are textually and semantically distinct from all of them, from NEUTRAL
N1-N3 (counter:111-119) and from the decoy.

## Method (counter-equivalent environment)

- Scratch copies only: `S=/fast/scratch/hyaku/tsukuroi-r41/C1HeldOutMutants`; pristine copy
  `base.sh`, sha256 `646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95` — byte-equal
  to the lane file and taken before any mutation.
- Detector, one run at a time (host loaded; serial, never overlapped):
  `cd / && TMPDIR=$S/t HOME=$S/t/home PATH=/usr/bin:/bin LC_ALL=C bash <copy> --selftest`
  (mirrors the counter's documented run environment, score-selftest-mounts-r41.py:8-9).
- Verdict rule (mirrors the counter's): KILLED = exit != 0 AND >=1 `FAIL <label>` line on stderr
  (bad() writes there, census:2019); SURVIVED = exit 0 AND `TSUKUROI_CENSUS_SELFTEST: PASS (128
  cases, 128 passed, 0 failed)` identical to baseline. A baseline failure would have been
  inconclusive, not a kill; the baseline passed (see flake note for one transient exception).
- Not run: the frozen counter itself (not required by my item); no tools installed.

## Results — nine new mutants

Baseline (pristine): exit 0, `PASS (128 cases, 128 passed, 0 failed)`, 33 s (base.out).

| id | mutation (count line 1913 / loop 1912-1914 / threshold 1915) | verdict | killing label(s) |
|----|------|---------|------------------|
| X1 fstype-prefix | `if [[ ${fst:-} == btrfs* ]]; then` | **SURVIVED** | — |
| X2 five-fields-only | 6 read vars, count iff `_d1`,`_d2` non-empty and `_extra` empty (accepts 5-field lines, rejects 6-field) | KILLED | 8 labels: both R39-C1 (census:2981, 2986), both R40-C1 (3015, 3023), H5 (3042), H6 (3048), H9 (3054), H10 (3061) |
| X2b exactly-six-fields | 7 read vars, count iff fields 4-6 non-empty and 7th empty | **SURVIVED** | — |
| X3 rw-only | `… = btrfs ] && [[ ${_rest:-} == rw* ]]` | KILLED | `healthy rollup: one read-only btrfs mount among four lines, empty root, is BLOCKED (R40-C1)` (census:3023; its btrfs line is `ro,noatime,…`, census:3021) |
| X4 no-`\0`-escape-mountpoint | `… = btrfs ] && [[ ${_mp:-} != *'\0'* ]]` (skips mountpoints carrying an octal escape) | **SURVIVED** | — |
| X5 threshold `-gt 2` | `if [ "$mt" -gt 2 ]; then blocked=1; …` | KILLED | 8 labels (same set as X2; the H10 two-line table, mt=2, no longer blocks) |
| X6 after-first-proc | `_after=1` on first `proc` fstype; count btrfs only when `_after=1` | KILLED | `healthy rollup: btrfs mounted with a root holding no fsid is BLOCKED (R39-C1)` (2986) and the R40-C1 read-only label (3023) — the two fixture tables that contain no proc line |
| X7 digit-bearing-source | `… = btrfs ] && [[ ${_src:-} == *[0-9]* ]]` | KILLED | both R39-C1 labels (2981, 2986) — the only tables whose btrfs source `/dev/mapper/root` (census:2978) has no digit |
| X8 relatime-required | `… = btrfs ] && [[ ${_rest:-} == *relatime* ]]` | KILLED | both R39-C1 labels (2981, 2986; `fxmt` is `noatime`), the R40-C1 ro label (3023, `ro,noatime`), and H9 (3054; `rw,commit=60`) |

Raw runs: base.out, x1.out/.err, x2-five-fields.out/.err, x2b.out/.err, x3…x8 .out/.err, diffs
x1-x8.diff, x2b.diff — all in this seat dir (each < 64 KB).

## The three survivors — separating tables, exact cases, kernel producibility

### X4 (no-`\0`-escape mountpoint) — GENUINE, kernel-producible gap

Separating table (mountpoint `/mnt/btr fs` as the kernel writes it):

```
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
/dev/sdz9 /mnt/btr\040fs btrfs rw,relatime,subvolid=5,subvol=/ 0 0
```

Correct behavior: this line counts, BLOCKED `detail=mounts:btrfs-without-sysfs`. X4 skips it and
reads silent `0/0/0 HEALTHY` while btrfs is mounted with no sysfs root.

Exact selftest case that kills it (drop-in beside the H-series, census:3050-3062):

```bash
  case_home='storage-mounts-escaped-space'; FX="$work/fx/$case_home"; mkdir -p "$FX"; fx_default "$FX"
  printf '%s\n' 'proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0' \
    '/dev/sdz9 /mnt/btr\040fs btrfs rw,relatime,subvolid=5,subvol=/ 0 0' > "$FX/mounts"
  check 'healthy rollup: a btrfs mountpoint with an escaped space still counts, BLOCKED (R41-C1 X4)' 0 HEALTHY \
    '^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$'
```

Kernel can produce that table — demonstrated live on this host (private namespace, allowed):
`unshare -rm bash -c 'mount -t tmpfs none "$1" && grep "esc/sp" /proc/self/mounts'` printed
`none /fast/scratch/hyaku/tsukuroi-r41/C1HeldOutMutants/esc/sp\040ace tmpfs rw,relatime,… 0 0`.
The kernel octal-escapes whitespace in mount fields, so a space-named btrfs mountpoint appears
exactly as `\040`. X4 is therefore an observable-behaviour survivor: a round-41-shaped mutant that
drops escaped mountpoints from the count reads HEALTHY on such a host, and the suite cannot see it.

### X1 (fstype prefix `btrfs*`) — kernel-equivalent, unpinned by the suite

Separating table: `proc /proc proc rw 0 0` + `/dev/fx9 /mnt/pool btrfssnap rw,relatime,subvol=/snap 0 0`.
Correct behavior: `btrfssnap` is not the fstype `btrfs` → `HEALTHY filesystems=0 devices=0 nonzero=0`
(the suite already pins exactness for case, census:3031-3034 `storage-mounts-fstype-case`); X1
counts it → BLOCKED. Exact case: mirror `storage-mounts-fstype-case` with fstype `btrfssnap` and the
must-not-block expectation above, label `healthy: the fstype match is exact, so btrfssnap is not btrfs (R41-C1 X1)`.

Kernel canNOT produce that table: `grep btrfs /proc/filesystems` → `btrfs` only (one registered
name); /proc/*/mounts carries the driver's registered name and no `btrfs*` sibling exists. X1 is
behaviourally equivalent on every kernel-producible table; the gap is contract-shaped (the suite
pins "match is exact" only against case variation, not prefix variation).

### X2b (exactly-six-fields gate) — kernel-equivalent for procfs, reachable via the override

Separating table: `proc /proc proc rw,nosuid 0 0` + `/dev/sdz1 /mnt/plain btrfs rw,commit=60`
(four fields, no dump/pass tail). Correct behavior: the fstype field decides → BLOCKED
`mounts:btrfs-without-sysfs`; X2b skips it → silent HEALTHY. Exact case: as above with label
`healthy rollup: a four-field btrfs line (no dump/pass tail) still counts, BLOCKED (R41-C1 X2b)`.

Kernel canNOT produce it via procfs — live check on this host: `awk '{print NF}' /proc/self/mounts
| sort -u` → `6` (every line exactly six fields). But the census accepts `TSUKUROI_PROC_MOUNTS`
(census:398-402), so a legacy 4-field mtab-style file fed through the override reaches this read;
the suite cannot see a field-count gate that accepts 6-field lines. Pair X2/X2b brackets the shape:
a gate rejecting 6-field lines dies on all eight mount cases (X2), one accepting only them survives
(X2b) — field-count is an unpinned axis.

## Flake observation (non-target, one occurrence)

Restored-bytes run 1 of the pristine `base.sh` (hash-equal to the lane file) failed 127/128:
`FAIL degraded: memory arm — oom_kill is a presence flag, not a count (S7-2): hostname override not
honoured — possible host read` (base-restored.err, 52 s), after every earlier run in the same
session passed. The `host=fixture-host` assertion runs for every case (census:2175) and the host
read is `|| true`-guarded (census:3109), so a single-case failure is consistent with a transient
subshell/read failure swallowed into `host=unknown` under load [INFERENCE]. A bounded re-run passed
128/128 in 29 s (base-restored2.out); the flake did not reproduce and hit no mount-table case, so
no mutant verdict is affected (survivors require a full pass, and every KILLED label set matches
its construction exactly). Relevant to the frozen counter: this is one live instance of the
load-flake class its kill attribution already guards against ("a kill needs a baseline case label
failing, twice", score-selftest-mounts-r41.py:16-19); a sibling seat is separately diagnosing a
base flake this wave. Recorded, not fixed — outside my item.

## Restoration evidence

- Lane file untouched throughout (read-only; no git/jj mutation): sha256 after all runs
  `646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95` = before = `git rev-parse
  HEAD:tools/tsukuroi-census.sh` blob `dda066f4…`'s worktree content at tip 71851d63….
- Detector on restored bytes: pristine re-run after all nine mutants → exit 0,
  `PASS (128 cases, 128 passed, 0 failed)` (base-restored2.out).

## Bounds / not done

- Detector = `bash <copy> --selftest` only; the frozen counter score-selftest-mounts-r41.py was
  not run (bound: counter not required by this item; one census selftest at a time was respected).
- Mutants were applied to scratch copies only; nothing under /tmp; scratch
  /fast/scratch/hyaku/tsukuroi-r41/C1HeldOutMutants removed after copying receipts (the `unshare
  -rm` tmpfs mount died with its namespace).
- I did not verify whether any lane fixture outside run_selftest (e.g. live census paths) depends
  on the read's exact shape; the attack is scoped to the selftest contract, as itemed.
