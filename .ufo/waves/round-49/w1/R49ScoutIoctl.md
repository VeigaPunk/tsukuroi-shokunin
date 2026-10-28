VERDICT: supports

Seat R49ScoutIoctl. S240 re-opened live 2026-10-28. Row at freeze `55c07cd3f8bff2e12117c34d57b4c618de74d85c:corpus/SOURCES.md:249` is the same text as the worktree row. Receipt: `.ufo/waves/round-49/w1/R49ScoutIoctl/fetch-receipt.txt`.

## 1. Fetch

SOURCES URL (tree view): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/fs/btrfs/ioctl.c?h=v7.2.11`
`curl -fsSL --max-time 60` → HTTP 200, `redirects=0`, `content-type: text/html`, 367878 bytes, sha256 `20dbc2e730ed89fd65d9c9b190cb3d8340909d33cca21e2a8ac0284c2bdfebd4`. That page is cgit HTML, not the pinned file (`cmp` rc 1).

Raw bytes of the same tag (the URL in `.ufo/waves/round-43/frozen/src/FETCH.txt:4`, which round 43 recorded as byte-identical to the tree ref): `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11`
`curl -fsSL --max-time 60 -D` → HTTP/2 200, `redirects=0` (`url_effective` equals the request URL), `content-type: text/plain`, 145999 bytes, 5678 lines. Access date `date -u +%F` = 2026-10-28 (header `date: Wed, 28 Oct 2026 17:20:10 GMT`). sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`. `cmp -s` against `.ufo/waves/round-43/frozen/src/ioctl.c` rc 0. `sha256sum` of that pin is the same digest (`SHA256SUMS` line 1).

Mirror named in `FETCH.txt:2`: `https://raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/ioctl.c` → HTTP 200, `redirects=0`, same sha256, `cmp` against the plain fetch rc 0.

Upstream did not move. `h=v7.2.11` is a tag, not a branch. The tag blob equals the 2026-10-26 pin. No `git ls-remote` this seat; equality of the tag URL's bytes is the movement check.

## 2. Anchors (live bytes; identical to the pin)

Scrub-progress gate, `btrfs_ioctl_scrub_progress` opens at line 3126:

- live:3132 — `if (!capable(CAP_SYS_ADMIN))` (2 words)
- live:3133 — `return -EPERM;` (2 words)

Same pair at the start handler (3072-3073, inside the pinned range 3066-3075) and the cancel handler (3120-3121, inside 3118-3140). Dispatch inside 5578-5584: live:5582 `case BTRFS_IOC_SCRUB_PROGRESS:`.

Replace exclusive-op, inside `btrfs_ioctl_dev_replace` (opens at 3168), `BTRFS_IOCTL_DEV_REPLACE_CMD_START`:

- live:3190 — `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` (4 words)

That is the line GR2 cites (`corpus/knowledge/btrfs-scrub-grounding-r45.md:147`).

## 3. Cadence and pins

`on-release` still fits: the pin is tag v7.2.11 (peeled commit named in the row, `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`), not a moving branch, and the sha256 plus ranges 3066-3075, 3118-3140 and 5578-5584 still match the live tag. Line 3190 is in that same blob, outside those ranges (the row's scope is the scrub `CAP_SYS_ADMIN` gates). Status stays `mined`. `used-by` still names the two knowledge entries whose `source:` headers declare S240, plus `corpus/lessons/round-48.md`. `btrfs-scrub-grounding-r45.md:147` cites S240 but its `source:` line does not, so that omission is not treated as a stale used-by cell.

## 4. Proposed change

no change
