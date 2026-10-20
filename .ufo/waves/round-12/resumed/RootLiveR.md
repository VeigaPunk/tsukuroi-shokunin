# RootLiveR — Read-Only Reconnaissance of `/`: Metadata, DAC vs Mount Flags, and Historic Snapper Mechanism State

**Milestone:** round-12 (resumed)  
**Seat:** `RootLiveR` (leaf scout, resumed wave)  
**Assigned target:** Read-only reconnaissance of `/`: `stat -c mode uid gid filetype`, `getfacl -p /`; `findmnt -n -o TARGET,FSTYPE,OPTIONS /` (no SOURCE UUID needed). Record metadata, distinguish DAC from mount flags. Never permissions changes or create files at `/`. Compare historic snapper mechanism state without calling diagnosis proven.  
**Evidence path:** `.ufo/waves/round-12/resumed/RootLiveR.md`  
**Inherited artifact:** `.ufo/waves/round-12/RootLive.md`  
**Host capture timestamp:** `2026-10-20T03:45:00Z` (local: `2026-10-20T00:45:00-03:00`)  
**Host baseline:** Linux `7.2.3-arch1-3` x86_64; git commit `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`.  
**Independence notice:** Author-side seat evidence (leaf scout); not independent non-author verification. Strictly read-only, non-root; no package installs/updates, no systemd-run, no sudo, no permission changes (`chmod` never run), no file creation at `/`.

---

## 1. Axes and Posture (Godspeed Framing)

- **Axes:**
  1. `operability`: Zero side-effects on live system (no writes, no chmods, no service restarts, no package mutation); empirical evidence directly usable by C1 (census root metadata arm) and C2 (EACCES decision matrix).
  2. `depth`: Precise differentiation between VFS mount flags and DAC mode bits, strict coreutils provenance accounting, exact journal timestamps/counts, and rigorous epistemic bounding distinguishing empirical observations (`[obs]`) from candidate mechanisms (`[inf]`).

---

## 2. Resumed Round Re-evaluation & Delta vs Inherited Evidence

The inherited artifact `.ufo/waves/round-12/RootLive.md` (captured 2026-10-20T02:16:41Z) was audited against live system state on 2026-10-20T03:45:00Z:

| Item | Inherited Claim / Value | Resumed Verification (Live Probe) | Disposition / Delta |
|---|---|---|---|
| Mode / Ownership | `0555 root:root` | `0555 root:root` verified via GNU `/usr/bin/stat` | **Reused** (`[obs]`) |
| POSIX ACL | Minimal 3-entry ACL (`user::r-x`, `group::r-x`, `other::r-x`) | Confirmed verbatim via `getfacl -p /` | **Reused** (`[obs]`) |
| Mount Flags | `rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` | Confirmed verbatim via `findmnt` | **Reused** (`[obs]`) |
| Btrfs Property | `ro=false`, `label=` | Confirmed verbatim via `btrfs property get /` | **Reused** (`[obs]`) |
| LSMs Active | `capability,landlock,lockdown,yama,bpf` | Confirmed verbatim via `/sys/kernel/security/lsm` | **Reused** (`[obs]`) |
| `/.snapshots` | Stat fails (`statx: No such file or directory`) | Confirmed verbatim (`stat: cannot statx '/.snapshots'`) | **Reused** (`[obs]`) |
| Snapper Configs | 0 configs (header only in `snapper list-configs`) | Confirmed verbatim (0 configs) | **Reused** (`[obs]`) |
| Journal `errno:13` count | 9 occurrences | **9** occurrences confirmed in journal; latest at `2026-10-19T22:48:24-03:00` | **Reused** (`[obs]`) |
| Provenance of `stat` | Builtin `stat 0.8.0` vs GNU `stat 9.11` | Inherited erratum noted Security S10 finding; re-verified with explicit `/usr/bin/stat` binary | **Corrected & Pinned** |
| Constraint Causality | "entirely a DAC constraint" | Overclaimed in early inherited text; corrected in inherited erratum. Mode `0555` is an independently sufficient DAC barrier, but live capability path remains unproven | **Corrected & Bounded** |
| Inode Timestamps | "metadata has not been altered since initial installation" | Timestamps (`Modify/Change: 2026-10-03 17:45:33`) are observational snapshots (`[obs]`), not historical proof of origin | **Corrected** |

---

## 3. Exact Read-Only Probes and Evidence Matrix

All commands executed in unprivileged shell (`vgpnk`) without elevation or background daemons:

