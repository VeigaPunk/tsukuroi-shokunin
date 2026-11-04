# C1Connector — sibling and lane-internal overlap scan (round 70, w1)

Read-only. No sibling edited, no mutation anywhere. Lane HEAD at scan time `84e013a732d7526d08064c6823858d602029ecd7`;
declaration commit `1710bd74aec840c71d5e4ffbdc0ca54198e953fa`. `git diff 1710bd74..HEAD -- corpus/ SKILL.md PROVINCE.md`
is **empty**, so every lane count below holds identically at the declaration and at HEAD.

Axes touched: **depth** (C1) and **operability** (C2) — this scan can only confirm or reduce them; it adds none.

## 1. Sibling scan

Scope: for each of the 20 sibling lanes, `PROVINCE.md` and `corpus/knowledge/*.md` at that sibling's current HEAD, terms
`xfs`, `xfs_info`, `xfs_spaceman`, `stats_clear`, `log_head_lsn`, `fail_at_unmount`, `max_retries`, `/sys/fs/xfs`.

| sibling | HEAD | hits | classification |
|---|---|---|---|
| mori-shokunin | `84c6cbc3b47c536a504aaee329c77897d389935e` | 19 | 18 shared/adjacent XFS ground, 1 peripheral |
| chousa-shokunin | `f748abbb6bf58388e732facd4ecec5612419c457` | 2 | peripheral |
| souji-shokunin | `83d3813257648e99fb4ab2ddef217124f39cf324` | 2 | peripheral |
| kumitate-shokunin | `3c369336218329e30248b5d69c41348c02658169` | 1 | peripheral (+2 registry rows, §1b) |
| audio, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, lore, mado, revenger, tabi, tameshi | (see run log) | 0 | no xfs mention |

SIBLINGS_SCANNED=20, SIBLING_HITS=24, TS_OWNED=0, SHARED=18 lines in 2 mori entries (+ a registry supplement in §1b).

### 1a. Shared / adjacent (mori) — file:line at mori HEAD `84c6cbc3`

`corpus/knowledge/disk-runway-enospc-r55.md` (source `S535 S536 S537 S538 S539 S540 S541 S542 S543`):

- `:19` XFS statfs assigns `f_bavail = f_bfree` (S537, `fs/xfs/xfs_super.c` v7.3)
- `:20` XFS subtracts `xfs_freecounter_unavailable` from `f_bfree` and clamps at 0 (S537)
- `:21` XFS derives `f_files` as `icount + fakeinos` from free blocks (S537)
- `:22` `maxicount` caps the reported inode total (S537)
- `:41`, `:42` decision rows: XFS `df -P` Avail→0 means block runway; XFS `df -i` IFree→0 means inode runway
- `:2` `:50` `:58` host prose: `/tmp` and `/fast` are XFS on this host, with `stat -f`/`df` figures

`corpus/knowledge/quota-observability-r48.md` (source `S479`–`S484`, `xfs_quota(8)`):

- `:26`–`:30` five XFS quota rules (accounting vs enforcement, mount-time accounting, superuser/ID-0 exemption)
- `:61`–`:63`, `:76`, `:91` boundary prose: `xfs_quota(8)` is XFS-specific; no extension to other filesystems

