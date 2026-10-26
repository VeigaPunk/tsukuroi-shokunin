VERDICT: supports

Hypothesis C1-9 holds, with one correction to its example: on a real namespace the
`mounts:unreadable` branch **is** reachable and prints the declared line byte-for-byte, but only
while `/proc/self/fd` keeps working. The example in the item — masking `/proc` in a private
namespace — does **not** reach the storage arm: `tools/tsukuroi-census.sh:673` uses bash process
substitution (`mapfile -t names < <(...)`), which needs `/dev/fd` → `/proc/self/fd`, so the whole
census aborts with exit 1 and emits **no** STORAGE line, hidden sysfs or not. Under the corrected
construction the branch fires and the line matches the declaration exactly.

## Identity / environment (read-only)
- Lane HEAD `394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (`git -C … rev-parse HEAD`).
- `tools/tsukuroi-census.sh` sha256 `e5666331caf08477d4e3a704e8349c2cd64b9f16456818fef2e9e80e82766f0d`;
  byte-identical to `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82:tools/tsukuroi-census.sh`
  (`git show …:tools/tsukuroi-census.sh | sha256sum` and `git diff --stat 49cc53c HEAD -- tools/tsukuroi-census.sh` → empty).
- Branch under test: `tools/tsukuroi-census.sh:1903-1914` (`if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]`;
  table open at :1906, `mounts:unreadable` at :1912).
- Host: `unshare from util-linux 2.42.4`, `GNU bash, version 5.3.20(1)-release`; host `/proc/self/mounts`
  lists 4 btrfs mounts (`/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`); `/sys/fs/btrfs` holds fsid
  `1d02a454-c549-4a35-b567-89d60902af8e`.
- Counter sha256 `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` matches the declaration
  (`sha256sum tools/score-storage-hidden-r39.py`).
- No host mutation: every mount below is inside a private `unshare -rm` namespace; scratch
  `/fast/scratch/hyaku/tsukuroi-r39/C1LabratProcAbsent/` (removed at the end); no pacman/sudo/service action,
  nothing installed.

## Probes (all commands run as shown; `$CEN` = `tools/tsukuroi-census.sh`; full transcript in
`.ufo/waves/round-39/w1/C1LabratProcAbsent/receipts.txt`)

| # | namespace construction | observed STORAGE line |
|---|---|---|
| A | `unshare -rm`, nothing hidden | `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` (ns table: 4 btrfs lines) |
| B | `mount -t tmpfs r39hide /sys/fs/btrfs` only | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |
| C | B **plus** `mount -t tmpfs r39proc /proc` | **no STORAGE line**: `census_rc=1`, `out_lines=2`, `storage_lines=0`, output = banner + `tools/tsukuroi-census.sh: line 673: /dev/fd/63: No such file or directory` |
| D | `mount -t tmpfs r39proc /proc` only (control, sysfs visible) | **no STORAGE line**: `census_rc=1`, `out_lines=2`, `storage_lines=0`, same line-673 error → the abort is caused by the masked `/proc`, not by the storage arm |
| E | `unshare -rmpf --mount-proc` + hidden sysfs | `STORAGE … state=BLOCKED … detail=mounts:btrfs-without-sysfs` (fresh proc still lists 4 btrfs mounts) |
| F | `unshare -rm`, `umount /proc` | `umount: /proc: not mounted.` `umount_rc=32`; `/proc/self/mounts` still present → "no /proc at all" not constructible this way |
| G | `mount --bind /dev/null /proc/$$/mounts`, then read from a child | `child-sees-bytes=3377` → a per-PID mask never reaches the reader (`/proc/self` resolves to the reader's own PID) |
| H | **pid+mount ns**: real procfs at `$S/realproc-h`, tmpfs over `/proc`, `/proc/self/fd` symlinked to `$S/realproc-h/self/fd`, sysfs hidden | `procsub-ok=n=2`; `census-table-open: cat: /proc/self/mounts: No such file or directory` `cat_rc=1`; `census_rc=2`; **`STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable`** |
| I | H but sysfs **visible** (control) | `STORAGE … state=HEALTHY filesystems=1 devices=1 nonzero=0` → fsid path, table never read |
| J | H but `/proc/self/mounts` present and **empty** | `masked-table-bytes=0`; **`STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0`** (no `mounts:` token) |
| K | `/proc` intact, sysfs hidden, `TSUKUROI_PROC_MOUNTS=/nonexistent/table` | `STORAGE … detail=mounts:unreadable` |
| L | `/proc` intact, sysfs hidden, `TSUKUROI_PROC_MOUNTS=/dev/null` | `STORAGE … state=HEALTHY filesystems=0 devices=0 nonzero=0` (no `mounts:` token) |
| M | `/proc` intact, sysfs hidden, `TSUKUROI_PROC_MOUNTS=/proc/mounts` | `STORAGE … detail=mounts:btrfs-without-sysfs` |

Exact commands for the two decisive legs (verbatim from `receipts.txt`):

```
$ unshare -rmpf bash -c 'S=$S; mkdir -p $S/realproc-h && mount -t proc proc $S/realproc-h
  mount -t tmpfs r39hide /sys/fs/btrfs; mount -t tmpfs r39proc /proc
  mkdir -p /proc/self && ln -s $S/realproc-h/self/fd /proc/self/fd
  bash $CEN > $S/h-p7.out 2>&1; echo census_rc=$?'
