# UnitLiveR — `limine-snapper-sync.service` Unit Properties, S020 Comparison, and Capability Analysis

**Axes**: `operability`, `depth`  
**Seat**: `TsukuroiR12.UnitLiveR` (leaf scout)  
**Timestamp**: 2026-10-20  
**Scope**: Read-only host inspection and upstream S020 comparison. Paths relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.  
**Safety & Contract**: No service restart, no daemon mutation, no host writes. Strictly no `Environment`, `ExecStart`, or credentials recorded.

---

## 1. Resumed Round Re-check of Inherited Evidence

- **Inherited Artifact**: `.ufo/waves/round-12/UnitLive.md` (inherited from initial wave).
- **Re-check Status**: Re-evaluated and verified against live host state and current upstream git sources on 2026-10-20.
- **Reused**:
  - Load and active states (`LoadState=loaded`, `ActiveState=inactive`, `SubState=dead`, `UnitFileState=enabled`).
  - The 9 effective unit property measurements (`User`, `Group`, `CapabilityBoundingSet`, `AmbientCapabilities`, `ProtectSystem`, `ReadOnlyPaths`, `ReadWritePaths`, `ProtectHome`, `NoNewPrivileges`).
  - Package identity (`limine-snapper-sync 1.31.0-1.1`) and unit file SHA-256 digest (`6fb0d3d4c39523f7caf53a6106b714f43621c7dde3f937b9262b9a7ff95e5829`).
  - Core distinction between static systemd unit configuration and dynamic kernel process capabilities.
- **Rejected / Corrected**:
  - *Upstream URL Reproducibility*: Inherited UnitLive cited only the mutable master raw URL for S020. As documented in SourceReview (F3), GitLab raw URLs using commit hashes (`/-/raw/<commit>/...`) return HTTP 403 or Cloudflare challenge pages. Corrected to record and verify both the master raw URL and the durable GitLab API raw ref URL (`.../repository/files/.../raw?ref=cd909745ad4ee136aaf4adca6d018e72df81c740`), which returns HTTP 200 and matches the installed unit byte-for-byte.
  - *Negative Constraint Rigor*: Fully sanitized all command records and tables to ensure strictly no `Environment`, `ExecStart`, or credentials appear in this report.
  - *Package-to-Commit Mapping*: Audited pacman local database (`/var/lib/pacman/local/limine-snapper-sync-1.31.0-1.1/desc`), confirming package version `1.31.0-1.1`, build date `2026-09-05`. The installed unit file is confirmed byte-identical to upstream commit `cd909745ad4ee136aaf4adca6d018e72df81c740` (dated `2025-10-10`) and master.

---

## 2. Load and Active State

Live measurement via `systemctl show limine-snapper-sync.service -p Id,Names,LoadState,ActiveState,SubState,UnitFileState,UnitFilePreset,MainPID`:

| Property | Measured Value | Meaning |
|---|---|---|
| `Id` | `limine-snapper-sync.service` | Primary unit name |
| `LoadState` | `loaded` | Unit configuration file is loaded by systemd |
| `ActiveState` | `inactive` | Service is not currently active |
| `SubState` | `dead` | Service process is terminated / not running |
| `UnitFileState` | `enabled` | Enabled in systemd presets / target symlinks |
| `UnitFilePreset` | `disabled` | Distribution default preset was disabled |
| `MainPID` | `0` | No running process exists |

Live CLI execution check:
```sh
systemctl is-active limine-snapper-sync.service
# output: inactive
# exit code: 3

systemctl is-enabled limine-snapper-sync.service
# output: enabled
# exit code: 0
```
[obs] The service unit is `enabled` on this host, but its current execution state is `inactive` (`dead`) with `MainPID=0`.

---

## 3. Effective Unit Properties

Live measurement via `systemctl show limine-snapper-sync.service -p User,Group,CapabilityBoundingSet,AmbientCapabilities,ProtectSystem,ReadOnlyPaths,ReadWritePaths,ProtectHome,NoNewPrivileges` (exit code 0):

| Property | Effective Value | Unit Declaration | Effective Behavior / Semantics |
|---|---|---|---|
| `User` | `root` | `User=root` | Service process runs as UID 0 (`root`) |
| `Group` | `""` (empty) | *(omitted)* | Defaults to primary group of user `root` (GID 0) |
| `CapabilityBoundingSet` | `cap_sys_admin` | `CapabilityBoundingSet=CAP_SYS_ADMIN` | Allowlist: restricts capability bounding set strictly to `CAP_SYS_ADMIN`; drops all other capabilities |
| `AmbientCapabilities` | `""` (empty) | *(omitted)* | No ambient capabilities configured (`0x0`) |
| `ProtectSystem` | `no` | *(omitted)* | System directories (`/usr`, `/boot`, `/etc`) are not mounted read-only by systemd |
| `ReadOnlyPaths` | `""` (empty) | *(omitted)* | No path-level read-only mount sandboxing applied |
| `ReadWritePaths` | `/tmp` | `ReadWritePaths=/tmp` | Grants read-write access to `/tmp` |
| `ProtectHome` | `yes` | `ProtectHome=yes` | Inaccessible sandbox: `/home`, `/root`, `/run/user` are made inaccessible |
| `NoNewPrivileges` | `yes` | `NoNewPrivileges=yes` | Sets `PR_SET_NO_NEW_PRIVS=1`; prevents gaining capabilities via setuid/file-caps across `execve` |

