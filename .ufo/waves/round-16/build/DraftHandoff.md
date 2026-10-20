# DraftHandoff — operator recovery status (r15)

Packet `TSUKUROI-R15-INCIDENT-01`, lifecycle **prepared**.

**Observed** (snapshot 2026-10-20T07:44:39Z, SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`):
- pacman.log 2429/2432/2436: `-S --needed --noconfirm libinput libinput-tools`; libinput 1.31.3-1 → 1.32.0-1; libinput-tools 1.32.0-1 installed.
- Installed: libinput 1.32.0-1; mkinitcpio 41.1-1 (42.2-1 pending).
- `pacman -Qu`: 413 rows against sync DB born 2026-10-18T17:11:00Z.
- Hooks `btrfs-overlayfs`:4 and `plymouth`:11 reference `/new_root` only.

**Not measured:** running mapped version, UI, ABI, causation, boot. "Hyprland keeps 1.31.3" is unverified.

**Operator decisions (agents execute none):** (a) keep or revert libinput 1.32.0-1; (b) full-upgrade timing after the mkinitcpio-42 hook gate and tested fallback; (c) restart/reboot timing. L0 line 55 (pacman pause): no operator answer retained.

**Not authorized:** `-S/-Sy/-Syu/-U/-R`, refresh, services, sudo, downgrade. `--needed` and `pacman -Sp` guards are not clearance.

**Staleness:** void after any pacman transaction or sync change; recapture all five probes.

**Sources:** S047, S048. **Tools:** none installed or updated.
