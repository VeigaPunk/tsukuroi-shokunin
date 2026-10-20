# TemporaryReadonly — systemd.exec TemporaryFileSystem Investigation

- **Seat:** `TemporaryReadonly` (scout)
- **Target:** Open `systemd.exec(5)` `TemporaryFileSystem=` section; locate `ro` option example and its limits.
- **Source Reopened:** `systemd.exec(5)` (Arch manual pages, `https://man.archlinux.org/man/systemd.exec.5.en.txt`, systemd 262.1).

---

## 1. Verbatim Source Excerpt: `TemporaryFileSystem=` Section

From `systemd.exec(5)` § `SANDBOXING` > `TemporaryFileSystem=`:

```text
       TemporaryFileSystem=
           Takes a space-separated list of mount points for temporary file
           systems (tmpfs). If set, a new file system namespace is set up for
           executed processes, and a temporary file system is mounted on each
           mount point. This option may be specified more than once, in which
           case temporary file systems are mounted on all listed mount points.
           If the empty string is assigned to this option, the list is reset,
           and all prior assignments have no effect. Each mount point may
           optionally be suffixed with a colon (":") and mount options such as
           "size=10%" or "ro". By default, each temporary file system is
           mounted with "nodev,strictatime,mode=0755". These can be disabled
           by explicitly specifying the corresponding mount options, e.g.,
           "dev" or "nostrictatime".

           This is useful to hide files or directories not relevant to the
           processes invoked by the unit, while necessary files or directories
           can be still accessed by combining with BindPaths= or
           BindReadOnlyPaths=:

           Example: if a unit has the following,

               TemporaryFileSystem=/var:ro
               BindReadOnlyPaths=/var/lib/systemd

           then the invoked processes by the unit cannot see any files or
           directories under /var/ except for /var/lib/systemd or its
           contents.

           This option is only available for system services, or for services
           running in per-user instances of the service manager in which case
           PrivateUsers= is implicitly enabled (requires unprivileged user
           namespaces support to be enabled in the kernel via the
           "kernel.unprivileged_userns_clone=" sysctl).

           Added in version 238.
```

Additional cross-reference from `systemd.exec(5)` § `BindPaths=, BindReadOnlyPaths=`:
```text
           Note that the destination directory must exist or systemd must be
           able to create it. Thus, it is not possible to use those options
           for mount points nested underneath paths specified in
           InaccessiblePaths=, or under /home/ and other protected directories
           if ProtectHome=yes is specified.  TemporaryFileSystem= with ":ro"
           or ProtectHome=tmpfs should be used instead.
```

---

## 2. Located `ro` Option Example

- **Verbatim unit directive:**
  ```ini
  TemporaryFileSystem=/var:ro
  BindReadOnlyPaths=/var/lib/systemd
  ```
- **Syntax mechanism:** The mount point path is suffixed with a colon and mount options string: `path[:options]`. Passing `:ro` mounts the underlying `tmpfs` read-only.
- **Combined behavior:** Hides host contents under the specified path behind an empty, read-only `tmpfs`, while selective subtrees can be re-exposed read-only via `BindReadOnlyPaths=` (or writable via `BindPaths=`).

---

## 3. Limits and Constraints of `TemporaryFileSystem=` and `:ro`

1. **Unit-Private Mount Namespace Isolation:**
   - Setting `TemporaryFileSystem=` allocates a new Linux mount namespace (`CLONE_NEWNS`) for the executed processes.
   - Any `tmpfs` mounted by `TemporaryFileSystem=` exists strictly inside the unit's private mount namespace.
   - It is completely **invisible to host-level inspection tools** (such as `findmnt` executed in the default/host mount namespace).
2. **Reset Semantics:**
   - Assigning an empty string (`TemporaryFileSystem=`) resets the list entirely; all prior assignments have no effect.
3. **Availability and Privilege Requirements:**
   - Only available for system services, or for per-user service manager instances when `PrivateUsers=` is implicitly enabled (which requires unprivileged user namespaces enabled via sysctl `kernel.unprivileged_userns_clone=`).
4. **Hiding Semantics vs InaccessiblePaths:**
   - Unlike `InaccessiblePaths=` (which strictly forbids nesting `BindPaths=`, `BindReadOnlyPaths=`, or `ReadWritePaths=`), `TemporaryFileSystem=...:ro` creates a clean mountpoint upon which sub-mounts can be nested.
5. **Impact on Root Exclusivity Claims (Refuting False Universal):**
   - A unit directive such as `TemporaryFileSystem=/:ro` (or mounting over path prefixes) can create a read-only filesystem environment for the unit without configuring `ProtectSystem=strict` or `ReadOnlyPaths=/`.
   - Therefore, assertions claiming that **only** `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit are demonstrably false.

---

## 4. Bounded Source Anchors and Quotes

- **Source ID:** Reopened via `systemd.exec(5)` (Arch manual pages 2026-02 / systemd 262.1, S028 / candidate S041).
- **Exact quote (<=25 words):**
  > "Each mount point may optionally be suffixed with a colon (\":\") and mount options such as \"size=10%\" or \"ro\"."
- **Example quote (<=25 words):**
  > "TemporaryFileSystem=/var:ro BindReadOnlyPaths=/var/lib/systemd then the invoked processes by the unit cannot see any files or directories under /var/ except"

---

## 5. Tooling and Conformance Record

- **Tool installs/updates:** None needed; standard system tools and URL reader were sufficient.
- **Write Scope Conformance:** Only assigned report path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-13/correction/TemporaryReadonly.md` modified. No tests, linters, git commits, or external mutation executed.
