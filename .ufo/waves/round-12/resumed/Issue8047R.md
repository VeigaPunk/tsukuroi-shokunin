# Scout Evidence: omacom/omarchy#8047 Frontier Analysis (Resumed Round 12)

source: https://github.com/omacom/omarchy/issues/8047; host probes 2026-10-20; S019, S020, S021, S028, S034, S036.
verified-at: 2026-10-20
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
- **Comments**: 1 comment by `@omarchybot` on `2026-10-09T00:27:22Z` (worker VM repro test with maintainer findings; thread remains open pending reporter response; no pull request created).

---

## 2. Located Quote and Accept/Reject Determination

### Located Quote (19 words)
> "The result is that snapshot rollback cannot work on a stock Omarchy install — omarchy-snapshot restore walks straight into it."
— *omacom/omarchy#8047, § "What's wrong?", paragraph 1.*

### Evaluation: REJECT as Primary Ground / Falsified Central Claim
- **Reasoning**:
  1. **Tier C community assertion**: Per `corpus/SOURCES.md` and `corpus/QUALITY.md`, unverified issue tracker submissions are Tier C community claims and do not constitute authoritative host truth.
  2. **Source-reported maintainer test**: On `2026-10-09T00:27:22Z`, `@omarchybot` reported reproducing and testing the scenario on a stock Omarchy worker VM (`limine-snapper-sync 1.31.0`, `limine-mkinitcpio-hook 1.38.0`, stock `btrfs-overlayfs`, `RESTORE_METHOD=replace`). This is source-reported evidence from an upstream maintainer bot (`[community:bot]`), not non-author empirical verification by this lane. The bot reported that while executing `/usr/lib/limine/limine-snapper-sync --help` directly fails with `"You are not in Btrfs, the tool does not update anything!"` (because `/` is an overlay filesystem), the public restore execution path called by `limine-snapper-restore` / `omarchy-snapshot restore` (`/usr/bin/limine-snapper-sync --restore --no-mutex`) operates on `/run/lss` (mounting the Btrfs top-level subvolume) and succeeded with `RESTORE_METHOD=replace`.
  3. **Upstream design alignment**: Upstream `limine-snapper-sync` README (S019) explicitly documents that OverlayFS is supported and recommended for `replace` and `rsync` restore methods. Only `snapper`/`opensuse` methods reject overlay roots.
  4. **Grounding scope**: The report maps to no C1 (census) or C2 (matrix) branch and cannot ground core claims. It is retained strictly as an opened boundary lead (S036, rejected as primary claim).

---

## 3. Applicability to Current Host Analysis

### A. Applicability to Host Mode 0555 / Snapper `EACCES` (`snapper-eacces-mechanism.md`): INAPPLICABLE
- **[obs]** The live host root filesystem is mounted directly as native Btrfs, not OverlayFS: `findmnt -no FSTYPE,SOURCE,TARGET /` returns `btrfs /dev/mapper/root[/@] /` (re-verified live 2026-10-20).
- **[obs]** Issue #8047 addresses snapshot-boot OverlayFS semantics and does not discuss root inode permissions (`0555` vs `0755`), DAC access checks, or capability restrictions (`CapabilityBoundingSet=CAP_SYS_ADMIN` in `limine-snapper-sync.service` dropping `CAP_DAC_OVERRIDE`).
- **[inf]** The recurring `errno:13` (`create subvolume failed`) in `limine-snapper-sync.service` occurs during normal system operation. While the hypothesis that root directory mode `0555` and dropped `CAP_DAC_OVERRIDE` prevent subvolume creation is consistent with observed DAC bits and unit capabilities, **host causality remains UNPROVEN** (no historical syscall trace, target path trace, or runtime credentials capture has been executed on this host; it remains an unproven inference `[inf]`). Regardless of root cause, Issue #8047 addresses snapshot-boot OverlayFS and has zero causal or diagnostic relevance to normal-boot Btrfs operation.

