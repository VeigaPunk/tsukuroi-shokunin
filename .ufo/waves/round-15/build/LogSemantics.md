> L1 durability note (round15): this completed seat claimed a report path, but the final inventory found it absent. The following is the seat's complete returned text recovered verbatim from agent://TsukuroiR15.LogSemantics; advisory content, not final verification. No new seat was dispatched.

# LogSemantics Research: pacman(8) Log Transaction vs Package Installed State

**Seat:** `TsukuroiR15.LogSemantics` (scout)  
**Judged on:** depth  
**Axis:** depth (grounded structural distinction between historical transactional log records, database state, on-disk filesystem state, and unmeasured process runtime mappings)  
**Read-only contract held:** All findings derived purely from reading manual pages (`pacman(8)`, `pacman.conf(5)`) and committed corpus notes/records. Zero host commands, live queries, network fetches, package actions, or service queries were executed.

---

## 1. Primary Evidence: pacman(8) and pacman.conf(5) Specifications

From the installed Pacman manual page (`pacman(8)`, Pacman 7.1.0, dated 2026-05-06):
1. **Description & Scope:**
   - *"Pacman is a package management utility that tracks installed packages on a Linux system... Since version 3.0.0, pacman has been the front-end to libalpm(3), the 'Arch Linux Package Management' library."*
   - Package tracking is maintained within a local database (default `/var/lib/pacman/local`).
2. **Operations vs State:**
   - **`-Q, --query`**: Operates on the local package database (`/var/lib/pacman/local/`) to inspect what is currently recorded as installed, package metadata, dependencies, and file manifests (`-Ql`, `-Qk`).
   - **`-S, --sync` / `-U, --upgrade` / `-R, --remove`**: Execute state transitions on packages, downloading/unpacking archives, running scriptlets/hooks, and committing changes to the database.
   - **`--logfile <file>`** (and `pacman.conf(5)` `LogFile = /var/log/pacman.log`):
     Pacman appends operational messages to the log file via `libalpm`. This is an append-only transaction journal.
3. **Transaction Mechanics & Edge Cases:**
   - **`--dbonly`**: *"Adds/removes the database entry only, leaving all files in place."*
     - *Implication:* Pacman can record a package install or upgrade in the database and log without altering files on disk.
   - **Handling Config Files (`.pacnew` / `.pacsave`):**
     - Three-way MD5 hashing determines whether a config file is overwritten, retained, or written as `.pacnew` / saved as `.pacsave`.
     - The log records notices (e.g. `[ALPM] warning: /etc/locale.gen installed as /etc/locale.gen.pacnew`). The log notes the historical event, but *does not* reflect whether the operator subsequently merged, renamed, or deleted the file.

---

## 2. Structural Differentiation: Log Transaction vs Package Installed State

From the corpus doctrine (`pacnew-plane.md`, `update-safety-note.md`, `package-state-plane.md`, `closeout-r11.md`, `aur-risk-plane.md`, and `degraded-triage-r4.md`), four decoupled tiers of state must never be conflated:

### Tier 1: Log Transaction Record (`/var/log/pacman.log`)
- **Nature:** Append-only event history / audit trail.
- **Content:**
  - `[PACMAN] Running 'pacman ...'`: The exact CLI invocation executed by a user or script.
  - `[ALPM] synchronizing package lists`: Database sync attempt.
  - `[ALPM] installed <pkg> (<ver>)` / `[ALPM] upgraded <pkg> (<old> -> <new>)` / `[ALPM] removed <pkg> (<ver>)`: libalpm hook and package commitment events.
  - `[ALPM] running '<hook>'`: Hook executions.
- **Semantics & Limits:**
  - Historical only: An entry indicates what transaction transpired at timestamp $T$.
  - It does **not** assert that the files currently exist on disk or match package checksums.
  - Absence from a bounded log window (e.g. `TSUKUROI_LOG_TAIL_N`) does not prove a package was never installed; log rotation (`logrotate`) or truncation alters log history independently of database state.
  - In `pacnew-plane.md`, the log records historical warning events (`installed as .pacnew`), while `find /etc` is required to ascertain whether those files are still present on the filesystem.

### Tier 2: ALPM Local Database State (`/var/lib/pacman/local/<pkg>-<ver>/`)
- **Nature:** The current package authority according to `pacman -Q`.
- **Content:**
  - Directory entries containing `desc`, `files`, `mtree`, `install`.
- **Semantics & Limits:**
  - Certifies what `pacman` believes is installed on the host.
  - If a transaction is aborted, rolled back via filesystem snapshots, or modified out-of-band (e.g., via `--dbonly`, manual file extraction, or file corruption), database state can diverge from the filesystem.

### Tier 3: Filesystem Inode State (`/usr/bin/*`, `/usr/lib/*.so`, `/etc/*`)
- **Nature:** Actual files present on the storage volume.
- **Content:** Concrete binary executables, shared library inodes, configuration files.
- **Semantics & Limits:**
  - Verified only via filesystem queries (`pacman -Qk`, `pacman -Qkk`, `stat`, `sha256sum`, `find`).
  - When `pacman` upgrades a shared library (`unlink(2)` followed by writing a new file/inode), the on-disk directory points to the new inode.

