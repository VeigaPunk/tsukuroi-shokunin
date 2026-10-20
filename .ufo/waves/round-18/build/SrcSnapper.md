# SrcSnapper — snapper(8): config existence ≠ rollback feasibility (R18)

model: opencode-go/deepseek-v4.1-flash

- [obs] https://man.archlinux.org/man/snapper.8, accessed 2026-10-20; sha256 c9d84f29e14aed60169cd49e2d969a41c5e0334619461f3ffb9b2caffb83ee6b; extra/snapper 0.13.2-1, footer 2026-01-02; fragment `#COMMANDS` > rollback; `#FILES`.
- [obs] rollback: “Rollback is only supported with btrfs and requires a properly configured system.” (12 words).
- [obs] caveats: “Support for individual filesystems, rollback and extended attributes are compile-time options and may not be available.” (16 words).
- [obs] create-config: “Manually set filesystem type. Supported values are btrfs, ext4 (discontinued) and lvm.” (12 words).
- [obs] CONCEPTS: “For each filesystem or subvolume that should be snapshotted by snapper, a configuration file is required, see snapper-configs(5).” (18 words); FILES: “Directory containing configuration files.”

Proposition: [obs] snapshotting needs a config file; rollback separately needs btrfs plus a “properly configured system”, may be compiled out, and excludes lvm/ext4 configs create-config accepts. [inf] config existence is necessary, not sufficient, for rollback restore; the page never equates them or defines “properly configured”. [unk] that definition, per-config validity, snapshot inventory, restore test.

Host (S060): configs `home`,`root` (`:76-77`), `SNAPPER_CONFIGS="root home"` (`:80`), `/` btrfs subvol=/@ (`:97-98`); no `snapper list-configs` ran ([unk] listing).

Candidate SOURCES row (S062; S061 claimed thrice — registry decides):

| S062 | snapper(8) — https://man.archlinux.org/man/snapper.8 | docs | A | Rollback preconditions vs config existence; not host restore success | COMMANDS > rollback; CONCEPTS > Configurations; FILES > /etc/snapper/configs; 0.13.2-1, 2026-01-02; sha256 c9d84f29… | A config file is required for snapshotting, but rollback is btrfs-only and requires a properly configured system; rollback support may be compiled out | queued | 2026-10-20 | on-release | — |

Routing (C3 seat): dated “0 configs” text (`update-safety-v3.md:231`, `host-health-report-r3.md:301`) conflicts with S060 names; `round-18.md:12` rejects configs-prove-rollback.

Scope: executed=read-only `curl` (snapper.8/.en/.txt), `grep`/`sed`/`sha256sum` on fetched and lane files; no host probes, sudo or pacman; only this report written.
