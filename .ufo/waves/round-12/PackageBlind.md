# Package Blind Spot: Package Ownership and Mtree Root Entry Inspection

**Role:** UFO-FSD scout (`PackageBlind`)  
**Lane milestone:** round-12  
**Target:** Reproduce package ownership blind spot with `pacman -Qo /` and filesystem package mtree root entry bounded inspection. No full `-Qkk`. Establish why existing package sample cannot certify `/`. Record exact command/output rc and counterexamples (file itself vs parent metadata).  
**Judged on:** operability, depth  
**Status:** COMPLETE (grounded host and package db observations; no unsupported PASS)  

---

## 1. Summary of Findings

1. **Package Ownership Blind Spot (`pacman -Qo /`):**
   `pacman -Qo /` exits with code `1` and emits `error: No package owns /` on stderr. In ALPM/pacman, all package file entries in `/var/lib/pacman/local/<pkg>/files` are recorded relative to root without a leading slash (`bin`, `boot/`, `etc/`). Neither `/` nor `.` exists in any installed package filelist. Even canonicalized paths `pacman -Qo /.`, `pacman -Qo /..` exit `1` with `error: No package owns <path>`.

2. **Filesystem Package Mtree Root Entry Omission:**
   Bounded inspection of `/var/lib/pacman/local/filesystem-2025.10.12-1/mtree` (gzip-compressed BSD mtree format, 137 lines, 68 directories) reveals that **0** entries exist for `.` or `./` (`zcat ... | grep -cE '^\./?[[:space:]]'` returns `0`, exit code `1`). Furthermore, inspection of the distribution package archive in the pacman cache (`/var/cache/pacman/pkg/filesystem-2025.10.12-1-any.pkg.tar.zst`) confirms that this package artifact lacks an entry for `.` or `./`. [Qualification] This observation is bounded to the installed/cached `filesystem-2025.10.12-1` artifact; it is not proof that `makepkg` universally omits `pkgdir` root across all packages or tooling versions.

3. **Inability of Existing Package Sample to Certify `/`:**
   In `tools/tsukuroi-census.sh`, the package health arm samples the first `SAMPLE_N=8` packages from `pacman -Qq` (`1password-beta`, `1password-cli`, `7zip`, `aalib`, `abseil-cpp`, `acl`, `adwaita-cursors`, `adwaita-fonts`). `filesystem` is not in this sample. However, even if `filesystem` is explicitly tested (`pacman -Qkk filesystem`), `pacman -Qkk` only iterates over entries present in `mtree`. Because `/` is omitted from `mtree`, `pacman -Qkk` never stats, checks, or reports on `/`.
   On this live host, `/` is currently mode `0555` (`dr-xr-xr-x 0 0 /`). When `pacman -Qkk filesystem` is executed, it checks 127 child files and reports 8 altered files (`/boot` permissions mismatch and 7 unreadable/symlink files); **`/` is neither counted in the 127 total files nor flagged as altered**. The finding is isolated unowned root omission: pacman does not observe `/` at all, regardless of whether child files pass or drift.

