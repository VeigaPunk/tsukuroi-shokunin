VERDICT: supports

# C1-15 — does the host's real mount table separate H5, H6, H9, H10?

Answered item: for the census at `71851d636ab1bffaf8fee5016617c88878a666f1` and each held-out mutant, run the
live census with `TSUKUROI_BTRFS_SYSFS=<absent>` and `TSUKUROI_PROC_MOUNTS=<copy of /proc/self/mounts>` and
record the STORAGE line.

Result: the real table separates **H10 only**. H5, H6 and H9 produce the baseline STORAGE line byte for byte,
so they are exercised by the synthetic selftest fixture tables alone — which is exactly what the C1 claim
asserts (the census `--selftest` gains the four cases; `probe_storage_arm` unchanged), so nothing here
falsifies it.

## Setup and identity

- census at the dispatched tip, read with `git -C <lane> show 71851d63:tools/tsukuroi-census.sh`
  → sha256 `646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95`; identical to the lane working
  tree `tools/tsukuroi-census.sh` and to my scratch copy `base.sh` (three-way `sha256sum`, same digest).
  Scratch copy used because the item requires a *copy* (four mutants must not touch the lane).
- mount table: `cp /proc/self/mounts` → 33 lines, sha256
  `412f26302973326877038f32e533640d56745a874f974dcdf33095b308dc832e`; receipt `.ufo/waves/round-41/w1/C1ExecLiveMounts/mounts`.
- mutants: texts taken verbatim from `tools/score-selftest-mounts-r41.py` `MUTANTS` (`H5-mountpoint-absolute`,
  `H6-source-devonly`, `H9-subvolkey-option`, `H10-count-exactly-one`), each applied with `str.replace` and
  accepted only at occurrence count 1 (`H5 1 / H6 1 / H9 1 / H10 1`). Diffs are one line each
  (`diff -u base.sh H5.sh` etc.), e.g. H10 changes `[ "$mt" -gt 0 ]` → `[ "$mt" -eq 1 ]` at the guard inside the
  STORAGE arm; H5/H6 add a conjunct to the count line; H9 replaces the whole read loop with
  `case $mtab in *'subvol='*)`.
- command per run (paths under `/fast/scratch/hyaku/tsukuroi-r41/C1ExecLiveMounts/`):

```
TSUKUROI_BTRFS_SYSFS=$PWD/absent TSUKUROI_PROC_MOUNTS=$PWD/mounts bash {base,H5,H6,H9,H10}.sh
```

  (`absent/` was the path the item names; I first created it as an *empty* directory — the arm's "root holding
  no fsid entry" route — and, because an empty directory is not literally absent, also re-ran every variant with
  a path that does not exist at all. Both readings give the table below unchanged, since both land in the same
  `[ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]` guard at `tools/tsukuroi-census.sh:1906`.)

## Condition A — prescribed (no sysfs, real mount table)

Same five lines were observed with the empty-directory root (run set A) and with a root path that does not
exist (run set A2, receipt `.ufo/waves/round-41/w1/C1ExecLiveMounts/live-output/missing-sysfs/`):

| variant | STORAGE line | vs baseline |
|---|---|---|
| base | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | — |
| H5 | same as base | **not separated** |
| H6 | same as base | **not separated** |
| H9 | same as base | **not separated** |
| H10 | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | **separated** |

`diff base.live.out H10.live.out` shows exactly three hunks: the `tsukuroi-census … <timestamp>` banner, the
volatile `PLANE drivers: …` mem counters, and line 11, the STORAGE line above (BLOCKED+detail → HEALTHY 0/0/0).
`diff base.live.out {H5,H6,H9}.live.out` shows only the banner timestamp and the volatile mem counters — no
STORAGE difference. Receipt `.ufo/waves/round-41/w1/C1ExecLiveMounts/storage-lines.txt`; the full 12-line
outputs of all ten runs are kept verbatim in `.ufo/waves/round-41/w1/C1ExecLiveMounts/live-output/`
(`base.live.out`, `H5.live.out`, …, `H10.realsys.out`).

