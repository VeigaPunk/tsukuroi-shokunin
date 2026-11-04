# ExecHost — round 77 / w1

Axes: depth (8, lowest tied), freshness (9). Read-only triage completed; no remediation or production integration.

Detailed evidence, command exits, source anchors, limits, and operator handoff: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/ExecHost/report.md`.

All four required commands exited 0: `pacman -Q systemd` returned `systemd 262.1-1`; `journalctl --disk-usage` returned `185.4M`; filesystem stat returned `bsize=4096 blocks=243661568 bavail=186221277`; merged journald configuration showed `SystemMaxUse=256M`, `RuntimeMaxUse=64M`, no active KeepFree override.

[INFERENCE] Round-76 documented default KeepFree rule gives 4GiB; configured persistent max_use is 268435456 bytes. With explicitly hypothetical used=134217728 bytes and valid hypothetical min_use<=max_use, saturated subtraction gives avail=758467383296, clamp gives limit=268435456, and saturated remaining allowance=134217728. This is not live manager state: actual min_use/startup-normalized metrics and loaded configuration are unknown; the rounded aggregate is not used as exact per-storage manager usage.

C1 remains exactly "six pinned arithmetic vectors match"; C2 remains exactly "three exact corrective blocks exist". No gates were run or judged. Parent owns integration and post-integration checks. No tool installs, package transactions, tests/build/lint/formatters, source changes, journal-message reads, commits, pushes, or delegated workers. Own scratch contained no fixture and is removed before terminal handoff. No blocker.