### B. Applicability to Snapshot Boot and OverlayFS Analysis (`initramfs-v42-sysroot-recovery.md`): APPLICABLE (Context / Frontier Boundary)
- **[obs]** Local host configuration in `/etc/limine-snapper-sync.conf:159` defines `RESTORE_METHOD=replace` (`grep -n '^RESTORE_METHOD' /etc/limine-snapper-sync.conf` re-probed 2026-10-20). This matches the default method reported by upstream and `@omarchybot` to succeed even with an active OverlayFS.
- **[obs]** Confirms known snapshot-boot degradation: booting into a snapshot entry triggers `btrfs-overlayfs` (`run_latehook` in S021), mounting OverlayFS on `/`. Under this state, `findmnt -no FSTYPE /` is `overlay`, `btrfs property get / ro` and `snapper list` fail, and `systemd-remount-fs.service` fails (tracked in omarchy issue #6634).
- **[obs] Present hook text**: Upstream `limine-entry-tool` `btrfs-overlayfs` hook (S021:4) currently hardcodes `root_mnt="/new_root"`.
- **[inf] Predicted future upgrade effect**: Under a future `mkinitcpio` 42 upgrade (`initramfs-v42-sysroot-recovery.md`), initramfs will mount root at `/sysroot`. If the hook is not updated upstream to inspect `/sysroot`, `run_latehook`'s `findmnt` check will fail and silently exit 0 without mounting OverlayFS. This is a predicted compatibility effect of a future upgrade, not a failure of the current installed `mkinitcpio 41.1-1` configuration.

---

## 4. Resumed Round Audit of Inherited Evidence (`.ufo/waves/round-12/Issue8047.md`)

In accordance with resumed round requirements, the inherited round-12 evidence file `.ufo/waves/round-12/Issue8047.md` was audited against live host and upstream source state:
- **Reused**:
  - Exact issue identity, 19-word located quote from § "What's wrong?", source-reported maintainer VM reproduction details, upstream S019/S020/S021 citations, and the distinction between normal-boot Btrfs and snapshot-boot OverlayFS.
- **Rejected**:
  - Any unverified community assertion that snapshot rollback is impossible on stock Omarchy.
  - Using Tier C issue submissions to establish causal proof for host health claims.
- **Corrected & Freshly Verified (2026-10-20)**:
  - All host commands re-executed and verified live on 2026-10-20.
  - Epistemic markers strictly separated: `[obs]` for observed command outputs and source text, `[inf]` for deductive causal reasoning, `[unk]` for untested operator paths.
  - Re-verified that no new comments or commits have altered the state of #8047 since `2026-10-09T00:27:22Z`.

---

## 5. Measured Host Evidence Summary (Probed 2026-10-20)

| Dimension | Command / Source | Observed Value / Finding | Status |
|---|---|---|---|
| Issue Status | `issue://omacom/omarchy/8047` | OPEN, created 2026-08-24, updated 2026-10-09, 1 comment | Verified |
| Host Root FSTYPE | `findmnt -no FSTYPE,SOURCE,TARGET /` | `btrfs /dev/mapper/root[/@] /` (native Btrfs, not overlay) | Verified |
| Host Root Mode | `stat -c '%a %U:%G' /` | `555 root:root` | Verified |
| Local Restore Method | `/etc/limine-snapper-sync.conf:159` | `RESTORE_METHOD=replace` | Verified |
| Installed Packages | `pacman -Q limine-snapper-sync limine-mkinitcpio-hook` | `limine-snapper-sync 1.31.0-1.1`, `limine-mkinitcpio-hook 1.38.0-1.1` | Verified |

---

## 6. Risks and Remaining Unknowns

- **[unk]** Whether `limine-snapper-restore` would encounter non-overlay errors if executed on this host with mode `0555` on `/` when replacing `@` (untested; non-root read-only boundary forbids running restore or sudo tests).
- **[risk]** If an operator changes `RESTORE_METHOD` to `snapper` or `opensuse` in `/etc/limine-snapper-sync.conf`, snapshot rollback from an OverlayFS snapshot boot would fail as described in #8047.
- **[risk]** Upgrading to `mkinitcpio` 42 before `limine-mkinitcpio-hook` updates its `/new_root` path to `/sysroot` will silently disable `btrfs-overlayfs`, changing snapshot boots from writable overlay to read-only btrfs.

---

## 7. QUALITY check

1. **Provenance**: Claims cite opened issue URL, exact line/comment anchors, upstream Git commits (S019, S020, S021), and live host command invocations.
2. **Epistemic Hygiene**: `[obs]`, `[inf]`, and `[unk]` tags are explicitly applied; maintainer findings are tagged as empirical maintainer comments, not unverified host truth.
3. **No Oral Knowledge**: All statements are grounded in primary sources, configuration files, package manager outputs, or live filesystem inspection.
4. **Resumed Round Compliance**: Inherited evidence from round 12 was re-audited and re-measured; historical evidence was not overwritten; fresh findings are recorded in this durable resumed file.

---

## 8. Epistemic Precision Correction & Errata (Parent Steering)

- **Host EACCES Causality Status**: Host causality for `errno:13` in `limine-snapper-sync.service` remains UNPROVEN. Observed DAC mode `0555` and `CapabilityBoundingSet=CAP_SYS_ADMIN` provide a consistent mechanism hypothesis, but no syscall trace, target path trace, or runtime credentials capture has been performed on this host. Any phrasing asserting proven causation is corrected to consistent hypothesis `[inf]`.
- **Source Attribution for Maintainer VM Test**: The test of `limine-snapper-restore` under OverlayFS with `RESTORE_METHOD=replace` is source-reported evidence from upstream maintainer bot `@omarchybot` on GitHub issue #8047 (`[community:bot]`), not empirical non-author verification performed by this lane.
- **Hook Code vs Future Upgrade Effect**: Distinguished present hook text (`root_mnt="/new_root"` in S021) from the predicted future upgrade behavior (silent exit 0 if paired with `mkinitcpio` 42 `/sysroot`). Present host runs `mkinitcpio 41.1-1`.