realproc-mounted / real-ns-mounts-btrfs-lines=4 / sysfs-hidden / proc-masked
procsub-ok=n=2
census-table-open: cat: /proc/self/mounts: No such file or directory   (cat_rc=1)
census_rc=2
STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:unreadable
```

```
$ unshare -rm bash -c 'mount -t tmpfs r39hide /sys/fs/btrfs; mount -t tmpfs r39proc /proc
  bash $CEN > $S/c-p2.out 2>&1; echo census_rc=$?; echo storage_lines=$(grep -c "^STORAGE" $S/c-p2.out)'
census_rc=1
storage_lines=0
```
(`.ufo/waves/round-39/w1/C1LabratProcAbsent/c-p2.out`, `d-p2c.out`, `h-p7.out`, `j-p9.out` are the captured runs.)

## What this establishes
1. **Reachability (the item's question): yes.** H shows the branch executing inside a real namespace with
   only real mounts (no fixture, no counter override): `/sys/fs/btrfs` hidden by a tmpfs, `/proc` a tmpfs with
   no `self/mounts`, and the emitted line is character-identical to the declaration
   (`SCORECARD.md:2220`, clause "an unreadable table prints `detail=mounts:unreadable`").
   The trigger is the table open failing (`cat` rc=1, ENOENT), which is exactly what
   `tools/tsukuroi-census.sh:1906` tests; an absent path and an unreadable file are the same branch.
   The H run completes to its `TSUKUROI_CENSUS:` rollup line (six PLANE lines present, `census_rc=2`), so the
   arm executed inside the whole tool, not in isolation.
2. **The example named in the item fails as stated.** Masking `/proc` alone (D) or together with the hidden
   sysfs (also C) never reaches `probe_storage_arm`: the census dies at `tools/tsukuroi-census.sh:673`
   (`mapfile -t names < <(...)`, one of 7 process substitutions in the file) because bash resolves
   `/dev/fd/63` through `/proc/self/fd`. Observed: `census_rc=1`, 2 output lines, `storage_lines=0`.
   Control D proves the cause is `/proc`, not the storage arm. Line 673 predates round 39
   (`git log -S'mapfile -t names'` → `5f90645`, the first census commit), so this is structural, not a
   round-39 regression.
3. **A fresh procfs is not a way out.** E mounts a *new* procfs (`--mount-proc`) and it lists the namespace's
   inherited btrfs mounts, so the arm correctly reads `mounts:btrfs-without-sysfs`, not `unreadable`.
4. **Per-PID masking is a dead end (G).** `/proc/self/mounts` is resolved by each reader, so
   `mount --bind /dev/null /proc/$$/mounts` leaves the census's own `cat` reading the unmasked table
   (`child-sees-bytes=3377`). This is why H needs the fd relay.
5. **"No `/proc` at all" was not constructed.** `umount /proc` inside `unshare -rm` (also `-l`,
   `mount --make-rslave /`, `--propagation private`) returns `umount: /proc: not mounted.` rc=32 while
   `/proc/self/mounts` stays present (F); mounting a real procfs at a scratch path without a PID namespace
   fails `mount: … permission denied` (procfs needs a PID namespace owned by the userns — hence `-p` in H/J).
   I therefore cannot report the "not mounted" leg; I did not pursue a second mechanism.
6. **The override seam also reaches the branch (K)** and behaves consistently on the production path
   (M → `btrfs-without-sysfs`), so the branch is exercised by the declared seam as well as by a namespace.

## Adjacent defect candidate (reported, not judged; the counter cannot see it)
**A readable but empty mount table still reads as a clean disk.** With `/sys/fs/btrfs` hidden and
`/proc/self/mounts` present but empty (J: `masked-table-bytes=0`, real namespace table holding 4 btrfs mounts),
the line is `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` — no `mounts:` token.
The same happens through the documented seam with an empty file (L: `TSUKUROI_PROC_MOUNTS=/dev/null`).
- Against the enumerated spec this is conformant: the contract (`tools/tsukuroi-census.sh:364-368`) and the
  claim (`SCORECARD.md:2220`) say HEALTHY only when the table "lists no btrfs mount", which an empty table does.
- Against the leading sentence of C1 ("stops reading a hidden or absent btrfs sysfs root as a clean disk",
  `SCORECARD.md:2220`) it is a counterexample: the root is hidden and the arm reads clean.
- Why the frozen counter cannot catch it: both hidden legs assert equality with `HIDDEN_LINE`
  (`detail=mounts:btrfs-without-sysfs`, `tools/score-storage-hidden-r39.py:60-61,206`), the view and live legs
  reject any `mounts:` token outright (`:223,261`), and the only fixture for this branch feeds a **missing**
  file, never an empty one — `'F3-absent-root-mounts-unreadable': (None, None, …detail=mounts:unreadable')` at
  `tools/score-storage-hidden-r39.py:72-74` writes no `mounts` file at all (`mounts is None`, `:243-244`).
  A sixth fixture with `mounts=''` (empty file) encoded as `mounts:unreadable` would pin the stricter reading;
  against the current code that fixture would read `HEALTHY 0/0/0` and fail, which is the gap in one line.
- Severity for operability [INFERENCE]: a mask that hides both the sysfs root and the table (or an operator
  pointing the seam at an empty file) yields a GREEN storage line with counters invisible. Closing it means
  treating an empty table as `mounts:unreadable` (or adding a distinct `mounts:empty` token), which changes
  the frozen literal in the claim and would need a new round.

## Self-assessment / limits
- Supported: H, K, M (branch executes, declared line exact), B, E (production path in a namespace), A, I (controls).
- Not done: no attempt at a kernel-level EACCES mask of `/proc/self/mounts` on a live host (would need an LSM
  or `/etc` change — forbidden here); no attempt to construct "no procfs mounted at all" beyond F; I did not run
  the frozen counters (`tools/score-storage-hidden-r39.py`) — that is the parent's gate, and my scratch clone
  was unnecessary for a read-only reachability question.
- C2 TO rows judged: none (C2 not in this seat's scope).
- Tooling: nothing installed or upgraded (pacman paused host-wide; `unshare`/`bash` already present).
- Lane writes: only `.ufo/waves/round-39/w1/C1LabratProcAbsent.md` and its receipt dir; every other write went to
  `/fast/scratch/hyaku/tsukuroi-r39/C1LabratProcAbsent/` (deleted after the receipts were copied). `git status`
  at report time also shows `M PROVINCE.md` and `M SKILL.md` — concurrent seats' edits, never opened for write
  by this seat; no tracked file was modified here.

## Receipts (in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/w1/C1LabratProcAbsent/`)
- `receipts.txt` — transcript of legs A–K with identity header (lane HEAD, census sha256, tool versions).
- `receipts-addendum.txt` — P11/P12 (= table rows L and M): override seam with an empty file and with the real table.
- `probe.sh` — the exact probe script that produced `receipts.txt`.
- `c-p2.out` (2 lines, naive masked `/proc`), `d-p2c.out` (control), `h-p7.out` (branch fires,
  `detail=mounts:unreadable`), `j-p9.out` (empty readable table → HEALTHY 0/0/0).
