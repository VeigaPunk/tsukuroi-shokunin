VERDICT: supports

# C1-13 — hand reproduction of the hidden STORAGE legs (after 49cc53c vs base 0eff65b) + live

Seat C1ExecLiveHidden, round 39. Item: reproduce the two hidden legs by hand without the counter
(`unshare -rm sh -c 'mount -t tmpfs t /sys/fs/btrfs && exec bash <census>'` and the `/sys/fs` variant) for
the census at 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82 and at 0eff65b21bb81195ee06c96a83afbd7a07e52eef, plus
the live host run, and compare `grep btrfs /proc/self/mounts` inside the namespace with the STORAGE line.

Result: every leg reproduces the declared C1 behaviour and the frozen counter's own leg values exactly.
Base is a false all-clear; the after commit is BLOCKED with `detail=mounts:btrfs-without-sysfs`; live is
unchanged at `HEALTHY filesystems=1 devices=1 nonzero=0`.

## Script identity (no lane write; blobs read with `git show`)

| rev | `git show <rev>:tools/tsukuroi-census.sh` sha256 | note |
|---|---|---|
| 0eff65b2 (base) | `6a675a4e06939e451bb6d1f7eb50f783b61c435e0d9d1efc983a0c7dfc81c33d` | no `PROC_MOUNTS` symbol at all (`grep -n PROC_MOUNTS` → empty); only `BTRFS_SYSFS` at `tools/tsukuroi-census.sh:453` |
| 49cc53c7 (after) | `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d` | `BTRFS_SYSFS`/`PROC_MOUNTS` env at `:459-460`; contract at `:355-368`; new branch at `:1903-1914` |
| 2e1c2a4 (lane tip at dispatch) | `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d` | same bytes as 49cc53c — no drift between the C1 commit and the dispatched tip |

`git log --format='%h %s' 0eff65b2..49cc53c7 -- tools/tsukuroi-census.sh` prints only `49cc53c`, so the two
inputs differ by exactly that commit's storage-arm change.

Branch under test, `tools/tsukuroi-census.sh:1903-1914` (after):
```
if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]; then
  local mtab mt=0 _src _mp fst _rest
  if mtab=$(cat -- "$PROC_MOUNTS" 2>/dev/null); then
    while read -r _src _mp fst _rest; do
      if [ "${fst:-}" = btrfs ]; then mt=$((mt + 1)); fi
```
Base contract at `0eff65b2:tools/tsukuroi-census.sh:363`: "An absent TSUKUROI_BTRFS_SYSFS means no btrfs
filesystem is mounted: HEALTHY 0/0/0." — the defect the round-39 claim closes.

## Method

Scratch `/fast/scratch/hyaku/tsukuroi-r39/C1ExecLiveHidden` (removed after receipts were copied);
`TMPDIR`/`HOME` private inside it. Each run: `env -i PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch>/home
TMPDIR=<scratch>/tmp unshare -rm sh <leg>` with **no `TSUKUROI_*` variable set** (verified below), stdin
`/dev/null`, stdout/stderr kept. The leg script does the item's literal sequence — `mount -t tmpfs t
/sys/fs/btrfs` (or `/sys/fs`) then `exec bash <census>` — with a `grep btrfs /proc/self/mounts` and a full
`cat /proc/self/mounts` captured **inside the namespace** between mount and exec. The item's literal
one-liner form was also run for all four rev×variant cells and produced the identical STORAGE line. Receipts:
`.ufo/waves/round-39/w1/C1ExecLiveHidden/receipts/`; scripts as run: `../C1ExecLiveHidden/leg-*.sh`,
`census-after.sh`, `census-base.sh`.

Environment facts for reproduction: kernel `7.2.11-arch1-1`, `kernel.unprivileged_userns_clone = 1`,
`user.max_user_namespaces = 122865`, `unshare from util-linux 2.42.4`, uid 1000, no sudo used.

## Leg results (mounts inside the child vs the STORAGE line)

Host mount table (unchanged, outside any namespace) lists 4 btrfs lines (`/`, `/home`,
`/var/cache/pacman/pkg`, `/var/log`, single device `/dev/mapper/root`); host `/sys/fs/btrfs` holds one fsid
`1d02a454-c549-4a35-b567-89d60902af8e` with `devinfo/1/error_stats` all five counters `0`.

| leg | census | mount lines `grep btrfs /proc/self/mounts` inside ns | STORAGE line | census exit |
|---|---|---|---|---|
| H1 `/sys/fs/btrfs`←tmpfs | after | 4 host btrfs lines **+** `t /sys/fs/btrfs tmpfs …` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | 2 |
| H2 `/sys/fs`←tmpfs | after | 4 host btrfs lines (the tmpfs mountpoint `/sys/fs` contains no "btrfs", so `grep` adds no row) | same BLOCKED line | 2 |
| H1 | base | 4 host btrfs lines + tmpfs line | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | 2 |
| H2 | base | 4 host btrfs lines | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | 2 |
| live (no ns) | after | 4 host btrfs lines | `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` | 2 |
| live (no ns) | base | 4 host btrfs lines | `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` | 2 |

Evidence files: `receipts/after-prod.{out,mounts-grep.txt,mounts.txt}`,
`receipts/after-sysfs.*`, `receipts/base-prod.*`, `receipts/base-sysfs.*`, `receipts/after-live.out`,
`receipts/base-live.out`, and the literal-form reruns `receipts/{after,base}-h{1,2}-literal.out`.
`receipts/after-prod.mounts-grep.txt` in full:
```
/dev/mapper/root / btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@ 0 0
/dev/mapper/root /home btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=257,subvol=/@home 0 0
/dev/mapper/root /var/cache/pacman/pkg btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=259,subvol=/@pkg 0 0
/dev/mapper/root /var/log btrfs rw,noatime,compress=zstd:3,ssd,discard=async,space_cache=v2,subvolid=258,subvol=/@log 0 0
t /sys/fs/btrfs tmpfs rw,relatime,uid=1000,gid=1000,inode64,huge=advise 0 0
```
So the mounted-tmpfs sysfs root is empty (`ls -a /sys/fs/btrfs` → `. ..` only) while the mount table the
child reads still names four btrfs mounts: the after arm refuses the all-clear, the base arm prints it.
Two details that make this a faithful comparison rather than a grep artefact: (a) the base arm has no
`PROC_MOUNTS` code path, so its `HEALTHY 0/0/0` cannot be mount-table-dependent; (b) the census counts a
mount by field 3 (`fst`), so the `tmpfs` line — matched by `grep` only because its mountpoint path contains
"btrfs" — is not counted as a btrfs mount, and the BLOCKED verdict necessarily comes from the four host
btrfs rows.

Namespace isolation actually held: host `readlink /proc/self/ns/mnt` = `mnt:[4026531832]`, child =
`mnt:[4026533811]`; inside the child `env | grep -c TSUKUROI` = `0`; host `/sys/fs/btrfs` after all runs
still lists `1d02a454-c549-4a35-b567-89d60902af8e` and `features`; host `/proc/self/mounts` still 4 btrfs
lines. No host mount, package, service, hook, sysctl or `/etc` change was made.

## Hand controls for the two branch conditions (after census, namespace)

Both are hand-thrown, not the counter's fixtures — they show the new branch is not over-blocking and that
the table is read only on an empty root:

| control | setup | STORAGE line |
|---|---|---|
| A empty root, no btrfs mounted | tmpfs over `/sys/fs/btrfs`; `TSUKUROI_PROC_MOUNTS` → a mounts fixture with only `proc`/`ext4` rows | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` |
| B populated root, unreadable table | tmpfs over `/sys/fs/btrfs` seeded with `1d02a454-…/devinfo/1/error_stats` (five zeros); `TSUKUROI_PROC_MOUNTS=/nonexistent` | `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` |

