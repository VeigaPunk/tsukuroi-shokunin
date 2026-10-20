# ProtectSystem Scope and Documented Exceptions (systemd.exec)

- **Source:** `systemd.exec(5)` man page (systemd 262.1-1 on Arch Linux, man page version / footer dated 2026-02-11 / systemd 262.1; added in version 214).
- **Online Anchor:** https://man.archlinux.org/man/systemd.exec.5 § ProtectSystem=
- **Local Source:** `/usr/share/man/man5/systemd.exec.5.gz` line 1813 (`ProtectSystem=`) under `.SH "SANDBOXING"`.

## 1. Syntax and Parameter Values

`ProtectSystem=` takes a boolean argument (`true`/`false`, `yes`/`no`, `1`/`0`, `on`/`off`) or the special values `"full"` or `"strict"`. Defaults to `off`.

> “Takes a boolean argument or the special values "full" or "strict".”

## 2. Exact Coverage Scope Across Values

| Value | Documented Coverage Scope | Located Quote from `systemd.exec(5)` |
|---|---|---|
| `false` / `no` / `off` | No file system paths are made read-only by this directive. | “Defaults to off.” |
| `true` / `yes` / `1` | Mounts `/usr/` and the boot loader directories (`/boot` and `/efi`) read-only for processes invoked by the unit. | “If true, mounts the /usr/ and the boot loader directories (/boot and /efi) read-only for processes invoked by this unit.” |
| `"full"` | Mounts `/usr/`, `/boot`, `/efi`, and `/etc/` read-only. Does **not** mount `/` read-only. | “If set to "full", the /etc/ directory is mounted read-only, too.” |
| `"strict"` | Mounts the **entire file system hierarchy** read-only, except for API file systems and explicitly excluded directories. | “If set to "strict" the entire file system hierarchy is mounted read-only, except for the API file system subtrees /dev/, /proc/ and /sys/” |

## 3. Documented Exceptions and Exclusions for `ProtectSystem=strict`

When `ProtectSystem=strict` mounts the hierarchy read-only, the man page explicitly specifies multiple exceptions, exclusions, and interactions:

### A. Excluded API File Systems
- `/dev/`, `/proc/`, and `/sys/` are explicitly excluded from being mounted read-only by `ProtectSystem=strict`.
- *Source Quote:* “except for the API file system subtrees /dev/, /proc/ and /sys/ (protect these directories using PrivateDevices=, ProtectKernelTunables=, ProtectControlGroups=).”

### B. Explicit Unit Path Exclusions via Allow-Listing Directives
- **`ReadWritePaths=`**:
  - *Source Quote:* “If this option is used, ReadWritePaths= may be used to exclude specific directories from being made read-only.”
  - Also in `ReadOnlyPaths=` section: “Use ReadWritePaths= in order to allow-list specific paths for write access if ProtectSystem=strict is used.”
  - *Superblock Limit:* “Note that ReadWritePaths= cannot be used to gain write access to a file system whose superblock is mounted read-only.”
- **Standard Unit Directories**:
  - *Source Quote:* “Similar, StateDirectory=, LogsDirectory=, ... and related directory settings (see below) also exclude the specific directories from the effect of ProtectSystem=.”
  - Covers `RuntimeDirectory=`, `StateDirectory=`, `CacheDirectory=`, `LogsDirectory=`, `ConfigurationDirectory=`.

### C. Private Temporary Directory Exemption
- When combined with `PrivateTmp=true`, `/tmp/` and `/var/tmp/` remain writable.
- *Source Quote:* “Note that if ProtectSystem= is set to "strict" and PrivateTmp= is enabled, then /tmp/ and /var/tmp/ will be writable.”

### D. IPC / UNIX Domain Socket Non-Restriction
- *Source Quote:* “Note that the various options that turn directories read-only (such as ProtectSystem=, ReadOnlyPaths=, ...) do not affect the ability for programs to connect to and communicate with AF_UNIX sockets in these directories. These options cannot be used to lock down access to IPC services hence.”

### E. Container / Kernel Namespace / Service Manager Dependencies
- *Source Quote:* “ProtectSystem= has no effect if the kernel is built without file system namespacing or if the service manager runs in a container manager that makes file system namespacing unavailable to its payload.”
- *Source Quote:* “Specifically, the various settings requiring file system namespacing support (such as ProtectSystem=) are not available, as the underlying kernel functionality is only accessible to privileged processes. However, most namespacing settings, that will not work on their own in user services, will work when used in conjunction with PrivateUsers=true.”

## 4. Impact on Root-Level Read-Only Claims (R13 Correction)

1. **`ProtectSystem=full` does NOT make `/` read-only**:
   - It only covers `/usr/`, `/boot`, `/efi`, and `/etc/`. Any claim that `ProtectSystem=full` mounts `/` read-only is false.
2. **`ProtectSystem=strict` vs Alternative Unit Mechanisms**:
   - While `ProtectSystem=strict` mounts the hierarchy read-only (subject to API subtrees and allow-listed paths like `ReadWritePaths=`, `StateDirectory=`, and `PrivateTmp=`), it is **not the exclusive mechanism** that can make `/` or paths under `/` read-only.
   - Alternatives include `ReadOnlyPaths=/`, `BindReadOnlyPaths=`, `TemporaryFileSystem=` with `:ro`, or path-view alterations via `RootDirectory=` / `RootImage=`.
   - Therefore, a statement claiming that *only* `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit is a false universal; the correct statement must be restricted to comparison *among ProtectSystem values*.
