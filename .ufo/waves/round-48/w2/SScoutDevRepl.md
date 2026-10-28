VERDICT: supports

Item SRC-SScoutDevRepl — S247 live re-open (round 48, w2). Opener of record: SScoutDevRepl.

## 1. Fetch

- SOURCES row (frozen corpus/SOURCES.md line 256, revision ae99f021b76f8eb1c8805d32d80644464afb1ff6): `S247 | Linux v7.2.11 fs/btrfs/dev-replace.c — https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/dev-replace.c?h=v7.2.11`.
- Row URL is the cgit `tree` (HTML) view; the pinned raw bytes were fetched per the round-45 FETCH.txt via the `plain` endpoint. Fetched LIVE this round:
  `curl -fsSL --max-time 60 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/dev-replace.c?h=v7.2.11'` → HTTP 200, **no redirect** (`%{redirect_url}` empty).
- Access date (UTC): **2026-10-28**.
- sha256 of fetched bytes (39841 bytes): **f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a**.
- Pinned snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-45/frozen/src/dev-replace.c` sha256: **f07ef0a0d260cf67b7c2aff0542ec13204f9761e33df0ea9feedf143cc034f3a** (matches the digest recorded in the row and in frozen src/SHA256SUMS).
- `cmp snapshot live` → byte-identical. **Upstream did not move**: the pin is tag `v7.2.11` (annotated tag object 8316c24ec1b77dba19ba072ca4fe251b36dc65d3, peeled commit a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea); `git ls-remote` on 2026-10-28 returns the same tag object and same peeled commit as the round-45 FETCH.txt. This is a tag pin, not a branch tip — no drift expected and none observed.

Receipts (same dir as this report): `SScoutDevRepl/S247-fetch-log.txt`, `SScoutDevRepl/S247-anchors.txt`, `SScoutDevRepl/S247-dev-replace-live-2026-10-28.c` (the fetched bytes).

## 2. Anchors (live bytes, verified against identical pinned snapshot)

- `btrfs_dev_replace_cancel` — **live line 1085**: `int btrfs_dev_replace_cancel(struct btrfs_fs_info *fs_info)` — definition begins.
- `btrfs_scrub_cancel` call #1 — **live line 1111**: `ret = btrfs_scrub_cancel(fs_info);` — inside `btrfs_dev_replace_cancel`, in the `BTRFS_IOCTL_DEV_REPLACE_STATE_STARTED` switch arm (function spans 1085–1169).
- `btrfs_scrub_cancel` call #2 — **live line 1144**: `btrfs_scrub_cancel(fs_info);` — inside `btrfs_dev_replace_cancel`, in the `BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED` arm; line 1143 is the preceding comment `/* Scrub for replace must not be running in suspended state */` (so "1143-1144" = comment + call).
- `btrfs_dev_replace_suspend_for_unmount` — **live lines 1171–1195**: `void btrfs_dev_replace_suspend_for_unmount(struct btrfs_fs_info *fs_info)` at 1171, closing `}` at 1195 (1171–1195; the item's "1171-1199" brackets it with 4 lines of trailing comment/blank + next function's declaration).
- Function containment resolved for GR2: **both `btrfs_scrub_cancel` calls (1111, 1144) live inside `btrfs_dev_replace_cancel`**, not `btrfs_dev_replace_suspend_for_unmount` — the suspend-for-unmount switch (1171–1195) contains no scrub call; it only flips `replace_state` to SUSPENDED and logs "suspending dev_replace for unmount" (live line 1188).
- Corroborating the row's claim text: `btrfs_scrub_dev(fs_info, src_device->devid, 0,` at live line 701 (replace start path) and `btrfs_scrub_dev(fs_info, dev_replace->srcdev->devid,` at live line 1265 (resume/continue path) — consistent with the row's "Both the replace start and the continue path call btrfs_scrub_dev on the source devid".

## 3. Recheck cadence and pins

The row reads right: `status mined`, `recheck on-release` remains correct because the pin is an immutable annotated tag whose peeled commit and file bytes are re-verified byte-identical today — the only staleness vector would be a new kernel release (the natural on-release trigger), not drift under this row.

## 4. Proposed row update

`no change` — fetched 2026-10-28 bytes are byte-identical to the pinned snapshot; tag v7.2.11 unresolved-changed (8316c24e… / a2de78ee…); all anchors located at the pinned line numbers; `status`/`recheck`/`used-by` cells all still accurate (used-by corpus/knowledge/btrfs-scrub-grounding-r45.md is exactly the file C2's GR2 row depends on).

Not done: the cgit `tree` URL in the row was not fetched as HTML (the pinned artifact is the `plain` bytes; fetching the HTML page would add nothing — noted for completeness, not a defect).
