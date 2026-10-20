# SrcMkinitcpioV42x — 42.x release notes vs `/new_root` (access 2026-10-20)

**Q:** Does any 42.x release note mention `/new_root` compatibility, a `/new_root` directory, or hook migration to `/sysroot`?

**Answer: No.** The only `/sysroot` sentence is an init-script statement, not a hook-migration or compatibility note.

## Observed
- [obs] Opened `https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases` (JSON, HTTP 200). Top releases: `v42.2` (2026-10-01), `v42.1` (2026-09-27), `v42` (2026-09-02); latest is v42.2. Full `description` fields carry the changelog text.
- [obs] Release `v42`, JSON key `description`, fragment `CHANGES WITH v42` → `Changes in mkinitcpio`: "Busybox-based init now uses /sysroot as the root mountpoint just like the systemd-based one." (14 words). Sole 42.x `/sysroot` mention.
- [obs] v42.1 and v42.2 descriptions: no root-path item at all (v42.2 covers systemd-tpm2-setup-early/pcrnvdone; v42.1 covers `/EFI/Linux` plus symlink/unit fixes).
- [obs] Corroborating canonical file `https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/CHANGELOG`: headings at line 3 (`v42.2`), 19 (`v42.1`), 42 (`v42`); `/sysroot` bullet at lines 46-47; `/new_root` matches over lines 1-924: **zero**.
- [obs] HTML page `/-/releases/v42` opened but yielded only meta/title, no body; API description used. Blob-search API `.../search?scope=blobs` returned HTTP 401 (auth required) — no repo-wide absence claim.

## Does NOT establish
Nothing says `/new_root` is removed, aliased or symlinked; nothing says hooks (`btrfs-overlayfs:4`, `plymouth:11`) must migrate; 42.2 init behavior toward `/new_root` is untested here [unk]. Release-note silence is documentation absence only [inf].

Scope: executed=none
