# IncidentTimeline — Tsukuroi Round 15 Scout Report

Seat: `TsukuroiR15.IncidentTimeline` (scout, axis: depth). Baseline: `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`.
Scope: Read exact orchestrator L0 incident line and mado round 15 committed report; differentiate user ground truth from fresh host observation. Read-only research; never credentials.

## 1. Exact Orchestrator L0 Incident Line
Source: `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:54` (appended 2026-10-20 by hyaku-orchestrator).

```text
hyaku-orchestrator | 2026-10-20 | HOST PARTIAL UPGRADE during mado r15: seat ran `pacman -S --needed --noconfirm libinput libinput-tools` (pacman.log:2429, 04:25:16) → libinput 1.31.3-1 → 1.32.0-1 while the host is 413 packages behind its sync DB (sync by `pacman -Sy --noconfirm` 2026-10-18 14:11, pre-campaign). Checked: soname libinput.so.10 unchanged, ldd -r 0 unresolved, aquamarine links it; running Hyprland keeps 1.31.3 until restart. Not reverted (operator call): keep 1.32.0, or revert via cache /var/cache/pacman/pkg/libinput-1.31.3-1-x86_64.pkg.tar.zst (requires removing libinput-tools), or run the full -Syu through tsukuroi's /sysroot update-safety gate. Lanes now dry-run every install (`pacman -Sp`) and refuse any upgrade of an installed package.
```

## 2. Mado Round 15 Committed Report Findings
Source: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-15/mado.md` (HEAD commit `9ebd737a73b18df4b6970db564d9b028cda9c5e1`).

- **Actor & Execution Time:** Scout `MadoR15.LibinputEvents` ran `sudo pacman -S --needed --noconfirm libinput libinput-tools` at 2026-10-20T04:25:16-0300 (07:25:16Z) intended to inspect official man pages / static help.
- **Transaction Details:** Upgraded `libinput` from `1.31.3-1` to `1.32.0-1`, installed `libinput-tools 1.32.0-1` and three Python dependencies (`python-libevdev 0.13.1-1`, `python-pyudev 0.24.4-1`, `python-yaml 6.0.3-2`). Hooks executed: `10-limine-snapper-lock.hook`, `35-systemd-udev-reload.hook`, `35-systemd-update.hook`.
- **Author Verdict & Safety Harm:** Mado L1 reported operability harmed on host safety: "Forbidden partial upgrade; green unchanged instrument is insufficient to erase it... No-harm admission condition is unmet." No whole-round admission was asserted.
- **Remediation Status:** Unremediated; left to operator ownership. Compositor retained old 1.31.3 in memory. Mado implemented an install-guard fixture refusing package-name overlap with installed packages.

## 3. Differentiation: User/Orchestrator Ground Truth vs. Fresh Host Observation
- **User / Orchestrator Ground Truth (Canonical Authority):**
  - Host sync database was synchronized on 2026-10-18 14:11:00-0300 (`pacman.log:2288`, `stat` ctime/mtime 14:11:00).
  - At the time of the incident, the host was 413 packages behind its sync DB.
  - The partial upgrade of `libinput` was ruled a forbidden partial upgrade.
  - Hyprland running in memory retained `1.31.3-1` mapping; `soname libinput.so.10` remained unchanged; `ldd -r` had 0 unresolved symbols.
  - Remediation is explicitly operator-owned; agents must not attempt pacman package changes or service restarts.
- **Fresh Host Observation (from HostSnapshot capture `host-snapshot.json` at 2026-10-20T07:44:39Z):**
  - `pacman -Q libinput libinput-tools mkinitcpio systemd`: `libinput 1.32.0-1`, `libinput-tools 1.32.0-1`, `mkinitcpio 41.1-1`, `systemd 261.2-1`.
  - `pacman -Qu`: Pending update count in retained host snapshot is 413 packages (413 nonempty stdout lines in `probes.pending_updates.stdout`; the earlier mention of 229 was a draft counting error). Both pre-campaign sync DB state and current snapshot confirm 413 pending packages.
  - `/var/log/pacman.log`: Lines 2429–2439 record the exact command and ALPM actions.
  - `/usr/lib/initcpio/hooks/{btrfs-overlayfs,plymouth}`: Both retain hardcoded `/new_root` paths, confirming the `mkinitcpio 42` update-safety gate blocker is active.

## 4. Recommendations for Tsukuroi Round 15
1. **Decision Gate:** Re-verify update safety and declare `BLOCKED_FOR_AGENT_PACKAGE_ACTION` for C2 freshness. No package transaction, upgrade, downgrade, or removal.
2. **Pacman Guard:** Enforce dry-run guard (`pacman -Sp --print-format '%n %v'`) for any hypothetical install, rejecting any installed package overlap.
3. **Census & Scoring:** Keep depth at 8 and freshness at 9 (no ordinal inflation). Treat historical 413 pending count as context, citing fresh measured snapshot counts alongside it.

## Sources, Limits, and Tools
- Sources read: `.ufo/l0-questions.md:54`, `.ufo/reports/round-15/mado.md:1-122`, `/var/log/pacman.log:2285-2439`, `host-snapshot.json`.
- Limits: Read-only research; no live host commands executed, no verification run, no credentials handled.
- Tools installed or updated: none.