4. **File Itself vs Parent Metadata (Counterexamples):**
   Verifying child files under `/` (e.g. `/bin`, `/boot`, `/etc`, `/usr`) tests child inode metadata (`st_mode`, `st_uid`, `st_size`, checksum). It does NOT and CANNOT test parent directory metadata (`/`'s inode mode `0555`). Under POSIX `path_resolution(7)`, child path traversal requires execute (`+x`) on `/`, which succeeds under `0555`, even while write (`+w`) permission on `/` is absent. [Qualification] Mode `0555` combined with dropped `CAP_DAC_OVERRIDE` is a source-grounded consistent explanation for `limine-snapper-sync.service` `errno: 13`; no live service restart, strace, or syscall interception was run this round under non-mutation constraints.
---

## 2. Reproduction of Package Ownership Blind Spot (`pacman -Qo`)

### 2.1 Exact Command and Output: Root Directory Query

Probing ownership of `/` on host `plazir27` (Arch Linux x86_64, kernel 7.2.3-arch1-3):

```bash
pacman -Qo /
```
- **Stdout:** *(empty)*
- **Stderr:** `error: No package owns /`
- **Exit code:** `1`

Testing variations with trailing dots/canonicalization:
```bash
pacman -Qo /.
# stderr: error: No package owns /.
# exit code: 1

pacman -Qo /..
# stderr: error: No package owns /..
# exit code: 1
```

### 2.2 Contrast with Direct Child Directories

In contrast to `/`, every primary directory created directly under `/` is registered in ALPM:

| Query Command | Exit Code | Reported Package Ownership |
|---|---|---|
| `pacman -Qo /bin` | `0` | `/bin is owned by filesystem 2025.10.12-1` |
| `pacman -Qo /boot` | `0` | `/boot is owned by filesystem 2025.10.12-1` |
| `pacman -Qo /dev` | `0` | `/dev is owned by filesystem 2025.10.12-1` |
| `pacman -Qo /etc` | `0` | `/etc/ is owned by alsa-plugins ... filesystem 2025.10.12-1` (116 packages) |
| `pacman -Qo /usr` | `0` | `/usr/ is owned by filesystem 2025.10.12-1` (11 packages) |
| `pacman -Qo /var` | `0` | `/var/ is owned by filesystem 2025.10.12-1` (17 packages) |
| `pacman -Qo /` | **`1`** | `error: No package owns /` |

### 2.3 ALPM Implementation Mechanism

In `libalpm` (the ALPM library driving `pacman`):
- Package database file `/var/lib/pacman/local/<pkg>/files` stores paths relative to target root, stripped of leading slashes.
- For example, `/var/lib/pacman/local/filesystem-2025.10.12-1/files` begins with:
  ```
  %FILES%
  bin
  boot/
  dev/
  etc/
  ...
  ```
- When `pacman -Qo <path>` queries `alpm_filelist_contains()`, the queried path `/` canonicalizes to `""` or `"/"`.
- A bounded sweep over the local package database proves that **zero** packages contain an entry for `""`, `"."`, or `"/"`:
  ```bash
  find /var/lib/pacman/local -name files -exec grep -l -E '^(\.|\/)$' {} + 2>/dev/null
  # stdout: (empty)
  # exit code: 0
  ```
- Result: `/` is strictly outside ALPM's file ownership namespace.

---

## 3. Bounded Inspection of `filesystem` Package Metadata

### 3.1 Package Identification and File Inventory

- Installed package: `filesystem 2025.10.12-1` (`pacman -Q filesystem`, exit code 0).
- Local ALPM DB directory: `/var/lib/pacman/local/filesystem-2025.10.12-1/`.
- Contents of directory:
  - `desc` (337 bytes)
  - `files` (3,042 bytes, 148 lines)
  - `mtree` (2,396 bytes gzip-compressed data)

### 3.2 Bounded Mtree Inspection

Uncompressing and inspecting the local package mtree:
```bash
zcat /var/lib/pacman/local/filesystem-2025.10.12-1/mtree | head -n 12
```
Output:
```
#mtree
/set type=file uid=0 gid=0 mode=755
./.BUILDINFO time=1760286101.0 mode=644 size=5270 sha256digest=be37048f773d7a7ac03041220a96fb8cae8a13360d9f7a0ae8fa0eebaa03a2d8
./.PKGINFO time=1760286101.0 mode=644 size=694 sha256digest=78614f076659fda0c613ce7123f1d0e02a1b327b9d5aa22f7cdf39672fc1fb32
./bin time=1760286101.0 mode=777 type=link link=usr/bin
./lib time=1760286101.0 mode=777 type=link link=usr/lib
./lib64 time=1760286101.0 mode=777 type=link link=usr/lib
./sbin time=1760286101.0 mode=777 type=link link=usr/bin
./boot time=1760286101.0 type=dir
./dev time=1760286101.0 type=dir
/set mode=644
./etc time=1760286101.0 mode=755 type=dir
```

Mtree structural measurements:
- Total lines: `137` (`zcat .../mtree | wc -l`)
- Declared directory entries (`type=dir`): `68` (`zcat .../mtree | grep -c 'type=dir'`)
- Root directory entries matching `.` or `./`:
  ```bash
  zcat /var/lib/pacman/local/filesystem-2025.10.12-1/mtree | grep -cE '^\./?[[:space:]]'
  # stdout: 0
  # exit code: 1
  ```

### 3.3 Original Distribution Archive Inspection

Inspecting the cached binary package archive:
```bash
bsdtar -tf /var/cache/pacman/pkg/filesystem-2025.10.12-1-any.pkg.tar.zst | grep -E '^(\.|\./)$'
# stdout: (empty)
# exit code: 1
```
The tarball contains `.BUILDINFO`, `.MTREE`, `.PKGINFO`, `bin -> usr/bin`, `boot/`, `dev/`, `etc/`, etc. Neither `.` nor `./` is an archive member.

[Qualification] This bounded observation applies specifically to the local cached `filesystem-2025.10.12-1-any.pkg.tar.zst` artifact. The lack of a root entry in this artifact is not proof that `makepkg` universally omits the `pkgdir` root entry across all Arch packages, PKGBUILD designs, or makepkg versions.

---

## 4. Why the Existing Package Sample Cannot Certify `/`

### 4.1 Census Package Sampling Logic

In `tools/tsukuroi-census.sh` (lines 551–585):
```bash
mapfile -t names < <(printf '%s\n' "$CAP_OUT" | grep -v '^[[:space:]]*$' | head -n "$SAMPLE_N")
cap "$PACMAN" -Qkk "${names[@]}"
```
Where `$CAP_OUT` is generated from `pacman -Qq`.

1. **Default Sample Membership:**
   By default, `SAMPLE_N=8`. The first 8 packages returned by `pacman -Qq` are:
   `1password-beta`, `1password-cli`, `7zip`, `aalib`, `abseil-cpp`, `acl`, `adwaita-cursors`, `adwaita-fonts`.
   `filesystem` is package index 278 (`pacman -Qq | grep -n '^filesystem$'` -> `278:filesystem`). It is never included in the default 8-package sample.

2. **Domain Incompleteness of `pacman -Qkk`:**
   Even if `--sample` is enlarged or `filesystem` is tested explicitly:
   `pacman -Qkk` iterates strictly over the records defined in `.MTREE` (`alpm_pkg_mtree_open()` / `alpm_pkg_mtree_next()`). Because `/` is not an entry in `.MTREE`, `pacman -Qkk` never stats `/`.

### 4.2 Empirical Verification on Live Host

On host `plazir27`:
- Current stat of `/`:
  ```bash
  stat -c "%a %A %u %g %n" /
  # 555 dr-xr-xr-x 0 0 /
  ```
  Expected baseline mode on Arch Linux: `0755` (`drwxr-xr-x`).
- Running bounded `-Qkk` on `filesystem`:
  ```bash
  pacman -Qkk filesystem
  ```
  Output:
  ```
  warning: filesystem: /boot (Permissions mismatch)
  warning: filesystem: /etc/crypttab (failed to calculate SHA256 checksum)
  warning: filesystem: /etc/gshadow (failed to calculate SHA256 checksum)
  warning: filesystem: /etc/resolv.conf (File type mismatch)
  warning: filesystem: /etc/shadow (failed to calculate SHA256 checksum)
  warning: filesystem: /usr/share/factory/etc/crypttab (failed to calculate SHA256 checksum)
  warning: filesystem: /usr/share/factory/etc/gshadow (failed to calculate SHA256 checksum)
  warning: filesystem: /usr/share/factory/etc/shadow (failed to calculate SHA256 checksum)
  ... [backup file lines] ...
  filesystem: 127 total files, 8 altered files
  ```
  - `127 total files` corresponds to the 127 path entries in `files`/`mtree`.
  - **`/` is NOT in the 127 total files.**
  - **`/` is NOT in the 8 altered files.**
  - **Zero warnings are printed for `/`.**
  - [Observed & Qualified] On this live host, child verification is *not* 100% healthy: `pacman -Qkk filesystem` found 8 altered child files. Crucially, however, none of those 8 reports relates to `/`. This isolates the unowned root omission: pacman evaluates child entries, but has no entry or check for `/` itself. Even if all child files were unaltered, pacman would report healthy child status while `/` remained `0555`.

Conclusion: Neither the bounded 8-package sample nor a full `pacman -Qkk filesystem` run can certify `/`. Pacman has zero observational capability over root directory metadata due to unowned root omission.

---

## 5. Counterexamples: File Itself vs Parent Metadata

Verifying children (files and subdirectories under `/`) cannot certify the parent directory (`/`). The underlying POSIX and Linux filesystem mechanics demonstrate this structural separation across five dimensions:

### Counterexample A: DAC Search vs Directory Write (`path_resolution(7)`)
- **Mechanism:** According to `path_resolution(7)`, looking up an existing file like `/etc/passwd` or `/bin/sh` requires execute (`search`, `+x`) permission on every ancestor directory in the path (`/` and `/etc`). It does **not** require read (`+r`) or write (`+w`) permission on `/`.
- **Observation under mode 0555 (`dr-xr-xr-x`):**
  - Search (`+x` on `/`): `S_IXUSR | S_IXGRP | S_IXOTH` are all set. Traversal succeeds.
  - Read (`+r` on `/`): `S_IRUSR | S_IRGRP | S_IROTH` are all set. Directory listing succeeds.
  - Write (`+w` on `/`): Cleared for all (`0555`).
- **Counterexample Effect:**
  - `pacman -Qkk` traverses through `/` to stat, open, read, and calculate SHA256 checksums on all installed files. The traversal and search checks succeed because `/` has execute permission (`0555`).
  - In contrast, creating directory entries directly under `/` (e.g., `mkdir /.snapshots`, `btrfs subvolume create /.snapshots`) requires write (`+w`) on `/`.
  - [Qualification] The correlation between mode `0555` and `limine-snapper-sync.service` `errno: 13` (where `CapabilityBoundingSet=CAP_SYS_ADMIN` drops `CAP_DAC_OVERRIDE`) is a source-grounded consistency inference (`[inf]`). No service restarts, `strace`, or live syscall interception were run this round under host non-mutation rules.
  - [Child status qualification] On this host, child verification is not 100% clean (8 altered child files were observed). The core counterexample is that child path verification evaluates child inodes, completely omitting parent directory write capability.

### Counterexample B: Inode Structural Isolation (Parent Inode vs Child Inode)
- **Mechanism:** In Linux filesystems (ext4, Btrfs, xfs), each file and directory is represented by a separate inode:
  - Parent directory `/`: Inode `256` (on Btrfs root subvolume), `st_mode = 0555` (`dr-xr-xr-x`).
  - Child directory `/etc`: Inode `264`, `st_mode = 0755` (`drwxr-xr-x`).
  - Child symlink `/bin`: Inode `318`, `st_mode = 0777` (`lrwxrwxrwx`).
  - Child directory `/boot`: Inode `257`, `st_mode = 0755` (`drwxr-xr-x`).
- **Counterexample Effect:**
  - Stating `/bin`, `/boot`, or `/etc` returns the `struct stat` for inodes 318, 257, and 264.
  - Directory entries inside `/` map names to child inode numbers. There is zero inheritance or propagation of mode bits from parent inode 256 to child inodes.
  - Altering `/`'s mode (e.g. `chmod 0555 /`) does not modify a single byte or bit in child inodes.
  - Any verification tool that queries child paths observes only child inode metadata, remaining 100% blind to the parent inode.

### Counterexample C: ALPM Package Boundary (Owned Child vs Unowned Parent)
- **Mechanism:** ALPM tracks integrity strictly by comparing on-disk filesystem state against receipt manifests (`.MTREE` / `desc` / `files`).
- **Counterexample Effect:**
  - `/bin` is owned by `filesystem 2025.10.12-1` (`pacman -Qo /bin` -> rc 0).
  - `/` is owned by no package (`pacman -Qo /` -> rc 1).
  - Pacman's domain model defines "drift" as divergence between observed state and declared state for owned objects. Because `/` has no declared state in ALPM, drift cannot be computed, reported, or conceived within the pacman verification engine.

### Counterexample D: Unlink / Creation Asymmetry vs Leaf Content Modification
- **Mechanism:** In POSIX filesystem semantics:
  - Modifying the contents of a file (e.g., `/etc/issue`) requires write permission on that file's inode (`S_IWUSR`). It does not require write permission on `/etc` or `/`.
  - Creating a file in a directory (e.g., `touch /new_file`) or removing a file (e.g., `unlink /file`) requires write and search permission on the parent directory inode (`/`). It does not depend on child file permissions.
- **Counterexample Effect:**
  - If parent directory `/` is `0555`, no file can be created or unlinked in `/`.
  - Package integrity tools evaluate file content modification (hashes and leaf permissions). They never test parent directory mutation invariants.

### Counterexample E: Reinstallation Ineffectiveness Hypothesis (`pacman -S filesystem`)
- **Mechanism:** In theory, package reinstallation can repair permission drift on owned files when archive members are unpacked.
- **Counterexample Effect:**
  - In the inspected cached archive (`filesystem-2025.10.12-1-any.pkg.tar.zst`), there is no entry for `./` (only `bin`, `boot/`, `etc/`, etc.).
  - [Qualification / Not executed] Host non-mutation rules strictly forbid running package transactions (`pacman -S`). Reinstalling `filesystem` was **not executed** on this host. The claim that reinstalling `filesystem` would not restore `/` from `0555` to `0755` is an architectural inference based on the missing archive root entry and libarchive extraction semantics, not an executed empirical test. It must not be reported as guaranteed runtime behavior.

---

## 6. Operational Risks & Census Implementation Implications

### 6.1 Operational Risk Matrix for Root Directory Mode

| Root Mode | Search (`+x`) | List (`+r`) | Write (`+w`) | Normal Root User | Bounded Root Service (`CAP_SYS_ADMIN`) | Unprivileged User (`vgpnk`) | `pacman -Qkk` Child Behavior | OS Impact |
|---|---|---|---|---|---|---|---|---|
| `0755` | Yes | Yes | Yes (owner) | Pass | Pass (DAC owner write) | Read/traverse only | Evaluates children only | Normal operating state |
| `0555` | Yes | Yes | **No** | Pass (via `CAP_DAC_OVERRIDE`) | **FAIL (`EACCES` / errno 13) [inf]** | Read/traverse only | **Blind spot: evaluates children only (8 altered here; 0 on /)** | Snapper / limine snapshot creation fails; `/` read-only for bounded services |
| `0700` | Yes | Yes | Yes (owner) | Pass | Pass | **FAIL (`EACCES`) on all paths** | Evaluates children only (passes when run as root) | Catastrophic: all user logins, graphical session, user services blocked |
| `0000` / unreadable | No | No | No | Pass (via `CAP_DAC_OVERRIDE`) | **FAIL (`EACCES`) [inf]** | **FAIL (`EACCES`)** | Blocked/Permission denied on children | System unusable |

*[inf] Qualification: Service EACCES under CapabilityBoundingSet=CAP_SYS_ADMIN is a source-grounded consistency inference (S020, S027, S028, S034); no service restart or live syscall probe was run this round under non-mutation constraints.*

### 6.2 Implications for Tsukuroi Round 12 Census (C1)

To close this blind spot, the tsukuroi host census (`tools/tsukuroi-census.sh`) cannot rely on `pacman -Qkk` or ALPM queries:
1. **Explicit Root Directory Inode Probe:**
   The census must independently probe root directory metadata via `stat`:
   ```bash
   stat -c '%a %u %g' "$TSUKUROI_ROOT_DIR"  # defaults to /
   ```
2. **Discrimination Logic:**
   - Mode `0755`, UID `0`, GID `0` -> HEALTHY root metadata.
   - Mode `0555`, UID `0`, GID `0` -> DEGRADED (identifies the specific `0555` write-inhibition state responsible for Snapper `errno: 13`).
   - Mode != `0755` and != `0555` (e.g. `0700`, `0750`) -> DEGRADED.
   - Root unreadable, nonexistent, or stat failure -> BLOCKED.
3. **Plane Integration:**
   Appending `root_mode=`, `root_uid=`, `root_gid=` to `PLANE packages` note or update-safety note directly closes the unowned metadata census blind spot (advancing root metadata findings from 0 to 1).

---

## 7. Contract Keys and Evidence Sources

- **source:** live host probes on `plazir27` (`pacman -Qo`, `pacman -Qkk`, `stat`, `bsdtar`, `zcat`), ALPM package db `/var/lib/pacman/local/filesystem-2025.10.12-1/`, pacman cache `/var/cache/pacman/pkg/filesystem-2025.10.12-1-any.pkg.tar.zst`, `tools/tsukuroi-census.sh`, S027 `capabilities(7)`, S028 `systemd.exec(5)`, S034 `access(2)`, `path_resolution(7)`.
- **verified-at:** 2026-10-19T23:35:00Z.
- **recheck:** on-release; procedure: `pacman -Qo /; zcat /var/lib/pacman/local/filesystem-*/mtree | grep -cE '^\./?[[:space:]]'; stat -c '%a %u %g' /; pacman -Qkk filesystem`.
- **tags:** `[obs]` for all command outputs, exit codes, line counts, and host filesystem states; `[inf]` for ALPM domain boundaries and POSIX capability/DAC interactions.
