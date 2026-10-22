# C2/P3 mechanism probe — symlink resolution of findmnt/mount under mkinitcpio 42.2

Verdict: under mkinitcpio 42.2, the `findmnt --mountpoint /new_root` probe and the `mount --move` / `mount -t overlay overlay` operations of the btrfs-overlayfs latehook all resolve through the `new_root -> sysroot` relative symlink that mkinitcpio 42 ships in the initramfs; the installed util-linux 2.42.4 binaries (identical to the ones packaged in the shipped UKI initramfs) behave correctly, so the hook's mechanism is not broken by the symlink per se. The btrfs-specific steps (`btrfs property get -t subvol ... ro`) remain untested in a namespace and are the only unverified segment [unk].

## Findings

1. [obs] Tool versions. Host binaries: `findmnt --version` → `findmnt from util-linux 2.42.4`; `mount --version` → `mount from util-linux 2.42.4 (libmount 2.42.4: btrfs, verity, namespaces, idmapping, fd-based-mount, statmount, statx, fanotify, udev, assert, debug)`; kernel `7.2.11-arch1-1`. The shipped initramfs extracted from `/boot/EFI/Linux/omarchy_linux.efi` (built 2026-10-20 09:18 by mkinitcpio 42.2, per `/var/log/pacman.log` lines 2539, 2982–3046) contains `usr/bin/findmnt` and `usr/bin/mount`; running the extracted binaries directly reports the same `util-linux 2.42.4`. So the path-resolution semantics probed on the host are the ones present inside the initramfs image.

2. [obs] The shipped initramfs image contains the symlink in question. Extracted from `uki-linux.initrd` (main cpio) at `/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/uki-x/`: `new_root -> sysroot` (relative symlink) and an empty directory `sysroot/`. This matches `mkinitcpio` 42.2 `functions:1212-1213` (`install -dm755 "$buildroot/sysroot"`; `ln -s "sysroot" "$buildroot/new_root"`). The runtime `init` mounts root at `/sysroot` before late hooks: `init:67` `"$mount_handler" /sysroot`, `init:71` runs `run_latehook`, so at late-hook time `/new_root` resolves to `/sysroot`, which is the mounted root.

3. [obs] `findmnt --mountpoint` resolves through the relative symlink. In an unprivileged user+mount namespace (`unshare -rm --propagation private`), with a tmpfs mounted on `$BASE/sysroot` and `$BASE/new_root -> sysroot`:
   - `findmnt --mountpoint $BASE/new_root -no FSTYPE,SOURCE,TARGET` → `tmpfs tmpfs /fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/tree/sysroot`, exit 0 (TARGET shows the resolved path).
   - Same with trailing slash `$BASE/new_root/` → identical result, exit 0.
   - `findmnt -T $BASE/new_root` and `findmnt --target $BASE/new_root` → identical result, exit 0.
   - Control: symlink to a directory that is not a mountpoint → exit 1, no output.
   Full transcript: `/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/probe-run1.txt`.

4. [obs] `mount --move` resolves the symlink source. `mount --move $BASE/new_root $BASE/lowdir` exits 0; afterwards `findmnt --mountpoint $BASE/new_root` returns nothing (exit 1) and `findmnt --mountpoint $BASE/lowdir` shows the tmpfs, i.e. the mount was detached from the resolved `/sysroot` location and attached at `$BASE/lowdir` (probe-run1.txt section 4; faithful sequence rerun `faithful2.sh` S5 exit=0).

5. [obs] `mount -t overlay overlay -o ... <target>` resolves the symlink target. With tmpfs mounted on `$BASE/sysroot`, symlink `$BASE/new_root`, and upper/work directories created on a tmpfs *after* the tmpfs mount, `mount -t overlay overlay -o "lowerdir=$BASE/low,upperdir=$BASE/ram/upper,workdir=$BASE/ram/work" $BASE/new_root` exits 0 and lands the overlay at the resolved `.../sysroot` path; `findmnt --mountpoint $BASE/new_root -no FSTYPE,SOURCE,TARGET` then shows `overlay overlay .../sysroot` (exit 0). Same result with real root privileges (`sudo unshare -m --propagation private`), ruling out a user-namespace artifact (transcript: `iso2.sh`, `faithful2.sh`, `faithful.sh` corrected run).

