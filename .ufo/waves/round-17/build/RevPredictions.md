# RevPredictions — v42 sysroot entry vs boot-chain capture

**HIGH — the "silent no-op" prediction is observed FALSE.** The entry's [inf] bullet assumes `/new_root` is not a mountpoint. mkinitcpio 42.2 ships `/new_root` as a symlink to `/sysroot`: `/usr/lib/initcpio/functions:1212-1213` (`install -dm755 "$buildroot/sysroot"`; `ln -s "sysroot" "$buildroot/new_root"`); upstream v41 made `new_root` a real directory (v41 `functions:1188`). Both images are 42.2 builds (`boot-chain-capture.txt:174-175`: `VERSION 42.2`, init 7 `/sysroot`, 0 `/new_root`); init sha256 equals installed (`:182,:251`). `findmnt --mountpoint` canonicalizes by default (findmnt(8) § Options, `-C`: “Do not canonicalize paths at all”; access 2026-10-20): libmount `mnt_fs_match_target()` retries with `realpath(target)`. Hence `/new_root` resolves to `/sysroot`, the hook's first `findmnt` succeeds, and it proceeds. This falsifies `boot-chain-r17.md` § Rejected readings bullet 2 and its DEGRADED-PREDICTED verdict; its [unk] "which install step creates `new_root`" is `initialize_buildroot`. Correction belongs in a dated erratum (QUALITY 4).

**Observed true.** Count 2 still holds: `btrfs-overlayfs:4`, `plymouth:11` (`:20-21`); image `LATEHOOKS="plymouth btrfs-overlayfs"` (`:178,:194`). `usr` now uses `/sysroot` (`:22-23`) and is unconfigured (`:17`). v42 init 0 `/new_root`; 41.1 image 7 (`:207`). Busybox flavor and R5 rejection stand. Entry host surface superseded: 42.2-1, plymouth -3, hook 1.40.0-2 (`:32-35`).

**Untested.** The Falsifier's snapshot boot (boot 0 is `subvol=@`, `:12`); plymouth runtime; linux-lts.

**Gaps.** `dirs: new_root sysroot` (`:181`) omits file type; confirm via `ls -l` on the extraction. Snapshot cmdlines truncated (`:51,:57`).

Scope: executed=none
