# Capabilities and Access Semantics Audit (S027 vs S034) — Resumed Round 12

**Seat ID**: `TsukuroiR12.CapabilitiesR`  
**Role**: `scout` (leaf member; resumed wave)  
**Milestone**: `round-12`  
**Judged on**: `operability`, `depth`  
**Target Sources**: S027 (`capabilities(7)`), S034 (`access(2)`)  
**Audit Target**: `corpus/knowledge/snapper-eacces-mechanism.md` § Falsifier and capability/DAC claims  
**Contract & Provenance**: Author-side seat evidence only; not independent non-author verification. Read-only domain and source probes; no `sudo`, no package installations/upgrades, no systemd-run, no service restarts, and no check/test execution. All paths relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

---

## 1. Axes

1. **Operability**: Provide source-grounded, non-privileged diagnostic rules to evaluate directory write access and permission denials without requiring `sudo`, without executing live mutating commands, and accounting for the runtime divergence between binary execution (`/usr/bin/test`) and shell builtins (`test`).
2. **Depth**: Map the exact kernel VFS permission check flow (`inode_permission`), capability bounding set filtering during `execve(2)`, thread capability set transitions (Permitted vs Effective vs Bounding), real vs effective UID/GID credential checking in `access(2)` vs `open(2)`/`mkdir(2)`, and identify exact contradictions in prior falsifier language.

---

## 2. Primary Source Evidence and Verbatim Anchors

### 2.1 S027 — `capabilities(7)`
- **Source Identity**: `https://man.archlinux.org/man/capabilities.7` (Linux man-pages 6.19, dated 2026-02-08).
- **`CAP_DAC_OVERRIDE`**:
  > *"Bypass file read, write, and execute permission checks. (DAC is an abbreviation of "discretionary access control".)"*
- **`CAP_DAC_READ_SEARCH`**:
  > *"• Bypass file read permission checks and directory read and execute permission checks;*  
  > *• invoke open_by_handle_at(2);*  
  > *• use the linkat(2) AT_EMPTY_PATH flag to create a link to a file referred to by a file descriptor."*
- **Effective capability set (`CapEff`)**:
  > *"This is the set of capabilities used by the kernel to perform permission checks for the thread."*
- **Permitted capability set (`CapPrm`)**:
  > *"This is a limiting superset for the effective capabilities that the thread may assume. It is also a limiting superset for the capabilities that may be added to the inheritable set by a thread that does not have the CAP_SETPCAP capability in its effective set."*
- **Capability bounding set (`CapBnd`)**:
  > *"The capability bounding set is a mechanism that can be used to limit the capabilities that are gained during execve(2). ... From Linux 2.6.25, the capability bounding set is a per-thread attribute."*
- **Transformation during `execve(2)` for root (`UID 0`)**:
  > *"Thus, when a process with nonzero UIDs execve(2)s a set-user-ID-root program that does not have capabilities attached, or when a process whose real and effective UIDs are zero execve(2)s a program, the calculation of the process's new permitted capabilities simplifies to:*  
  > *`P'(permitted) = P(inheritable) | P(bounding)`*  
  > *`P'(effective) = P'(permitted)`*  
  > *Consequently, the process gains all capabilities in its permitted and effective capability sets, except those masked out by the capability bounding set."*
- **Effect of UID changes**:
  > *"If the filesystem user ID is changed from 0 to nonzero (see setfsuid(2)), then the following capabilities are cleared from the effective set: CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_DAC_READ_SEARCH, CAP_FOWNER, CAP_FSETID, CAP_LINUX_IMMUTABLE (since Linux 2.6.30), CAP_MAC_OVERRIDE, and CAP_MKNOD (since Linux 2.6.30)."*  
  > *"If one or more of the real, effective, or saved set user IDs was previously 0, and as a result of the UID changes all of these IDs have a nonzero value, then all capabilities are cleared from the permitted, effective, and ambient capability sets."*  
  > *"If the effective user ID is changed from 0 to nonzero, then all capabilities are cleared from the effective set."*  
  > *"If the effective user ID is changed from nonzero to 0, then the permitted set is copied to the effective set."*