6. [obs] Earlier apparent failure "special device overlay does not exist" was a harness bug, not a symlink effect: probe v1 created `upper/`/`work/` directories *before* mounting the tmpfs on their parent, so the mount hid the directories, the kernel failed with ENOENT (`dmesg`: `overlayfs: failed to resolve '.../ramdir/upper': -2`), and libmount reported the misleading "special device overlay does not exist". With the correct ordering (tmpfs mount first, then `mkdir`), the overlay mount succeeds in all tested shapes (plain dir, symlink target, moved lowerdir, tmpfs upper/work), both unprivileged and as real root. This is a limitation of the early probe, not of the symlink mechanism.

7. [obs] Duplicate-device candidate selection: with the same tmpfs bind-mounted at two paths, `findmnt --mountpoint` on either symlink returns the entry matching the *resolved path* (not the other same-device entry), so matching is path-based, not merely st_dev-based (`dupdev.sh`: symA→A row, symB→B row). This is the behavior the hook needs when `/sysroot` is the only mount on the root device at late-hook time.

8. [inf] Prediction for snapshot boots under 42.2: when a snapshot is booted (limine.cn entry with `rootflags=subvol=/@/.snapshots/N/snapshot`), the hook's first three probes should work: `findmnt --mountpoint /new_root -no FSTYPE` returns `btrfs`; `findmnt --mountpoint /new_root -no SOURCE` returns a source like `/dev/mapper/root[/@/.snapshots/N/snapshot]` matching the `*/snapshot*` case (verified pattern match: `/dev/mapper/root[/@/.snapshots/2/snapshot]` contains `/snapshot`); `mount --move /new_root $lower_dir` and `mount -t overlay overlay -o ... /new_root` both resolve through the symlink (findings 4–5). The mechanism therefore predicts the hook completes and leaves the overlay mounted at `/sysroot`, which `switch_root /sysroot` (`init:110`) then uses. No observed contradiction in the journal: boots -1 and 0 completed under 42.2, but with `subvol=@ rw` (not snapshot), so the hook correctly no-ops and produced no "[OverlayFS setup]" line.

9. [unk] Untested segment: `btrfs property get -t subvol "/new_root" ro` and `btrfs` path handling were not exercised because btrfs cannot be mounted inside the unprivileged namespace and the host root is a live mounted btrfs (read-only host constraint). btrfs(8) opens the given path; symlink following is standard kernel path semantics, but this specific command was not verified. The plymouth latehook's `plymouth update-root-fs --new-root-dir=/new_root` (hooks/plymouth line 11) is a separate binary path not covered by this probe; it was not run (host read-only).

10. [obs] Limits of the probe environment stated: (a) the namespace is not the initramfs busybox environment — the hook script runs under busybox ash, but the `findmnt`/`mount`/`btrfs` commands are the util-linux binaries packaged from the host (verified identical 2.42.4), so the tested semantics are the shipped ones; (b) the root mount stand-in was tmpfs, not btrfs; (c) no actual snapshot boot has been executed on this host under mkinitcpio 42.2 (journal, no `OverlayFS setup` lines; boot cmdlines all `subvol=@ rw`), so the prediction in finding 8 is supported by the mechanism probe, not by an observed snapshot boot.

## Tooling
No installs were performed; all tools used (`unshare`, `findmnt`, `mount`, `strace`, `cpio`, `bsdtar`, `objcopy`, `python3`+zstandard) were already present on the host.

