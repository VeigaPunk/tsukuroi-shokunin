# BootCoupling — Review of Existing Initramfs Recovery Knowledge & Gate Invariants

author: TsukuroiR15.BootCoupling (scout)
date: 2026-10-20
status: read-only research complete; leaf seat (no subagent dispatch)
judged_on: depth

## 1. Scope & Declared Axes

- **Axes:** `depth` (source-grounded separation of early-boot initramfs stage vs runtime userspace; exact hook code path invariant) and `operability` (preserving update-safety gate constraints without boot mutation).
- **Target:** Review existing initramfs recovery knowledge only (`corpus/knowledge/initramfs-v42-sysroot-recovery.md`, historical `BootBoundary.md` / `BootBoundaryR.md`, and primary sources S014–S016, S021–S022).
- **Task Mandate:** Determine whether existing gate constraints remain unchanged; strictly avoid any new boot writes, image rebuilds, test boots, package transactions, or service activations.

## 2. Review of Existing Initramfs Knowledge & Evidence Pins

1. **Busybox Initramfs Selection:**
   - Shipped configuration in `/etc/mkinitcpio.conf` and drop-in `/etc/mkinitcpio.conf.d/omarchy_hooks.conf` omits the `systemd` hook.
   - Per ArchWiki (S014, tier A), omission of `systemd` selects the busybox-based initramfs, which relies on runtime shell hook scripts in `/usr/lib/initcpio/hooks/*`.
2. **Upstream mkinitcpio v42 Root Mount Shift:**
   - Upstream mkinitcpio v42 release notes (S015, tier A) and raw `init` source (S016, tier A) establish that busybox init mounts the real root at `/sysroot` (`# Mount root at /sysroot`, `init:66-67`) and invokes `/usr/bin/switch_root /sysroot` (`init:110`).
   - Upstream v42 `init` has exactly **0** `/new_root` mentions (compared to **7** in v41.x).
3. **Hardcoded Hook Path Invariant (`/new_root`):**
   - Host runtime hooks `/usr/lib/initcpio/hooks/btrfs-overlayfs:4` (`root_mnt="/new_root"`) and `/usr/lib/initcpio/hooks/plymouth:11` (`--new-root-dir=/new_root`) hardcode `/new_root` (S021, S022).
   - In `btrfs-overlayfs`, line 7 executes `fstype=$(findmnt --mountpoint "$root_mnt" -no FSTYPE 2>/dev/null) || return 0`. Under mkinitcpio v42 where root mounts at `/sysroot`, `/new_root` remains unmounted; the check fails and exits 0 cleanly without mounting OverlayFS.
4. **Current Host State (Observed from Snapshot & Prior Pins):**
   - Host `plazir27` currently has `mkinitcpio 41.1-1` installed (`pacman -Q mkinitcpio`).
   - The pending sync database holds `core/mkinitcpio 42.2-1`.
   - The 2 runtime hooks (`btrfs-overlayfs` and `plymouth`) remain unchanged on disk.

## 3. Existing Gate Constraints Remain Strictly Unchanged

- **Dual-Gate Invariant Maintained:**
  - Runtime userspace findings (C1 root mode `0555`, C2 partial-upgrade observations of `libinput 1.32.0-1`) are causally disjoint from early-boot initramfs stages.
  - No userspace package query, root directory inode observation, or partial-upgrade logging resolves or touches the initramfs hook path mismatch.
- **Update-Safety Gate Policy:**
  - `pacman -Syu` (full system upgrade) MUST remain locked and BLOCKED for any autonomous agent action.
  - Upgrading `mkinitcpio` from `41.1-1` to `42.2-1` without patched runtime hooks would cause silent failure of `btrfs-overlayfs` during snapshot boots.
  - The operator-reported 2026-10-20 04:25 `libinput` transaction does not clear the boot gate; `mkinitcpio` remains at `41.1-1`.
- **Zero Boot Writes:**
  - No writes to `/boot`, ESP, `/etc/mkinitcpio.conf*`, `/usr/lib/initcpio/*`, or initramfs images (`mkinitcpio -P`).
  - Read-only constraint preserved in full.

## 4. Recommendations & Exact Sources / Limits

- **Recommendations for L1 / Decision Seats:**
  1. Maintain `BLOCKED_FOR_AGENT_PACKAGE_ACTION` on all full-upgrade workflows.
  2. Treat boot-chain upgrade requirements as operator-only interventions requiring verified hook compatibility (`/sysroot` support in `limine-mkinitcpio-hook` and `plymouth`).
  3. Keep C1/C2 documentation and recheck reports decoupled from boot-chain clearance.
- **Exact Sources:**
  - S014 (ArchWiki Mkinitcpio, docs/A/mined, oldid 886405).
  - S015 (mkinitcpio releases v40/v42, docs/A/mined).
  - S016 (mkinitcpio v42 raw init, code/A/mined).
  - S021 (limine-entry-tool btrfs-overlayfs hook, code/A/mined).
  - S022 (Arch plymouth initcpio hook, code/A/mined).
- **Limits:** Read-only analysis of existing committed knowledge, snapshot data, and source pins. No image decompression, kernel execution, test boots, or live host probes performed by this seat.
- **Tools installed/updated:** none.
