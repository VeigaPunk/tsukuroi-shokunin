# tsukuroi-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `knowledge/package-state-plane.md` | pacman plane measured anchors: trust surface (`/etc/pacman.conf` — no version pins, single omarchy mirror, `[omarchy] SigLevel = Optional TrustAll`), census (1188 installed / 207 explicit / 16 foreign / 3 orphans), sync-db birth-vs-mtime trap (dbs born 2026-10-11 12:54:13.542; mtimes are upstream stamps), keyring (184 pub / 230 sub) + cache shape (8.6 G, never pruned), `-Qkk` rc semantics (0 = none, 1 = ≥1 altered) + non-root benign-altered decision table + full-sweep decomposition (86 backup-diff / 36 non-root / 17 metadata-drift lines; one content signal `powerprofilesctl`), unknowns (elephant channel provenance, root `-Qkk` delta) | live read-only probes 2026-10-14, host `plazir27`, non-root; commands embedded per section; landed round 1 |
| `knowledge/systemd-user-plane.md` | systemd user plane: manager state (both scopes `running`), unit inventory (`~/.config/systemd/user/` 7 units + 1 drop-in + 5 symlinks; `/usr/lib/systemd/user/` ships 109), timer plane (`ai-usage.timer` only active, `Result=success`), condition-gated units, boot err classes (entry-count discipline — line counts are a trap), coredump census (198 this boot: godot 142, node 47), method lessons, unknowns/errata | `systemctl --user` / `journalctl` / `coredumpctl` probes 2026-10-14; landed round 1 |
| `knowledge/driver-firmware-plane.md` | nvidia driver + firmware plane: loaded module census (`lsmod`), driver presence (`nvidia-open-dkms` 610.57.04, upgraded 2026-10-11), GSP firmware shape (presence/sizes only, contents never read), boot err/warn classes via `journalctl -k`, update candidates, obs/inf/unk split, errata (stale `7.1.4-arch1-1` dkms registration; unowned `nvidia.ko.zst` pacman cannot verify) | `lsmod`/`dkms status`/`modinfo`/`nvidia-smi --query-*` probes 2026-10-14; landed round 1 |

## Quality bar

See `QUALITY.md` (admits only falsifiable, source-cited claims;
rejection kept as evidence of taste).