Scope: read=<lane repo capture/SCORECARD context; /usr/lib/initcpio/{init,functions,install/*,hooks/*}; /usr/lib/initcpio/busybox lists; /boot/EFI/Linux/omarchy_linux.efi UKI sections and embedded initramfs; /var/log/pacman.log excerpts; /etc/mkinitcpio.conf.d; journalctl; host findmnt/mount versions>; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecSymlinkMountProbe.md; executed=namespace probe scripts under /fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/ (probe.sh, probe2.sh, probe3.sh, probe4.sh, matrix.sh, iso.sh, iso2.sh, faithful.sh, faithful2.sh, dupdev.sh, strace-overlay.txt), mkinitcpio -g fresh image build to scratch, UKI/initramfs extraction to scratch.
Installs: none

---

## Wave-2 disclosure (appended per L1 RevWave1Scope; no earlier bytes rewritten)

### Exact privileged commands executed
All privileged commands ran with `sudo` (passwordless, interactive shell), never `su`/`pkexec`.

1. `sudo ls -la /boot` — read-only directory listing.
2. `sudo ls -laR /boot/EFI` ; `sudo cat /boot/limine.conf` — read-only.
3. `sudo objcopy -O binary --only-section=.initrd /boot/EFI/Linux/omarchy_linux.efi uki-linux.initrd`
   — read the shipped UKI (root-owned, mode 0600) and wrote `uki-linux.initrd` (267,063,511 bytes, root-owned) to scratch.
4. `sudo objcopy -h /boot/EFI/Linux/omarchy_linux.efi` — attempted; fails ("Usage") because `objcopy` has no `-h`; read-only attempt, no side effect.
5. `sudo zstd -dc uki-linux.initrd 2>/dev/null | cpio -itv > uki-list.txt` — read-only decompress/list of the extracted initramfs.
6. Four `sudo python3 - <<'EOF' ... EOF` runs, all reading only scratch files and writing only scratch files:
   a. parse `uki-linux.initrd` trailer offsets → write `main2.cpio` (70,902,492 B);
   b. parse `fresh-initramfs.img` trailer offsets → attempted write of `fresh-main.cpio` (zstd header-size probe failed, no file);
   c. stream-decompress zstd payload of `fresh-initramfs.img` → `fresh-main.cpio` (170,393,600 B);
   d. stream-decompress zstd payload of `uki-linux.initrd` → `uki-main.cpio` (170,393,600 B).
7. `sudo mkinitcpio -k 7.2.11-arch1-1 -g /fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/fresh-initramfs.img --nopost`
   — built a fresh initramfs image into scratch (267,053,271 B, root-owned). This read host config (`/etc/mkinitcpio.conf`, `/etc/mkinitcpio.conf.d/*`), host hooks (`/usr/lib/initcpio/install/*`, `/hooks/*`), host kernel modules and firmware; post hooks were skipped via `--nopost`; the only written output was the scratch image.
8. `sudo unshare -m --propagation private bash -c 'B=/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/root; ...'` — real-root mount-namespace test (tmpfs + overlayfs + `mount --move` on a scratch tree); all mounts inside a private namespace, auto-released on exit; no host mount table change persisted.
9. Read-only host btrfs queries: `sudo findmnt -b -n -o SOURCE -t btrfs /`; `sudo btrfs subvol list /`; `sudo btrfs subvol show /.snapshots/1/snapshot`; `sudo ls /.snapshots /@/.snapshots`.

Non-privileged execution (user `vgpnk`): `unshare -rm --propagation private bash probe.sh|probe2.sh|probe3.sh|probe4.sh|matrix.sh|iso.sh|iso2.sh|faithful.sh|faithful2.sh|dupdev.sh` (unprivileged user+mount namespaces), `strace -f -e trace=mount,...` inside such namespaces, `cpio`, `bsdtar`, `python3` (listings), `dd`, `mkdir`, `ln`, `file`, `od`, `strings`.

### Host state check
- `/etc`: no files written or modified. `mkinitcpio -g` only reads config; `btrfs`/`findmnt` queries only read.
- `/boot`: only read (via `sudo ls`, `sudo cat`, `sudo objcopy` extraction). No writes; UKI files' mtimes unchanged (Oct 20 09:26/09:18).
- Host package state: no `pacman` invocation of any kind (no install/upgrade/downgrade/remove/cache/`-Sy`/`-Scc`/`paccache`); no service restarts; no config writes; no reboot; no kernel/bootloader/boot-chain change.
- No host mount table change persisted (all mounts were inside disposable namespaces).

### Scratch residue
All probe artifacts lived under `/fast/scratch/hyaku/tsuku24-ExecSymlinkMountProbe/` (~1.4 GB total, incl. root-owned files listed above). Small text/script receipts and the two extracted binary receipts (`findmnt.img`, `mount.img`) were retained at
`.ufo/waves/round-24/w1/ExecSymlinkMountProbe/` (this lane draft path). The scratch directory was then removed in full by this seat; nothing of the probe remains outside the lane report/draft path.

Scope: read=<same as prior section, plus /boot listings and btrfs queries>; wrote=.ufo/waves/round-24/w1/ExecSymlinkMountProbe/ (receipts) and appended this section; executed=sudo/privileged commands listed above, namespaces, extractions.
Installs: none
