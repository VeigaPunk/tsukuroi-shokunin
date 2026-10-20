# SyncTimestamp — Lane Sync Birth/Ctime vs Upstream Mtime & Log Evidence

Author: TsukuroiR15.SyncTimestamp (scout, depth axis)
Target: Review existing lane sync birth/ctime vs upstream mtime teaching; distinguish latest sync log evidence from file metadata.
Ownership: Report only; read-only research.
Path: `.ufo/waves/round-15/build/SyncTimestamp.md`

## 1. Declared Axes
- **depth**: Comprehensive technical grounding distinguishing local filesystem inode metadata (`%w`, `%z`, `%y`) from pacman transaction logs (`/var/log/pacman.log`) and upstream repository state.
- **freshness**: Grounded against round 15 host snapshot capture (`2026-10-20T07:44:39Z`) and prior lane anchors (rounds 1–14).

## 2. Review of Existing Lane Sync Inode Teaching
In `corpus/knowledge/package-state-plane.md:73-81`, `update-safety-note.md:44-50`, and `SKILL.md:94-96`, the lane established the foundational "sync-db mtime trap" correction (originally landed in round 1, commit `55b2186`):
1. **Preservation of Upstream File Mtime (`%y` / `%Y`)**:
   - Pacman preserves server-side file modification times (`mtime`) upon downloading database archives (`/var/lib/pacman/sync/*.db`).
   - Consequently, `mtime` reflects when the repository database was built/signed upstream on the mirror infrastructure (e.g. historical `core.db` mtime 2026-09-08 15:23:46), NOT the moment the host fetched it.
2. **Local Arrival Dating via Birth (`%w` / `%W`) and Ctime (`%z` / `%Z`)**:
   - Inode creation/birth (`%w`) and inode change time (`%z`) record local arrival. When pacman writes or replaces `/var/lib/pacman/sync/*.db`, the file system sets birth time (`%w`) and ctime (`%z`) to the local download/extraction instant.
   - Historical anchor: in round 1, all four sync databases (`core`, `extra`, `multilib`, `omarchy`) were born at `2026-10-11 12:54:13.542 -0300`, while their mtimes were weeks older (September 8).

## 3. Distinguishing Sync Log Evidence from File Metadata
Crucially, file metadata (`stat -c '%w|%z|%n'`) and pacman log records (`/var/log/pacman.log`) supply complementary, distinct evidence classes:

| Evidence Plane | Artifact / Probe | Observed Fact | Technical Distinction |
|---|---|---|---|
| **File Metadata (Inode)** | `stat -c '%w\|%z\|%n' /var/lib/pacman/sync/*.db` | All 5 sync DBs born `2026-10-18 14:11:00.026135178 -0300`, ctime `14:11:00.921`–`.923` | **Point-in-time filesystem state.** Proves when files were written to disk. Does NOT prove command line invocation, user flags (`-Sy` vs `-Syu`), transaction scope, or non-sync operations. |
| **Transaction Log** | `/var/log/pacman.log:2288` | `[2026-10-18T14:11:00-0300] [PACMAN] synchronizing package lists` | **Transaction Intent & Engine Execution.** Proves that ALPM completed list synchronization at that timestamp. Correlates second-exact with the inode birth (`14:11:00`). |
| **Subsequent Package Operations** | `/var/log/pacman.log:2429-2436` | `[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'` | **Action Without Sync.** Proves that at 2026-10-20 04:25:16, a package install/upgrade was executed WITHOUT refreshing databases (no preceding sync marker after line 2288). |

### Key Distinctions
1. **Timestamp ≠ Freshness Guarantee**:
   - Inode birth (`2026-10-18 14:11:00`) marks local arrival, NOT upstream freshness. The upstream repo might have advanced minutes after that sync.
   - Conversely, upstream mtime marks upstream build time, NOT current validity.
2. **Log Proves Execution Context**:
   - Inode metadata alone cannot reveal whether databases were refreshed during a full system upgrade (`-Syu`) or a partial sync (`-Sy`). Only `/var/log/pacman.log` confirms whether `-u` was passed and what packages were installed.
3. **Absence of Log Sync Markers Post-Oct 18**:
   - The absence of any `synchronizing package lists` entry between line 2288 (Oct 18 14:11:00) and line 2429 (Oct 20 04:25:16) proves conclusively that the `libinput` transaction operated against 1.6-day-stale sync databases, constituting an uncoordinated partial upgrade.

## 4. Recommendations for Round 15
1. **Citation Rigor**:
   - In C2 (`partial-upgrade-recheck-r15`), explicitly separate the inode metadata finding (`sync_metadata` probe: birth `2026-10-18 14:11:00.026 -0300`) from the transaction log finding (`libinput_log` probe: lines 2288 and 2429).
2. **Preserve Invariant**:
   - Reaffirm that empty `-Qu` only means "nothing newer than the local sync database", never "host packages match current upstream Arch Linux".
3. **Decision Gate**:
   - Maintain `BLOCKED_FOR_AGENT_PACKAGE_ACTION` on autonomous package operations.

## 5. Sources, Limits, and Tools
- **Sources**: `corpus/knowledge/package-state-plane.md:73-81`, `corpus/knowledge/update-safety-note.md:44-50`, `SKILL.md:94-96`, `tools/tsukuroi-census.sh:1466-1488`, `host-snapshot.json` (`captured_at: 2026-10-20T07:44:39Z`).
- **Limits**: Read-only investigation of existing notes, scripts, and snapshot JSON. No live host commands executed, no verification checks run.
- **Tools**: None installed or updated.
