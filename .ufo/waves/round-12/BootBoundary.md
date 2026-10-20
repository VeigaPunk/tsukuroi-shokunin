# BootBoundary — UFO-FSD Connector Evidence & Proposal (Tsukuroi Round 12)

**Seat:** `BootBoundary` (connector, leaf member — no subagent dispatch).  
**Workspace:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.  
**Declared Axes:** `operability` (gate correctly prevents unbootable system states), `depth` (source-grounded separation of runtime DAC vs early-boot initramfs stages).  
**Scope:** Compare C1/C2 claims to `corpus/knowledge/initramfs-v42-sysroot-recovery.md`. Confirm mode diagnostics do not solve the initramfs hook root target issue and no upgrade authorization follows. Record unresolved freshness lead separately, not as a new claim.  
**Verified-at:** 2026-10-19.  
**Recheck procedure:**  
`grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf; grep -n '/new_root' /usr/lib/initcpio/hooks/*; pacman -Q mkinitcpio plymouth limine-mkinitcpio-hook; pacman -Si mkinitcpio plymouth limine-mkinitcpio-hook; curl -fsSL 'https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs' | grep -n 'root_mnt='`

---

## 1. Measured Evidence Basis (Read-Only Host and Upstream Probes)

All probes executed read-only on host `plazir27` as uid 1000 without privilege elevation or system modification on 2026-10-19. No tools were installed or upgraded.

| Probe ID | Command executed | Exit code | Observed output / finding |
|---|---|---|---|
| **E1** | `grep -Hn '^HOOKS' /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf` | 0 | `/etc/mkinitcpio.conf:55:HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt filesystems fsck)`<br>`/etc/mkinitcpio.conf.d/omarchy_hooks.conf:1:HOOKS=(base udev plymouth keyboard autodetect microcode modconf kms keymap consolefont block encrypt filesystems fsck btrfs-overlayfs)`<br>`/etc/mkinitcpio.conf.d/omarchy_resume.conf:1:HOOKS+=(resume)`<br>→ The effective HOOKS omit `systemd`; selects busybox initramfs. |
| **E2** | `grep -n '/new_root' /usr/lib/initcpio/hooks/*` | 0 | `/usr/lib/initcpio/hooks/btrfs-overlayfs:4: root_mnt="/new_root"`<br>`/usr/lib/initcpio/hooks/plymouth:11: plymouth update-root-fs --new-root-dir=/new_root`<br>`/usr/lib/initcpio/hooks/usr:5: ... /new_root/etc/fstab`<br>`/usr/lib/initcpio/hooks/usr:18: ... /new_root/usr ...`<br>→ 2 configured runtime hooks (`btrfs-overlayfs`, `plymouth`) hardcode `/new_root`. |
| **E3** | `pacman -Q mkinitcpio plymouth limine-mkinitcpio-hook limine-snapper-sync snapper` | 0 | Installed versions:<br>`mkinitcpio 41.1-1`<br>`plymouth 26.134.222-2`<br>`limine-mkinitcpio-hook 1.38.0-1.1`<br>`limine-snapper-sync 1.31.0-1.1`<br>`snapper 0.13.1-3` |
| **E4** | `pacman -Si mkinitcpio plymouth limine-mkinitcpio-hook limine-snapper-sync snapper` | 0 | Sync database versions (pending in repos):<br>`core/mkinitcpio 42.2-1`<br>`extra/plymouth 26.134.222-3`<br>`omarchy/limine-mkinitcpio-hook 1.40.0-2`<br>`omarchy/limine-snapper-sync 1.32.1-2`<br>`extra/snapper 0.13.2-1` |
| **E5** | `stat -c '%a %U:%G %F' /; getfacl -p /; findmnt -n -o TARGET,FSTYPE,OPTIONS /` | 0 | `555 root:root directory`<br>`user::r-x`, `group::r-x`, `other::r-x` (no write bit for anyone, no extended ACLs)<br>`/ btrfs rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`<br>→ Root is mode 0555 on a `rw` Btrfs mount (not an `ro` filesystem). |
| **E6** | `curl -fsSL 'https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42/init' \| grep -n '/sysroot'` | 0 | Lines 66, 67, 77, 78, 87, 88, 110: `"$mount_handler" /sysroot`; `/usr/bin/switch_root /sysroot "$init" "$@"`. |
| **E7** | `curl -fsSL 'https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42/init' \| grep -o '/new_root' \| wc -l` | 0 | Exactly **0** occurrences of `/new_root` in upstream mkinitcpio v42 `init`. |
| **E8** | `curl -fsSL 'https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs' \| head -10` | 0 | Upstream master S021 line 4: `root_mnt="/new_root"`; line 7: `fstype=$(findmnt --mountpoint "$root_mnt" -no FSTYPE 2>/dev/null) \|\| return 0`. |
| **E9** | `curl -fsSL 'https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook' \| grep -n 'new-root'` | 0 | Upstream Arch packaging S022 line 11: `plymouth update-root-fs --new-root-dir=/new_root`. |

