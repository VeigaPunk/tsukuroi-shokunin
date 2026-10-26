VERDICT: supports

# C1-14 — does this host's real mount table separate the frozen mutants?

Seat C1ExecLiveMounts, round 40 w1. Read-only on the lane; all clones/variants under
`/fast/scratch/hyaku/tsukuroi-r40/C1ExecLiveMounts/` (removed after the receipts were copied to
`.ufo/waves/round-40/w1/C1ExecLiveMounts/`). No host mutation, no sudo, no package action, no tool
install (nothing needed; python 3.14.8, GNU bash 5.3.20(1)-release from the host).

## Answer

**One of nine.** On the live table only **M9-last-line-only** produces a different STORAGE line from
the unmutated census. M1–M8 are byte-identical to the original, so they are separated **only** by the
round-40 synthetic fixtures in `run_selftest` — exactly the five cases the declaration names
(`tools/tsukuroi-census.sh:3011,3018,3026,3032,3037`).

| variant | STORAGE line (real table, absent sysfs) | separated? |
|---|---|---|
| original (f951f28) | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | — |
| M1-VA-device-literal | same as original | **no** |
| M2-VB-root-mountpoint | same as original | **no** |
| M3-VC-substring-btrfs | same as original | **no** |
| M4-VG-subvolid-256 | same as original | **no** |
| M5-a-grep-count | same as original | **no** |
| M6-b-fstype-casefold | same as original | **no** |
| M7-e-guard-drops-blocked | same as original | **no** |
| M8-subvol-at-literal | same as original | **no** |
| M9-last-line-only | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | **yes** |

Receipts: `.ufo/waves/round-40/w1/C1ExecLiveMounts/summary.txt` (all 10 runs, exact lines),
`runs.txt` (env + command template), `mounts` (the table copy, 3258 B < 50 KB, sha256
`0fe57247486e7c0002e09729f65564b83a3b748f01b299e7002129fe06fc49fe`), `original-tail.txt`.

## Method (exactly the assigned command)

- Census text: `git -C <lane> show f951f288483c1af0cef4afd458488b84cf7a2165:tools/tsukuroi-census.sh`
  (scratch copy sha256 `032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733`; the
  file is not copied into the seat dir).
- Mutants applied exactly as the frozen counter does it — import `MUTANTS` from
  `tools/score-selftest-literals-r40.py:69-80` and `text.replace(old, new)` **only** when
  `text.count(old) == 1`. All nine applied (occurrences 1/1 each), M1–M9.
- Per variant: `bash <scratch>/<variant>/tsukuroi-census.sh`, `cwd=/`, env
  `PATH=/usr/bin:/bin:/usr/sbin:/sbin LC_ALL=C HOME=<scratch> TMPDIR=<scratch>/tmp
  TSUKUROI_BTRFS_SYSFS=<scratch>/absent TSUKUROI_PROC_MOUNTS=<scratch>/mounts`; captured the
  `STORAGE ` line and the exit code. Ten runs, 40 s wall.

Original run (unmutated, real table): STORAGE **BLOCKED** as above, exit 2. The exit 2 is *not* the
storage arm: the STORAGE line is verdict-neutral (`tools/tsukuroi-census.sh:353`, printed after the
PLANE rollup at `:3128-3129`), and the census rollup on this host is
`TSUKUROI_CENSUS: BLOCKED (... systemd=BLOCKED ...)` because `systemctl --user` has no bus
(`original-tail.txt`). Therefore M1–M8 change **neither** the STORAGE text **nor** the exit status:
a live census run on this host carries zero signal about the literal-keying defect class.

## Why each mutant survives the real table

The table (`mounts`, 33 lines) has four btrfs mounts on the same device:

```
7:/dev/mapper/root / btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@ 0 0
23:/dev/mapper/root /home btrfs ... subvolid=257,subvol=/@home 0 0
24:/dev/mapper/root /var/cache/pacman/pkg btrfs ... subvolid=259,subvol=/@pkg 0 0
25:/dev/mapper/root /var/log btrfs ... subvolid=258,subvol=/@log 0 0
```

