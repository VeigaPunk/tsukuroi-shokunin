# UnitLive — `limine-snapper-sync.service` Unit Properties, S020 Comparison, and Capability Analysis

Scope: Leaf scout read-only inspection. Paths relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. No service restart, no daemon mutation, no host changes. No `Environment`, `ExecStart`, or credentials recorded.

## 1. Load and Active State

Probed via `systemctl show limine-snapper-sync.service -p LoadState,ActiveState,SubState,UnitFileState,MainPID`:
- **LoadState**: `loaded`
- **ActiveState**: `inactive`
- **SubState**: `dead`
- **UnitFileState**: `enabled`
- **MainPID**: `0`

Command and exit status:
```sh
systemctl is-active limine-snapper-sync.service
# output: inactive
# rc: 3

systemctl is-enabled limine-snapper-sync.service
# output: enabled
# rc: 0
```
[obs] The service is enabled in systemd presets / symlinks (`/etc/systemd/system/multi-user.target.wants/limine-snapper-sync.service`), but is currently inactive (`dead`) with `MainPID=0`. No running process exists on the host.

## 2. Effective Unit Properties

Probed via `systemctl show limine-snapper-sync.service -p User,Group,CapabilityBoundingSet,AmbientCapabilities,ProtectSystem,ReadOnlyPaths,ReadWritePaths,ProtectHome,NoNewPrivileges` (rc=0):

| Property | Effective Value | Unit Declaration | Default / Fallback Behavior |
|---|---|---|---|
| `User` | `root` | `User=root` (line 6) | Runs as user `root` (UID 0) |
| `Group` | `""` (empty) | *(omitted)* | Resolves to primary group of user `root` (GID 0) |
| `CapabilityBoundingSet` | `cap_sys_admin` | `CapabilityBoundingSet=CAP_SYS_ADMIN` (line 13) | Allowlist: drops all capabilities except `CAP_SYS_ADMIN` |
| `AmbientCapabilities` | `""` (empty) | *(omitted)* | No ambient capabilities configured (`0x0`) |
| `ProtectSystem` | `no` | *(omitted)* | System directories (`/usr`, `/boot`, `/etc`) are not mounted read-only |
| `ReadOnlyPaths` | `""` (empty) | *(omitted)* | No path-level read-only isolation configured |
| `ReadWritePaths` | `/tmp` | `ReadWritePaths=/tmp` (line 23) | Grants read-write access to `/tmp` in private/sandboxed mount namespace |
| `ProtectHome` | `yes` | `ProtectHome=yes` (line 18) | `/home`, `/root`, `/run/user` are made inaccessible |
| `NoNewPrivileges` | `yes` | `NoNewPrivileges=yes` (line 29) | Sets `PR_SET_NO_NEW_PRIVS=1`; child processes cannot gain privileges via setuid/file-caps |

Unit fragment path: `/usr/lib/systemd/system/limine-snapper-sync.service`  
Drop-in paths: `DropInPaths=` (none present; `/etc/systemd/system/limine-snapper-sync.service.d/` does not exist).

## 3. Comparison with S020

- **Installed Unit**:
  - File: `/usr/lib/systemd/system/limine-snapper-sync.service`
  - Providing package: `limine-snapper-sync 1.31.0-1.1` (`pacman -Qo /usr/lib/systemd/system/limine-snapper-sync.service`, rc=0)
  - Mode / Owner: `644 root:root` (`stat -c '%a %U:%G %s %n'`, rc=0)
  - Size: `856 bytes`
  - SHA-256: `6fb0d3d4c39523f7caf53a6106b714f43621c7dde3f937b9262b9a7ff95e5829`

- **S020 Upstream Reference**:
  - Source: `https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service`
  - Pinned commit: `cd909745ad4ee136aaf4adca6d018e72df81c740` dated `2025-10-10`
  - Size: `856 bytes`
  - SHA-256: `6fb0d3d4c39523f7caf53a6106b714f43621c7dde3f937b9262b9a7ff95e5829`

