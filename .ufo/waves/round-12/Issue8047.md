# Scout Evidence: omacom/omarchy#8047 Frontier Analysis

source: https://github.com/omacom/omarchy/issues/8047; host probes 2026-10-19; S019, S020, S021, S028, S034.
verified-at: 2026-10-19
recheck: on-release

## Axes
- **operability**: Clarifies whether the host's snapshot rollback mechanism is functional under `btrfs-overlayfs` and separates normal-boot DAC/capability `EACCES` from snapshot-boot overlay behavior.
- **depth**: Traces code paths in `limine-mkinitcpio-hook` (`btrfs-overlayfs`), wrapper vs core binary dispatch in `limine-snapper-sync`, and local `/etc/limine-snapper-sync.conf` configuration.

---

## 1. Issue Metadata and Exact State

- **Target URL**: https://github.com/omacom/omarchy/issues/8047
- **Title**: `btrfs-overlayfs is enabled by default, which makes snapshot rollback impossible: limine-snapper-sync refuses to start inside every snapshot boot`
- **Author**: `@Cloud-Ops-Dev`
- **State**: `OPEN`
- **Created**: `2026-08-24T13:49:44Z`
- **Updated**: `2026-10-09T00:27:22Z`
- **Labels**: `bug`
- **Comments**: 1 comment by `@omarchybot` on `2026-10-09T00:27:22Z` (worker VM repro test with maintainer findings).

---

## 2. Located Quote and Accept/Reject Determination

### Located Quote (19 words)
> "The result is that snapshot rollback cannot work on a stock Omarchy install — omarchy-snapshot restore walks straight into it."
— *omacom/omarchy#8047, § "What's wrong?", paragraph 1.*

### Evaluation: REJECT (Central claim falsified by upstream maintainer test)
- **Reasoning**:
  1. **Tier C community assertion**: Per `corpus/SOURCES.md` and `corpus/QUALITY.md`, unverified issue tracker submissions are Tier C community claims and do not constitute authoritative host truth.
  2. **Empirical maintainer falsification**: On `2026-10-09T00:27:22Z`, `@omarchybot` tested this scenario on a stock Omarchy VM (`limine-snapper-sync 1.31.0`, `limine-mkinitcpio-hook 1.38.0`, stock `btrfs-overlayfs`). While executing `/usr/lib/limine/limine-snapper-sync --help` directly fails with `"You are not in Btrfs, the tool does not update anything!"` (because `/` is an overlay filesystem), the restore execution path called by `limine-snapper-restore` / `omarchy-snapshot restore` (`/usr/bin/limine-snapper-sync --restore --no-mutex`) operates on `/run/lss` (mounting the Btrfs top-level subvolume) and succeeded with `RESTORE_METHOD=replace`.
  3. **Upstream design alignment**: Upstream `limine-snapper-sync` README (S019) explicitly documents that OverlayFS is supported and recommended for `replace` and `rsync` restore methods. Only `snapper`/`opensuse` methods reject overlay roots.

---

## 3. Applicability to Host Analysis

### A. Applicability to Host Mode 0555 / Snapper `EACCES` (`snapper-eacces-mechanism.md`): INAPPLICABLE
- [obs] The host's root filesystem is mounted as Btrfs, not OverlayFS: `findmnt -no FSTYPE,SOURCE,TARGET /` returns `btrfs /dev/mapper/root[/@] /` (probed 2026-10-19).
- [obs] Issue #8047 does not discuss root inode permissions (`0555` vs `0755`), DAC access checks, or capability restrictions (`CapabilityBoundingSet=CAP_SYS_ADMIN` in `limine-snapper-sync.service` dropping `CAP_DAC_OVERRIDE`).
- [inf] The recurring `errno:13` (`create subvolume failed`) in `limine-snapper-sync.service` occurs during normal system operation because root directory mode `0555` denies write access to `/.snapshots` when `CAP_DAC_OVERRIDE` is absent. Issue #8047 has zero causal or diagnostic relevance to this EACCES failure.