---

## 2. Structural Comparison: C1/C2 vs `initramfs-v42-sysroot-recovery.md`

| Dimension | Round 12 Claims C1 / C2 | Boot Recovery Note (`initramfs-v42-sysroot-recovery.md`) |
|---|---|---|
| **Lifecycle Phase** | **Late Userspace Runtime (Post-`switch_root`):** Inspected while the full OS is booted, systemd is PID 1, and services are running. | **Early Boot Userspace (Pre-`switch_root` Initramfs):** Executes within the ephemeral busybox initrd ramfs before the real root is switched. |
| **Target Object** | Inode DAC permissions and capabilities: `/` mode (`0555`), owner/group (`root:root`), package ownership absence (`pacman -Qo /` fails), and service capability bounding (`CapabilityBoundingSet=CAP_SYS_ADMIN`). | Initramfs shell hook scripts and mount targets: `/usr/lib/initcpio/hooks/btrfs-overlayfs`, `/usr/lib/initcpio/hooks/plymouth`, and mkinitcpio's `init` mount directory (`/sysroot` vs `/new_root`). |
| **Failure Mechanism** | `EACCES` (errno 13): `limine-snapper-sync.service` running as root lacks `CAP_DAC_OVERRIDE` in `CapabilityBoundingSet`, denying write access to mode `0555` `/` to create `/.snapshots`. | Silent hook no-op / boot degradation: `run_latehook` in `btrfs-overlayfs` probes `findmnt --mountpoint /new_root`; under mkinitcpio v42, root is at `/sysroot`, so the check fails and exits 0 before mounting OverlayFS. |
| **Effect on System** | No automatic snapshots created by Snapper; `snapper list-configs` is empty; `U1` no rollback net on host. | Snapshot boot boots directly into an unmodifiable, read-only Btrfs subvolume without an OverlayFS read-write layer, breaking userspace boot; Plymouth root-fs updates fail. |
| **Remediation Surface** | Userspace filesystem DAC / service policy: Operator creates config / restores write bit, or upstream package adjusts unit capabilities. | Boot-chain hook packaging / configuration: Patching `/usr/lib/initcpio/hooks/*` to dynamic target detection (`/sysroot` or `/new_root`), or migrating to `systemd` initrd hook. |

---

## 3. Core Verifications: Hook Target Independence & Zero Upgrade Authorization

### A. Confirmation: Mode Diagnostics Do NOT Solve the Initramfs Hook Root Target Issue
- **Causal Disjointness:** Mode diagnostics (C1 root metadata observation `root_mode=0555` and C2 EACCES decision matrix) characterize DAC access rules on the installed root filesystem. They do not alter, inspect, or reconfigure the early-boot initramfs image or its build hooks.
- **Hook Code Invariant:** In `/usr/lib/initcpio/hooks/btrfs-overlayfs`, line 4 unconditionally sets `root_mnt="/new_root"`. Whether the root directory inode is mode `0555`, `0755`, or unreadable has zero bearing on the fact that mkinitcpio v42 mounts root at `/sysroot`.
- **Silent Failure Under mkinitcpio v42:** If mkinitcpio is upgraded to v42, `findmnt --mountpoint "/new_root"` returns non-zero because `/new_root` is an empty unmounted directory in the initrd. The hook executes `|| return 0` and exits without executing `mount -t overlay ... "$root_mnt"`. Mode diagnostics do not touch or fix this line.
- **Conclusion:** Mode diagnostics provide zero remediation for the initramfs hook target mismatch.