`corpus/knowledge/oom-tracepoints-r47.md:31` — `max_retries` as an `mm/page_alloc.c` compaction field. **Peripheral**
(kernel allocator, not the storage plane; the round's `max_retries` is the XFS error-configuration file).

Classification of the 18: **shared/report-only, sibling-owned rules**. Both entries are about *different planes* of the
same filesystem: mori holds XFS **statfs/free-space reporting** (`xfs_super.c`) and **quota accounting/enforcement**
(`xfs_quota`), while the round holds the XFS **sysfs storage plane** (`/sys/fs/xfs/<dev>/{stats,error,log}`,
`stats_clear`, `log_head_lsn`, `fail_at_unmount`). No line in either mori entry mentions `/sys/fs/xfs`, `stats_clear`,
`log_head_lsn` or `fail_at_unmount` — a targeted grep for those six terms across all 20 siblings returned **0 hits**.
Nothing here is tsukuroi-owned.

**Standing lane boundary that already covers this adjacency:** `PROVINCE.md:165` ("disk-space runway and
free-capacity [reporting] stay out"), `:216` and `:283` ("**Mori's:** disk-space runway as fleet capacity, under the
round-26 wave-2 split"), corrected at `:176` (this lane does report `/` and `/boot` free space for update safety).
A sysfs counter/error/log read is neither `df -P` runway nor capacity, so the XFS plane does not enter mori's surface.
**Gap noted, not a collision:** the lane has no overlap register against mori `disk-runway-enospc-r55.md` or
`quota-observability-r48.md` (`git grep -E 'enospc-r55|observability-r48'` over `corpus/knowledge/*.md` → 0). The new
entry should carry one boundary sentence naming mori's two entries, so the split is stated rather than assumed.

### 1b. Registry supplement (outside the item's stated grep set — reported for completeness)

`corpus/SOURCES.md` was not in the item's scan scope, but the same documents were checked there because the risk is
document identity, not prose:

- kumitate `corpus/SOURCES.md:83` **S077** = `Documentation/admin-guide/xfs.rst` at **v7.2** — the *same document*
  the round snapshots at **v7.2.11** (`before/src/xfs.rst`). Its teaches cell is mount-option ground (`noquota`,
  `pquota`, limit enforcement at mount) and it is used by `corpus/knowledge/agent-isolation-substrates.md`.
- kumitate `corpus/SOURCES.md:84` **S078** = `fs/xfs/xfs_super.c` v7.2 — emitted accounting/enforcement options.
- mori `corpus/SOURCES.md:317` **S537** = `fs/xfs/xfs_super.c` v7.3 — statfs fields (same ground as §1a).
- mori `corpus/SOURCES.md:258` **S479** = `xfs_quota(8)`.

The round's other three snapshots (`fs/xfs/xfs_stats.c`, `fs/xfs/xfs_sysfs.c`, `spaceman/health.c`) appear in **no**
sibling registry row. So: **one shared document, disjoint sections.** Rows XS1–XS6 must stay on the stats/error/log/
health sections of `xfs.rst`; a row quoting its `noquota`/`quotactl` mount-option section would duplicate kumitate
S077/S078 ground. State that as a drafting constraint, not a defect — no such row exists yet.

### 1c. Peripheral (6 lines)

- `chousa-shokunin:corpus/knowledge/openat2-resolve-r62.md:2` and `:43` — the probe ran in an xfs scratch directory on
  `/fast`; the lane tree is btrfs and was not probed. Filesystem type only.
- `kumitate-shokunin:corpus/knowledge/agent-isolation-substrates.md:47` — "`/fast/scratch` is xfs". Filesystem type only.
- `souji-shokunin:corpus/knowledge/quarantine-staging-no-copy-r23.md:30` and `:42` — `xfs 4.0` as the kernel version
  that gained `RENAME_NOREPLACE`, and an xfs probe result for the no-replace case. Kernel-version and syscall ground.

## 2. Lane-internal duplication

`git grep -n -i 'xfs' HEAD -- corpus/ SKILL.md PROVINCE.md` → **18 lines** (identical at `1710bd74`; diff empty).
Per-file: `PROVINCE.md` 2, `SKILL.md` 3, `boot-chain-r17.md` 2, `pacman-exec-environment-r40.md` 1,
`statement-corrections-r18.json` 1, and 9 lines in `corpus/lessons/*`.

All 18 are **peripheral**: mount type of `/tmp` (`PROVINCE.md:214`, `:280`; `SKILL.md:3440`, `:3465-3466`;
`pacman-exec-environment-r40.md:65`), the `xfsprogs` package in a package list (`boot-chain-r17.md:196`,
`statement-corrections-r18.json:12`, `lessons/round-18*`, `lessons/round-40*`), and the append-only `/tmp is not tmpfs`
correction (`lessons/round-26.md:136`, `lessons/round-26-verifier-spotcheck.md:86`, `lessons/round-40*`, `:43*`, `:45*`).
No line states an XFS rule. Held XFS ground in this lane: **none**.

`corpus/knowledge/storage-health-r26.md` SH1–SH6, row by row, why XFS is not covered:

| row | what it holds | why XFS is not covered |
|---|---|---|
| SH1 | btrfs's five per-device error counters, read via `btrfs device stats` and `/sys/fs/btrfs/FSID/devinfo/DEVID/error_stats` (S128, S132, S133) | btrfs-only sysfs path and btrfs-only counter set; XFS's per-filesystem `error/` tree is a different file family and XFS has no `devinfo` node |
| SH2 | those counters are a stored lifetime total, dated only by error-level kernel lines (S132) | XFS reset/clear is the write-only `stats_clear` (0200 per `before/host.txt`), a different mechanism SH2 does not describe |
| SH3 | btrfs scrub repairs only from a replica; `single` data errors uncorrectable; NOCOW file data not verified (S129, S139) | no XFS scrub is read at all (`xfs_scrub` never appears in the lane); the statement is scoped to btrfs profiles |
| SH4 | no scrub record exists on this host (`/var/lib/btrfs/scrub.status.<fsid>`, `scrub.progress` socket) (S129) | the record surface is btrfs-progs'; XFS keeps `log/` and `error/` files instead, which no row names |
| SH5 | smartctl `PASSED` is the Critical Warning byte alone (S134, S135) | device-level NVMe SMART, not a filesystem-level plane; XFS counters are per-filesystem, not per-device |
| SH6 | NVMe lifetime counters (Unexpected Power Losses) are not dated events (S135) | same device-level plane as SH5; says nothing about any filesystem's counters |

Registry rows S128–S139 (`corpus/SOURCES.md:134-145`): S128 `btrfs-device(8)`, S129 `btrfs-scrub.rst`,
S130 `mkfs.btrfs.rst`, S131 `btrfs-scrub@.timer`, S132 `fs/btrfs/volumes.c`, S133 `fs/btrfs/sysfs.c`,
S134 `nvmeprint.cpp`, S135 NVMe Base 2.4, S136 `systemd.resource-control.xml`, S137 `systemd-oomd.service.xml`,
S138 `cgroup-v2.rst`, S139 `ch-scrub-intro.rst`. **Not one is an XFS file.** S133 is the nearest *shape* — a sysfs
attribute reader — but for `fs/btrfs/sysfs.c`; the round's `fs/xfs/xfs_sysfs.c` is a different subsystem and file, and
no rule sentence is shared.

`git ls-tree -r --name-only HEAD -- corpus/ | grep -ci xfs` = **0**; `corpus/knowledge/xfs-storage-plane-r70.md` is
absent (`git cat-file -e` rc **128**). No lane-internal duplicate rule exists.

## 3. PROVINCE verdict

Declared storage frontier: `PROVINCE.md:154-176` — "**Round-26 frontier: storage integrity.** Btrfs device error
counters, scrub records and NVMe health enter this province as a frontier area of the OS substrate." It enumerates
exactly three mechanisms (btrfs's five counters; the scrub record + `btrfs-scrub@.timer`; NVMe SMART lifetime fields)
and closes with "Detection and report [only] … no package, service, mount, scrub, counter-reset, firmware or
Btrfs/LUKS operation."

Promotions: `:199` R38-STORAGE-CORE (btrfs counters Frontier→Core, on a verdict-neutral census arm);
`:256` R44-SCRUB-VIEW (unprivileged scrub-record view Frontier→Core, same condition).

**Both promotion sections name the XFS device as unread:** `:214` and `:280` — "The second NVMe device (xfs on `/tmp`,
`/fast`) has no btrfs counters and **stays unread**." `corpus/README.md:243` states the promotion rule: storage
integrity "becomes Core only after a read-only census arm reads it."

So the new surface is **inside the province's storage-integrity area** (same host, same second NVMe device the province
already names, read-only detection) but is **not on the enumerated frontier list**, and the province twice declares the
device unread. The C1 note alone is Frontier-level knowledge and could be appended as a new frontier reading; the C2
census arm (`XFS xfs-stats …`, a read-only unprivileged arm with no rollup term, exactly the R38/R44 shape) makes the
surface Core-class, and under README:243 plus the R38/R44 precedent that requires an **appended frontier-to-core
promotion paragraph** naming the plane, the arm, the frontier limit that remains (`stats_clear` is 0200 write-only and
operator-owned, so a reset is never read or performed) and the operator-owned actions (counter clear, repair, mount).
It is **not** a promotion of the btrfs counter row and must not supersede `:214`/`:280`; those sentences stay true for
btrfs and are narrowed, not deleted, by an appended XFS paragraph. It is **not** out of province: it is neither
mori's `df` capacity surface (`:165`, `:216`, `:283`) nor a sibling's declared surface.

## 4. Novelty sweep — not defeated, with one stated discrepancy

Same greps at the frozen declaration `1710bd74` and at HEAD (corpus/, SKILL.md, PROVINCE.md):

- `grep -ci xfs` → **18** at `1710bd74`, **18** at HEAD, per-file identical (`git diff --stat` empty). Matches the
  declaration's "18 xfs lines, all peripheral".
- `/sys/fs/xfs`, `stats_clear`, `log_head_lsn`, `fail_at_unmount`, `xfs_info`, `xfs_spaceman` → **0** hits at both
  revisions (`git grep` rc 1).
- `corpus/knowledge/xfs-storage-plane-r70.md` → absent (rc 128); `ls-tree -- corpus/ | grep -ci xfs` → 0.

**Counterexample check (a held XFS rule):** none in this lane. The nearest held XFS rules live in mori and are
statfs/quota ground, not the sysfs plane — `mori:corpus/knowledge/disk-runway-enospc-r55.md:19,20,21,22` (six rules with
their decision rows at `:41,:42`) and `mori:corpus/knowledge/quota-observability-r48.md:26,27,28,29,30`. **Zero**
duplicate rules for XS1–XS6.

**Discrepancy, stated rather than smoothed.** The declaration's sweep command is written as
`git ls-tree … | grep -i xfs | wc -l` = **0**. Run as written at the declaration commit it prints **3**:
`.ufo/waves/round-70/before/src/{xfs.rst,xfs_stats.c,xfs_sysfs.c}` were committed *by that same commit*
(`git log --diff-filter=A` → `1710bd74 round-70: declaration`). The intended proposition — no held XFS knowledge note —
is true (`-- corpus/` → 0), and the substantive novelty finding is unaffected; the `0` is a mis-transcribed command
scope, not a false novelty claim. Anyone re-deriving the sweep must add `-- corpus/` or the before/src path filter, and
the round's own record should say so rather than leave a counterexample to its own receipt.

## Risks and verification

- **Risk — shared document, not shared ground.** `before/src/xfs.rst` is the same URL as kumitate S077 at the older tag.
  If any XS row quotes the mount-option or quota section, it duplicates sibling ground. Verification: every XS quote,
  whitespace-normalized, must fall outside the `Mount Options`/quota sections of the snapshot; the frozen counter's
  quote-in-snapshot check cannot see this, so it is a drafting constraint on the note's author.
- **Risk — province silence.** If the round lands C1 and C2 without a promotion paragraph, the census reads a device
  `PROVINCE.md:214`/`:280` declares unread, and the round's own province record contradicts its arm.
- **Risk — mori boundary drift.** mori's r55 entry reports `/tmp` and `/fast` XFS capacity; the round must not restate
  capacity or threshold it (`PROVINCE.md:216`).
- **Verification.** `git -C mori-shokunin grep -n -E '/sys/fs/xfs|stats_clear|log_head_lsn' HEAD` → empty (re-run at the
  next mori commit); `git -C tsukuroi-shokunin grep -c -i xfs HEAD -- corpus/ SKILL.md PROVINCE.md` → 18 until the note
  lands; `bash tools/tsukuroi-census.sh --selftest` must keep the base rollup and rc 1 (untouched by this scan).

SIBLINGS_SCANNED=20 SIBLING_HITS=24 TS_OWNED=0 SHARED=18 LANE_XFS_LINES=18 DUPLICATE_RULES=0 PROVINCE_VERDICT=promote