- **Bounding set reduction**:
  > *"A thread may remove capabilities from its capability bounding set using the prctl(2) PR_CAPBSET_DROP operation, provided it has the CAP_SETPCAP capability. Once a capability has been dropped from the bounding set, it cannot be restored to that set."*

### 2.2 S034 — `access(2)`
- **Source Identity**: `https://man.archlinux.org/man/access.2` (Linux man-pages 6.19, dated 2026-02-08).
- **Credential checking rule (Real vs Effective UID; Permitted vs Effective Capabilities)**:
  > *"The check is done using the calling process's real UID and GID, rather than the effective IDs as is done when actually attempting an operation (e.g., open(2)) on the file. Similarly, for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities; and for non-root users, the check uses an empty set of capabilities."*
- **Design intent / Oracle warning**:
  > *"This allows set-user-ID programs and capability-endowed programs to easily determine the invoking user's authority. In other words, access() does not answer the "can I read/write/execute this file?" question. It answers a slightly different question: "(assuming I'm a setuid binary) can the user who invoked me read/write/execute this file?", which gives set-user-ID programs the possibility to prevent malicious users from causing them to read files which users shouldn't be able to read."*
- **Directory path prefix search requirement**:
  > *"A file is accessible only if the permissions on each of the directories in the path prefix of path grant search (i.e., execute) access. If any directory is inaccessible, then the access() call fails, regardless of the permissions on the file itself."*
- **Directory writability caveat**:
  > *"Only access bits are checked, not the file type or contents. Therefore, if a directory is found to be writable, it probably means that files can be created in the directory, and not that the directory can be written as a file."*
- **Error constants returned**:
  - `EACCES`: *"The requested access would be denied to the file, or search permission is denied for one of the directories in the path prefix of path."*
  - `EROFS`: *"Write permission was requested for a file on a read-only filesystem."*
  - `EPERM`: *"Write permission was requested to a file that has the immutable flag set."*
- **`faccessat()` and `AT_EACCESS`**:
  > *"AT_EACCESS: Perform access checks using the effective user and group IDs. By default, faccessat() uses the real IDs (like access())."*

---

## 3. Comparative Inspection

### 3.1 `CAP_DAC_OVERRIDE` vs `CAP_DAC_READ_SEARCH`
| Dimension | `CAP_DAC_OVERRIDE` | `CAP_DAC_READ_SEARCH` |
|---|---|---|
| **File read (`r`)** | Bypassed | Bypassed |
| **File write (`w`)** | Bypassed | **Enforced (Not bypassed)** |
| **File execute (`x`)** | Bypassed | **Enforced (Not bypassed)** |
| **Directory read (`r` / `getdents`)** | Bypassed | Bypassed |
| **Directory search (`x` / traversal)** | Bypassed | Bypassed |
| **Directory modify (`w` / create / unlink / rename)** | Bypassed | **Enforced (Not bypassed)** |
| **Additional privileges** | None | `open_by_handle_at(2)`, `linkat(2)` `AT_EMPTY_PATH` |

**Application to `/` mode `0555`**:
- On this host, `/` is mode `0555` (`dr-xr-xr-x`, `root:root`).
- Traversing `/` requires directory search (`x`), which is granted to all identities by mode bit `0005` (and group `0050`, owner `0500`). Neither capability is needed for directory traversal or reading directory contents.
- Creating an entry in `/` (such as `/.snapshots` or subvolume creation) requires directory write permission (`w`, `MAY_WRITE`) on `/`.
- Mode `0555` has no write bit for owner, group, or others.
- `CAP_DAC_READ_SEARCH` does **not** bypass directory write checks. Even if possessed, it cannot permit directory modifications or file creation.
- Only `CAP_DAC_OVERRIDE` allows a process to bypass the missing write permission on a mode `0555` directory.
- Consequently, dropping `CAP_DAC_OVERRIDE` while retaining `CAP_DAC_READ_SEARCH` or `CAP_SYS_ADMIN` leaves the process bound by DAC mode bits.

### 3.2 Real vs Effective UID and Permitted vs Effective Capabilities
Linux distinguishes between normal filesystem operations (`open`, `mkdir`, `ioctl`) and access probes (`access`, `faccessat`):

```
Operational Syscall (e.g., mkdir, open, ioctl)
  ├── Credentials used: fsuid / fsgid (normally equals effective UID/GID)
  └── Capability set used: P(effective)
       ├── DAC granted by mode/ACL? ── Yes ──> ALLOW
       └── DAC denied?
            ├── Requires write/execute/read -> Check CAP_DAC_OVERRIDE in P(effective)
            └── Requires read/search        -> Check CAP_DAC_READ_SEARCH in P(effective)

Permission Query Syscall (access)
  ├── Credentials used: Real UID / Real GID (ruid / rgid)
  └── Capability set used:
       ├── If ruid == 0 (root): P(permitted)
       └── If ruid != 0 (non-root): EMPTY SET (regardless of thread capabilities!)
```

**Key Asymmetries**:
1. **Root process with dropped effective capabilities**:
   If a root process has `CAP_DAC_OVERRIDE` in `P(permitted)` but clears it from `P(effective)`:
   - `access("/", W_OK)` returns `0` (SUCCESS) because `access()` looks at `P(permitted)`.
   - Real operations (`open("/", O_RDWR)`, `mkdir("/.snapshots", ...)`) fail with `EACCES` because the kernel looks at `P(effective)`.
2. **Unprivileged process with granted capabilities (e.g. ambient or file caps)**:
   If an unprivileged process (`ruid=1000`) has `CAP_DAC_OVERRIDE` in `P(effective)`:
   - `access("/", W_OK)` returns `-1 EACCES` because for `ruid != 0`, `access()` substitutes an empty capability set.
   - Real write operations succeed.
3. **`access(2)` is fundamentally unsuited as an operational oracle**:
   As S034 explicitly warns, `access(2)` answers whether the *invoking user* has access, not whether the *running process* has effective permission.

---

## 4. Audit of Old `test -w` Falsifier Language

The falsifier in `corpus/knowledge/snapper-eacces-mechanism.md` § Falsifier reads:
```sh
sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /; echo rc=$?  # predicted rc=1
sudo test -w /; echo rc=$?  # predicted rc=0

The first returning 0 falsifies the proposed DAC/capability mechanism. access(2) (S034) explains why this test -w comparison distinguishes root's permitted capabilities from its effective capabilities; it is a permission probe, not a subvolume-create test.
```

### 4.1 Exact Mismatches and Contradictions

#### Mismatch 1: False Claim that `test -w` Distinguishes Permitted from Effective Capabilities
- **Old claim**: *"access(2) (S034) explains why this test -w comparison distinguishes root's permitted capabilities from its effective capabilities"*.
- **Kernel reality (S027 & S034)**:
  - In `sudo systemd-run -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /`:
    The process runs as `UID 0`. Under `execve(2)` for root:
    `P'(permitted) = P(inheritable) | P(bounding)`
    `P'(effective) = P'(permitted)`
    Since `P(bounding) = {CAP_SYS_ADMIN}` (and inheritable is empty), `CAP_DAC_OVERRIDE` is absent from **both** `P(permitted)` and `P(effective)`. Both sets are `{CAP_SYS_ADMIN}`.
  - In `sudo test -w /`:
    `CAP_DAC_OVERRIDE` is present in **both** `P(permitted)` and `P(effective)`. Both sets are full.
  - In neither command do permitted and effective capabilities differ within the process. Both commands have `P(permitted) == P(effective)`.
  - The comparison distinguishes a **capability-bounded root process** from an **unbounded root process**. It changes the entire credential envelope. It does **not** distinguish permitted capabilities from effective capabilities within a single process.
  - Furthermore, `access(2)` *only* inspects `P(permitted)` for root. It cannot detect whether a capability is cleared from `P(effective)` if it remains in `P(permitted)`.

#### Mismatch 2: Coreutils Binary vs Shell Builtin Syscall Divergence
- Executing `/usr/bin/test -w /` executes GNU coreutils:
  - Probed fact (strace): `/usr/bin/test -w /` calls `access("/", W_OK)`.
  - `access(2)` uses Real UID (`ruid`) and `P(permitted)`.
- Executing `test -w /` within a shell (e.g. `bash -c 'test -w /'`):
  - Probed fact (strace): Bash builtin `test` calls `faccessat2(AT_FDCWD, "/", W_OK, AT_EACCESS)`.
  - `AT_EACCESS` forces the check to use Effective UID (`euid`) rather than Real UID (`ruid`).
- When `ruid != euid` (such as under setuid wrappers, ambient capabilities, or daemons changing credentials), `/usr/bin/test` and shell builtin `test` can yield conflicting results.

#### Mismatch 3: Erasure of Diagnostic Error Classes (Exit Code rc=1 vs Kernel Errno)
- `test -w /` yields a binary exit status: `0` (true) or `1` (false).
- An exit code of `1` collapses multiple distinct kernel conditions:
  1. `EACCES` (13): Parent directory lacks write permission, or path-prefix directory lacks search permission, and bypass capability is absent.
  2. `EROFS` (30): Mount superblock or namespace is mounted read-only (`MS_RDONLY`).
  3. `EPERM` (1): Inode has the immutable flag set (`FS_IMMUTABLE_FL`).
- `access(2)` sets specific `errno` values. The falsifier shell snippet `test -w /; echo rc=$?` discards the `errno` distinction, masking whether a denial was caused by DAC mode bits or a read-only filesystem mount.

#### Mismatch 4: Permission Probe vs Subvolume Creation Mechanics
- `limine-snapper-sync.service` failed with `errno:13` (`EACCES`) during Btrfs subvolume creation (`btrfs subvolume create` / `BTRFS_IOC_SUBVOL_CREATE`).
- A Btrfs subvolume create operation requires:
  1. Directory write and search permission on the parent directory (`MAY_WRITE | MAY_EXEC` in kernel VFS) -> requires `CAP_DAC_OVERRIDE` when parent is mode `0555`.
  2. Btrfs ioctl privilege -> requires `CAP_SYS_ADMIN` in the caller's user namespace.
  3. Writable filesystem mount (not read-only).
  4. Absence of target collision (not existing).
  5. LSM (SELinux/AppArmor) allowance.
- `test -w /` probes only the DAC write bit (and `EROFS`). It does **not** test `CAP_SYS_ADMIN`, Btrfs ioctl authorization, or path collision.
- A process with `CAP_DAC_OVERRIDE` but lacking `CAP_SYS_ADMIN` passes `test -w /` (`rc=0`), yet immediately fails `btrfs subvolume create` with `EPERM`!
- As S034 explicitly warns, `access()` "does not answer the 'can I read/write/execute this file?' question".

#### Mismatch 5: Sandboxing Directives and Unit Divergence
- `limine-snapper-sync.service` configures:
  `User=root`  
  `CapabilityBoundingSet=CAP_SYS_ADMIN`  
  `ProtectHome=yes`  
  `NoNewPrivileges=yes`  
  `ReadWritePaths=/tmp`  
  `SystemCallFilter=@system-service @mount`
- `systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` sets up a transient unit. While it mimics `CapabilityBoundingSet`, it does not replicate all sandboxing flags, filesystem namespaces, or private mount options that the production unit specifies.

#### Mismatch 6: Violation of Read-Only Safety Contract
- The proposed falsifier instructed running `sudo systemd-run` and `sudo test -w /`.
- Executing `sudo systemd-run` on a production host:
  - Invokes systemd D-Bus IPC to create transient units under PID 1.
  - Requires elevated root privilege (`sudo`).
  - Mutates host state and violates the strict read-only inspection contract of this tooling suite (`NO sudo/host mutation, package operations, service restarts or systemd-run`).
- Diagnostic verification must be achieved via static unit analysis (`systemctl cat`, `systemctl show`) and read-only filesystem metadata inspection (`stat`, `getfacl`, `findmnt`) without issuing privileged commands.

---

## 5. Evaluation of Inherited Artifacts & Erratum Integration

1. **Inherited `Capabilities.md` Status**:
   - Reused: Detailed S027 and S034 primary quote extractions; matrix comparing `CAP_DAC_OVERRIDE` vs `CAP_DAC_READ_SEARCH`; the six specific falsifier mismatches; read-only strace syscall observations.
   - Refined & Corrected:
     - Clarified that for root execution, `P'(permitted) = P(inheritable) | P(bounding)` and `P'(effective) = P'(permitted)`, so permitted and effective sets are identical under the unit's bounding set.
     - Connected the audit findings to the completed round-12 C2 Decision Matrix (`corpus/knowledge/root-dac-decision-r12.json` and `.md`), where B1 (DAC write denial) and B3 (capability-bound root) form an explanatory conjunction for the `EACCES` class, while B2 (`EROFS`) and B4 (`EEXIST`) remain distinct controls.
     - Documented the dated erratum added to `corpus/knowledge/snapper-eacces-mechanism.md` (round 12) affirming that permission proxy is not causal proof and that inactive unit text reflects configured properties rather than live runtime capability sets.

---

## 6. Host Probes Executed (Read-Only, Non-Root)

All probes executed as unprivileged user (`uid=1000`):

| Command | Exit Code | Key Output Observed | Grounded Interpretation |
|---|---|---|---|
| `stat -c '%A %a %U:%G %n' /` | 0 | `dr-xr-xr-x 555 root:root /` | Root directory is mode `0555`, no write bit for any entity |
| `/usr/bin/test -w /` | 1 | `rc=1` | GNU coreutils `test` reports `/` not writable |
| `strace -e trace=access,faccessat,faccessat2 /usr/bin/test -w /` | 1 | `access("/", W_OK) = -1 EACCES (Permission denied)` | Coreutils binary uses `access(2)` (real UID) |
| `strace -e trace=access,faccessat,faccessat2 bash -c 'test -w /'` | 1 | `faccessat2(AT_FDCWD, "/", W_OK, AT_EACCESS) = -1 EACCES (Permission denied)` | Bash builtin uses `faccessat2` with `AT_EACCESS` (effective UID) |
| `systemctl show -p User -p CapabilityBoundingSet -p AmbientCapabilities -p NoNewPrivileges limine-snapper-sync.service` | 0 | `CapabilityBoundingSet=cap_sys_admin`<br>`AmbientCapabilities=`<br>`User=root`<br>`NoNewPrivileges=yes` | Inactive unit configures `User=root` and restricts bounding set to `cap_sys_admin` |

**Tooling Report**:
- Zero package installations or updates performed.
- Zero sudo executions performed.
- Zero host mutations, service restarts, or systemd-run executions.

---

## 7. Risks and Open Items

- **R1 (Configuration vs Runtime Observation)**: Unit inspection reflects configured properties on an inactive unit (`is-active` rc=3). Determining whether a live process held specific capabilities requires inspecting `/proc/$PID/status` (`CapEff`, `CapPrm`, `CapBnd`) while the unit executes, which cannot be done on an inactive service without privileged execution.
- **R2 (Syscall Divergence in Scripts)**: Automated health scripts calling `test -w` invoke either `access()` or `faccessat2(..., AT_EACCESS)` depending on whether they invoke `/usr/bin/test` or the shell builtin. If credentials diverge (`ruid != euid`), results will differ.
- **R3 (Non-Author Seat Boundary)**: This analysis provides author-side evidence from this lane's scout assignment. Final verification, quality checks, and integration belong to the parent coordinator. No unsupported PASS is claimed.
