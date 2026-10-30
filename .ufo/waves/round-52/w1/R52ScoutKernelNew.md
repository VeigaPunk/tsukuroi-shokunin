VERDICT: supports

# R52ScoutKernelNew — Item W-S3 (freshness receipt for S240)

Scope: `git ls-remote --tags` on the kernel.org stable tree, then fetch `fs/btrfs/ioctl.c`
at any newer tag and `diff -u` it against the pinned
`.ufo/waves/round-43/frozen/src/ioctl.c` (v7.2.11). Read-only; no entry edit, no lane write.
Receipts: `.ufo/waves/round-52/w1/R52ScoutKernelNew/` (`receipt-freshness-r52.txt`,
`diff-v7.2.11-v7.3-ioctl.c.diff`, `ioctl-v7.3.c`, `ioctl-v7.2.13.c`).

## 1. Tags found

Command (2026-10-30, from scratch dir `/fast/scratch/hyaku/tsukuroi-r52/R52ScoutKernelNew`):

```
git ls-remote --tags https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git 'v7.2.*' 'v7.3*'
```

Observed (full listing in `receipt-freshness-r52.txt`):

- **v7.2.x tags: 13** — `v7.2.1` … `v7.2.13`. The **newest v7.2.x tag is `v7.2.13`**
  (tag object `296212c45bc6d5df741180926c80a1c262fa5c7f`, peeled commit
  `3c172eede0d6b889ead876f45cc843070209208f`).
- **A `v7.3` final tag exists** (tag object `091b06388b117fefdcb63336ac09956a4914b961`,
  peeled commit `c03c1a14507dfaf8b856c2608f9ac216021fc222`), preceded by
  `v7.3-rc1` … `v7.3-rc7`.
