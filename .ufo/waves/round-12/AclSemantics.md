# AclSemantics — Authoritative POSIX ACL & Capability Semantics for Tsukuroi C1/C2

source: `acl(5)` (Linux man-pages, June 5, 2026); `capabilities(7)` (S027); `systemd.exec(5)` (S028); `access(2)` (S034); `path_resolution(7)`; host probes 2026-10-19.
verified-at: 2026-10-19
recheck: on-release

## Axes
- **operability**: Grounds `tsukuroi-census.sh` root metadata discrimination so that census findings do not conflate DAC owner permission bits with filesystem mount options or declare valid configurations corrupt, preventing false-positive degraded rollups.
- **depth**: Traces the 5-step `acl(5)` Access Check Algorithm, IEEE 1003.1e `ACL_MASK` mapping to `st_mode` group bits, capability bypass via `CAP_DAC_OVERRIDE`, and errno discrimination between DAC denial (`EACCES`) and read-only storage (`EROFS`).

---

## 1. Executive Summary & Core Evaluated Questions

### Q1: Does mode owner-write absence alone prove write denial with ACLs/capabilities?
**Verdict: NO (Definitively False).**
Owner-write absence (`st_mode & S_IWUSR == 0`, e.g. mode `0555`, `0575`, `0444`) alone does **not** prove write denial for three structural reasons:
1. **Capability Bypass (`CAP_DAC_OVERRIDE`)**: A process possessing `CAP_DAC_OVERRIDE` bypasses standard DAC file read, write, and execute permission checks (`capabilities(7)`). Unbounded root processes (e.g. PID 1, standard system daemons, root shell) retain write capability to an owner-write-absent directory unless restricted by a read-only VFS mount (`EROFS`), immutable flags, or LSM.
2. **Caller Identity Mismatch (Non-Owner Callers)**: Under `acl(5)` Step 1, owner permission bits (`ACL_USER_OBJ`) are evaluated **only** when the effective UID (EUID) of the process matches the file owner UID. If EUID does not match the owner, owner bits are ignored: the process is evaluated against named user entries (`ACL_USER`, Step 2), group entries (`ACL_GROUP_OBJ`/`ACL_GROUP`, Step 3), or other entries (`ACL_OTHER`, Step 4). If any matching entry and mask contain write permission (e.g. mode `0575` with `mask::rwx`, or mode `0557`), the non-owner is granted write access even though owner-write is absent.
3. **Host-Specific Root Directory Context (`/` at `0555 root:root`)**:
   - For an unprivileged process (UID 1000, such as the census probe), write to `/` is evaluated under `ACL_OTHER` (Step 4). Other bits are `r-x`. Write is denied under both `0555` and `0755` (where other is also `r-x`). The absence of the owner-write bit (`0200`) is irrelevant to UID 1000.
   - For an unbounded root process (UID 0), `CAP_DAC_OVERRIDE` bypasses DAC; write is granted despite `0555`.
   - For a capability-bounded root process lacking `CAP_DAC_OVERRIDE` (e.g. `limine-snapper-sync.service` with `CapabilityBoundingSet=CAP_SYS_ADMIN`), EUID is 0, Step 1 evaluates `ACL_USER_OBJ` (`r-x`), `CAP_DAC_OVERRIDE` is absent, and write is denied with `EACCES`.
   - **Conclusion**: Write denial is a joint property of DAC mode/ACL, process EUID/groups, and process capabilities. Mode owner-write absence alone proves nothing without process context.

### Q2: How does `stat` reflect the ACL mask (`ACL_MASK`)?
**Mapping Rule (`acl(5)` § CORRESPONDENCE BETWEEN ACL ENTRIES AND FILE PERMISSION BITS):**
- Owner bits (`st_mode & S_IRWXU`) **always** match `ACL_USER_OBJ`.
- Other bits (`st_mode & S_IRWXO`) **always** match `ACL_OTHER`.
- Group bits (`st_mode & S_IRWXG`):
  - If the file has **no** `ACL_MASK` entry (minimal ACL: owner, group, other): group bits correspond to `ACL_GROUP_OBJ` (owning group rights).
  - If the file **has** an `ACL_MASK` entry (mandatory whenever named `ACL_USER` or `ACL_GROUP` entries exist): group bits correspond to `ACL_MASK`, **NOT** `ACL_GROUP_OBJ`.

**Implications for Inspection & Tooling:**
1. **Stat Group Bits = Effective Maximum Rights Mask**:
   The `ACL_MASK` defines the maximum permissions granted to any `ACL_USER`, `ACL_GROUP_OBJ`, or `ACL_GROUP` entry. Therefore:
   - When `st_mode` group bits lack write (`st_mode & S_IWGRP == 0`, e.g. `0555` or `0755`): the mask has no write bit. Even if an extended ACL exists, **no** named user or group can have effective write access (`entry & ACL_MASK` clears `w`).
   - When `st_mode` group bits have write (`st_mode & S_IWGRP != 0`, e.g. `0775` or `0575`): the mask permits write, but the owning group (`ACL_GROUP_OBJ`) may have `r--` or `---`. `stat` group bits reflect the mask, not the owning group.
