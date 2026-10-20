# FxPathAliased — PATH-ALIASED-EMULATED (snapshot-2)

**Verdict: SURVIVES.** I found no step where the symlink breaks the overlay. I did not boot-test it, so a real boot could still falsify the claim.

- FSTYPE and SOURCE: [obs] init:67 mounts root at `/sysroot`. Hook lines 7 and 11 run `findmnt --mountpoint /new_root`. The capture resolved that path to the sysroot mount (overlay-emulation.txt:40-42), and the findmnt in the image is byte-identical to the host copy (:11-12). [inf] The `[/@/.snapshots/2/snapshot]` part of SOURCE comes from the fsroot in mountinfo, not from the path, so `*/snapshot*` matches. Source: https://manpages.ubuntu.com/manpages/bionic/man8/findmnt.8.html, `-v, --nofsroot`: "Do not print a [/dir] in the SOURCE column for bind mounts or btrfs subvolumes" (accessed 2026-10-20).
- `btrfs property get -t subvol` (hook:18): [obs] With `-t`, the command skips autodetection (cmds/property.c `parse_args`). `btrfs_util_get_subvolume_read_only` then calls `open(path, O_RDONLY)`, which follows symlinks, before `BTRFS_IOC_SUBVOL_GETFLAGS` (libbtrfsutil/subvolume.c, kdave/btrfs-progs master).
- Move, overlay mount and switch_root: [obs] In the emulation, `--move` and the overlay mount both landed on sysroot (overlay-emulation.txt:43-47). init:77 and :87 then check `/sysroot`, and :110 switches to it, so the top overlay mount is the one that gets moved.

[inf] Not a break: the plymouth late hook runs first (boot-chain-capture.txt:226-228) and chroots into the pre-overlay mount. Pre-42 did the same.

[unk] Not checked:
- an overlay on top of a btrfs read-only lower layer (the emulation used tmpfs);
- whether the image's `libmount.so` matches the host copy;
- the btrfs-progs version on the host (I read master);
- behaviour under the 6.18 LTS kernel.

Scope: executed=true
