# FxOwnS055 — S055 vs capture

Row: `corpus/SOURCES.md:61` (worktree). `:N` = `.ufo/waves/round-17/l1-capture/overlay-emulation.txt:N`.

**Verdict: FAILS** — `teaches` overreaches; anchor incomplete. Lesson quotes SURVIVE.

- [obs] Anchors resolve (`:5-8` listings, `:9-10` functions:1212-1213, `:11-15` hashes, `:40-48` output), but "13:0x" blurs `:2` "13:02:39" and omits the 13:28:44 append `:51-66`, sole linux-lts typing (`:53-58`), cited by `boot-chain-r17.json`. [inf] Present at landing: `.git/logs/HEAD:42` dd15c183 epoch 1792515301 = 13:55:01-03.
- [obs] "42.2 images": anchored `:5`,`:8` are one UKI, omarchy_linux.efi (`:4`); the capture names no mkinitcpio version (`:15` is util-linux). 42.2 is S051's (`boot-chain-capture.txt:174,190`), S058's correction class.
- [obs] "making it writable": the stand-in root was writable pre-overlay (`:27` `touch sysroot/marker-real-root`); `:47` only shows a write landing in upper. Hook overlays only past “`[ "$ro_state" = "ro=true" ] || return 0`” (https://gitlab.com/api/v4/projects/Zesko%2Flimine-entry-tool/repository/files/install%2Farch-linux%2Flimine-mkinitcpio-hook%2Fusr%2Flib%2Finitcpio%2Fhooks%2Fbtrfs-overlayfs/raw?ref=3c011dc2aebc0346f5e1d5dc2132a2a5f6c71169 § run_latehook “Is the subvolume read-only?”, accessed 2026-10-20) — never emulated. Overlay lands on vacated sysroot (`:44` rc=[1]), not "onto the real root mount". Echoed: `corpus/knowledge/boot-chain-r17.md:57`.
- [obs] `:48` “new_root -> sysroot” is the emulation's own symlink (`:26`,`:37`), yet alone satisfies `tools/check-boot-chain.py:313`; snapshot-2/linux cites it.
- Gate: `corpus/lessons/round-17.md:27` quotes verbatim (`:8` suffix, `:46` prefix). `round-17.md:11` cites `:5,8` (linux UKI only) for snapshot #2; snapshot-2/linux-lts is typed only at `:56-58`. Same: `corpus/knowledge/initramfs-v42-sysroot-recovery.md:85`.

[unk] dd15c183 row bytes (no git run); image libmount identity (only binaries hashed).

Scope: executed=none
