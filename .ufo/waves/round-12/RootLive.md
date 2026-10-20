# RootLive — Read-only reconnaissance of `/`: metadata, DAC vs mount flags, and historic snapper mechanism state

**Milestone:** round-12  
**Seat:** `RootLive` (scout)  
**Assigned target:** Read-only reconnaissance of `/`: `stat -c mode uid gid filetype`, `getfacl -p /`; `findmnt -n -o TARGET,FSTYPE,OPTIONS /`. Record metadata, distinguish DAC from mount flags. Never permissions changes or create files at `/`. Compare historic snapper mechanism state without calling diagnosis proven.  
**Evidence path:** `.ufo/waves/round-12/RootLive.md`  
**Host capture timestamp:** `2026-10-20T02:16:41Z` (UTC)  
**Host baseline:** Linux `7.2.3-arch1-3` x86_64; working tree HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`.  
**Independence notice:** Author-side seat evidence (leaf scout); not independent non-author verification. Strictly read-only, non-root; no package install, no systemd-run, no sudo, no permission changes (`chmod` never run), no file creation at `/`.

---

## 1. Exact Read-Only Probes and Evidence

All probes were executed from an unprivileged shell (`vgpnk`) without elevation.

### Probe Suite Matrix

| Probe Command | RC | Output (Sanitized / Verbatim) | Classification |
|---|---|---|---|
| `stat -c "mode=%a uid=%u gid=%g filetype=%F" /` | `0` | `mode=555 uid=0 gid=0 filetype=directory` | `[obs]` |
| `stat -c "%a %u %g %F" /` | `0` | `555 0 0 directory` | `[obs]` |
| `stat /` | `0` | `Size: 130 Blocks: 0 IO Block: 4096 directory` <br> `Device: 0,31 Inode: 256 Links: 1` <br> `Access: (0555/dr-xr-xr-x) Uid: ( 0/ root) Gid: ( 0/ root)` <br> `Access: 2026-10-19 15:46:24.628824179 -0300` <br> `Modify: 2026-10-03 17:45:33.001630573 -0300` <br> `Change: 2026-10-03 17:45:33.001630573 -0300` <br> `Birth: 2026-10-03 17:41:30.687657678 -0300` | `[obs]` |
| `getfacl -p /` | `0` | `# file: /` <br> `# owner: root` <br> `# group: root` <br> `user::r-x` <br> `group::r-x` <br> `other::r-x` | `[obs]` |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | `0` | `/ btrfs rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` | `[obs]` |
| `findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS /` | `0` | `TARGET: /` <br> `SOURCE: /dev/mapper/root[/@]` <br> `FSTYPE: btrfs` <br> `OPTIONS: rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@` | `[obs]` |
| `btrfs property get /` | `0` | `ro=false` <br> `label=` | `[obs]` |
| `lsattr -d /` | `0` | `---------------------- /` (no immutable `i` or append `a` flags) | `[obs]` |
| `cat /sys/kernel/security/lsm` | `0` | `capability,landlock,lockdown,yama,bpf` (no SELinux, no AppArmor, no Smack, no Tomoyo) | `[obs]` |
| `test -r /` | `0` | Read test succeeds (exit 0) | `[obs]` |
| `test -w /` | `1` | Write test fails (exit 1, unprivileged write denied) | `[obs]` |
| `test -x /` | `0` | Search/execute test succeeds (exit 0) | `[obs]` |
| `stat /.snapshots` | `1` | `stat: cannot stat '/.snapshots': No such file or directory` (rc=1) | `[obs]` |
| `snapper list-configs` | `0` | Header only: `Config │ Subvolume` / `───────┼──────────` (0 configured rows) | `[obs]` |
| `journalctl --no-pager -o short-iso -g "create subvolume failed" \| grep -c "errno:13"` | `0` | `9` (increased from 8 reported in round-1 baseline) | `[obs]` |
| `systemctl cat limine-snapper-sync.service \| grep -n -E "CapabilityBoundingSet\|User\|ProtectHome\|ProtectSystem\|ReadOnlyPaths"` | `0` | `7:User=root` <br> `14:CapabilityBoundingSet=CAP_SYS_ADMIN` <br> `19:ProtectHome=yes` | `[obs]` |