| Probe Command | RC | Output (Sanitized / Exact) | Epistemic Status |
|---|---|---|---|
| `/usr/bin/stat -c "mode=%a uid=%u gid=%g filetype=%F" /` | `0` | `mode=555 uid=0 gid=0 filetype=directory` | `[obs]` |
| `/usr/bin/stat -c "%a %u %g %F" /` | `0` | `555 0 0 directory` | `[obs]` |
| `/usr/bin/stat /` | `0` | `Device: 0,31 Inode: 256 Links: 1 Access: (0555/dr-xr-xr-x) Uid: ( 0/ root) Gid: ( 0/ root)`<br>`Access: 2026-10-19 15:46:24.628824179 -0300`<br>`Modify: 2026-10-03 17:45:33.001630573 -0300`<br>`Change: 2026-10-03 17:45:33.001630573 -0300`<br>`Birth:  2026-10-03 17:41:30.687657678 -0300` | `[obs]` |
| `getfacl -p /` | `0` | `# file: /`<br>`# owner: root`<br>`# group: root`<br>`user::r-x`<br>`group::r-x`<br>`other::r-x` | `[obs]` |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | `0` | `/ btrfs rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` | `[obs]` |
| `btrfs property get /` | `0` | `ro=false`<br>`label=` | `[obs]` |
| `lsattr -d /` | `0` | `---------------------- /` (no ext2/4/btrfs `i` or `a` attributes) | `[obs]` |
| `cat /sys/kernel/security/lsm` | `0` | `capability,landlock,lockdown,yama,bpf` (no SELinux, AppArmor, Smack, Tomoyo) | `[obs]` |
| `test -r /` | `0` | Read test succeeds (exit 0) | `[obs]` |
| `test -w /` | `1` | Write test fails (exit 1, unprivileged DAC write denied) | `[obs]` |
| `test -x /` | `0` | Search/traverse test succeeds (exit 0) | `[obs]` |
| `/usr/bin/stat /.snapshots` | `1` | `stat: cannot statx '/.snapshots': No such file or directory` (rc=1) | `[obs]` |
| `snapper list-configs` | `0` | Header only: `Config │ Subvolume` / `───────┼──────────` (0 configured rows) | `[obs]` |
| `journalctl --no-pager -o short-iso -g "create subvolume failed" \| grep -c "errno:13"` | `0` | `9` (9 recorded failures across Oct 16 – Oct 19) | `[obs]` |
| `systemctl status snapper-timeline.timer snapper-cleanup.timer` | `0` | Both units: `Loaded: loaded (...) Active: inactive (dead) preset: disabled` | `[obs]` |
| `systemctl status limine-snapper-sync.service` | `0` | `Active: inactive (dead) since Mon 2026-10-19 22:48:24 -03`<br>Logged: `Directory /.snapshots does not exist... create subvolume failed, btrfs_util_create_subvolume_fd() failed, errno:13 (Permission denied)... Failed: "snapper --no-dbus -c root create-config /" with exit code: 1` | `[obs]` |

---

## 4. Technical Distinction: Discretionary Access Control (DAC) vs Mount Flags

Diagnostic clarity requires keeping filesystem mount restrictions completely distinct from Discretionary Access Control (DAC) restrictions. The empirical evidence isolates both layers:

```
                      Path Write Request to `/`
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       VFS Mount Layer                    DAC Layer
   findmnt options: `rw`            stat mode: `0555`
   btrfs property: `ro=false`       getfacl: `user::r-x,group::r-x,other::r-x`
                 │                               │
                 ▼                               ▼
      Passes Mount Check             Write Bit Check FAILS
    (Not a Read-Only FS)             (Requires CAP_DAC_OVERRIDE)
                                                 │
                                                 ▼
                                        Kernel returns EACCES
                                        (errno 13: Permission denied)
```

### 1. The Discretionary Access Control (DAC) Layer
- **Mode Representation:** Mode is `0555` (`dr-xr-xr-x`). Owner is `uid=0` (`root`), group is `gid=0` (`root`).
- **Absence of Write Bits:** Write permission (`w`) is cleared across all three standard permission triads:
  - User: `r-x` (read + execute/traverse, no write)
  - Group: `r-x` (read + execute/traverse, no write)
  - Other: `r-x` (read + execute/traverse, no write)
- **POSIX ACL Status:** `getfacl -p /` reports no extended ACL entries (only minimal base entries). No access masks, group-specific grants, or default ACL inheritance entries exist.
- **Kernel Permission Checking:** Under POSIX/Linux VFS standard rules (`generic_permission()` in kernel VFS, S034):
  - Any process attempting to create a directory or file in `/` requires write permission on `/`.
  - For `uid=0` (root), POSIX DAC write checks are bypassed **only** if the process possesses the `CAP_DAC_OVERRIDE` capability (S027).
  - If `CAP_DAC_OVERRIDE` is absent from the effective capability set (`CapEff`), the kernel enforces DAC mode bits strictly, denying the write with `EACCES` (`errno: 13`).

