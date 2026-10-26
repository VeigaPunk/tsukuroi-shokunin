VERDICT: supports

# C2-4 — Does Arch kernel 7.2.11-arch1-1 patch fs/btrfs/ioctl.c?

**Answer: no.** The Arch patch delta for this tag touches four files, none under `fs/`; `fs/btrfs/ioctl.c`
(and `fs/btrfs/scrub.c`) in the `archlinux/linux` tag tree are byte-identical to upstream v7.2.11 and to the
frozen S240 snapshot. `btrfs_ioctl_scrub_progress` does **not** differ between what SR6 cites and what the
host actually boots.

## Evidence chain

### 1. The packaging tag names exactly one patch, and its digest matches the PKGBUILD

`linux` packaging repo, tag `7.2.11.arch1-1` (gitlab API HTTP 200, target commit
`a66ce8bcdbf375dd221655524cba034944a3beb1`):

- `PKGBUILD:45` `_srctag=v${pkgver%.*}-${pkgver##*.}` → `v7.2.11-arch1`; `PKGBUILD:7` `url='https://github.com/archlinux/linux'`.
- `PKGBUILD:46-49`
  ```
  source=(
    https://cdn.kernel.org/pub/linux/kernel/v${pkgver%%.*}.x/${_srcname}.tar.{xz,sign}
    $url/releases/download/$_srctag/linux-$_srctag.patch.zst{,.sig}
  )
  ```
  i.e. one tarball + one patch; `source_x86_64=(config.x86_64)` (`PKGBUILD:50`) is a config, not a patch.
- `PKGBUILD:63-66` sums, in that order: `fd0fc479…` (tar.xz), `SKIP` (tar.sign), `741d473c…` (patch.zst), `SKIP` (patch.sig).
  `linux-7.2.11.tar.xz` at kernel.org's `v7.x/sha256sums.asc` line 129 is `fd0fc479f983a8c05313f13e9c36330fe6651cf725396748c40d5cd93fa1e6a4`,
  so `741d473c…` is unambiguously the patch entry.
- Fetched `https://github.com/archlinux/linux/releases/download/v7.2.11-arch1/linux-v7.2.11-arch1.patch.zst`
  (2026-10-26) → 2316 bytes, sha256 `741d473c4db335d97d9e1d9b8be9337090522550804fe6454ba336d21e580fd6` = PKGBUILD entry. Match.
- `PKGBUILD:79-91` `prepare()` applies only `*.patch` from `$source` (`[[ $src = *.patch ]] || continue; patch -Np1 < "../$src"`),
  so this single patch is the entire source deformation the package build applies.

### 2. The patch's own delta contains no fs/ path

`patch.diff` (zstd -d of the above; sha256 `2c167a9335b3270a0d59d0b954669b67d9624e447e61c4c5fbe0cc1f7be73dc7`), diffstat verbatim:

```
 Makefile                                          |  2 +-
 drivers/gpu/drm/amd/display/amdgpu_dm/amdgpu_dm.c | 15 +++------
 drivers/gpu/drm/i915/display/intel_dp.c           | 38 +++++++++++++++++++++++
 kernel/fork.c                                     | 24 ++++++++++++++
```
`grep -c '^diff --git' patch.diff` = 4; `grep -c '^diff --git a/fs/' patch.diff` = 0.

### 3. fs/btrfs/ioctl.c: upstream == arch tag == frozen S240, byte for byte

| file | source | sha256 |
|---|---|---|
| `ioctl-up.c` | `raw.githubusercontent.com/gregkh/linux/v7.2.11/fs/btrfs/ioctl.c` | `7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01` |
| `ioctl-arch.c` | `raw.githubusercontent.com/archlinux/linux/v7.2.11-arch1/fs/btrfs/ioctl.c` | `7b3488f2f8…` (same) |
| `.ufo/waves/round-43/frozen/src/ioctl.c` (S240) | lane freeze | `7b3488f2f8…` (same) |

`cmp ioctl-up.c ioctl-arch.c` → identical; `cmp ioctl-arch.c …/frozen/src/ioctl.c` → identical.