Host unit fragment location:
- `FragmentPath`: `/usr/lib/systemd/system/limine-snapper-sync.service`
- `DropInPaths`: *(none; `/etc/systemd/system/limine-snapper-sync.service.d/` does not exist)*

---

## 4. Comparison with S020

### A. Installed Unit Artifact
- Path: `/usr/lib/systemd/system/limine-snapper-sync.service`
- Package: `limine-snapper-sync 1.31.0-1.1` (`pacman -Qo /usr/lib/systemd/system/limine-snapper-sync.service`)
- Permissions: `644 -rw-r--r-- root:root`
- File Size: `856 bytes`
- SHA-256 Digest: `6fb0d3d4c39523f7caf53a6106b714f43621c7dde3f937b9262b9a7ff95e5829`

### B. Upstream S020 Reference
- Source: `https://gitlab.com/Zesko/limine-snapper-sync`
- Pinned commit: `cd909745ad4ee136aaf4adca6d018e72df81c740` dated `2025-10-10`
- URLs verified:
  - Master raw: `https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service` (SHA-256: `6fb0d3d4...`)
  - Commit-pinned API raw: `https://gitlab.com/api/v4/projects/Zesko%2Flimine-snapper-sync/repository/files/install%2Farch-linux%2Fusr%2Flib%2Fsystemd%2Fsystem%2Flimine-snapper-sync.service/raw?ref=cd909745ad4ee136aaf4adca6d018e72df81c740` (SHA-256: `6fb0d3d4...`)
- Size: `856 bytes`
- SHA-256 Digest: `6fb0d3d4c39523f7caf53a6106b714f43621c7dde3f937b9262b9a7ff95e5829`

### C. Comparison Outcome
- Direct diff:
  ```sh
  diff -u /usr/lib/systemd/system/limine-snapper-sync.service <(curl -sS https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service)
  # exit code: 0 (zero differences, byte-for-byte identical)
  ```
- The installed unit on the host is byte-identical to both S020 at pinned commit `cd909745` and upstream `master`.
- The installed security hardening block is identical to S020:
  `CapabilityBoundingSet=CAP_SYS_ADMIN`, `ProtectHome=yes`, `ReadWritePaths=/tmp`, `NoNewPrivileges=yes`.
- No local administrative drop-ins or vendor overrides are present.

---

## 5. Configuration vs. Running Process Capability Distinction

A critical depth requirement is separating static unit configuration from dynamic kernel process credentials:

### A. Static Unit Configuration (Systemd Service Manager Layer)
1. **Directive Parsing**:
   - Systemd parses the declarative unit directives (`CapabilityBoundingSet=CAP_SYS_ADMIN`, `NoNewPrivileges=yes`, `AmbientCapabilities=`).
   - The bounding set directive acts as an allowlist (`systemd.exec(5)` S028): any capability not listed is dropped.
   - S028 explicitly establishes: *"Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets."*
2. **Configuration vs Execution Separation**:
   - The configuration properties stored in systemd memory (`systemctl show`) represent **intent and configuration constraints**.
   - Systemd applies these constraints during process spawn in `src/core/execute.c` via `prctl(PR_CAPBSET_DROP, ...)` and `cap_set_proc()`.

### B. Dynamic Kernel Capability State (Kernel Process Credential Layer — [inf])
Kernel capabilities (`capabilities(7)` S027) exist in the task's `struct cred` in kernel space across five 64-bit bitmasks (`CapInh`, `CapPrm`, `CapEff`, `CapBnd`, `CapAmb`), readable via `/proc/<PID>/status`:
1. **Bounding Set (`CapBnd`)** (`[inf]`):
   - Expected to retain exclusively bit 21 (`CAP_SYS_ADMIN`, `0x0000000000200000`).
   - All other capability bits—critically including `CAP_DAC_OVERRIDE` (bit 1, `0x0000000000000002`) and `CAP_DAC_READ_SEARCH` (bit 2, `0x0000000000000004`)—are expected to be dropped.
2. **Permitted Set (`CapPrm`)** (`[inf]`):
   - Expected to be masked by the bounding set to contain at most `CAP_SYS_ADMIN`.
3. **Effective Set (`CapEff`)** (`[inf]`):
   - Expected to contain at most `CAP_SYS_ADMIN`.
4. **Inheritable Set (`CapInh`)** (`[inf]`):
   - Expected to be empty (`0x0`).
5. **Ambient Set (`CapAmb`)** (`[inf]`):
   - Expected to be empty (`0x0`).

### C. The Access Check and DAC Bypass Consequence (`[inf]`)
1. **Unbounded Root vs Bounded Root**:
   - An unbounded root process (UID 0) possesses `CAP_DAC_OVERRIDE` in `CapEff` and `CapPrm`, allowing it to bypass standard filesystem DAC permission checks (read, write, execute mode bits) per S027.
   - For processes with UID 0, `access(2)` (S034) specifies that kernel permission checks use the **permitted** capability set (`CapPrm`), not effective capabilities.
