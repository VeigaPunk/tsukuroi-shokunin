# RevWatcher — W-WATCHER (limine-snapper-sync.service → limine-snapper-watcher)

Shorthand: r19/r19b/r19c = .ufo/waves/round-19/l1-capture/host-capture-r19{,b,c}.txt.

**Verdict:** the enabled unit (ExecStart=limine-snapper-watcher, r19:160; enabled r19:192) ran at every boot but wrote /boot zero times in-window (2026-10-19 00:00 → 2026-10-20T17:58:55, r19c:2-4). Dormant writer path; attributed_events = 0. [obs]

**Mechanism:** the watcher never writes /boot itself; it only spawns limine-snapper-sync children: initial sync when /.snapshots is missing (r19b:1361-1362) and an inotifywait create/delete loop spawning `--add`/`--debounce` (r19b:1371,1376,1378).

**Why dormant — three observed closures:**
1. inotifywait absent: `if ! command -v inotifywait &>/dev/null; then` → info message → `exit 0` (r19b:1365-1367), logged by all six in-window instances, PIDs 1372/1386/1394/1392/10021/1385 (r19b:1645,1655,1665,1675,1678,1683). The monitor loop never ran: no [EVENT]/[SKIP] line in any capture; the cleanup-lock skip (r19b:1373-1374; lock set by unit r19:258-259) is loop-only, unreachable. [obs]
2. Initial-sync child failed pre-/boot every time: subvolume errno 13 (r19b:1650,1660,1670), `Failed: "snapper --no-dbus -c root create-config /" with exit code: 1` (r19b:1652,1662,1672). Operator created the config via sudo at 09:03:02 (r19c:27); thereafter /.snapshots exists and later starts (r19b:1678,1683) log no initial-sync line. [obs]
3. All 10 `Updated: /boot/limine.conf` rows carry _SYSTEMD_UNIT snapper-cleanup.service (8) or limine-snapper-add-{1-5846,2-260668}.service (2), never limine-snapper-sync.service — which a watcher child would inherit (r19c:11-20). [obs]

**Rejected:** sync[5929]/[260715] Copied/Saved lines are plugin add-unit runs, not watcher (r19c:11-12). **[unk]:** why watcher PID 10021 restarted mid-boot 09:10:54 (r19b:1678); no captured trigger.

**Flip to active:** install inotify-tools → loop engages, each /.snapshots event spawns a /boot-writing sync (lock-gated, r19b:1373-1374); or delete /.snapshots → initial-sync branch now succeeds past create-config and writes /boot. [inf from r19b:1360-1362,1365-1378]

Installs: none. Model: zai/glm-5.3-flash.
Scope: executed=none