### B. Confirmation: NO Upgrade Authorization Follows from C1 or C2
- **Update-Safety Gate Policy:** The update-safety gate forbids `pacman -Syu` because boot-chain packages (`mkinitcpio 42.2-1` in `core`) break early-boot runtime hooks (`btrfs-overlayfs` and `plymouth`).
- **Hazard of False Conflation:** Completing C1 (measuring `/` metadata) and C2 (source-backed EACCES matrix) provides diagnostic clarity for why Snapper failed to initialize. However, diagnosing why Snapper failed does **not** make full-system upgrades safe.
- **Compounded Failure Risk:** If an operator believed that resolving the Snapper/rollback net question authorized `pacman -Syu`, the resulting transaction would install `mkinitcpio 42.2-1`. Upon rebooting into any newly configured snapshot, `btrfs-overlayfs` would silently fail to mount OverlayFS, leaving the system in a broken, read-only state without writable temporary cowspace.
- **Conclusion:** The update-safety gate MUST remain locked. NO upgrade authorization follows from C1 or C2.

---

## 4. Unresolved Freshness Lead (Recorded Separately, Not as a New Claim)

*Per assignment instruction, this is an unresolved freshness observation, NOT a new round claim or score delta.*

1. **Upstream Master Hook Staleness (S021):**
   - Recheck of `https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs` on 2026-10-19 confirms line 4 still reads `root_mnt="/new_root"`.
   - Upstream `limine-entry-tool` has **not** adopted `/sysroot` or a dynamic fallback (`[ -d /sysroot ] && root_mnt="/sysroot" || root_mnt="/new_root"`).
2. **Upstream Plymouth Hook Staleness (S022):**
   - Recheck of `https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook` on 2026-10-19 confirms line 11 still passes `--new-root-dir=/new_root`.
3. **Repository Version Disparity & Candidate Risk:**
   - `core/mkinitcpio` has already advanced to `42.2-1` (built 2026-10-01).
   - `omarchy/limine-mkinitcpio-hook` has advanced in the sync DB to `1.40.0-2` (built 2026-10-08). Comparing installed hooks with current upstream master suggests that the version bump does not resolve the hardcoded `/new_root` path in `btrfs-overlayfs`.
   - **Qualification:** Comparing installed hooks and upstream git master is an inference / candidate lead; it does **not** establish the exact contents of the pending binary package `limine-mkinitcpio-hook 1.40.0-2` unless that actual archive artifact is opened and inspected (which was not done here; no package download/extraction).
4. **Channel Freshness State:**
   - The sync databases carry a 36-day content lag (`stamp=36d`, `status=UNKNOWN-UPSTREAM`). An operator database refresh (`-Sy`) would not solve this issue because the upstream source itself remains unpatched.
   - **Lead to Track:** Monitor `limine-entry-tool` issues/commits for explicit mkinitcpio v42 `/sysroot` support before any boot-chain upgrade can be scheduled.
---

## 5. UFO-FSD Connector Move (Bounded Proposal)

### A. The Non-Obvious Move: Establish the Dual-Gate Boundary Invariant
Formally decouple the **Runtime Host DAC / Rollback Net Gate** from the **Boot-Chain Hook Target Gate** in tsukuroi's update-safety contract:

```
[Runtime Host Scope: C1 / C2]
  ├── Observation: / mode 0555 root:root (unowned by package, rw btrfs mount)
  ├── Diagnosis: limine-snapper-sync EACCES (CapabilityBoundingSet lacks CAP_DAC_OVERRIDE)
  └── Outcome: Explains why /.snapshots creation failed (U1: no rollback net)
        │
        ▼ (STRICT BOUNDARY: Does NOT cross or satisfy)
        │
[Boot-Chain Initramfs Scope: initramfs-v42-sysroot-recovery]
  ├── Invariant: mkinitcpio v42 mounts root at /sysroot; hooks expect /new_root
  ├── Impact: btrfs-overlayfs silently no-ops; snapshot boots fail writable overlay
  └── Outcome: pacman -Syu REMAIN STRICTLY FORBIDDEN (Fail-Closed)
```