2. **`chmod` Overwrites the ACL Mask**:
   In POSIX.1e, `chmod(path, mode)` operates on the file permission bits. When invoked on a file with an extended ACL, changing group bits sets `ACL_MASK`, not `ACL_GROUP_OBJ`. For example, `chmod 755` masks out write access from all named users and groups without deleting their ACL entries.
3. **`stat` Blind Spot**:
   `stat(1)` (`stat -c '%a'`) outputs only octal permission bits (e.g. `555` or `755`). It provides **no** indicator of whether an extended ACL exists (unlike `ls -l`, which appends `+`), hides `ACL_GROUP_OBJ` when a mask is present, and cannot display named `ACL_USER` entries. Only `getfacl` or `acl_get_file(3)` reveals the full ACL structure.

---

## 2. Authoritative Quotes (≤25 words each)

| Source | Section / Anchor | Located Quote (≤25 words) | Teaching / Significance |
|---|---|---|---|
| `acl(5)` | § ACL ENTRIES (ACL_MASK) | “The ACL_MASK entry denotes the maximum access rights that can be granted by entries of type ACL_USER, ACL_GROUP_OBJ, or ACL_GROUP.” (21 words) | Defines ACL_MASK as the universal ceiling for all non-owner, non-other ACL entries. |
| `acl(5)` | § CORRESPONDENCE | “If the ACL has an ACL_MASK entry, the group permissions correspond to the permissions of the ACL_MASK entry.” (18 words) | Proves `st_mode` group bits represent the mask, not `ACL_GROUP_OBJ`, when extended ACLs exist. |
| `acl(5)` | § ACCESS CHECK ALGORITHM (Step 1) | “if the ACL_USER_OBJ entry contains the requested permissions, access is granted, else access is denied.” (15 words) | Owner access checks evaluate `ACL_USER_OBJ` exclusively; group/mask/other are never reached for the owner. |
| `capabilities(7)` | § Capabilities list (CAP_DAC_OVERRIDE) | “Bypass file read, write, and execute permission checks.” (8 words) | Proves capability presence overrides DAC mode bits entirely, precluding static denial claims. |
| `systemd.exec(5)` | § CapabilityBoundingSet= | “Capabilities listed will be included in the bounding set, all others are removed” (12 words) | Grounding for why `CapabilityBoundingSet=CAP_SYS_ADMIN` strips `CAP_DAC_OVERRIDE`, subjecting root to DAC. |
| `access(2)` | § DESCRIPTION (Privileged processes) | “for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities” (19 words) | Distinguishes root access checks from standard syscall checks; grounds capability falsifiers. |
| `path_resolution(7)` | § Permissions | “The first group of three is used when the effective user ID of the calling process equals the owner ID of the file.” (23 words) | Confirms DAC triplet selection: owner bits apply solely when process EUID equals file owner UID. |

---

## 3. Measured Host Evidence (Read-Only, non-root, 2026-10-19)

Probes executed from lane user `vgpnk` (UID 1000, GID 1000):