- No `v7.2.14`+ and no `v7.3.1`+ point releases exist yet
  (`git ls-remote --tags … 'v7.2.1[4-9]*' 'v7.3.[1-9]*' 'v7.2.2*' 'v7.3.1*'` returned only
  `refs/tags/v7.2.2`; no later v7.2.x/v7.3.x). So `v7.2.13` and `v7.3` are the two tips
  above the pinned `v7.2.11` (`8316c24ec1b77dba19ba072ca4fe251b36dc65d3`, peeled
  `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` — matching the S240 row's own pin).

## 2. Fetched bytes

```
curl -sSfL "https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=<TAG>" -o ioctl-<TAG>.c
```

| file | sha256 | lines |
|---|---|---|
| pinned `round-43/frozen/src/ioctl.c` (v7.2.11) | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` | 5678 |
| `ioctl-v7.2.12.c` | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` | 5678 |
| `ioctl-v7.2.13.c` | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` | 5678 |
| `ioctl-v7.3.c` | `c8f10829c360592a025e3ec738a8abf17ef1c038fee92dbe564a3f328cf58710` | 5720 |

**The newest v7.2.x (v7.2.13) `ioctl.c` is byte-identical to the pinned v7.2.11 snapshot** —
same sha256. The stable v7.2 series did not touch this file after v7.2.11.

`v7.3` **does** change it: `diff -u` yields 29 hunks, **+84 / −48** lines
(`diff-v7.2.11-v7.3-ioctl.c.diff`). The change is entirely outside the scrub surface:
compression-type handling for `FS_IOC_SETFLAGS` (keep the algorithm recorded in the inode
property instead of resetting it to the mount default), `btrfs_start_transaction(root, 3)` →
`(root, 2)`, snapshot-create losing its explicit `file_mnt_idmap(file)` argument, and a
refactor of `btrfs_search_path_in_tree` (`info, tree_id, dirid` → `root, dirid`).
**`grep -i scrub` over the diff returns nothing** — no line of the diff mentions scrub.

## 3. Did the cited regions change?

The gap block cites `ioctl.c` **3066-3075**, **3118-3140**, **5578-5584** (the S240 row in
`corpus/SOURCES.md:249` cites the same three ranges). In v7.3 the file grew by 42 lines,
so the regions shift; the *content* is compared at the shifted offsets
(`+6` for the two handler blocks, `+42` for the dispatch block — the extra 36 lines come from
hunks between lines 3140 and 5578):

| cited region (v7.2.11) | v7.3 location | byte comparison |
|---|---|---|
| 3066-3075 (`btrfs_ioctl_scrub`, `capable(CAP_SYS_ADMIN)`/`-EPERM`) | 3072-3081 | **IDENTICAL** |
| 3118-3140 (`btrfs_ioctl_scrub_cancel`, `btrfs_ioctl_scrub_progress`) | 3124-3146 | **IDENTICAL** |
| 5578-5584 (dispatch `case BTRFS_IOC_SCRUB:` … `SCRUB_PROGRESS`) | 5620-5626 | **IDENTICAL** |

No diff hunk overlaps any cited range: the v7.3 hunks fall at baseline lines
384-392, 1143-1155, 1227-1278, 1664-1746, 1884-1916, 2636-2692, 2848-2855, 3620-3794 —
the last one ends at baseline 3794, well before the 5578 dispatch block.

The same check was run for **every individual line** the round-52 grounding row quotes from
S240 (`corpus/knowledge/btrfs-scrub-grounding-r45.md:191-209`, `:370`), i.e. baseline
3075, 3080, 3084, 3085, 3088, 3093, 3109, 3110, 3115, 3120, 3132, 3133, 3190 — all 13 are
byte-identical at +6 in v7.3, including:

```
base ioctl.c:3072 = "	if (!capable(CAP_SYS_ADMIN))"   == v7.3 ioctl.c:3078
base ioctl.c:3133 = "		return -EPERM;"              == v7.3 ioctl.c:3139
base ioctl.c:3093 = "	ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end," == v7.3 ioctl.c:3099
```

(Sources of the line list: `corpus/knowledge/btrfs-scrub-grounding-r45.md:191-209` and
`:370`; the record `corpus/knowledge/btrfs-scrub-record-r43.md:119-129` quotes
`ioctl.c:5582`, `:3126`, `:3132-3133`, `:3072`, `:3120`.)

## 4. Verdict — pins stale or current

**The S240 pin is CURRENT in substance; only its tag is no longer the newest of its
series, and that costs nothing.**

- The substantive claim — "the scrub start, cancel and progress ioctls each return `EPERM`
  to a caller without `CAP_SYS_ADMIN` before any other check" — holds byte-for-byte at the
  newest v7.2.x (**v7.2.13**, file identical to the pin) and at **v7.3** (same code at
  shifted line numbers). Nothing in the cited regions changed.
- The pin's own re-open discipline is also still satisfied: the S240 row says
  "reopened live 2026-10-28, byte-identical" (`corpus/SOURCES.md:249`), and that re-open
  was already recorded at
  `corpus/lessons/round-51-verifier-spotcheck.md:70` (145999 B, same sha256). This seat
  independently re-confirms byte-identity for v7.2.12/v7.2.13.
- The only "stale" aspect is **label freshness of the anchor**: the row pins tag `v7.2.11`
  while `v7.2.12` and `v7.2.13` now exist, and a `v7.3` final release exists (the newest
  release of the series line, 2026-10-30). This is a *pin-vintage* observation, not a
  *correctness* defect: the file the row cites is unchanged across both, so every quote and
  every line-range the row states remains true of the bytes it pins, and remains true of the
  latest upstream `ioctl.c` modulo a uniform +6 / +42 line shift.

**Consequence for the round-52 counted rows (C1 / GR1-GR3):** nothing here disturbs them.
S240's quotes and ranges are unaffected by the newer tags. No entry edit was made (the item
is read-only).

## 5. Frontier note (for the L1, optional, non-binding)

If the lane ever wants the anchor to name the newest stable point release rather than
v7.2.11, `v7.2.13` is a drop-in replacement for the *file* (identical sha256) — but the
row's tag/peeled-commit string and the `verified-at:` date would then need updating, and
that is an entry edit this seat was not authorized to make. Note also that the row's line
ranges are tag-relative; under v7.3 they become 3072-3081 / 3124-3146 / 5620-5626, so any
future re-pin must re-derive the ranges rather than carry them over.

## 6. What I did NOT do

- Did not edit any tracked lane file, any corpus/SOURCES.md row, or any knowledge file.
- Did not run `git add/commit/checkout` anywhere; no fixture repo was needed (no commit
  required by this item). No jj command was run.
- Did not fetch or diff `fs/btrfs/scrub.c` (S242), `fs/btrfs/sysfs.c` (S243) or the
  `lib/` files (S246) at newer tags — out of this item's scope; their freshness is
  unmeasured here.
- Did not re-fetch `ioctl.c` at `v7.2.11` itself (the round-51 re-open at
  `corpus/lessons/round-51-verifier-spotcheck.md:70` already did, live, on 2026-10-28);
  byte-identity of v7.2.12/v7.2.13 to the pinned v7.2.11 snapshot is established by equal
  sha256 of the fetched bytes.
- Did not install or upgrade any tool; none was needed.

## 7. Tooling

No installs, no upgrades. Everything used was already present (`git`, `curl`, `diff`,
`sed`, `grep`, `sha256sum`).

Scratch: `/fast/scratch/hyaku/tsukuroi-r52/R52ScoutKernelNew/` — removed after the
receipts above were copied into
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-52/w1/R52ScoutKernelNew/`.