### Tier 4: Runtime Memory Mappings (`/proc/<pid>/maps`, running processes)
- **Nature:** Process virtual memory address spaces.
- **Semantics & Limits:**
  - Under Linux VFS and ELF dynamic linking, processes that already mapped an older `.so` (`MAP_PRIVATE`) continue executing from the *unlinked, deleted inode*.
  - A log line `[ALPM] upgraded libinput (1.31.3-1 -> 1.32.0-1)` proves that the filesystem and database were updated. It provides **zero evidence** that running desktop sessions (e.g., Hyprland, Xwayland) are executing the upgraded version. In fact, long-running processes retain the old binary until restarted.

---

## 3. Analysis of Incident & Partial-Upgrade Implications

Applying these semantics to the 2026-10-20 partial upgrade incident (`pacman.log:2429`):
1. **Logged Transaction (`pacman.log:2429-2436`):**
   - Command: `pacman -S --needed --noconfirm libinput libinput-tools` at `2026-10-20T04:25:16-0300`.
   - ALPM events: `upgraded libinput (1.31.3-1 -> 1.32.0-1)` and `installed libinput-tools (1.32.0-1)`.
   - Sync marker context: Preceding sync was `2026-10-18T14:11:00-0300` (`pacman.log:2288`).
2. **Local DB State vs Sync DB State:**
   - Local DB records `libinput 1.32.0-1` as installed.
   - Sync DB (born 2026-10-18) also lists `1.32.0-1`, so `pacman -Qu` does not list `libinput` as pending.
   - However, the host is ~413 packages behind its sync DB (including `mkinitcpio`, `linux`, `systemd`, `plymouth`).
   - Installing/upgrading a single component (`libinput`) against a database when older dependencies or system components remain un-upgraded defines the unsupported partial upgrade state forbidden by S010 / ArchWiki.
3. **Execution vs Log Divergence:**
   - The log entry does **not** signify that running desktop sessions are running `1.32.0-1`.
   - The log entry does **not** certify that runtime ABI compatibility between the on-disk library and in-memory callers is preserved without session restart.
   - The log entry strictly documents that ALPM completed the filesystem write and database registration.

---

## 4. Recommendations for Tsukuroi Round 15 Artifacts

1. **In `IncidentEntry` / `partial-upgrade-recheck-r15.md` & `.json`:**
   - Rigorously isolate `command_key` observations:
     - `libinput_log` = historical transaction entry from `/var/log/pacman.log`.
     - `package_versions` = ALPM installed database state (`pacman -Q`).
     - `pending_updates` = difference between installed DB and sync DB (`pacman -Qu`).
     - `sync_metadata` = arrival/birth timestamp of repository databases.
   - Explicitly declare that process memory mappings (`/proc/*/maps`) and running binary versions were **not measured** and remain unknown.
2. **Never Conflate Log Events with System Health:**
   - Prohibit claiming that a green log entry or successful ALPM transaction implies system health or operational safety.
   - Maintain decision `BLOCKED_FOR_AGENT_PACKAGE_ACTION`: full upgrades remain blocked by the `mkinitcpio 42` hook compatibility constraint (`/new_root` vs `/sysroot`).

---

## 5. Exact Sources, Limits, and Tools

### Exact Sources Read
- **`pacman(8)`** — Pacman Manual, Pacman 7.1.0, dated 2026-05-06 (`/usr/share/man/man8/pacman.8.gz`).
  - Key sections: `DESCRIPTION`, `OPERATIONS` (`-Q`, `-S`, `-U`), `OPTIONS` (`--logfile`), `TRANSACTION OPTIONS` (`--dbonly`, `-p, --print`, `--print-format`), `UPGRADE OPTIONS` (`--needed`), `HANDLING CONFIG FILES`.
- **`pacman.conf(5)`** — Pacman Configuration Manual, Pacman 7.1.0, dated 2026-05-06 (`/usr/share/man/man5/pacman.conf.5.gz`).
  - Key sections: `LogFile`, `DBPath`, `RootDir`, `NoUpgrade`.
- **Corpus Knowledge & Lessons:**
  - `corpus/knowledge/pacnew-plane.md` (distinction between historical log events and current filesystem config state).
  - `corpus/knowledge/package-state-plane.md` (database directories vs query outputs, mtime server stamps vs arrival birth stamps).
  - `corpus/knowledge/update-safety-note.md` & `update-safety-v2.md` / `v3.md` (plan-only `-Sup` vs execution, candidate sets, running workload coupling).
  - `corpus/knowledge/closeout-r11.md` (bare `-Sy` transaction logging vs full system upgrade requirements).
  - `SKILL.md:1645-1650` (pacman.log transaction anchoring).
  - `.ufo/waves/round-15/build/host-snapshot.json` & `HostSnapshot.md` (read-only snapshot artifact).

### Limits
- Read-only analysis of documentation and existing committed evidence; no live host commands executed by this seat.
- No inspection of live processes, `/proc`, sockets, or hardware state.
- Does not assert whether the host's running compositor experienced defects or ABI breakage.

### Tools
- None installed, updated, or removed. No `pacman`, `sudo`, or service commands run.