| Probe | Command | Result / Exit | Interpretation |
|---|---|---|---|
| Root Stat | `stat -c '%a %A %u:%g %F %n' /` | `555 dr-xr-xr-x 0:0 directory /` (rc=0) | `/` has octal mode 555 (`r-xr-xr-x`), owned by UID 0, GID 0. Owner-write bit (0200) absent. |
| Root ACL | `getfacl -p /` | `user::r-x`, `group::r-x`, `other::r-x` (rc=0) | Exactly 3 base entries; no `ACL_MASK`, no named `ACL_USER`/`ACL_GROUP`, no default ACLs. |
| Root Mount | `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | `/ btrfs rw,relatime,ssd,discard=async,subvol=/@` (rc=0) | `/` is mounted `rw` on Btrfs. Mode 0555 is **not** a read-only filesystem mount. |
| Caller Credentials | `id && grep -E '^(CapPrm\|CapEff\|CapBnd)' /proc/self/status` | `uid=1000(vgpnk) ... CapPrm: 0 CapEff: 0 CapBnd: 000001ffffffffff` (rc=0) | Unprivileged caller with zero effective/permitted capabilities; evaluated via `ACL_OTHER` for `/`. |
| Service Hardening | `systemctl cat limine-snapper-sync.service` | `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN`, `ReadWritePaths=/tmp` (rc=0) | Service runs as UID 0 but strips `CAP_DAC_OVERRIDE`; subjected to DAC `ACL_USER_OBJ` on `/`. |

---

## 4. Advice for C1 Finding Vocabulary (`tools/tsukuroi-census.sh`)

Claim C1 introduces root metadata observation (`root_mode=`, `root_uid=`, `root_gid=`) into the census to close the unowned `/` blind spot. To prevent false-positive rollups and ungrounded policy claims:

1. **PROHIBITED Vocabulary & Patterns**:
   - **Do NOT call mode `0555` a "read-only mount" or "read-only filesystem".** It is an inode DAC mode bit pattern. The mount is `rw`. Confusing DAC with VFS mount flags violates domain accuracy.
   - **Do NOT declare mode `0555` "unhealthy", "corrupt", or "should be 0755".** Arch packages do not specify a mode for `/` (unowned, 0 mtree entries); distros like Fedora explicitly ship `/` at 0555. Imposing 0755 as an absolute health standard is an ungrounded policy overclaim.
   - **Do NOT use `test -w "$ROOT"` or `access(2)` to evaluate root directory health.** If the census is ever run under `sudo` (UID 0 with `CAP_DAC_OVERRIDE`), `test -w` returns 0 (writable) even when mode is `0555`. Conversely, for UID 1000, `test -w` returns 1 (non-writable) even when mode is `0755`! Access probes measure caller privilege, not target metadata.
2. **RECOMMENDED Vocabulary & Patterns**:
   - **Emit pure factual tokens**: `root_mode=%04a` (e.g. `0555`), `root_uid=%u` (e.g. `0`), `root_gid=%g` (e.g. `0`).
   - **Differentiate permission states explicitly**:
     - `owner-write present` (when `st_mode & 0200 != 0`, e.g. `0755`).
     - `owner-write absent` (when `st_mode & 0200 == 0`, e.g. `0555`).
     - `metadata unreadable` (when `stat` fails or target is non-directory / dangling symlink).
   - **Verdict qualification**:
     If the census chooses to mark owner-write absence as `DEGRADED`, describe it as:
     `owner-write absent (DAC restricted for unprivileged or capability-bounded root services)`
     Never claim that `/` is write-denied for all processes.

---

## 5. Advice for C2 Limits (`corpus/knowledge/root-dac-decision-r12.md`)

Claim C2 builds an independent EACCES decision matrix with at least 4 grounded branches. The matrix must enforce the following boundaries:

1. **Branch 1: DAC / ACL / Capability Restriction (`EACCES`, errno 13)**:
   - **Condition**: Process fsuid/EUID equals object owner UID (`ACL_USER_OBJ`) AND `st_mode & S_IWUSR == 0` (or non-owner matching an entry where entry/mask lacks write), **AND** the process lacks `CAP_DAC_OVERRIDE` in its effective capabilities (`systemd.exec(5)` S028).
   - **Syscall Result**: Returns `EACCES` (Permission denied).
   - **Limit**: Mode `0555` on `/` alone does **not** prove host `EACCES`. It explains `EACCES` only when paired with the service's capability bounding set.
2. **Branch 2: Read-Only Filesystem / Mount (`EROFS`, errno 30)**:
   - **Condition**: Target path resides on a filesystem mounted with `MS_RDONLY` (`ro`), or a read-only block device.
   - **Syscall Result**: Returns `EROFS` (Read-only file system), **NOT** `EACCES`.
   - **Limit**: The matrix must explicitly isolate `EROFS` as a separate non-EACCES failure mode. A read-only mount cannot be cited as the cause of an observed `errno:13`.
3. **Branch 3: Service Sandboxing & Namespace Isolation (`EACCES` or `EROFS` depending on directive)**:
   - **Condition**: systemd sandbox directives applied to the unit, such as `ProtectSystem=strict` (mounts `/usr`, `/boot`, `/etc` read-only -> `EROFS`), `ReadOnlyPaths=/` (`EROFS`), or `InaccessiblePaths=` (`EACCES` / `ENOENT`).
   - **Limit**: On the current host, `systemctl show -p ProtectSystem,ReadOnlyPaths limine-snapper-sync.service` confirms `ProtectSystem=no` and no `ReadOnlyPaths`. Sandboxing directives must be inspected per unit and not assumed.
4. **Branch 4: Destination Collision & Path Resolution (`EEXIST` or `EACCES`)**:
   - **Condition A (Collision)**: Destination path (e.g. `/.snapshots`) already exists as a directory, mountpoint, or subvolume (`stat` succeeds). Returns `EEXIST` (File exists) or tool-specific failure, **NOT** `EACCES`.
   - **Condition B (Directory Search Traversal)**: Intermediate parent directory lacks search/execute permission (`+x`). Per `path_resolution(7)` Step 2, lookup fails with `EACCES` even if write permission on the parent exists.
   - **Limit**: On the current host, `/.snapshots` does not exist (`ENOENT`), and `/` has search permission (`r-x`), so traversal succeeds. Collision is ruled out by `stat`.

---

## 6. Risks & Verification Gaps

- **R1 (Author-Side Evidence)**: Findings in this document represent author-side seat analysis; they do not constitute independent non-author verification.
- **R2 (Unrun Falsifier)**: The proposed sudo discriminator (`sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /`) was **not run**, respecting the strict non-root/no-sudo boundary. All findings are derived from static source analysis of `acl(5)`, `capabilities(7)`, `access(2)`, and non-mutating unprivileged host probes.
- **R3 (Tooling Directive Compliance)**: Zero tools installed, zero packages upgraded. System packages `acl` (`getfacl`), `coreutils` (`stat`), and `util-linux` (`findmnt`) were already installed and functional.