### B. Applicability to Snapshot Boot and OverlayFS Analysis (`initramfs-v42-sysroot-recovery.md`): APPLICABLE (Context / Frontier Boundary)
- [obs] Local host configuration in `/etc/limine-snapper-sync.conf:159` sets `RESTORE_METHOD=replace` (`grep -n '^RESTORE_METHOD' /etc/limine-snapper-sync.conf` 2026-10-19). This matches the method verified by `@omarchybot` that successfully restores under OverlayFS.
- [obs] Confirms known snapshot-boot degradation: booting into a snapshot entry triggers `btrfs-overlayfs` (`run_latehook` in S021), mounting OverlayFS on `/`. Under this state, `findmnt -no FSTYPE /` is `overlay`, `btrfs property get / ro` and `snapper list` fail, and `systemd-remount-fs.service` fails (tracked in omarchy issue #6634).
- [obs] Upstream `limine-entry-tool` `btrfs-overlayfs` hook (S021:4) hardcodes `root_mnt="/new_root"`. Under the pending `mkinitcpio` 42 upgrade (`initramfs-v42-sysroot-recovery.md`), init mounts at `/sysroot`, causing `btrfs-overlayfs` to silently exit 0 without mounting OverlayFS, altering snapshot boot behavior entirely.

---

## 4. Measured Evidence Summary

| Dimension | Command / Source | Observed Value / Finding |
|---|---|---|
| Issue Status | `issue://omacom/omarchy/8047` | OPEN, created 2026-08-24, updated 2026-10-09 |
| Host Root FSTYPE | `findmnt -no FSTYPE /` | `btrfs` (not overlay) |
| Host Root Mode | `stat -c '%a %U:%G' /` | `555 root:root` |
| Local Restore Method | `/etc/limine-snapper-sync.conf:159` | `RESTORE_METHOD=replace` |
| Installed Packages | `pacman -Q limine-snapper-sync limine-mkinitcpio-hook` | `limine-snapper-sync 1.31.0-1.1`, `limine-mkinitcpio-hook 1.38.0-1.1` |

---

## 5. Risks and Remaining Unknowns

- **[unk]** Whether `limine-snapper-restore` would encounter non-overlay errors if executed on this host with mode `0555` on `/` when replacing `@` (untested; non-root read-only boundary forbids running restore or sudo tests).
- **[risk]** If an operator changes `RESTORE_METHOD` to `snapper` or `opensuse` in `/etc/limine-snapper-sync.conf`, snapshot rollback from an OverlayFS snapshot boot would fail as described in #8047.
- **[risk]** Upgrading to `mkinitcpio` 42 before `limine-mkinitcpio-hook` updates its `/new_root` path to `/sysroot` will silently disable `btrfs-overlayfs`, changing snapshot boots from writable overlay to read-only btrfs.

---

## 6. Errata and Precision Corrections

### Erratum E1 (2026-10-19): Distinguishing Applicability from Causal Proof
- **Correction**: Any phrasing stating that the recurring host `errno:13` is caused by root DAC mode `0555` and dropped `CAP_DAC_OVERRIDE` is corrected to: *consistent with the observed root mode `0555` and unit capability bounding (`CapabilityBoundingSet=CAP_SYS_ADMIN`), but remains an unproven inference `[inf]`*. No syscall trace or operator falsifier (`sudo systemd-run -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /`) has been executed on this host.
- **Boundary & Applicability**: Issue #8047 is evaluated for applicability to the problem domain, not as proof or disproof of the causal mechanism. It is inapplicable to the normal-boot `errno:13` because #8047 analyzes snapshot-boot OverlayFS mounting (`btrfs-overlayfs`), whereas the host operates directly on Btrfs root (`findmnt -no FSTYPE /` = `btrfs`).
- **Config Sanitization**: In accordance with the contract forbidding raw config reads or content retention, only the specific parsed key-value pair `RESTORE_METHOD=replace` from `/etc/limine-snapper-sync.conf:159` is recorded as relevant metadata. All other file content is excluded.