---

## 2. Distinction: Discretionary Access Control (DAC) vs Mount Flags

A critical diagnostic failure identified in prior investigations (e.g., screened out in rejected source S033) is conflating DAC permission restrictions with filesystem mount-level read-only flags. The probes provide explicit, source-grounded discrimination between these two layers:

### Discretionary Access Control (DAC) Layer
1. **Mode Bits:** `0555` (`dr-xr-xr-x`). Owner is `uid=0` (`root`), group is `gid=0` (`root`).
2. **POSIX ACLs:** `getfacl -p /` confirms only the minimal standard 3-entry ACL (`user::r-x`, `group::r-x`, `other::r-x`). There are no extended ACL entries, no POSIX access mask overrides, and no default ACL inheritance attributes.
3. **Write Bit Absence:** The write bit (`w`) is absent for user (`r-x`), group (`r-x`), and other (`r-x`).
4. **VFS Enforcement:** Under Linux standard permission checks (`access(2)`, S034), write access to `/` requires either:
   - DAC write permission (`w` bit matching the caller's identity), or
   - The `CAP_DAC_OVERRIDE` capability (S027: "Bypass file read, write, and execute permission checks").
5. **Observed Unprivileged Behavior:** The unprivileged test `test -w /` returns exit code `1` (`EACCES`), while `test -r /` and `test -x /` return exit code `0`.

### VFS Mount Layer
1. **Mount Options:** `findmnt -n -o TARGET,FSTYPE,OPTIONS /` reports `rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`.
2. **Read-Write Status:** The root filesystem is mounted `rw` (read-write), **not** `ro` (read-only).
3. **Subvolume Property:** `btrfs property get /` confirms `ro=false`.
4. **Filesystem Attributes:** `lsattr -d /` confirms no special immutable (`i`) or append-only (`a`) ext2/4/btrfs inode flags are set.

### Structural Finding
The inability of a process lacking `CAP_DAC_OVERRIDE` to create entries in `/` (such as `/.snapshots`) is **entirely a DAC constraint** (file mode `0555` omitting write bits), **not a filesystem mount constraint** (the mount is active and `rw`). An attempt to write on an `ro` mount fails with `EROFS` (Read-only file system); write denial on a `rw` mount with mode `0555` fails with `EACCES` (Permission denied, errno 13).

---

## 3. Comparison with Historic Snapper Mechanism State

### Baseline State (`corpus/knowledge/snapper-eacces-mechanism.md`)
- Historic observation: `/` mode was recorded as `555 root:root`; `getfacl -p /` showed `user::r-x`, `group::r-x`, `other::r-x`.
- Historic service properties: `limine-snapper-sync.service` declared `User=root`, `CapabilityBoundingSet=CAP_SYS_ADMIN`, `ProtectHome=yes`.
- Historic error frequency: Journal query for `create subvolume failed ... errno:13` matched **8** entries between `2026-10-16T12:47:26-03:00` and `2026-10-19T08:11:47-03:00`.
- Historic rollback net: `snapper list-configs` returned 0 configs (header only); `stat /.snapshots` failed with No such file or directory.
- Historic candidate mechanism (`[inf]`):
  `limine-snapper-sync.service` runs as root (`User=root`), but its capability bounding set is restricted strictly to `CapabilityBoundingSet=CAP_SYS_ADMIN` (S020). Per `systemd.exec(5)` (S028), capabilities omitted from the bounding set are dropped from the bounding, effective, and permitted sets. Because `CAP_DAC_OVERRIDE` (S027) is not included in `CAP_SYS_ADMIN`, the service lacks the authority to bypass DAC checks. When snapper attempts to execute `btrfs_util_create_subvolume_fd()` to create `/.snapshots`, the kernel VFS layer checks DAC write permissions on `/`. Because `/` has mode `0555` (no write bit), the operation is denied with `EACCES` (`errno: 13`).

### Current Re-Measurement (2026-10-20)
1. **Metadata Invariance:** `/` remains `0555 root:root`. Inode timestamps show:
   - `Modify: 2026-10-03 17:45:33.001630573 -0300`
   - `Change: 2026-10-03 17:45:33.001630573 -0300`
   Metadata has not been altered since the initial system installation on 2026-10-03.
2. **Error Recurrence:** The `errno:13` error count in the journal has advanced from **8 to 9**. The 9th occurrence was recorded at:
   Sanitized inherited event metadata: latest retained create-subvolume failure at `2026-10-19T22:48:24-03:00`, errno 13. Raw journal body and process identity omitted by the integrating L1.
3. **Rollback Net Still Inactive:** `snapper list-configs` remains header-only (0 configurations); `/.snapshots` remains non-existent.

### Epistemic Status: Why the Diagnosis is NOT Proven
Per the contract, this reconnaissance explicitly avoids calling the diagnosis proven. The mechanism remains an inference (`[inf]`) because:
1. **Unexecuted Falsifier:** The non-mutating discriminator proposed in `snapper-eacces-mechanism.md`:
   ```sh
   sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /; echo rc=$?  # predicted rc=1
   sudo test -w /; echo rc=$?  # predicted rc=0
   ```
   requires `sudo` and systemd-run execution, which is strictly prohibited for leaf scout seats and must be performed by the human operator.
2. **No Syscall/Kernel Tracing:** Non-root reconnaissance cannot attach `strace` or kernel eBPF probes to the live daemon to inspect the exact kernel capability evaluation during the `BTRFS_IOC_SUBVOL_CREATE` ioctl.
3. **Interacting Environmental Factors:** While `cat /sys/kernel/security/lsm` demonstrates that SELinux and AppArmor are not active, other system-level configurations (such as Omarchy install script defaults, btrfs subvolume layout assumptions, or landlock rules) remain potential co-factors.
4. **Access vs Ioctl Semantics:** While `access(2)` (S034) explains permitted capability checking for `test -w`, subvolume creation occurs via filesystem ioctls inside `libbtrfsutil`. While both require write authorization on the parent directory, kernel-level path resolution nuance has not been traced end-to-end.

---

## 4. Implications for Round-12 Claims (C1 & C2)

### C1: Closing the Unowned `/` Metadata Census Blind Spot
- `pacman -Qo /` fails with `error: No package owns /` (exit code 1).
- The `filesystem` package mtree (`/var/lib/pacman/local/filesystem-*/mtree`) defines subdirectories but contains 0 entries for the root directory itself (`.`).
- Because `/` is unowned, `pacman -Qkk` is structurally blind to `/` mode or ownership drift.
- The census (`tools/tsukuroi-census.sh`) currently has 0 probes inspecting `/` metadata.
- **C1 Requirement:** Adding a root-directory metadata arm requires discriminating between:
  1. `0755` -> standard expected writable root for owner (PASS)
  2. `0555` -> DAC owner-write restricted root (DEGRADED)
  3. Unreadable / stat error -> BLOCKED / UNKNOWN

### C2: Source-Backed Discriminating EACCES Decision Matrix
The probe data establishes the empirical basis for at least 4 grounded branches in the EACCES decision matrix:
1. **Branch 1 (VFS Mount Protection):** `findmnt` options contain `ro` -> Read-only mount barrier (`EROFS` or caller-wrapped `EACCES`). Remediation: Remount read-write (`mount -o remount,rw /`).
2. **Branch 2 (DAC Mode + Dropped Capability):** `findmnt` options contain `rw`, `stat -c %a /` is `0555` (no `w`), and unit drops `CAP_DAC_OVERRIDE` (e.g. `CapabilityBoundingSet=CAP_SYS_ADMIN`) -> DAC permission denial (`EACCES`, errno 13). Remediation: Adjust DAC mode (`chmod 755 /`) or grant `CAP_DAC_OVERRIDE` to service.
3. **Branch 3 (Collision / Non-Subvolume Target):** Directory `/.snapshots` already exists as a standard directory rather than a btrfs subvolume -> Btrfs collision / conflict (`EEXIST` or subvolume create refusal). Remediation: Remove or migrate existing directory.
4. **Branch 4 (Missing Mount Point / Resolution Failure):** Parent directory unresolvable or missing mount point -> Path lookup failure (`ENOENT`). Remediation: Restore mount point path structure.

---

## 5. Risks and Limits

1. **Host Operability Risk:** Mode `0555` on `/` prevents any process running without `CAP_DAC_OVERRIDE` from creating any file or directory directly under `/`. Daemons running with restricted bounding sets cannot self-initialize top-level directories.
2. **Scope Boundaries:** No files were created, no permissions were altered, and no services were restarted.
3. **Tool Invariance:** All probes utilized standard pre-installed utilities (`coreutils`, `acl`, `util-linux`, `btrfs-progs`, `systemd`). Zero tool installations or upgrades occurred.

---

## 6. Erratum Addendum (2026-10-20, Append-Only)

1. **Correction to "entirely a DAC constraint":**
   - The probe observes DAC mode `0555` alongside mount options `rw` and Btrfs property `ro=false`. While mode `0555` is an independently sufficient DAC barrier to deny writes to callers lacking `CAP_DAC_OVERRIDE`, framing this as "entirely a DAC constraint" overclaims. The measured distinction is between DAC mode bits and VFS mount flags (`rw` vs `ro`), ruling out a read-only filesystem mount. However, whether DAC is the *sole* constraint in all runtime paths cannot be asserted without live capability and kernel syscall tracing.
2. **Correction to "metadata has remained unchanged since initial installation":**
   - Inode timestamps (`Modify: 2026-10-03 17:45:33`, `Change: 2026-10-03 17:45:33`) are point-in-time observational snapshots (`[obs]`). A static ctime/mtime snapshot does not prove an uninterrupted historical continuity (metadata could have been set by imaging tools, restored, or touched by processes that preserved timestamps). The exact origin and historical evolution of `/`'s mode remain `[unknown]`, aligning with the `Origin` seat findings.
3. **Synthesis & Parent Agreement:**
   - Retained as measured facts (`[obs]`): `/` mode `0555`, mount options `rw`, Btrfs property `ro=false`, and base POSIX ACL (no extended entries).
   - Retained as consistent inference (`[inf]`, not proof): the historical subvolume `EACCES` cause via capability bounding. No live runtime capability verification or syscall trace was performed.
   - Observational timestamps stand as recorded point measurements; origin history remains unknown.
4. **Provenance Note on `stat` (Harness Builtin vs GNU coreutils 9.11):**
   - Per Security seat finding P8/S10, the unadorned `stat` command in this harness shell resolves to a shell builtin (`stat 0.8.0`). With an explicit target path `/`, both the builtin and GNU coreutils `/usr/bin/stat` (`coreutils 9.11-2`) produce identical outputs: `mode=555 uid=0 gid=0 filetype=directory` and `555 0 0 directory` (rc=0).
   - However, with empty or missing operands, the builtin defaults to the current working directory (rc=0), whereas GNU `/usr/bin/stat` errors with rc=1 (`cannot statx ''`).
   - Re-verified explicitly with canonical `/usr/bin/stat -c "mode=%a uid=%u gid=%g filetype=%F" /` and `/usr/bin/stat -c "%a %u %g %F" /` (rc=0) to ensure strictly reproducible GNU coreutils evidence.
