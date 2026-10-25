# scout-live — round 1 (kaika), seat W2RoundTsukuroi-8.TsuR1Scout-3

(Verbatim L2 output persisted by the L1 so the pointer resolves at closure; L2 = author-side advisory seat, not a non-author verifier. Source transcript: history://W2RoundTsukuroi-8.TsuR1Scout-3 — session-scoped, this file is the durable copy.)

Capture time: **2026-10-19T22:04:51Z** (UTC).

- `pacman -Q`: current `pacman 7.1.0.r9.g54d9411-2; mkinitcpio 41.1-1; systemd 261.2-1; limine 12.8.0-1; limine-snapper-sync 1.31.0-1.1; limine-mkinitcpio-hook 1.38.0-1.1; snapper 0.13.1-3; btrfs-progs 7.1-1; linux 7.2.3.arch1-3; linux-firmware 20260810-2; nvidia-open-dkms 610.57.04-1; iptables 1:1.8.13-1; rsync 3.5.0-1; filesystem 2025.10.12-1`. ART: **MATCH** for the 12 packages with recorded versions; no exact ART version recorded for `snapper` or `filesystem`.
- `stat -c '%a %U:%G' /`: `555 root:root` → ART `555 root:root` → **MATCH**.
- Unit capability: `14:CapabilityBoundingSet=CAP_SYS_ADMIN` → ART same → **MATCH**.
- Snapper errors: count `8`; first `2026-10-16T12:47:26-03:00`, last `2026-10-19T08:11:47-03:00` → ART count/range same → **MATCH**.
- `snapper list-configs`: header only → ART header only → **MATCH**.
- HOOKS: default config plus `omarchy_hooks.conf` and `omarchy_resume.conf` drop-ins; drop-ins specify busybox hooks and `resume` → ART same effective drop-ins → **MATCH**.
- `/new_root` hooks: hits in `plymouth:11` and `btrfs-overlayfs:4` (2 total) → ART same two hooks → **MATCH**.
- Pacman history counts: `.pacnew` `3`; `.pacsave` `0` → ART `3`; `0` → **MATCH**.
- `find /etc` pac files: `locale.gen.pacnew`, `P_ECCP384SHA384.json.pacnew`, `P_RSA3072SHA384.json.pacnew` → ART same three paths → **MATCH**.
- `pacman-conf HookDir`: `/etc/pacman.d/hooks/` → ART same → **MATCH**.
- Hook `Exec` lines: packaged `mkinitcpio install`; `/etc` override `limine-mkinitcpio-install` → ART same → **MATCH**.
- Hook-run log: 3 entries (lines 269, 1362, 1989) → ART 3 → **MATCH**.
- Retained boots: `9` → ART `9` → **MATCH**.
- `df -h /boot`: `/dev/nvme0n1p1 2.0G 279M 1.8G 14%` → ART `2.0G`, `279M`, `14%` → **MATCH**.
- `pacman -Qo /`: `error: No package owns /` → ART same → **MATCH**.
- Pacman `-Sy` log sweep: lines 1405 (2026-10-11) and 2287 (2026-10-18) → ART records the 10-11 event; the 10-18 bare `-Sy` is unrecorded → **DRIFT**.
- Census `--selftest` last 3 lines: two `PASS cli` cases; `TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)`; `rc=0`. ART: no baseline → **N/A**.
- Live census last 3 lines (trimmed): update-safety `DEGRADED`; oom `DEGRADED`; rollup `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`; `rc=1`. ART: no baseline → **N/A**.
- `git status --porcelain tools/`: empty. No tracked tool changes; selftest used its `/tmp` fixture path.

[async-result] printf 'CAPTURE_UTC '; date -u +%FT%TZ printf '\n== packages ==\n'; pacman -Q pacman mkinitcpio systemd limine limine...
