VERDICT: supports

# C2-F3 — S240 live re-open (SrcReopenS240, wave 2, round 43)

Seat: re-open S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`) live, verify identity, locate the Gate
quote, and check every cell of the S240 row (`corpus/SOURCES.md:249`) against the source.
All commands ran 2026-10-26 19:53-19:58 local, scratch `/fast/scratch/hyaku/tsukuroi-r43/SrcReopenS240/`
(removed after copying receipts). Lane touched read-only only.

## 1. Identity of the source — holds

- Live fetch (exact seat command):
  `curl -sSfL 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11' -o s240-live.c`
  → 145,999 bytes, sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`.
- Frozen copy `.ufo/waves/round-43/frozen/src/ioctl.c`: same sha256; `diff -q` → identical.
- `.ufo/waves/round-43/frozen/src/SHA256SUMS:1` lists exactly that digest for `ioctl.c`.
- Gate's mirror claim (`corpus/lessons/round-43.md:19`, "byte-identical to
  https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/ioctl.c"): fetched it,
  sha256 identical, `diff -q` vs live → identical.
- Tag: `GIT_TERMINAL_PROMPT=0 git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git 'refs/tags/v7.2.11' 'refs/tags/v7.2.11^{}'` →
  `8316c24ec1b77dba19ba072ca4fe251b36dc65d3  refs/tags/v7.2.11`,
  `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea  refs/tags/v7.2.11^{}`.
  The peeled commit matches the row, the Gate row, and `FETCH.txt:1`.
- Provenance cross-check: `.ufo/waves/round-43/frozen/src/FETCH.txt:1-4` records the L1's
  2026-10-26 fetch from the GitHub mirror with the same digest and the same tag peel from the
  stable tree; my re-open went the opposite direction (git.kernel.org plain + stable ls-remote)
  with identical results. No drift between the pinned snapshot and today's upstream.
- Not done (stated): no full/partial clone, so the blob is tied to the tag by the plain
  endpoint's bytes plus ls-remote, not by a local tree walk. Two independent hosts agree, and
  the plain URL is parameterized `?h=v7.2.11`.

## 2. Gate quote — holds (one cosmetic location nit)

Gate row for S240 is `corpus/lessons/round-43.md:19`; quote: `"if (!capable(CAP_SYS_ADMIN))"` /
`"return -EPERM;"` — "the first check in each of the three scrub handlers"; location
`.ufo/waves/round-43/frozen/src/ioctl.c:3072-3073, 3120-3121, 3132-3133` (handlers open
`:3066`, `:3118`, `:3126`; dispatch `:5582-5583`).

Verified in the frozen bytes (grep -n, and line-ranged reads; live copy byte-identical per §1):

- `ioctl.c:3066` `static long btrfs_ioctl_scrub(struct file *file, void __user *arg)`; first
  executable statement is `3072-3073` `if (!capable(CAP_SYS_ADMIN))` / `return -EPERM;`
  (declarations only at 3068-3070 precede it).
- `ioctl.c:3118` `static long btrfs_ioctl_scrub_cancel(struct btrfs_fs_info *fs_info)`;
  `3120-3121` capable/EPERM, then `3123` `return btrfs_scrub_cancel(fs_info);` — nothing before.
- `ioctl.c:3126` `static long btrfs_ioctl_scrub_progress(...)` (signature to 3127, `{` 3128,
  declarations 3129-3130); `3132-3133` capable/EPERM, then `3135` `memdup_user` — nothing before.
- Dispatch: `5578` `case BTRFS_IOC_SCRUB:`, `5580` `case BTRFS_IOC_SCRUB_CANCEL:`,
  `5582` `case BTRFS_IOC_SCRUB_PROGRESS:` with `5583` `return btrfs_ioctl_scrub_progress(...)`.

Nit (cosmetic, no claim depends on it): the Gate's `dispatch :5582-5583` names only the
SCRUB_PROGRESS case; the SCRUB and CANCEL dispatches sit at `5578-5579` and `5580-5581`. The
row's own anchor `5578-5584` spans all three, so the substance is located either way.

## 3. S240 row cells (`corpus/SOURCES.md:249`) — verdict per cell

| Cell | Value | Verdict | Evidence |
|---|---|---|---|
| kind | `code` | holds | Kernel C source implementing the btrfs ioctl switch; scrub handlers at `ioctl.c:3066/3118/3126`, dispatch `5578-5583`. |
| tier | `A` | holds | Pinned upstream tagged source on git.kernel.org; consistent with the registry's other pinned official code rows (e.g. S228-S235, S237-S238, all tier A); column layout defined at `SOURCES.md:5`. |
| scope | "Which btrfs scrub ioctls require CAP_SYS_ADMIN and what a caller without it gets back" | holds | All three scrub ioctls gate on `!capable(CAP_SYS_ADMIN)` → `-EPERM` before anything else (`3072-3073`, `3120-3121`, `3132-3133`). The scope names exactly what the anchors show, no more. |
| anchor | tag v7.2.11 (peeled `a2de78ee…cb6ea`), lines `3066-3075`, `3118-3140`, `5578-5584`; sha256 `7b3488f2…4ba01` | holds, 2 cosmetic notes | Peel verified by ls-remote today (§1); digest matches live fetch, frozen copy, `SHA256SUMS:1`. `3066-3075` = scrub handler open → EXTENT_TREE_V2 branch (`3075`). `3118-3140` = cancel handler whole (`3118-3124`) plus progress up to `3140` (the capable checks are inside; the `copy_to_user` epilogue `3141-3145` lies outside — acceptable as an anchor). Note 1: `5578-5584` includes `5584` `case BTRFS_IOC_BALANCE_V2:`, one line beyond the scrub dispatch (substantive range `5578-5583`). Note 2: `3118-3140` stops one line before progress's epilogue. Neither affects any adopted sentence. |
| teaches | "The scrub start, cancel and progress ioctls each return EPERM to a caller without CAP_SYS_ADMIN before any other check" | holds | "Before any other check" verified per handler: the capable test is the first executable statement in each (`3072`, `3120`, `3132`); only declarations precede. "Each" = exactly the three ioctl handlers dispatched at `5578/5580/5582`; other capable checks in the file (e.g. `456`, `2527`) belong to non-scrub handlers and are outside the row's anchors. |
| status | `mined` | holds | Row is consumed: `corpus/knowledge/btrfs-scrub-record-r43.md:1` names S240 in its source line and quotes it at `:118,120,122,124,126,128`, every quoted line matching the verified numbers (`5582`, `3126`, `3132`, `3133`, `3072`, `3120`). `lessons/round-43.md:34` "S240 and S241 are new rows (`mined` at entry)". |
| opened | `2026-10-26` | holds | `lessons/round-43.md:15` "New SOURCES rows (opened 2026-10-26 by this round's L1…)"; `FETCH.txt:1` dated 2026-10-26; Gate URL access date 2026-10-26 (`lessons/round-43.md:17`); my re-open fetched identical bytes the same day. |
| recheck | `on-release` | holds | Matches the registry's convention for pinned-tag code rows (S237 and S238, same tag pattern, also `on-release` at `SOURCES.md:247-248`); a new kernel release is the event that would move the anchor. |
| used-by | `corpus/knowledge/btrfs-scrub-record-r43.md` | holds | File exists at that path, sha256 `a5773068…27ce7d`, cites S240 seven times (line-accurate quotes, see status). |

## 4. Row-at-tip identity — holds

The row I audited is the frozen one: `git show 8acf0b022586a0f3164c77659fb96ba5f90949b6:corpus/SOURCES.md`
sha256 `b34dc1cd…7691ccf` == working-tree `corpus/SOURCES.md`; same equality for
`corpus/lessons/round-43.md` (`b4e6814f…c00fd06`) and `corpus/knowledge/btrfs-scrub-record-r43.md`
(`a5773068…27ce7d`); `git status --porcelain=v1 -- corpus/` → 0 lines. Note: current lane HEAD is
`64646d6e5749e0b5b6e458aa0753d39c47404e6b` (the L1 has moved past the tip under test); the
comparison was made against `8acf0b0…` explicitly.

## 5. Not done / residual

- No local clone of the linux tree, so no `git rev-parse v7.2.11:fs/btrfs/ioctl.c`-style blob-id
  proof; identity rests on byte-identical fetches from two hosts plus ls-remote of the tagged ref (§1).
- The Arch-kernel-patch claim ("7.2.11-arch1-1 applies one patch touching no `fs/` file",
  `lessons/round-43.md:24-25`) is out of this seat's item; not re-verified here.
- S241 (capture) cells are another seat's item; untouched.

## Receipts

`.ufo/waves/round-43/w2/SrcReopenS240/` — `ioctl.c-live-refetch-gitkernel.c` (145,999 B),
`ioctl.c-github-mirror.c` (145,999 B), `receipts.txt` (commands + observed outputs).
Scratch `/fast/scratch/hyaku/tsukuroi-r43/SrcReopenS240/` removed.

No installs or upgrades were performed (none needed).