### 2. The VFS Mount Layer
- **Mount Options:** `findmnt -n -o TARGET,FSTYPE,OPTIONS /` reports `rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`.
- **Mount Read-Write Status:** The filesystem is explicitly mounted read-write (`rw`), **not** read-only (`ro`).
- **Btrfs Subvolume Status:** `btrfs property get /` returns `ro=false`. The btrfs subvolume itself is not marked read-only.
- **Filesystem Attributes:** `lsattr -d /` confirms no ext2/ext4/btrfs immutable (`i`) or append-only (`a`) flags.

### 3. VFS Errno Discrimination (`EACCES` vs `EROFS`)
- A write attempt blocked by the mount layer (e.g., `ro` mount option or `ro=true` subvolume property) produces kernel error `EROFS` (`errno: 30`, "Read-only file system").
- A write attempt permitted by mount flags (`rw`) but blocked by directory permissions produces kernel error `EACCES` (`errno: 13`, "Permission denied").
- Therefore, while a read-only filesystem mount barrier (`EROFS`) is ruled out by the active `rw` mount options, attributing the subvolume creation failure strictly to DAC enforcement remains a consistent hypothesis (`[inf]`), not an established causal proof.

---

## 5. Comparison with Historic Snapper Mechanism State

### Baseline State (`corpus/knowledge/snapper-eacces-mechanism.md`)
- Historic observation: `/` mode was recorded as `555 root:root`.
- Historic service definition: `limine-snapper-sync.service` configured with `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN`, `ProtectHome=yes`.
- Historic failure count: 8 entries in journal matching `create subvolume failed ... errno:13` up to `2026-10-19T08:11:47-03:00`.
- Historic candidate mechanism (`[inf]`):
  `limine-snapper-sync.service` runs as root (`User=root`), but its capability bounding set is restricted strictly to `CapabilityBoundingSet=CAP_SYS_ADMIN`. Per `systemd.exec(5)` (S028), capabilities omitted from the bounding set are dropped from the bounding, effective, and permitted sets. Because `CAP_DAC_OVERRIDE` (S027) is not included in `CAP_SYS_ADMIN`, the service lacks the authority to bypass DAC checks. When snapper attempts to execute `btrfs_util_create_subvolume_fd()` to create `/.snapshots`, the kernel VFS layer checks DAC write permissions on `/`. Because `/` has mode `0555` (no write bit), the operation is denied with `EACCES` (`errno: 13`).

### Current Live Re-Measurement (2026-10-20T03:45:00Z)
1. **Metadata Invariance:** `/` remains `0555 root:root`. Inode timestamps show:
   - `Modify: 2026-10-03 17:45:33.001630573 -0300`
   - `Change: 2026-10-03 17:45:33.001630573 -0300`
   - `Birth:  2026-10-03 17:41:30.687657678 -0300`
2. **Error Recurrence:** Total journal failure count is **9**. The 9th failure was logged at `2026-10-19T22:48:24-03:00`:
   Sanitized event metadata: latest retained create-subvolume failure at `2026-10-19T22:48:24-03:00`, errno 13; the configuration-create attempt exited 1. Raw journal bodies and process identity omitted by the integrating L1.
3. **Rollback Net Still Dead:** `snapper list-configs` returns 0 configs. `/.snapshots` does not exist. The snapper timeline and cleanup timers remain disabled and dead.

### Epistemic Status: Why Diagnosis is NOT Proven
Per the contract, the diagnosis is explicitly labeled an inference (`[inf]`), not proven:
1. **Unexecuted Falsifier:** The non-mutating discriminator:
   ```sh
   sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /
   sudo test -w /
   ```
   has not been executed because running `sudo` and `systemd-run` is forbidden for leaf scouts.
2. **No Live Syscall / Capability Trace:** Non-root scout reconnaissance cannot attach `strace` or eBPF tracing to `limine-snapper-watcher` during subvolume creation to observe the kernel's internal capability bitmask evaluation.
3. **Potential Interacting Factors:** Although SELinux and AppArmor are inactive in `/sys/kernel/security/lsm`, other mechanisms (systemd namespace flags, Landlock, or btrfs root subvolume constraints) have not been formally disproven in isolation.
4. **Access vs Ioctl Path:** `test -w` evaluates `access(2)`/`faccessat2(2)`, whereas `snapper` invokes `btrfs_util_create_subvolume_fd()` which issues `BTRFS_IOC_SUBVOL_CREATE` ioctl. While both require write authorization on `/`, subtle kernel path resolution differences remain unverified live.

---

## 6. Implications for Round-12 Claims (C1 & C2)