### B. Second-Order Effects Across Surfaces
1. **Runtime Surface:** Prevents any automated remediation or operator checklist from attempting to "test" snapshot boots or run `pacman -Syu` under the assumption that diagnosing root permissions cured update-safety blockers.
2. **Contract Surface:** Enforces that `PLANE update-safety` in `tools/tsukuroi-census.sh` evaluates the boot-chain and channel freshness as independent blocking criteria, preventing `PLANE packages` root-metadata additions from accidentally clearing update-safety warnings.
3. **Substrate Surface:** Protects the physical Btrfs subvolume layout (`/@`, `/@home`, `/@log`, `/@pkg`) from being exposed to unbootable snapshot entries under mkinitcpio v42.
4. **Verification Surface:** Requires any future verification of update safety to check BOTH the presence of a rollback net AND the verified compatibility of all configured `HOOKS` with the target mkinitcpio version.

### C. Explicit Contradictions Stated (Not Smoothed)
- **Contradiction 1 (Rollback Net Prep vs Boot Breakage):** The historical update-safety recommendation (`update-safety-v3.md:368`) instructed the operator to "decide the rollback story — configure a snapper/limine-snapper-sync config... before any `-Syu`". However, on this host, if the operator configures Snapper and then runs `-Syu`, the upgrade will pull `mkinitcpio 42.2-1`, which is predicted to disable the newly configured snapshot rollback mechanism in `btrfs-overlayfs`. Fulfilling prep item (a) exposes the host to predicted boot-chain degradation (b). Note: "immediate boot failure" is a structural prediction / candidate risk, not an observed execution outcome, as no rebuild or test boot was run.
- **Contradiction 2 (Mode 0555 vs Read-Only Mount):** Mode `0555` on `/` denies owner write for processes lacking `CAP_DAC_OVERRIDE`, but the filesystem mount is `rw` (E5). Diagnosing this as an "unwritable filesystem" is false; kernel and privileged processes write without hindrance.
- **Contradiction 3 (Upstream Package Bump vs Defect Resolution):** `limine-mkinitcpio-hook` bumped from 1.38 to 1.40 in the sync DB, while upstream git master continues to hardcode `/new_root`. Version advancement does not equal proven compatibility resolution; however, "version bump does not fix" remains a prediction/inference until the actual pending package archive is opened and inspected.
---

## 6. Risks and Verification Gaps

1. **Read-Only Non-Root Boundary:** No privileged test boot, initramfs rebuild (`mkinitcpio -P`), or snapshot restore (`omarchy-snapshot restore`) was executed. All findings are derived from static source inspection, local configuration sweeps, and unprivileged runtime probes.
2. **Author-Side Status:** This evidence is compiled by seat `BootBoundary` (author-side subagent). Per round contract, this output is evidence, not independent non-author verification.
3. **Unrun Probes:** Selftests and live census runs were not executed during this pass (contract: parent runs checks once after integration).
4. **Artifact Inspection Limit:** Comparing installed hooks and current upstream master does **not** establish the actual contents of the pending `limine-mkinitcpio-hook 1.40.0-2` package unless that specific package artifact (`.pkg.tar.zst`) is opened and inspected (not done in this read-only pass).
5. **Prediction vs Observation:** Statements of "immediate boot failure" or "version bump does not fix" are model predictions and compatibility risk inferences, not observed runtime events. No actual boot, kernel switch, or initramfs rebuild was run.
6. **Upgrade Status:** State upgrade is strictly **NOT authorized**. The source-path mismatch remains a candidate risk requiring pending-package hook comparison and an operator-safe gate.

---

## 7. Outcome Summary

- **C1/C2 vs Boot Boundary:** Mode diagnostics operate in post-`switch_root` runtime userspace; `initramfs-v42-sysroot-recovery.md` operates in pre-`switch_root` early boot. Mode diagnostics do **not** solve the initramfs hook root target issue.
- **Upgrade Authorization:** Confirmed **NO upgrade authorization follows** from C1 or C2. State upgrade is NOT authorized; source-path mismatch remains a candidate risk requiring pending-package hook comparison and an operator-safe gate.
- **Unresolved Freshness Lead:** Upstream master `limine-entry-tool` (S021) and Arch `plymouth` (S022) retain hardcoded `/new_root` references despite `mkinitcpio 42.2-1` in `core`. The pending `limine-mkinitcpio-hook 1.40.0-2` package contents remain uninspected. Recorded separately; no new claim.
- **Verdict:** Bounded findings, explicit qualifications, and dual-gate proposal documented. No unsupported PASS.