Same check for the scrub implementation referenced by SR6's capability claim:
`fs/btrfs/scrub.c` upstream v7.2.11 and at `v7.2.11-arch1` are both
`f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8`, `cmp` identical (that kernel file is *not* the
round-42 frozen `scrub.c`, which is btrfs-progs' `cmds/scrub.c` — see §5).

### 4. The tag tree really is upstream + this patch (patch↔tag correspondence)

`kernel/fork.c` is one of the four patched files: at the arch tag commit
`64a90897d3c539033f24105968e3513957e70819` (peeled `refs/tags/v7.2.11-arch1`, resolved by `git ls-remote`) it contains
`unprivileged_userns_clone` 6 times (sha256 `1d3f9fd5…`); upstream v7.2.11 `kernel/fork.c` contains it 0 times
(sha256 `4548f28f…`). So the published tag = upstream + the fetched patch, i.e. the "no fs/ change" conclusion is a
property of the tree that was built, not merely of the patch filename.

### 5. The function in question, in the file the host boots (SR6 kernel side)

Frozen S240, i.e. the file identical to the arch tag tree above:

- `frozen/src/ioctl.c:3126` `static long btrfs_ioctl_scrub_progress(struct btrfs_fs_info *fs_info, void __user *arg)`
- `:3132-3133` `if (!capable(CAP_SYS_ADMIN))` / `return -EPERM;` — the EPERM SR6 asserts, in the ioctl itself, before any memdup.
- `:3139` `ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);`
- `:5582` `case BTRFS_IOC_SCRUB_PROGRESS:` dispatch.

Live corroboration that the host runs the arch-patched build of this tag, not a plain v7.2.11 or another distro kernel:
`/proc/version` = `Linux version 7.2.11-arch1-1 (linux@archlinux) (gcc …) #1 SMP PREEMPT_DYNAMIC Fri, 16 Oct 2026 00:28:58 +0000`;
`pacman -Qi linux` → `Version 7.2.11.arch1-1`, `Build Date Thu 15 Oct 2026 09:28:58 PM -03` (= 00:28:58Z, the same
timestamp); and the arch-only hunk of the patch is present at runtime: `/proc/sys/kernel/unprivileged_userns_clone`
exists (mode 0644, value `1`) — upstream v7.2.11 has no such sysctl (0 occurrences in `fork-up.c`).
`grep -w btrfs_scrub_progress /proc/kallsyms` → `T btrfs_scrub_progress` (btrfs is builtin: `modinfo -F vermagic btrfs` → `(builtin)`).

### 6. Side observation bearing on SR6's wording (btrfs-progs side, S237)

S237 `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c:1190-1206`
`is_scrub_running_in_kernel()` does `ret = ioctl(fd, BTRFS_IOC_SCRUB_PROGRESS, &sp.scrub_args); if (!ret) return 1;`
and returns 0 otherwise — it never inspects `errno`. So "an unprivileged status never reads `running`" holds, but via
*any* failing ioctl, not by an EPERM test; `EPERM` is not distinguished from `EINVAL`/`ENOTTY` there. (Round-42's
`scrub.c` also contains no `EPERM` string at all: `grep -n EPERM` → no match.) SR6 as written is true; this is a
precision note, not a contradiction — and per the item's instructions I do not draft counted C2 text (wave-1 seats are
first falsifiers).

## What I did not do

- No live unprivileged `BTRFS_IOC_SCRUB_PROGRESS` probe (that is `frozen/hostcap/capture.sh`'s business); the EPERM
  claim here is source-level only (ioctl.c:3132-3133) plus the host-identity facts above.
- Did not verify the patch GPG signature (`patch.sig` / heftig key) — digest match against the PKGBUILD was deemed sufficient.
- Did not check `/proc/config.gz` or `/usr/lib/modules/7.2.11-arch1-1/build` for btrfs source (not needed; that tree
  ships headers only — `ls …/build/fs/btrfs/` → `Kconfig` only).
- GitHub REST `compare` API and the `contents/fs/btrfs` listing for `gregkh/linux` returned 404 / HTTP 403 (unauthenticated
  rate limit from this IP); the per-file raw comparisons in §3-§4 stand in for a whole-tree listing. No install or upgrade
  was performed; no pacman transaction; no lane index or host state touched.

## Receipts

`.ufo/waves/round-43/w1/C2ExecKernelPatch/` — `receipt.txt` (all commands with observed output), `PKGBUILD`
(sha256 `afed8ab664a603feece3d1bef3380cf96f66dfbada8a9fd0d5548318abfec73e`), `patch.zst`
(`741d473c…`), `patch.diff` (`2c167a93…`), `kernelorg-sha256sums.asc` (`f35e50c9…`). The 146 KB `fs/btrfs/ioctl.c`
copy fetched from the arch tag is **not** retained because it is byte-identical to the already-frozen
`.ufo/waves/round-43/frozen/src/ioctl.c`; its digest and `cmp` result are in `receipt.txt`.
Scratch `/fast/scratch/hyaku/tsukuroi-r43/C2ExecKernelPatch/` was removed after copying receipts.