Why H10 separates: the table has **4** btrfs lines, the mutant trips only on `mt -eq 1`
(`if [ "$mt" -eq 1 ]; then blocked=1;`), so `blocked` stays 0 and the arm falls through to the "absent root means
no btrfs" path it is meant to forbid: `state=HEALTHY filesystems=0 devices=0 nonzero=0`, no detail. That is the
exact silent-`0/0/0` class the header forbids (`tools/tsukuroi-census.sh:363-366` at 71851d63: an absent root
"reads HEALTHY 0/0/0 only when the mount table … lists no btrfs mount; with a btrfs mount listed it is BLOCKED
detail=mounts:btrfs-without-sysfs").

Why H5/H6/H9 do not: the table's four btrfs lines are all absolute-mounted, all `/dev/`-sourced and all carry
`subvol=` — receipt `.ufo/waves/round-41/w1/C1ExecLiveMounts/mount-table-shape.txt`:

```
btrfs line 7:  src=/dev/mapper/root mp=/                   opts_has_subvol=yes
btrfs line 23: src=/dev/mapper/root mp=/home               opts_has_subvol=yes
btrfs line 24: src=/dev/mapper/root mp=/var/cache/pacman/pkg opts_has_subvol=yes
btrfs line 25: src=/dev/mapper/root mp=/var/log            opts_has_subvol=yes
TOTAL btrfs_lines=4 nonabsolute_mountpoint=0 source_not_under_/dev=0 no_subvol_option=0
```

H5's conjunct `[[ ${_mp:-} == /* ]]` is true for all 4, H6's `[[ ${_src:-} == /dev/* ]]` is true for all 4, and
H9's `*'subvol='*` substring matches the table string — each mutant therefore counts 4 and blocks, like the base.
The real table carries no instance of the three shapes those mutants mis-handle.

## Condition B — control, same table, the host's real sysfs

`env -u TSUKUROI_BTRFS_SYSFS TSUKUROI_PROC_MOUNTS=$PWD/mounts bash {base,H5,H6,H9,H10}.sh` — the host has one
fsid, `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats` with all five counters `0`.
All five runs print the identical line `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1
nonzero=0` (`diff` clean apart from banner/volatile mem lines). So with the sysfs present the arm never reaches
the mount-table branch at all (`tools/tsukuroi-census.sh:1906` guard `[ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]`),
and no mutant is separated. Real-table discrimination of *any* of these four exists only in the sysfs-absent
condition the item prescribes.

## Where H5/H6/H9 are actually covered (synthetic tables)

The four declared table shapes live in the selftest at `tools/tsukuroi-census.sh:3037-3062` (71851d63), each a
private `$FX/mounts` fixture:

- `storage-mounts-mp-relative` (line 3039): `/dev/vdc1 relative/mnt btrfs rw,relatime,subvolid=5,subvol=/` — the
  H5 shape; nothing in the real table has a relative mountpoint.
- `storage-mounts-src-uuid` (line 3045): source `UUID=0b1c2d3e-…-a3b4c5d6e7f8`, mountpoint `/data` — the H6 shape.
- `storage-mounts-no-subvol-opt` (line 3051): `/dev/sdc1 /mnt/plain btrfs rw,commit=60` — the H9 shape.
- `storage-mounts-two-btrfs` (line 3057): two btrfs lines (`/` and `/home` on `/dev/nvme0n1p2`) — the H10 shape.

Observed at the same revision, unmutated copy, `env -u TSUKUROI_BTRFS_SYSFS -u TSUKUROI_PROC_MOUNTS
TMPDIR=<scratch>/tmp bash base.sh --selftest` → exit 0,
`TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)` with these labels among the output
(receipt `.ufo/waves/round-41/w1/C1ExecLiveMounts/selftest-r41-labels.txt`; a first run with the ambient
`TSUKUROI_*` overrides exported gave the same 128/128, so the result does not depend on my exported env):

```
PASS healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5) (exit 0, HEALTHY)
PASS healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6) (exit 0, HEALTHY)
PASS healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9) (exit 0, HEALTHY)
PASS healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10) (exit 0, HEALTHY)
```

## Reading

- H10: separated by the real table *and* by its fixture — the real-table separation depends on this host having
  ≥2 btrfs mounts (it has 4 by subvolume design: `@`, `@home`, `@pkg`, `@log`). On a single-subvolume host the
  real table would not distinguish H10 either; the fixture remains the guarantee.
- H5, H6, H9: fixture-only on this host, by construction. That is consistent with the C1 claim (the surface is
  the hermetic `--selftest`, `probe_storage_arm` untouched), and it means no observation of these three on the
  live table can ever count as their kill — the counter's fixture-based kill attribution is the only route,
  which is what the frozen counter does.
- Nothing found that contradicts the claim. The mutants change the arm's behaviour only in the sysfs-absent
  branch; the host measurement does not add or remove any claim.

## Limits / not done

- I did not run the frozen counter `tools/score-selftest-mounts-r41.py` (the item asked for this targeted probe;
  the counter is other seats' item and is the expensive one). I also did not run it to confirm kills.
- I ran two `--selftest` passes of the unmutated copy (52 s and 51 s wall, same 128/128 result) and fifteen live
  census runs (~6 s each: five with an empty sysfs root, five with a nonexistent one, five with the real sysfs);
  those are the only census executions I started, sequential (never more than one at a time), with host
  background load the only other traffic.
- Live mode reads host paths read-only: no package query beyond the census's own, no host mutation, no sudo, no
  service or sysfs write, no `unshare` needed. No tool installed or upgraded.
- Scratch `/fast/scratch/hyaku/tsukuroi-r41/C1ExecLiveMounts/` removed after copying receipts; receipts under
  `.ufo/waves/round-41/w1/C1ExecLiveMounts/` are `mounts`, `mounts.sha256`, `mount-table-shape.txt`,
  `storage-lines.txt`, `selftest-r41-labels.txt`, `commands.txt` and `live-output/` (no census copy, no
  SOURCES.md copy).
