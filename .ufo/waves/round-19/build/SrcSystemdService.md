# SrcSystemdService — systemd.service(5) `ExecStopPost=`

[obs] `man.archlinux.org/man/systemd.service.5` was unreachable: ECONNRESET on six URL forms, no
body (transport failure, not 404). Same text read via Wayback capture 20261009204750 (lines
507-530) and pinned upstream v262.1 XML (`man/systemd.service.xml:591-613`); freedesktop `latest`
render confirmed it.

[obs] Anchor: OPTIONS > `ExecStopPost=`, fragment `#ExecStopPost=` (freedesktop shows
`[¶](#ExecStopPost=`); Arch fragment [inf] — page unread).

[obs] Version line `systemd 262`: archived Arch footer (capture line 1598) and freedesktop
header. [unk] Live Arch footer unread; the package page reports 262.1-1 (built 2026-10-17).

[obs] Quote, 10 words, identical at archive:509, XML:592, freedesktop:434 — "Additional commands
that are executed after the service is stopped."

[obs] No cgroup sentence on this page: XML `cgroup` hits only `ExitType=` (328-345) and
`OOMPolicy=` (1440-1441); `spawned|unit's|context` yields no `ExecStopPost=` statement. The sole
context sentence delegates to systemd.exec(5): "which define the execution environment the commands
are executed in". Cgroup membership is observed, not sourced: `host-capture-r19c.txt:13-20` carries
`/system.slice/snapper-cleanup.service`.

[obs] C2 wiring: `host-capture-r19.txt:260` `ExecStopPost=limine-snapper-sync`.

[inf] Eight cleanup events are that drop-in firing at unit stop; the page grounds timing, not
writer identity.

[inf] Land doc rows from S070: `ScribeSourcesOwn.rows.md:7-10` claims S066–S069, and
`SrcSystemdRun`/`SrcSnapperPlugins` each wrote literal S066 (duplicate-id red risk).

[inf] `used-by` names `corpus/knowledge/boot-writers-r19.md`; the mined used-by census reds if that
file is absent at landing.

Rejected: man7 `262~devel` footer; cgroup from this page; literal S066.

Draft: `.ufo/waves/round-19/build/drafts/SrcSystemdService.row.md`. Model:
commandcode/deepseek/deepseek-v4.1-flash (harness).

Scope: executed=none
