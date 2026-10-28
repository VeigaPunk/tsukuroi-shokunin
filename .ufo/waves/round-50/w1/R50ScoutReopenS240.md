VERDICT: supports

S240 (Linux v7.2.11 `fs/btrfs/ioctl.c`) re-fetched live on 2026-10-28 is byte-identical to the pinned digest. All five GR2 cites are in those bytes. Declared ranges cover only 3132-3133; the other four are the gap `Limits` already names.

## Identity

GET `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11` (HTTP/2 200, `Date: Wed, 28 Oct 2026 19:04:52 GMT`, `content-length: 145999`, `etag: "833052306964b102855a3838a90a3cec1c2b97e2"`).

Observed on the saved body (`w1/R50ScoutReopenS240/ioctl.c`):

- `wc -c` 145999, `wc -l` 5678
- sha256 `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01`
- `git hash-object` `833052306964b102855a3838a90a3cec1c2b97e2` (matches the etag)

That sha256 is the row pin at freeze `8029cdba1049df25632c91a23c8db4eefb54be5f`: `corpus/SOURCES.md:249` (`raw bytes sha256 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01; reopened live 2026-10-28, byte-identical`) and `.ufo/waves/round-43/frozen/src/SHA256SUMS:1`. `cmp` of the live body against `git show 8029cdba:.ufo/waves/round-43/frozen/src/ioctl.c` was byte-identical.

`git ls-remote` on the same stable URL: annotated tag `8316c24ec1b77dba19ba072ca4fe251b36dc65d3` `refs/tags/v7.2.11`, peeled `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea` `refs/tags/v7.2.11^{}`, the peel named in `corpus/SOURCES.md:249`. `last-modified` on the plain view equals `Date`; it is not the commit time.

Result: **byte-identical**, not drifted.

## Five GR2 cites, in the live bytes

GR2 at `corpus/knowledge/btrfs-scrub-grounding-r45.md` (same freeze) cites them in the statement (`:84-85`) and the host reading (`:144-145`, `:148`). Enclosing functions and text (receipt `cited-lines.txt`):

| Cite | Where | Text in the live file |
| --- | --- | --- |
| 3093-3095 `btrfs_scrub_dev` | `btrfs_ioctl_scrub` (`ioctl.c:3066`) | `:3093` `ret = btrfs_scrub_dev(fs_info, sa->devid, sa->start, sa->end,` / `:3094` `&sa->progress, sa->flags & BTRFS_SCRUB_READONLY,` / `:3095` `false);` |
| 3109-3110 `copy_to_user` → `-EFAULT` | same function | `:3109` `if (copy_to_user(arg, sa, sizeof(*sa)))` / `:3110` `ret = -EFAULT;` |
| 3115 `return ret;` | same function | `:3115` `return ret;` |
| 3132-3133 `CAP_SYS_ADMIN` | `btrfs_ioctl_scrub_progress` (`:3126`) | `:3132` `if (!capable(CAP_SYS_ADMIN))` / `:3133` `return -EPERM;` |
| 3190 replace `btrfs_exclop_start` | `btrfs_ioctl_dev_replace` (`:3168`), `BTRFS_IOCTL_DEV_REPLACE_CMD_START` (`:3187`) | `:3190` `if (!btrfs_exclop_start(fs_info, BTRFS_EXCLOP_DEV_REPLACE)) {` |

## Declared ranges vs those lines

`corpus/SOURCES.md:249` scope is `fs/btrfs/ioctl.c lines 3066-3075, 3118-3140, 5578-5584`.

| Cite | Inside a declared range? |
| --- | --- |
| 3093-3095 | no (after 3075, before 3118) |
| 3109-3110 | no (same gap) |
| 3115 | no (`3115` is before `3118`) |
| 3132-3133 | yes (`3118-3140`) |
| 3190 | no (after 3140, before 5578) |

`corpus/knowledge/btrfs-scrub-grounding-r45.md:233-235` declares that gap and no other S240 lines: ranges `(3066-3075, 3118-3140, 5578-5584)` "do not list `ioctl.c:3093-3095`, `:3109-3110`, `:3115` or `:3190`". It does not list 3132-3133, which the ranges do cover. Whole-file digest still covers the four lines outside the ranges.

## Not done

Admission counter `tools/check-scrub-admission-r50.py` was not run. No package was installed.
