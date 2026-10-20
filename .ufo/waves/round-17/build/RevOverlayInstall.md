# RevOverlayInstall — 42.2 late-hook branch model (default `@` vs snapshot #2)

Axis: C1 depth. Alias now measured: both 42.2 UKIs store `new_root -> sysroot` (overlay-emulation.txt:5,8; built by functions:1212-1213); 41.1 stores a directory (:7). In-image findmnt/mount are util-linux 2.42.4, byte-identical to host (:11-15).

Common: init mounts root at `/sysroot` (init:66-67) via `mount -t ${rootfstype:-auto} -o ${rwopt:-ro}${rootflags:+,$rootflags} root /sysroot` (init_functions:430-432; `rw|ro`→rwopt :159-160); latehooks run in image order `plymouth btrfs-overlayfs` (boot-chain-capture.txt:178) through init_functions:88-103, which calls `"$fn"` (:101) and never tests its status; init:110 execs switch_root /sysroot — hook rc never gates boot.

**(a) default `@`** (cmdline `rw rootflags=subvol=@`, capture:12-14): mount `-o rw,subvol=@`.
1. plymouth:10-12 `update-root-fs --new-root-dir=/new_root`; no branch, one command; path aliases /sysroot; rc 0 on daemon ack (plymouth.c:730-746); plymouthd started hooks/plymouth:3-8.
2. btrfs-overlayfs:4 `root_mnt=/new_root`; :7-8 findmnt FSTYPE=btrfs (pass); :11 SOURCE=`/dev/mapper/root[/@]`; :12-14 no `/snapshot` → `return 0`; no cowspace/overlay.
State: /sysroot = btrfs `/@` rw; switch_root moves it onto `/` (switch_root.c:179-184). Matches boot 0 (capture:14).

**(b) snapshot #2** (`subvol=/@/.snapshots/2/snapshot`, ro=true capture:160-161): mount `-o ro,subvol=…` (ro token, else `${rwopt:-ro}`).
1. plymouth: same call; resolves to the snapshot mount; rc 0.
2. btrfs-overlayfs: :7 pass; :11 SOURCE=`/dev/mapper/root[/@/.snapshots/2/snapshot]` → :12-13 `/snapshot` taken; :18-19 `btrfs property get` → `ro=true` (open() follows the alias, subvolume.c:489-502; handler property.c:241-247); :24-42 mktemp + tmpfs cowspace + upper/work; :44 `mount --move` (LOOKUP_FOLLOW, namespace.c:4347,3851-3863) detaches btrfs from /sysroot; :49-51 overlay mounted at /new_root=/sysroot; :56 rc 0.
Emulated: step1 rc 0, move rc 0, overlay rc 0, final FSTYPE=overlay, write lands in upper (emulation:40-47).
State: /sysroot = overlay rw (lower=ro snapshot, upper=tmpfs cowspace).

Residual: every :24-:54 error path returns 0, leaving the bare ro snapshot for switch_root → read-only root; only /home,/var/log,/var/cache/pacman/pkg are rw subvols (/etc/fstab), so /var/lib writes fail: systemd outcome [inf], untested.

Correction: boot-chain-r17.md's "empty /new_root directory" and DEGRADED-PREDICTED premise fall [obs image; obs emulation]; findmnt canonicalizes the alias unless `-C` (findmnt.c:2168-2177, fs.c:1806-1819, cache.c:621-644,695-735).

Unverified: exact snapshot cmdline token (limine.conf 0700 root); :18 not exercised in the tmpfs emulation.

Sources (raw upstream, accessed 2026-10-20): util-linux v2.42.4 misc-utils/findmnt.c, libmount/src/{fs,cache}.c; linux fs/namespace.c; btrfs-progs cmds/property.c, libbtrfsutil/subvolume.c; plymouth src/client/plymouth.c. Local copies in /tmp.

Scope: executed=grep,sed,ls,curl,python3,file,find,tr