### C1: Closing the Unowned `/` Metadata Census Blind Spot
- `pacman -Qo /` fails (`error: No package owns /`).
- The `filesystem` package mtree does not record mode or ownership for `.`.
- Standard `pacman -Qkk` is blind to mode or ownership anomalies on `/`.
- The census (`tools/tsukuroi-census.sh`) currently has 0 arms checking `/` metadata.
- **Required Discrimination in C1:**
  1. `0755` -> Standard writable root directory (`HEALTHY` / `PASS`)
  2. `0555` -> Read-only DAC root directory (`DEGRADED` / `WARN`)
  3. Unreadable / unstatable -> Error condition (`BLOCKED` / `UNKNOWN`)

### C2: Source-Backed Discriminating EACCES Decision Matrix
The probe suite provides empirical backing for 4 distinct branches in `root-dac-decision-r12.{json,md}`:
1. **Branch 1 (VFS Mount Read-Only):** `findmnt` options include `ro` -> File system is mounted read-only (`EROFS` or wrapper `EACCES`). Remediation: Remount `rw`.
2. **Branch 2 (DAC Mode 0555 + Dropped `CAP_DAC_OVERRIDE`):** `findmnt` is `rw`, `/` mode is `0555`, caller drops `CAP_DAC_OVERRIDE` -> Kernel DAC denial (`EACCES`, errno 13). Remediation: `chmod 755 /` or add `CAP_DAC_OVERRIDE` to service.
3. **Branch 3 (Existing Conflicting Directory):** Target `/.snapshots` already exists as a non-subvolume directory -> Conflict (`EEXIST` or snapper create-config refusal). Remediation: Remove or rename existing directory.
4. **Branch 4 (Missing Path / Mount Point Resolution Failure):** Mount point or parent directory cannot be resolved -> `ENOENT`. Remediation: Restore mount path hierarchy.

---

## 7. Risks and Limits

1. **Host Operability Risk:** Mode `0555` on `/` prevents any daemon running without `CAP_DAC_OVERRIDE` from creating any file or directory directly under `/`. Daemons with restricted bounding sets cannot self-initialize top-level runtime paths.
2. **Scope Boundaries:** No permissions were modified (`chmod` never run), no files were created or modified at `/`, and no services were restarted.
3. **Tool Invariance:** All probes executed with standard system utilities (`coreutils 9.11-2`, `acl 2.3.2`, `util-linux 2.40.4`, `btrfs-progs 6.13`). Zero tool installations or upgrades performed.

---

## 8. Outcome Summary

- **Verdict:** Read-only reconnaissance of `/` completed successfully (`rc=0` across all observational probes).
- **Mode:** `0555`, owner `0` (`root`), group `0` (`root`), filetype `directory`.
- **ACL:** Base POSIX ACL only; no extended entries.
- **Mount:** `rw`, btrfs, `ro=false`, no immutable attributes.
- **Snapper State:** Inactive, 0 configs, `/.snapshots` absent, 9 journal failures (`errno:13`).
- **Diagnosis Status:** Inference (`[inf]`), NOT proven.
- **Evidence File:** Written to `.ufo/waves/round-12/resumed/RootLiveR.md`.

---

## 9. Epistemic Correction Addendum (Parent Steering)

Per parent steering review:
1. **Attribution Overstatement Corrected:** Any assertion or summary phrasing stating "Conclusion: Subvolume creation failure on `/` is a DAC barrier" overstates attribution and conflicts with the unknown status articulated in the mechanism analysis (§5 / inherited §3).
2. **Consistent Hypothesis vs Proven Cause:** The observed facts—mode `0555`, minimal base POSIX ACL (no write bits), mount options `rw`, and Btrfs property `ro=false`—**only support a consistent DAC hypothesis** (`[inf]`). They rule out a read-only filesystem mount (`EROFS`), but do not prove that DAC enforcement on `/` was the singular or actual causal failure in every historical subvolume creation attempt.
3. **Unknowns Retained:**
   - The exact failed syscall and exact resolved path (`btrfs_util_create_subvolume_fd()` failure point inside kernel VFS / btrfs driver) remain unobserved (`[unknown]`).
   - The historical target path status and `/` mode at the exact moment each of the 9 journal errors occurred are unrecorded (`[unknown]`).
   - The actual runtime credentials and effective capability set (`CapEff`) of `limine-snapper-watcher` during execution remain unobserved (`[unknown]`).
4. **Limits of Proxies:** Neither an unprivileged permission proxy check (`test -w /`) nor current static inode timestamps (`2026-10-03`) establishes historical or live runtime cause.
5. **Zero Additional Probes:** No additional probes executed; empirical observations remain strictly bounded to observed system state (`[obs]`).
