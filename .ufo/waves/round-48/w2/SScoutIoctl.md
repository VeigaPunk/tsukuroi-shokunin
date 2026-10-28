VERDICT: supports

Item SRC-SScoutIoctl — live re-open of row S240 in corpus/SOURCES.md (SOURCES.md:249).

## 1. Fetch

- Row URL (SOURCES.md:249): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11` — the `tree` page is HTML; the raw bytes the row pins come from the `plain` variant of the same URL: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11`.
- Command: `curl -fsSL --max-time 60 -o ioctl-live.c '<plain URL>'`. Response: `HTTP/2 200`, `content-type: text/plain; charset=UTF-8`; no redirect (`-L` issued no second hop; receipt: `.ufo/waves/round-48/w2/SScoutIoctl/fetch-headers.txt`).
- Access date: 2026-10-28 (UTC, `date -u +%F`).
- Fetched bytes: sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`, 5678 lines, matching the row's recorded digest exactly.
- Comparison: `cmp ioctl-live.c .ufo/waves/round-43/frozen/src/ioctl.c` → byte-identical (receipt `cmp-result.txt`). Upstream did NOT move: the pin is to annotated tag `v7.2.11` (row states peeled commit `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`), not a branch tip, so immutability is expected and confirmed.

## 2. Anchor

- `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` — live line 3190 (snapshot line 3190; identical). Verbatim quote (14 words): "if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) { ret = BTRFS_ERROR_DEV_EXCL_RUN_IN_PROGRESS; }". Context (live ioctl.c:3186-3195): inside `case BTRFS_IOCTL_DEV_REPLACE_CMD_START`, after the `sb_rdonly` EROFS check; on exclop failure it returns `BTRFS_ERROR_DEV_EXCL_RUN_IN_PROGRESS`, else runs `btrfs_dev_replace_by_ioctl` and calls `btrfs_exclop_finish`. This is the host-reading clause the round-48 GR2 counter newly pins: `tools/check-scrub-admission-r48.py:70` lists `ioctl.c` among GR2's grounded files and line 50 pins the snapshot path/digest.

## 3. Cadence / pins

Row cadence is `on-release` with last recheck 2026-10-26; the pin is tag+sha256 against stable/linux.git, so the bytes cannot drift between releases and a 2-day-old recheck is fresh — everything still reads right.

## 4. Proposed cell update

`no change` — status `mined`, recheck `on-release`, used-by `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md` are all current; nothing is stale.
