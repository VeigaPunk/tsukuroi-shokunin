# RevCleanupHook — C2 hourly /boot writer (W-SNAPPER-CLEANUP)

Model: zai/glm-5.3-flash. No tool installs. Paths relative to lane root; r19/r19b/r19c = `.ufo/waves/round-19/l1-capture/host-capture-r19{,b,c}.txt`.

## Mechanism
- [obs] Timer `OnBootSec=10m`, `OnUnitActiveSec=1h` (r19:227-228); service `ExecStart=/usr/lib/snapper/systemd-helper --cleanup` (r19:244).
- [obs] Drop-in: `ExecStartPre=-touch /run/limine-snapper-cleanup.lock`, `ExecStopPost=-rm -f …lock`, `ExecStopPost=limine-snapper-sync` (r19:256-260). Drop-in ships in the limine-snapper-sync package list (r19:47), which lists no snapper-cleanup timer/service main files (r19:28-47); the `Description=Hourly` main units (r19:223, r19:235) have another, capture-unprovenanced source [inf].
- [obs] Why 8 events sit in snapper-cleanup.service: ExecStopPost runs inside the service's cgroup — all 8 carry `_SYSTEMD_UNIT=snapper-cleanup.service`, `_SYSTEMD_CGROUP=/system.slice/snapper-cleanup.service` (r19c:13-20). Plugin path spawns transients instead: `systemd-run --unit=limine-snapper-${op}-${SNAP_ID}-$$` (r19b:1183-1188) — EV-01/EV-04.

## Why 09:08:04 logged no Updated
[obs] Run belongs to boot ed8819 (08:57:58–09:56:15, r19b:10); OnBootSec due ~09:07:58, fired 09:08:04 (+6s accuracy [inf]). systemd logged "Starting Daily Cleanup of Snapper Snapshots..." (r19c:47-48) — stock description — while the 09:03:03 timer start logged "Hourly" (r19c:46). The unit-filtered query surfacing `Updated` lines under snapper-cleanup.service for every later run (r19:442-446) shows none in this window (r19c:49-57) → the loaded service then lacked effective ExecStopPost wiring [inf]; sync capability already existed (plugin Updated 09:03:03, r19c:11, r19c:25).
[unk] Package install/upgrade chronology sits outside the captured pacman.log windows; main `/usr/bin/limine-snapper-sync` body uncaptured, so an unchanged→silent path can't be excluded from text — but unit-generation divergence plus zero sync lines makes missing ExecStopPost wiring operative [inf].
Rejected: watcher lock-skip (r19b:1373-1374) is watcher-only and the lock is removed before sync (r19:259-260); plugin is-active skip (r19b:1159-1169) covers add/delete only.

## Schedule
[obs] Boot 0 09:57:09 (r19b:11) → 10:07:03 first run (r19c:13; ~10m; PID1 precedes first journal record [inf]). Hourly anchored to prior activation: intervals 3600–3604s, +13s cumulative drift, no wall-clock re-anchor (r19c:13-20); matches LAST 17:07:16 / NEXT 18:07:16 (r19:265). Journal `Updated` total = 10 = 2 plugin + 8 cleanup (r19:562-563): 09:08:04 contributed none.

Draft: `.ufo/waves/round-19/build/drafts/RevCleanupHook.writer.json` (EV-05..EV-12, schema mirrors ScribeWritersRecords.events.json).

Scope: executed=none