- M1 `/dev/mapper/root`: 4 matching lines; M2 `' / btrfs '`: 1 (line 7); M3 `*btrfs*`: 4;
  M4 `subvolid=256`: 1 (line 7); M5 `grep -c btrfs` → 4 > 0; M8 `subvol=/@`: 4 (it is a *prefix* of
  `/@home`, `/@pkg`, `/@log`, so it is an even looser literal than it reads). Every one of these
  literals was taken from this host's own table: at base 53b294a the round-39 fixture was
  `fxmt='/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0'`
  (`git show 53b294a274656be6479aadf2ec2fee890ded77ce:tools/tsukuroi-census.sh`, line 2978) — line 7 of
  `/proc/self/mounts` truncated of its options. The live table is the monoculture's source, which is
  why it cannot be its detector.
- M6 `[ "${fst,,}" = btrfs ]`: the fstype on all four btrfs lines is already lowercase, so casefolding
  is a no-op here. [INFERENCE] `/proc/self/mounts` prints the kernel's registered type name, so a
  `btrfs` mount can only ever read `btrfs`; on this host the only fstype field carrying uppercase is
  a FUSE mount (`mounts:33`, `fuse.Grok_Bot_0.70.2.AppImage`). M6 is separated solely by the
  synthetic `BTRFS` fixture (`tools/tsukuroi-census.sh:3032-3035`) — an input the kernel cannot
  produce for btrfs. This makes M6 equivalent-in-practice in the same sense as the excluded
  `$fsn -> $devn` mutant, and the counter docstring names only the latter
  (`tools/score-selftest-literals-r40.py:27-29`); worth a one-line addition there, not by me
  (counter is frozen).
- M7 `if [ "$fsn" -eq 0 ]` (dropping `&& [ "$blocked" -eq 0 ]`): **no mount table can separate it in
  this configuration.** With `TSUKUROI_BTRFS_SYSFS` absent, `blocked` is still 0 when the guard is
  reached (the only earlier writers are the unreadable-root branch and the devinfo loops), so both
  the correct and the mutated guard enter the mtab branch and set `blocked=1` themselves. Measured on
  two derived tables (supplementary, labelled derived, `summary-derived.txt`): real table minus its
  btrfs lines → original and M7 both `HEALTHY 0/0/0` (same); real table with the root btrfs line moved
  last → both `BLOCKED ... detail=mounts:btrfs-without-sysfs` (same). M7 is only reachable by the
  fifth fixture, unlistable root **with** btrfs mounted (`tools/tsukuroi-census.sh:3037-3042`, expected
  `detail=root:unreadable`).
- M9 `tail -n 1`: the real table's last line is a FUSE AppImage mount (`mounts:33`), so `mt=0` and the
  arm reports HEALTHY where the original reports BLOCKED — hence the one separation. It is
  **ordering luck, not table diversity**: on the derived table with a btrfs line moved to the end, M9
  is identical to the original (BLOCKED). A host whose last mount is btrfs would not separate M9
  either. The other round-40 fixtures are what kill it deterministically (`:3011`, `:3018` put the
  btrfs line in the middle / not last).

## Consequences for the claim

- Consistent with C1: the five synthetic fixtures are **load-bearing**; on this host the live table
  discriminates 1/9 mutants and, because STORAGE is verdict-neutral and the rollup is already
  BLOCKED by systemd, not even the exit code moves. Nothing here falsifies the declaration.
- Residual risk to record: the *live* arm remains unexercised against real mount-table diversity. If a
  future change re-keyed the arm on a literal, no run on this host would notice; only the selftest's
  synthetic tables (device, mountpoint, options, subvolume, position, fstype case, unlistable root
  with btrfs) stand between that regression and a quiet `BLOCKED`-that-means-`HEALTHY`.
- Secondary: M6's kill depends on a `/proc` line the kernel cannot emit for btrfs, and M7's kill needs
  a non-absent root; both are legitimate as harness inputs but should not be counted as
  "real-table" separation.

## What I did not do

- Did not run `tools/score-selftest-literals-r40.py` (13-seat counter) or the census `--selftest`; the
  kill/survivor predicate is other seats' item, so the claim's PASS is neither confirmed nor
  contradicted here.
- Did not modify `probe_storage_arm`, the counter, the census, or any lane file; only this report and
  the four receipts above were written.
- No host mutation, no package or service action, no tool installs.