- **Comparison Result**:
  - Diff: `diff -u /usr/lib/systemd/system/limine-snapper-sync.service <(upstream S020)` produces **zero differences** (byte-for-byte identical).
  - The installed unit contains the identical security hardening block as S020, including `CapabilityBoundingSet=CAP_SYS_ADMIN`, `ProtectHome=yes`, `ReadWritePaths=/tmp`, and `NoNewPrivileges=yes`.
  - No package-level or local administrator drop-ins have modified the unit configuration on this host.

## 4. Configuration vs. Running Process Capability Distinction

The capability semantics must be separated into static configuration directives and dynamic kernel process state:

### A. Static Configuration (Systemd Service Manager Level)
1. `CapabilityBoundingSet=CAP_SYS_ADMIN`:
   - Systemd documentation (`systemd.exec(5)` S028) establishes that `CapabilityBoundingSet=` acts as an allowlist when given without a `~` prefix.
   - Any capability not listed is removed from the process bounding set (`CapBnd`).
   - S028 explicitly specifies: *"Note that this option also affects the respective capabilities in the effective, permitted and inheritable capability sets."*
2. `AmbientCapabilities=`:
   - Unset, defaulting to empty. No ambient capabilities are added to the ambient capability set (`CapAmb`).
3. `NoNewPrivileges=yes`:
   - Enforces `prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)` before execution, prohibiting the process or descendants from acquiring capabilities across `execve` via setuid/setgid or extended attribute file capabilities.

### B. Dynamic Kernel Capability State (Process Level — [inf])
Linux kernel capabilities (`capabilities(7)` S027) govern process execution across five distinct sets. For a process launched under this configuration, the expected capability sets are inferred (`[inf]`) from documentation and systemd exec rules:
1. **Bounding Set (`CapBnd`)**: Inferred `[inf]` to retain strictly `CAP_SYS_ADMIN` (bit 21, `0x0000000000200000`). All other bits (including `CAP_DAC_OVERRIDE`, bit 1) are expected to be dropped.
2. **Permitted Set (`CapPrm`)**: Inferred `[inf]` to contain at most `CAP_SYS_ADMIN`, stripped by systemd to match the bounding set.
3. **Effective Set (`CapEff`)**: Inferred `[inf]` to contain at most `CAP_SYS_ADMIN`.
4. **Inheritable Set (`CapInh`)**: Inferred `[inf]` empty (`0x0`).
5. **Ambient Set (`CapAmb`)**: Inferred `[inf]` empty (`0x0`).

### C. The Access Check and DAC Bypass Consequence ([inf])
- Under standard unbounded root execution (`User=root` without `CapabilityBoundingSet`), root processes hold `CAP_DAC_OVERRIDE` in `CapEff` and `CapPrm`, allowing them to bypass filesystem DAC permissions (read/write/execute bits) per S027.
- For root processes, `access(2)` (S034) specifies that kernel permission checks use the **permitted** capability set (`CapPrm`), not effective capabilities.
- Because `CapabilityBoundingSet=CAP_SYS_ADMIN` drops `CAP_DAC_OVERRIDE` from both `CapBnd` and `CapPrm`, a running `limine-snapper-sync` process is expected (`[inf]`) to possess **no DAC bypass capability**.
- When accessing a directory whose DAC mode bits disallow write access for user/group/other (e.g. `/` at mode `0555` `r-xr-xr-x`), write operations (such as creating `/.snapshots`) would encounter kernel `EACCES` (errno 13). This is an explanatory candidate mechanism (`[inf]`), not a proven syscall trace.

### D. Observability Constraint on Current Host
- [obs] The service is currently inactive (`ActiveState=inactive`, `SubState=dead`, `MainPID=0`).
- [obs] No live PID exists in `/proc` for this unit.
- [unk] Actual dynamic kernel capability sets (`CapInh`, `CapPrm`, `CapEff`, `CapBnd`, `CapAmb`) and runtime syscall execution remain unknown on this host.
- Direct observation of running process capabilities would require launching or restarting the service, which is strictly prohibited under lane rules. No service restart or elevated falsifier probe was run.
## 5. Identified Risks and Operability Impact

1. **Rollback Net Inoperability (Host Exposure)**:
   - `limine-snapper-sync.service` is enabled but dead.
   - Together with `snapper list-configs` reporting 0 configurations, no automated snapshot synchronization or Limine boot menu rollback net is operational on this host.