2. **Absence of DAC Bypass**:
   - Because `CapabilityBoundingSet=CAP_SYS_ADMIN` strips `CAP_DAC_OVERRIDE` from `CapBnd` and `CapPrm`, a running `limine-snapper-sync` process possesses **no DAC bypass capability**.
   - Kernel VFS permission checks (`fs/namei.c:generic_permission()`) enforce DAC mode bits directly against the process UID/GID without bypass.
   - If `/` is mode `0555` (`r-xr-xr-x`), write operations (such as creating subvolumes or directories under `/`) return `EACCES` (errno 13).
   - This represents an explanatory candidate mechanism (`[inf]`), consistent with kernel semantics and historical journal errors, but is not a proven dynamic trace on this host.

### D. Observability Constraint on Current Host
- [obs] The service is currently inactive (`ActiveState=inactive`, `SubState=dead`, `MainPID=0`).
- [obs] No task exists in `/proc` for this unit.
- [unk] Dynamic kernel capability bitmasks (`CapInh`, `CapPrm`, `CapEff`, `CapBnd`, `CapAmb`) cannot be observed on this host without starting the service.
- [obs] In accordance with read-only lane constraints, no service start, restart, or elevated falsifier command (`sudo systemd-run`) was executed.

---

## 6. Operability Findings and Risks

1. **Rollback Net Inoperability (Host Exposure)**:
   - `limine-snapper-sync.service` is enabled in target symlinks but dead in memory.
   - Combined with `snapper list-configs` showing 0 configurations on the host, no automatic snapshot synchronization or Limine rollback net is operational.
2. **EACCES Creation Barrier (`0555` Root vs Dropped DAC Bypass — [inf])**:
   - Root filesystem mode `0555` coupled with `CapabilityBoundingSet=CAP_SYS_ADMIN` creates a barrier where attempts by the service to create `/.snapshots` or restore boot entries under `/` fail with `EACCES` (errno 13).
   - This explains the recurring historical journal entries (`errno:13 create subvolume failed`) without requiring speculative root-cause assertions.
3. **Sandbox Scope Verification**:
   - `ProtectHome=yes` isolates user home directories (`/home`, `/root`, `/run/user`).
   - `ReadWritePaths=/tmp` provides an explicit writeable directory for temporary files.
   - `ProtectSystem=no` does not place systemd-level mount restrictions on `/usr` or `/boot`.
   - `NoNewPrivileges=yes` prevents helper binaries from regaining dropped capabilities.

---

## 7. Sources and Primary Citations

- **S020 (tier A)**: `https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service` (commit `cd909745ad4ee136aaf4adca6d018e72df81c740`, SHA-256 `6fb0d3d4...`). Upstream unit hardening definition.
- **S027 (tier A)**: `capabilities(7)` (`https://man.archlinux.org/man/capabilities.7`). Defines `CAP_SYS_ADMIN`, `CAP_DAC_OVERRIDE` ("Bypass file read, write, and execute permission checks"), and capability sets.
- **S028 (tier A)**: `systemd.exec(5)` (`https://man.archlinux.org/man/systemd.exec.5`). Documents `CapabilityBoundingSet=` allowlist semantics and drop propagation to effective, permitted, and inheritable sets.
- **S034 (tier A)**: `access(2)` (`https://man.archlinux.org/man/access.2`). Documents that for root user checks, permitted capabilities determine access.

---

## 8. Epistemic Boundaries and Gaps

- **[obs] Directly Observed Facts**:
  - `LoadState=loaded`, `ActiveState=inactive`, `SubState=dead`, `UnitFileState=enabled`, `MainPID=0`.
  - Effective properties: `User=root`, `Group=""`, `CapabilityBoundingSet=cap_sys_admin`, `AmbientCapabilities=""`, `ProtectSystem=no`, `ReadOnlyPaths=""`, `ReadWritePaths=/tmp`, `ProtectHome=yes`, `NoNewPrivileges=yes`.
  - Installed unit file SHA-256 (`6fb0d3d4...`) is byte-identical to upstream S020 at master and commit `cd909745`.
  - Negative constraint compliance: no `Environment`, `ExecStart`, or credentials logged.
- **[inf] Grounded Inferences**:
  - The service configuration drops `CAP_DAC_OVERRIDE` from the bounding set and permitted set.
  - A running process under this configuration would be unable to bypass DAC mode `0555` on `/`, resulting in `EACCES` on write/mkdir/ioctl operations.
- **[unk] Unresolved Gaps / Unmeasured State**:
  - Live process capability bitmasks (`CapBnd`, `CapPrm`, `CapEff`, etc.) and runtime syscall execution are unmeasured because the unit is inactive (`MainPID=0`) and service restarts or privileged probes are forbidden.
  - No single host cause for historical `errno:13` is claimed as proven fact; multiple interacting branches (DAC mode bits, mount flags, LSM policies) remain subject to matrix discrimination.
