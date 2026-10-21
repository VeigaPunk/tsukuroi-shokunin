## Attack

Attack C2's watcher-side claim that the missing-`inotifywait` fallback makes the watcher unable to reach any write path, and reconstruct the 09:10:54 PID 10021 start. This is falsifiable from the captured script statement order and the captured service/timer declarations and journal records.

## Method

Read-only inspection of the committed captures and their capture scripts; no live host probes or service actions. Relevant recorded commands (captured, not rerun):

- `cat -n /usr/bin/limine-snapper-watcher`
- `journalctl --list-boots --no-pager | tail -n 6`
- `journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -t limine-snapper-sync -t limine-snapper-watcher | grep -v "Updated: /boot/limine.conf" | tail -n 40`
- `systemctl cat limine-snapper-sync.service --no-pager`
- `systemctl show limine-snapper-sync.service -p UnitFileState -p TriggeredBy -p WantedBy -p After -p Requires --no-pager`
- `systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service`
- `systemctl cat snapper-cleanup.timer snapper-cleanup.service --no-pager`
- `systemctl list-timers --all --no-pager "snapper*"`
- The r19c capture's journal queries for the 08:58–09:04, 09:28–09:29, and 08:57–09:10 windows, and its JSON projection of `/boot/limine.conf` records.

Capture artifact hashes/line counts were checked with `wc -l` and `sha256sum`; no tools were installed.

## Verdict

**REFUTE — C2 watcher subclaim, if read as “the fallback exits before any write path is reachable.”** The absent-`inotifywait` branch does exit before the monitor loop, but it is ordered after an optional initial `limine-snapper-sync` call and after background pacman-lock cleanup is launched. This does not refute the narrower observed result that none of the retained `/boot/limine.conf` updates was attributed to the watcher. The cause of PID 10021's 09:10:54 start is **[unk]** from the captured units/timers.

## Evidence

- **Control flow (high confidence):** The captured watcher is `host-capture-r19b.txt:1318-1381` (the script's own lines 72–134). `copy_config_if_needed` can copy a config to `/tmp` on the read-only-snapshot condition (script lines 72–80); the following read-only and snapshot checks exit before reaching the watcher fallback (lines 96–109). On the normal path, `cleanup_pacman_lock &` starts before initial sync (lines 82–94, 111). If `/.snapshots` is absent, the script prints its initialization message and invokes `limine-snapper-sync` at lines 113–117. Only after that does lines 119–122 test `command -v inotifywait`; when absent, they print the fallback message and `exit 0`. The `inotifywait ... | while ...` monitor loop is later, at lines 124–134, so it is unreachable on that fallback branch.
- **Write-path qualification:** The initial-sync command is reached before the missing-tool check when `/.snapshots` is absent; therefore the fallback does not gate that external sync path. The lock-cleanup function can run `rm -f "$lock_file"` after checking for a stale pacman lock (script lines 82–94), and is backgrounded before the fallback (line 111); the captures do not establish whether a lock existed or was removed. The optional `/tmp` copy is also present in the script, but its read-only/snapshot guard is followed by an early exit, so it is not evidence of a write during the observed fallback instances.
- **Six fallback records and boot context:** `host-capture-r19b.txt:5-11` gives the boot intervals/IDs; `:1643-1684` contains the journal tail:
  - 2026-10-19 08:11:47, PID 1372, boot `be045967...` (`:7`, `:1644-1645`). A sync “No Snapper config found” message precedes the fallback; no initial-sync “Directory /.snapshots does not exist” line is captured for this instance.
  - 2026-10-19 22:48:23–24, PID 1386, boot `430d3038...` (`:8`, `:1647-1655`): initial-sync message, failed root-config/subvolume creation (`errno:13`, exit 1), then fallback.
  - 2026-10-20 06:37:55, PID 1394, boot `84755511...` (`:9`, `:1657-1665`): initial-sync message, `errno:13`/exit 1, then fallback.
  - 2026-10-20 08:58:00–01, PID 1392, boot `ed8819b0...` (`:10`, `:1667-1675`): initial-sync message, `errno:13`/exit 1, then fallback.
  - 2026-10-20 09:10:54, PID 10021, same boot `ed8819b0...` (`:10`, `:1678`): fallback only; no initial-sync message is recorded.
  - 2026-10-20 09:57:11, PID 1385, boot `3e7084f4...` (`:11`, `:1682-1683`): fallback only.
- The r19c sudo projection records `snapper -c root create-config /` at 09:03:02 (`host-capture-r19c.txt:26-32`); after it, the 09:10:54 and 09:57:11 fallback records have no initial-sync message. The ordering is observed; that the successful config creation explains the later missing initial-sync branch is an inference, not a trigger attribution.
- **Observed boot writes remain distinct from reachable paths:** The complete retained JSON projection lists ten `Updated: /boot/limine.conf` events and assigns them to two `limine-snapper-add-*.service` units and `snapper-cleanup.service`, not `limine-snapper-sync.service` (`host-capture-r19c.txt:5-20`). The three initial-sync attempts visible in r19b fail while creating the Snapper root config (`:1648-1654`, `:1658-1664`, `:1668-1674`). This supports zero *observed watcher-attributed* boot updates in the retained projection, not a claim that no write-capable command is reachable before fallback.
- **09:10:54 trigger [unk]:** The unit is `Type=simple`, `ExecStart=limine-snapper-watcher`, `Restart=on-failure`, and enabled via `WantedBy=multi-user.target` (`host-capture-r19.txt:153-189`). Its captured `TriggeredBy=` is empty and reverse dependencies are `multi-user.target`/`graphical.target` (`:208-219`). The 09:10:54 event is within the boot that began at 08:57:58, after its 08:58:01 fallback (`host-capture-r19b.txt:10`, `:1675`, `:1678`); the script's fallback exits 0, so `Restart=on-failure` does not explain a restart after that successful exit. The captured cleanup timer is configured with `OnBootSec=10m` and `OnUnitActiveSec=1h`; it activates `snapper-cleanup.service`, whose `ExecStopPost` is `limine-snapper-sync`, not the watcher (`host-capture-r19.txt:220-261`). The cleanup run is recorded at 09:08:04 (`host-capture-r19c.txt:45-57`), but its captured chain does not declare a watcher start. The captures do not contain a systemd start record or sudo command at 09:10:54: the sudo windows are 08:58–09:04 and 09:28–09:29 (`host-capture-r19c.txt:22-44`), and the timer query ends at 09:10 (`:45`). An explicit start/restart or other uncaptured activation is possible but unproven; no trigger is assigned.

## Residual

The captures do not show whether `/var/lib/pacman/db.lck` existed when cleanup ran, whether `rm -f` executed, or what systemd/API/manual action caused PID 10021 to start. The 08:11:47 sync message's relationship to the watcher is also unresolved. Confidence is high for the captured control-flow ordering and loop bypass, and low/unknown for those causes and side effects.

Scope: executed=read-only `read`/`grep`/`glob` inspection of committed files; `wc -l host-capture-r19.txt host-capture-r19b.txt host-capture-r19c.txt capture-r19.sh capture-r19b.sh capture-r19c.sh`; `sha256sum host-capture-r19.txt host-capture-r19b.txt host-capture-r19c.txt capture-r19.sh capture-r19b.sh capture-r19c.sh`; `git rev-parse HEAD`; `jj --ignore-working-copy log -r @ --no-graph -T 'commit_id ++ "\n"' | head -3`