B is the decisive one: a nonexistent table would have produced `detail=mounts:unreadable` had the arm read
it, so the `fsn -eq 0` guard at `:1903` does short-circuit. Receipts:
`receipts/ctl-empty-nomounts.out`, `receipts/ctl-populated.out`, fixtures `receipts/nomounts.txt`.
(Control A/B use overrides, so they are seam checks, not hidden-leg reproductions; the hidden legs above
carry no override.)

## Agreement with the frozen counter's recorded legs

Read from the receipts (not re-run): `before/c1-before.jsonl` — `revision 0eff65b2`, `result FAIL`,
`hidden 0`, `views 3`, `fixtures 2`, `live 1`, `six 1`, both hidden legs `got: [STORAGE … HEALTHY
filesystems=0 devices=0 nonzero=0]`, `census_exit 2`, live `expected ['HEALTHY',1,1,0]`. After receipt
`after/c1-after-49cc53c.jsonl` — `result PASS`, `hidden 2 … fixtures 5 live 1 six 1`, both hidden legs
`got: [STORAGE … BLOCKED … detail=mounts:btrfs-without-sysfs]`, `census_exit 2`, live `['HEALTHY',1,1,0]`.
My hand runs match each of those leg values exactly (line strings, exits, six-plane shape), on a census
whose bytes hash to the same blob as the counter consumed.

Every one of the ten runs printed exactly six `PLANE ` lines, one `STORAGE ` line and one
`TSUKUROI_CENSUS:` line (counted over `receipts/*.out`), so the hand legs preserve the line-grammar shape
the counter's `six_planes_all` term checks.

## Risks / limits of this reproduction

1. **Exit code is not a storage signal.** All ten runs exited 2, including the base hidden legs that
   printed `HEALTHY 0/0/0` and the live runs: inside `unshare -rm` there is no user/system bus, so the
   systemd/journal planes read `BLOCKED` (`PLANE systemd: BLOCKED (systemctl --user unusable rc=1
   [Failed to connect to user scope bus …])`), and the worst-plane rule forces exit 2. The counter keys
   the STORAGE line, not the exit status, so its predicate is unaffected; a human reading exit 2 as "C1
   blocked" would be wrong in both directions.
2. **H2 perturbs other planes.** With `/sys/fs` masked the drivers plane loses its cgroup-derived fields
   (`C4_sweep=212` live/prod vs `C4_sweep=0 C5-slice=unknown` in `after-sysfs`). Irrelevant to STORAGE, but
   no other plane's line from the H2 runs is comparable to live.
3. **Userns prerequisite.** These legs (and the counter's) need unprivileged user namespaces; satisfied
   here (`kernel.unprivileged_userns_clone = 1`). If a host disables them, the counter's only binding check
   is the presence of the `unshare` binary, so it would surface as the "namespace legs produced no STORAGE
   line" error path with exit 2 rather than a distinct can't-evaluate reason — [INFERENCE] from reading
   `tools/score-storage-hidden-r39.py` (`ns_run` + the `RuntimeError` on empty stdout), not exercised.
4. **Not reproduced here** (owned by other seats): the counter's stdin-built views V0-V2 and its five
   `TSUKUROI_*` fixtures F1-F5, the hermetic selftest, and the counter run itself; this seat ran no
   counter and no `--selftest`. Only the two hidden legs, the live leg, and the two hand controls above
   were exercised. No build/lint/test gate was run by this seat (parent owns the post-integration gate).

No tooling was installed or upgraded for this seat.
