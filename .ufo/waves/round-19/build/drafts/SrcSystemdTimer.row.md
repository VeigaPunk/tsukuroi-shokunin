# SOURCES row draft — SrcSystemdTimer (C2)

Fetch note: `https://man.archlinux.org/man/systemd.timer.5` failed with ECONNRESET on five URL variants
(bare, `.en`, `.txt`, `/core/systemd/systemd.timer.5.en`, trailing slash) from this seat. Opened the
upstream systemd manual instead: https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
(native fetch; page header reads "systemd 262"; opened 2026-10-20).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | systemd.timer(5) — https://man.archlinux.org/man/systemd.timer.5 (opened fallback: https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html) | docs | A | Monotonic `OnBootSec=`/`OnUnitActiveSec=` semantics and the default `AccuracySec=` window bounding actual expiry; documentation only, not host timer state or causality | § Options > `OnActiveSec=`, `OnBootSec=`, `OnStartupSec=`, `OnUnitActiveSec=`, `OnUnitInactiveSec=` table rows; § `AccuracySec=`; § `RandomizedDelaySec=`; rendered page header "systemd 262" | `OnBootSec=` counts from machine boot and `OnUnitActiveSec=` from the last activation of the activated unit; timers need not expire at the configured instant because expiry is placed within the `AccuracySec=` window (default 1min), while `RandomizedDelaySec=` defaults to 0 | mined | 2026-10-20 | on-release | corpus/knowledge/boot-writers-r19.md |

## Quotes (verbatim, each <=25 words)

- `OnBootSec=`: "Defines a timer relative to when the machine was booted up." (11 words)
- `OnUnitActiveSec=`: "Defines a timer relative to when the unit the timer unit is activating was last activated." (18 words)
- Combination: "it is possible to define a timer that elapses in regular intervals and activates a specific service each time" (19 words)
- `AccuracySec=` default: "Specify the accuracy the timer shall elapse with. Defaults to 1min." (11 words)
- `AccuracySec=` placement: "Within this time window, the expiry time will be placed at a host-specific, randomized, but stable position that is synchronized between all local timer units." (25 words)
- Precision caveat: "Note that timers do not necessarily expire at the precise time configured with these settings, as they are subject to the `AccuracySec=` setting below." (24 words)
- `RandomizedDelaySec=` default: "Defaults to 0, indicating that no randomized delay shall be applied." (11 words)

## Drift note (10:07:03 -> 17:07:16)

[obs] Events: `host-capture-r19c.txt:13-20`; 13s spread over eight hourly writes.
[obs] Unit carries only `OnBootSec=10m` and `OnUnitActiveSec=1h` (host-capture-r19.txt:221-232, :256-260); `systemctl cat` shows no timer drop-in, so no AccuracySec/RandomizedDelaySec override.
[obs] `systemctl list-timers` LAST 17:07:16, NEXT 18:07:16 (host-capture-r19.txt:265).
[obs] Boot markers at `:60-64`; a new boot boundary (`3e7084f4...`) follows the 09:29 events (`:69`).
[inf] 10:07:03 is consistent with boot + `OnBootSec=10m`; each later firing is anchored to the previous
activation (`OnUnitActiveSec=`) and placed inside the default 60s `AccuracySec=` window, so seconds
accumulate instead of resetting to the boot instant. Journal time is the `limine-snapper-sync` message,
which trails activation by service/ExecStopPost runtime. `RandomizedDelaySec=` defaults to 0 and is
unconfigured, so randomized delay does not explain the spread.
[unk] Boot instant and per-iteration expiry placement are not in the captures.
