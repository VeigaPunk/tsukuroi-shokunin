# RootDirectory / RootImage Path Views vs Proof of Read-Only Mount (`systemd.exec`)

## 1. Axes
- **depth**: Semantic distinction between filesystem view reconfiguration (`pivot_root`/`chroot`/loopback mount) and VFS/superblock read-only mount state (`MS_RDONLY`/`SB_RDONLY`).
- **calibration**: Strict separation between unit root path topology (what represents `/`) and mount permissions (`rw` vs `ro`).
- **operability**: Verified non-privileged read-only commands (`systemctl show`, `findmnt`) without host mutation.
- **coverage**: Detailed evaluation of `RootDirectory=`, `RootImage=`, `RootImageOptions=`, `RootEphemeral=`, `MountAPIVFS=`, and path namespace directives.
- **freshness**: Re-opened against `systemd.exec(5)` (systemd 261.2 / 262.1).
- **adjacency**: Leaf seat write strictly bounded to `.ufo/waves/round-13/correction/RootViews.md`.

## 2. Upstream Systemd Classification & Syntax
- **Section Classification**:
  - `RootDirectory=`, `RootImage=`, and `RootImageOptions=` reside under `.SH "PATHS"` in `systemd.exec(5)`:
    > “The following settings may be used to change a service's view of the filesystem.”
  - Conversely, read-only sandboxing options (`ProtectSystem=`, `ReadOnlyPaths=`, `TemporaryFileSystem=`) reside under `.SH "SANDBOXING"`.
- **`RootDirectory=`**:
  - Sets root directory for executed processes via `pivot_root(2)` or `chroot(2)` relative to host root.
  - Upstream quote: *“Sets the root directory for executed processes, with the pivot_root(2) or chroot(2) system call.”*
- **`RootImage=`**:
  - Mounts a filesystem hierarchy from a block device node or loopback file image as the root directory.
  - Upstream quote: *“mounts a file system hierarchy from a block device node or loopback file instead of a directory.”*
- **Mount Options via `RootImageOptions=`**:
  - `RootImage=` does not intrinsically mount read-only. Mount options are supplied by `RootImageOptions=`:
    > “Takes a comma-separated list of mount options that will be used on disk images specified by RootImage=... For a list of valid mount options, please refer to mount(8).”
  - Writable root images are fully supported, as evidenced by `RootEphemeral=` (*“run in an ephemeral copy of the root directory or root image”*).

## 3. Distinguishing Path View from Proof of Read-Only Mount
- **Path View (Topology / Namespace Rooting)**:
  - Governed by `RootDirectory=`, `RootImage=`, `RootMStack=`.
  - Determines *which* directory tree or disk image represents `/` inside the unit process namespace.
  - Modifying the path view does not alter VFS mount flags (`MS_RDONLY`) or superblock flags (`SB_RDONLY`). A process in a `RootDirectory=` or `RootImage=` on a writable filesystem can write if DAC permits.
- **Proof of Read-Only Mount (VFS / Superblock Enforcement)**:
  - Enforces `EROFS` (S035) on write attempts regardless of DAC permissions or process capabilities.
  - Proved in unit configurations by:
    1. `ProtectSystem=strict` (mounts entire hierarchy read-only except API VFS subtrees `/dev`, `/proc`, `/sys`).
    2. `ReadOnlyPaths=/` (or covering destination path).
    3. `BindReadOnlyPaths=/` or `<src>:/` (explicit unit-private read-only bind mount).
    4. `TemporaryFileSystem=/:ro` (explicit read-only tmpfs mount).
    5. `RootImageOptions=ro` or `RootImageOptions=root:ro` (or Verity protection: `RootHash=`, `RootVerity=`).
    6. Underlying filesystem superblock mounted `ro` (which `ReadWritePaths=` cannot override, S028).

## 4. Interaction with Path Namespaces and Relative Resolution
- When `RootDirectory=` or `RootImage=` is set:
  - `ReadOnlyPaths=`, `ReadWritePaths=`, `InaccessiblePaths=`: Symlinks resolve relative to the unit root. Prefixed with `+`, paths are relative to unit root (*“taken relative to the root directory of the unit, as configured with RootDirectory=/RootImage=”*).
  - `BindPaths=`, `BindReadOnlyPaths=`: Source path refers to host filesystem; destination refers to path below unit root (*“particularly useful when RootDirectory=/RootImage= is used”*).
  - `MountAPIVFS=`: Mounts private API filesystems (`/proc`, `/sys`, `/dev`, `/run`); *“has no effect unless used in conjunction with RootDirectory=/RootImage=”*.

## 5. Refutation of Round-12 Universal & Discriminator B2 Correction
- **Round-12 False Universal**:
  - `root-dac-decision-r12.md` (§ "Current host evidence" line 53, R13 line 86) and JSON B2 claimed:
    *“only strict (or a ReadOnlyPaths= entry covering /) would make / read-only through the unit”*
    while conflating `RootDirectory=` and `RootImage=` with read-only mechanisms in discriminator B2.
- **Correction**:
  - The exclusivity of `strict` over `full` is valid only *among `ProtectSystem=` values* (`full` covers `/usr`, `/boot`, `/efi`, `/etc`, but not `/`).
  - It does not exclude `BindReadOnlyPaths=`, `TemporaryFileSystem=/:ro`, or `RootImageOptions=ro`.
  - `RootDirectory=` and `RootImage=` change the path view, not the mount writability; they can only cause read-only behavior if the redirected target is itself read-only.
  - Host `findmnt /` checks the host mount namespace; if `RootDirectory=` or `RootImage=` were set, host `findmnt /` would evaluate the wrong filesystem.

## 6. Host Observation vs Upstream Capability
- **Observed Unit State [obs]**:
  - `systemctl show -p ProtectSystem -p ReadOnlyPaths -p BindReadOnlyPaths -p TemporaryFileSystem -p RootDirectory -p RootImage limine-snapper-sync.service` exit 0:
    `ProtectSystem=no`, `ReadOnlyPaths=`, `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, `RootImage=`.
  - All alternate path view and sandboxing directives are empty/unset.
- **Observed Host Mount [obs]**:
  - `findmnt -n -o TARGET,FSTYPE,OPTIONS /` exit 0:
    `/ btrfs rw,relatime,compress=zstd:3,ssd,space_cache=v2,subvolid=256,subvol=/@`
- **Analytical Inference [inf]**:
  - Neither path view redirection (`RootDirectory=`/`RootImage=`) nor unit-side read-only sandboxing was configured.
  - The logged `errno:13` was not an `EROFS` failure caused by a read-only mount.

## 7. Tooling & Conformance Record
- **Tool installs/updates**: None needed (standard `systemctl`, `findmnt`, and local `systemd.exec(5)` man page).
- **Write Scope Conformance**: Only `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-13/correction/RootViews.md` modified. No checks, builds, tests, or git commits run.
