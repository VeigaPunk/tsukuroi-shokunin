# ScribeWritersRecords: C2 event registry draft

Draft: `.ufo/waves/round-19/build/drafts/ScribeWritersRecords.events.json` (JSON array, 12 records, keys id/capture/line/quote/writer).

## Records
- 12 events = 10 from source A + 2 from source B; time-ordered EV-01..EV-12.
- Writer counts: W-SNAPPER-PLUGIN 2 (EV-01, EV-04); W-SNAPPER-CLEANUP 8 (EV-05..EV-12); W-MKINITCPIO-HOOK 2 (EV-02, EV-03). [obs]
- Source A: `host-capture-r19c.txt:11-20`, quote = timestamp, PID, comm, unit fields (`journalctl -o json` via python; naive local time). [obs]
- Source B: `host-capture-r19.txt:578` and `:597` (pacman.log 3015, 3047). pacman.log has no unit field, so the quote is `[timestamp] [ALPM-SCRIPTLET]`. [obs]

## Writer mechanisms
- W-SNAPPER-PLUGIN: plugin `10-limine-snapper-sync` calls `systemd-run --unit="limine-snapper-${op}-${SNAP_ID}-$$"` at `host-capture-r19b.txt:1183-1185`; matches unit names `limine-snapper-add-1-5846` and `-add-2-260668`. [obs]
- W-SNAPPER-CLEANUP: drop-in `snapper-cleanup.service.d/limine-snapper-override.conf` with `ExecStopPost=limine-snapper-sync` at `host-capture-r19.txt:256-260`. [obs]
- W-MKINITCPIO-HOOK: `ALPM-SCRIPTLET` lines during the mkinitcpio hook run (`pacman.log` 3014-3050, r19b:1699-1703), with `90-mkinitcpio-install.hook` Exec `limine-mkinitcpio-install` at `host-capture-r19b.txt:1458`. Which hook file holds that Exec line is [inf]. [obs/inf]

## Exact probe strings (text after `$ `)
- Source A, `host-capture-r19c.txt:5` (continues to line 10):
  `journalctl --no-pager --since "2026-10-19 00:00" -t limine-snapper-sync -o json --output-fields=_SYSTEMD_UNIT,_SYSTEMD_CGROUP,_COMM,_PID,MESSAGE | python3 -c "import sys,json,datetime as d` … `print(t, r.get(\"_PID\"), r.get(\"_COMM\"), r.get(\"_SYSTEMD_UNIT\"), r.get(\"_SYSTEMD_CGROUP\"), r.get(\"MESSAGE\"))"`
- Source B, `host-capture-r19.txt:565`:
  `grep -n -E "limine|mkinitcpio|Running .*hook" /var/log/pacman.log | tail -n 40`

## Limits
- Source B's `tail -n 40` window covers only 2026-10-20 entries. Earlier `Updated: /boot/limine.conf` lines (e.g. pacman.log 2021, 2026-10-11) are outside the registry scope. [obs]
- Counts match the captures' own totals: 10 A-journal events (`host-capture-r19.txt:563`, `host-capture-r19b.txt:1686`) and 2 B-pacman events. [obs]
- Writer class for the mkinitcpio events is by mechanism, not by direct process observation. [inf]

Model: unverified; not stated here.

Scope: executed=none
