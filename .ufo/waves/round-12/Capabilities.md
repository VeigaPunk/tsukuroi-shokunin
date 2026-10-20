# Capabilities and Access Semantics Audit (S027 vs S034)

**Seat ID**: `Capabilities`  
**Role**: `scout`  
**Milestone**: `round-12`  
**Judged on**: `operability`, `depth`  
**Target Sources**: S027 (`capabilities(7)`), S034 (`access(2)`)  
**Audit Target**: `corpus/knowledge/snapper-eacces-mechanism.md` § Falsifier and related capability/DAC claims

---

## 1. Axes

1. **Operability**: Provide source-grounded, non-privileged diagnostic rules to evaluate directory write access and permission denials without requiring `sudo`, without executing live mutating commands, and accounting for the runtime divergence between binary execution (`/usr/bin/test`) and shell builtins.
2. **Depth**: Map the exact kernel VFS permission check flow (`inode_permission`), capability bounding set filtering during `execve(2)`, thread capability set transitions (Permitted vs Effective vs Bounding), real vs effective UID/GID credential checking in `access(2)` vs `open(2)`/`mkdir(2)`, and identify exact contradictions in prior falsifier text.

---

## 2. Primary Source Evidence and Verbatim Anchors

### 2.1 S027 — `capabilities(7)`
- **Location**: `https://man.archlinux.org/man/capabilities.7` (Linux man-pages 6.19, current upstream release).
- **CAP_DAC_OVERRIDE**:
  > *"Bypass file read, write, and execute permission checks. (DAC is an abbreviation of "discretionary access control".)"*
- **CAP_DAC_READ_SEARCH**:
  > *"• Bypass file read permission checks and directory read and execute permission checks;*  
  > *• invoke open_by_handle_at(2);*  
  > *• use the linkat(2) AT_EMPTY_PATH flag to create a link to a file referred to by a file descriptor."*
- **Effective capability set**:
  > *"This is the set of capabilities used by the kernel to perform permission checks for the thread."*
- **Permitted capability set**:
  > *"This is a limiting superset for the effective capabilities that the thread may assume."*
- **Capability bounding set**:
  > *"The capability bounding set is a mechanism that can be used to limit the capabilities that are gained during execve(2)."*
- **Transformation during `execve(2)` for root (`UID 0`)**:
  > *"when a process whose real and effective UIDs are zero execve(2)s a program, the calculation of the process's new permitted capabilities simplifies to:*  
  > *`P'(permitted) = P(inheritable) | P(bounding)`*  
  > *`P'(effective) = P'(permitted)`*  
  > *Consequently, the process gains all capabilities in its permitted and effective capability sets, except those masked out by the capability bounding set."*
- **Effect of UID changes**:
  > *"If the filesystem user ID is changed from 0 to nonzero (see setfsuid(2)), then the following capabilities are cleared from the effective set: CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_DAC_READ_SEARCH, CAP_FOWNER, CAP_FSETID, CAP_LINUX_IMMUTABLE (since Linux 2.6.30), CAP_MAC_OVERRIDE, and CAP_MKNOD (since Linux 2.6.30)."*

### 2.2 S034 — `access(2)`
- **Location**: `https://man.archlinux.org/man/access.2` (Linux man-pages 6.19).
- **Credential checking rule (Real vs Effective UID; Permitted vs Effective Capabilities)**:
  > *"The check is done using the calling process's real UID and GID, rather than the effective IDs as is done when actually attempting an operation (e.g., open(2)) on the file. Similarly, for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities; and for non-root users, the check uses an empty set of capabilities."*
