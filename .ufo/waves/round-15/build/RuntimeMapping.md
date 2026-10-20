# Runtime Mapping — Shared-Library Replacement vs Process Mappings

## Target & Boundary
- Target: Source-only architectural review of shared-library on-disk replacement versus process virtual memory mappings under Linux/ELF/ALPM.
- Scope bounds: Read-only research. No `/proc` probes, no live process inspection (`/proc/*/maps`, `lsof`, `fuser`), and strictly **no claim of actual running version** on host `plazir27` or any active session.
- Substrate bounds: Leaf scout role; no subagent dispatch; zero package transactions or service mutations.

## 1. On-Disk Replacement vs Process Address Space Mechanics
Under Linux ELF dynamic linking and VFS semantics, package upgrades replace on-disk shared libraries while running processes retain existing mappings:
1. **Unlink-and-Replace Inode Semantics (`unlink(2)` / atomic rename):**
   - Package managers (including `pacman`/`libalpm`) replace shared libraries (`.so`) by unlinking the existing directory entry and creating a new inode (or writing to a temporary file and atomically renaming via `rename(2)`).
   - Inode de-allocation only occurs when the inode's link count reaches zero AND all open file descriptors / memory mappings (`mmap(2)`) referencing the inode are closed.
2. **Virtual Memory Mappings (`mmap(2)` / VMA retention):**
   - Processes that loaded the library before replacement hold `MAP_PRIVATE` file-backed memory mappings (`PROT_READ|PROT_EXEC` text segments, `PROT_READ|PROT_WRITE` data/bss copies) pointing to the *original, unlinked inode*.
   - In `/proc/<pid>/maps`, this manifests as the legacy inode path suffixed with ` (deleted)`. The running process continues executing the unlinked code; it does *not* automatically transition to the newly installed inode.
3. **Dynamic Loading Boundary (`dlopen(3)`):**
   - Subprocesses spawned after the transaction or running processes making subsequent `dlopen(3)` calls will resolve the path to the *new* on-disk inode.
   - If a long-running process already loaded symbol tables or dependent libraries, partial reloading or IPC ABI mismatches can induce state divergence without crashing immediately.

## 2. Invariance & ABI Decoupling in Partial Upgrades
In a partial upgrade event (such as updating `libinput 1.31.3-1 -> 1.32.0-1` while compositors or Xwayland remain running):
- **Disk state:** `/usr/lib/libinput.so.10` points to the new library build on the filesystem.
- **Process state:** Long-running compositor processes (e.g., `Hyprland`, `Xwayland`) that initialized at session boot continue executing the old code from the unlinked inode mapped into their address space.
- **Critical Distinction:** Pacman log entries (`[ALPM] upgraded libinput (...)`) certify only filesystem transaction completion. They provide **zero evidence** of process address space reload, daemon restart, or live operational health.
- **Prohibition on Live Claims:** Without inspecting process maps (which is out of scope and forbidden for read-only static analysis), claiming that running processes are "safe", "repaired", or "broken" is an invalid inference.

## 3. Recommendations
1. Treat package transaction logs strictly as on-disk filesystem state transitions, never as live execution status.
2. Maintain clean separation between installed version (ALPM database), sync version (repo metadata), and running version (unobserved runtime mappings).
3. Require session restart / daemon reload as an operator decision rather than inferring automated hot-reload.

## Exact Sources & Limits
- **Sources:**
  - `man 2 mmap`, `man 2 unlink`, `man 3 dlopen` (Linux programmer's manual).
  - Corpus precedents: `update-safety-note.md` §3 (coupling to running sessions), `host-health-report-r3.md` / `degraded-triage-r4.md` (session transition boundaries).
  - `host-snapshot.json` (`libinput_log` transaction 2026-10-20T04:25:17-0300).
- **Limits:**
  - No `/proc` probes performed.
  - No inspection of process memory maps (`/proc/*/maps`), PIDs, or systemd scopes.
  - Strictly no claim regarding which library version is actively executing in any running process.
- **Tools installed/updated:** none.