2. **EACCES Creation Barrier (`0555` Root vs Dropped DAC Bypass — [inf])**:
   - Root filesystem mode `0555` combined with `CapabilityBoundingSet=CAP_SYS_ADMIN` indicates an expected candidate mechanism (`[inf]`) where attempts by `limine-snapper-sync` to create subvolumes or directories under `/` fail with `EACCES` (errno 13).
   - This candidate mechanism is consistent with historical journal entries (`errno:13 create subvolume failed`), though host cause remains unproven without dynamic syscall tracing.
3. **Sandbox Confinement Boundaries**:
   - `ProtectHome=yes` isolates `/home`, `/root`, and `/run/user`.
   - `ReadWritePaths=/tmp` provides isolated temporary storage.
   - `ProtectSystem=no` allows read-write access to system directories (provided DAC and other bounding capabilities permit it).
   - `NoNewPrivileges=yes` prevents helper binaries from regaining dropped capabilities.

## 6. Sources and Evidence

- **S020 (tier A)**: `https://gitlab.com/Zesko/limine-snapper-sync/-/raw/master/install/arch-linux/usr/lib/systemd/system/limine-snapper-sync.service` (commit `cd909745ad4ee136aaf4adca6d018e72df81c740`).
- **S027 (tier A)**: `capabilities(7)` — `CAP_DAC_OVERRIDE` bypasses file read, write, and execute permission checks; capability sets definition.
- **S028 (tier A)**: `systemd.exec(5)` — `CapabilityBoundingSet=` allowlist semantics and drop propagation to effective, permitted, and inheritable sets.
- **S034 (tier A)**: `access(2)` — root user permission check dependency on permitted capability set (`CapPrm`).
- **Host Evidence (read-only, non-mutating)**:
  - `systemctl show limine-snapper-sync.service -p User,Group,CapabilityBoundingSet,AmbientCapabilities,ProtectSystem,ReadOnlyPaths,ReadWritePaths,ProtectHome,NoNewPrivileges,LoadState,ActiveState,SubState,UnitFileState,FragmentPath,DropInPaths,MainPID`
  - `systemctl is-active limine-snapper-sync.service` (rc=3)
  - `systemctl is-enabled limine-snapper-sync.service` (rc=0)
  - `sha256sum /usr/lib/systemd/system/limine-snapper-sync.service` (`6fb0d3d4c39523f7caf53a6106b714f43621c7dde3f937b9262b9a7ff95e5829`)
  - `pacman -Qo /usr/lib/systemd/system/limine-snapper-sync.service` (`limine-snapper-sync 1.31.0-1.1`, rc=0)

## 7. Erratum and Verification Boundary

- **Runtime Process Capabilities Not Measured**: The runtime capability sets (`CapBnd`, `CapPrm`, `CapEff`, `CapInh`, `CapAmb`) described in §4 are expected inferences (`[inf]`) derived from systemd documentation (`systemd.exec(5)` S028) and kernel capability specifications (`capabilities(7)` S027). Because `limine-snapper-sync.service` is inactive (`MainPID=0`), no live kernel task credentials exist to read from `/proc/<PID>/status`. Actual runtime process capability and syscall behavior remain unknown (`[unk]`).
- **Effective Systemd Configuration Observed**: The effective systemd unit properties in §2 (`User=root`, `CapabilityBoundingSet=cap_sys_admin`, `ProtectHome=yes`, `ReadWritePaths=/tmp`, `NoNewPrivileges=yes`, `LoadState=loaded`, `ActiveState=inactive`, `SubState=dead`) are observed facts (`[obs]`) measured directly via `systemctl show` and verified against the unit file on disk.
- **No Host EACCES Cause Proven**: The explanation linking root directory mode `0555` and dropped `CAP_DAC_OVERRIDE` to the observed `errno:13` journal messages is a candidate explanatory mechanism (`[inf]`). It is not proven by host runtime tracing or strace execution. Other potential factors (such as mount namespaces, Btrfs-specific constraints, or LSM policies) were not evaluated dynamically.
- **Non-Mutating Lane Boundary**: In strict accordance with the read-only lane contract, no service start/restart, systemd drop-in, or elevated falsifier command (`sudo systemd-run`) was executed.