- **Design intent / Rationale**:
  > *"This allows set-user-ID programs and capability-endowed programs to easily determine the invoking user's authority. In other words, access() does not answer the "can I read/write/execute this file?" question. It answers a slightly different question: "(assuming I'm a setuid binary) can the user who invoked me read/write/execute this file?""*
- **Directory access prerequisite**:
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
- On this host, `/` is mode `0555` (`r-xr-xr-x`, `root:root`).
- Traversing `/` requires directory search (`x`), which is granted to everyone by mode bit `0005` (and `0050`, `0500`). Neither capability is needed for directory search.
- Creating an entry in `/` (such as `/.snapshots` or subvolume creation) requires directory write permission (`w`, `MAY_WRITE`) on `/`.
- Mode `0555` has no write bit for owner, group, or others.
- `CAP_DAC_READ_SEARCH` does **not** bypass directory write checks. Even if possessed, it cannot allow directory modifications.
- Only `CAP_DAC_OVERRIDE` allows a process to bypass the missing write permission on a mode `0555` directory.
- Consequently, dropping `CAP_DAC_OVERRIDE` while retaining `CAP_DAC_READ_SEARCH` or `CAP_SYS_ADMIN` leaves the process bound by DAC mode bits.

### 3.2 Real vs Effective UID and Permitted vs Effective Capabilities
Linux distinguishes between normal filesystem operations (`open`, `mkdir`, ioctl) and access probes (`access`, `faccessat`):

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
   As S034 explicitly notes, `access(2)` answers whether the *invoking user* has access, not whether the *running process* has effective permission.

---

## 4. Audit of Old `test -w` Falsifier Language

The falsifier proposed in `corpus/knowledge/snapper-eacces-mechanism.md` § Falsifier reads:
```sh
sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /; echo rc=$?  # predicted rc=1
sudo test -w /; echo rc=$?  # predicted rc=0

The first returning 0 falsifies the proposed DAC/capability mechanism. access(2) (S034) explains why this test -w comparison distinguishes root's permitted capabilities from its effective capabilities; it is a permission probe, not a subvolume-create test.
```

### 4.1 Exact Mismatches and Contradictions

#### Mismatch 1: Conflation and Inversion of Permitted vs Effective Capabilities
- **Old claim**: *"access(2) (S034) explains why this test -w comparison distinguishes root's permitted capabilities from its effective capabilities"*.
- **Kernel reality (S027 & S034)**:
  - In `sudo systemd-run -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /`:
    The process runs as `UID 0`. Under `execve(2)` for root:
    `P'(permitted) = P(inheritable) | P(bounding)`
    `P'(effective) = P'(permitted)`
    Since `P(bounding) = {CAP_SYS_ADMIN}`, `CAP_DAC_OVERRIDE` is absent from **both** `P(permitted)` and `P(effective)`.
  - In `sudo test -w /`:
    `CAP_DAC_OVERRIDE` is present in **both** `P(permitted)` and `P(effective)`.
  - In neither command do permitted and effective capabilities differ. Both commands have `P(permitted) == P(effective)`.
  - The comparison distinguishes a **capability-bounded root process** from an **unbounded root process**. It does **not** distinguish permitted capabilities from effective capabilities.
  - Furthermore, `access(2)` *only* inspects `P(permitted)` for root. It is incapable of detecting whether a capability is absent from `P(effective)` if it remains in `P(permitted)`. Describing it as distinguishing permitted from effective capabilities is backwards.

#### Mismatch 2: Coreutils Binary vs Shell Builtin Syscall Divergence
- `sudo test -w /` executes the external binary `/usr/bin/test` (GNU coreutils).
  - Probed fact: `/usr/bin/test -w /` calls `access("/", W_OK)`.
  - `access(2)` uses Real UID (`ruid`) and `P(permitted)`.
- If an operator evaluates `test -w /` in a shell script or shell subshell (`bash -c 'test -w /'`):
  - Probed fact: Bash builtin `test` calls `faccessat2(AT_FDCWD, "/", W_OK, AT_EACCESS)`.
  - `AT_EACCESS` causes `faccessat2` to use Effective UID (`euid`) rather than Real UID (`ruid`).
- Under environments where `ruid != euid` (such as setuid wrappers, sudo with preserving flags, or daemons changing credentials), `/usr/bin/test` and shell builtin `test` can yield conflicting results.

#### Mismatch 3: Erasure of Diagnostic Error Classes (rc=1 vs errno)
- `test -w /` evaluates to a binary exit status: `0` or `1`.
- If `test -w /` exits `1`, it collapses at least three distinct kernel conditions:
  1. `EACCES`: DAC permission bits lack write permission and `CAP_DAC_OVERRIDE` is missing.
  2. `EROFS`: Target path is on a filesystem mounted read-only (`MS_RDONLY`).
  3. `EPERM`: Target inode has the immutable flag set (`FS_IMMUTABLE_FL`).
- `access(2)` sets specific `errno` values (`EACCES`, `EROFS`, `EPERM`). The falsifier shell snippet `test -w /; echo rc=$?` discards the `errno` distinction, masking whether a denial was caused by DAC mode bits or a read-only filesystem mount.

#### Mismatch 4: Permission Probe vs Actual Subvolume Creation Mechanics
- `limine-snapper-sync.service` failed with `errno:13` (EACCES) during Btrfs subvolume creation (`btrfs subvolume create` / `BTRFS_IOC_SUBVOL_CREATE`).
- A Btrfs subvolume creation operation requires:
  1. Directory write/search permission on parent directory (`MAY_WRITE | MAY_EXEC` in kernel VFS) -> requires `CAP_DAC_OVERRIDE` when parent is mode 0555.
  2. Btrfs ioctl privilege -> requires `CAP_SYS_ADMIN` in the caller's user namespace.
  3. Non-read-only filesystem mount.
  4. LSM (SELinux/AppArmor) allowance.
- `test -w /` tests only the DAC write bit (and `EROFS`). It does **not** test whether the caller holds `CAP_SYS_ADMIN`, whether Btrfs ioctl permissions are satisfied, or whether subvolume collision occurs.
- A process endowed with `CAP_DAC_OVERRIDE` but lacking `CAP_SYS_ADMIN` would pass `test -w /` (`rc=0`), yet immediately fail `btrfs subvolume create` with `EPERM`!

#### Mismatch 5: Sandboxing Directives and Unit Divergence
- `limine-snapper-sync.service` declares:
  `User=root`  
  `CapabilityBoundingSet=CAP_SYS_ADMIN`  
  `ProtectHome=yes`
- `systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` sets up a transient service. While it mimics `CapabilityBoundingSet`, it does not replicate all sandboxing flags, filesystem namespaces, or private mount options that production units may configure.

#### Mismatch 6: Violation of Read-Only Safety Contract
- The proposed falsifier instructed running `sudo systemd-run` and `sudo test -w /`.
- Executing `sudo systemd-run` on a production host:
  - Invokes systemd D-Bus IPC to create transient units under PID 1.
  - Requires elevated root privilege (`sudo`).
  - Violates the read-only inspection contract of the tooling suite (`NO sudo/host mutation, package operations, service restarts or systemd-run`).
- Diagnostic verification must be achieved via static unit analysis (`systemctl cat`) and read-only filesystem metadata inspection (`stat`, `getfacl`, `findmnt`) without issuing privileged commands.

---

## 5. Bounded Recommendations for C2 Matrix and C1 Census

1. **For C2 Decision Matrix (`root-dac-decision-r12.json`)**:
   - **Separate DAC mode denial from filesystem read-only mount**: Mode `0555` is a DAC permission attribute, distinct from `MS_RDONLY` (`EROFS`).
   - **Ground EACCES cause in dual condition**: Denied write requires *both* (a) DAC write bit absence in mode and ACL, *and* (b) absence of `CAP_DAC_OVERRIDE` in the process's effective capability bounding set.
   - **Do not assert `test -w` as a subvolume creation oracle**: Note that `test -w` only probes DAC write bits (and mount ro) via `access()`, not ioctl capabilities (`CAP_SYS_ADMIN`) or filesystem subvolume state.
   - **Correct capability set attribution**: When a systemd unit specifies `CapabilityBoundingSet=CAP_SYS_ADMIN`, `CAP_DAC_OVERRIDE` is excluded from both `P(bounding)` and `P(effective)`. S034's use of permitted capabilities in `access(2)` is a quirk of `access(2)`, not a tool for isolating permitted from effective sets.

2. **For C1 Root Metadata Census (`tools/tsukuroi-census.sh`)**:
   - Report the observable facts: `root_mode=%a`, `root_uid=%u`, `root_gid=%g` without assuming mode `0555` alone is an operational error.
   - Because the census runs unprivileged (UID 1000), absence of owner-write does not affect the census process directly. Owner-write absence should be reported as explicit evidence without misclassifying an intentional 0555 host as broken.

---

## 6. Verification and Host Probes Executed (Read-Only)

| Command | Exit Code | Key Output Observed |
|---|---|---|
| `stat -c '%A %a %U:%G %n' /` | 0 | `dr-xr-xr-x 555 root:root /` |
| `strace -e access,faccessat,faccessat2 /usr/bin/test -w /` | 1 | `access("/", W_OK) = -1 EACCES (Permission denied)` |
| `strace -e access,faccessat,faccessat2 bash -c 'test -w /'` | 1 | `faccessat2(AT_FDCWD, "/", W_OK, AT_EACCESS) = -1 EACCES (Permission denied)` |
| Tool installations/updates | — | None. No packages installed, no sudo invoked, no host files modified. |

---

## 7. Risks and Open Items
- **R1 (Language Correction)**: `corpus/knowledge/snapper-eacces-mechanism.md` § Falsifier contains the misleading sentence regarding `access(2)` distinguishing permitted from effective capabilities. Per the round contract, existing notes are immutable historical records; corrections should be integrated into round-12 C2 matrix deliverables (`root-dac-decision-r12.md`).
- **R2 (Syscall Divergence)**: Automated scripts invoking `test -w` will invoke either `access()` or `faccessat2(..., AT_EACCESS)` depending on whether they run `/usr/bin/test` or bash built-in `test`. Tooling and tests must be cognizant of this distinction.
- **R3 (Status)**: All inspections complete. No unsupported PASS claimed.
