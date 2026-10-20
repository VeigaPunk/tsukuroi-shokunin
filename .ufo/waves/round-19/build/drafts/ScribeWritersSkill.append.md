
## R19 — expected /boot writers (decision table)

Authority: read-only attribution of `/boot/limine.conf` writes seen in the round-19 captures (window 2026-10-19 00:00 to 2026-10-20 17:58 -03). Detection only. Nothing here authorizes running `limine-snapper-sync`, `limine-update`, `limine-install`, `snapper`, `mkinitcpio`, any pacman command, `systemctl start|stop|restart|enable`, or any `/boot` write. Every action below is record, report, or operator handoff.

Evidence and pointers:
- Capture files (lane-relative, read-only): `.ufo/waves/round-19/l1-capture/host-capture-r19.txt` (`r19`), `host-capture-r19b.txt` (`r19b`), `host-capture-r19c.txt` (`r19c`).
- Knowledge entry `corpus/knowledge/boot-writers-r19.md`: **absent at this write** (no file under `corpus/knowledge/` matched). Until it lands, the capture lines below are the only evidence for this section.
- Window total: 10 journal `Updated: /boot/limine.conf` events (`r19c:11-20`; count `r19:562-563`, `r19b:1685-1686`) plus 2 ALPM-SCRIPTLET events (`r19:578`, `r19:597`) = 12 attributed events.

### Writer classes

| Signature seen | Writer | Expected when | Action |
|---|---|---|---|
| `Updated: /boot/limine.conf` with `_SYSTEMD_UNIT=snapper-cleanup.service` | W1 cleanup stop. Drop-in `ExecStopPost=limine-snapper-sync` (`r19:256-260`), timer `OnBootSec=10m` / `OnUnitActiveSec=1h` (`r19:221-231`) | Once per hourly `snapper-cleanup.timer` run. Observed 8 (`r19c:13-20`) | Record unit and PID. No action. |
| `Updated` with `_SYSTEMD_UNIT=limine-snapper-add-<id>-<pid>.service` | W2 snapper create plugin. `create-snapshot-post` runs `systemd-run --unit=limine-snapper-add-…` (`r19b:1184-1188`, dispatch `r19b:1229-1230`) | Seconds after a `snapper … create` in sudo trace (`r19c:29`→`r19c:11`; `r19c:43`→`r19c:12`). Observed 2 | Match to the sudo `COMMAND=/usr/bin/snapper` line; record. |
| `Updated` with `_SYSTEMD_UNIT=limine-snapper-delete-…` or `…-modify-…` | W3 snapper delete/modify plugin, `--debounce` (`r19b:1175-1176`, dispatch `r19b:1231-1236`) | After a snapper delete or modify. Observed 0 in window. Whether a delete ran is `[unk]` | Record. State "none observed" if absent. |
| `[EVENT] <CREATE|DELETE> -> <id>` from `limine-snapper-watcher` | W4 watcher service, `ExecStart=limine-snapper-watcher` (`r19:153-161`) | Only when `inotifywait` is installed. Not installed on this host: watcher prints fallback and exits 0 (`r19b:1365-1367`; journal `r19b:1645`, `1665`, `1675`, `1683`) | Any `[EVENT]` line in a boot that also shows the fallback line is error E3. |
| `ALPM-SCRIPTLET] Copied: /tmp/limine-mkinitcpio.*.efi -> /boot/EFI/Linux/…` then `ALPM-SCRIPTLET] Updated: /boot/limine.conf` | W5 pacman hook `90-mkinitcpio-install.hook` → `limine-mkinitcpio-install` (`r19:379-398`) | Inside the `running '90-mkinitcpio-install.hook'` span of `/var/log/pacman.log`. Observed 2026-10-20 09:18:13–09:18:24 (`r19:578`, `r19:597`; span `r19b:1688-1703`) | Confirm the span (step 2). Record. |
| `running '80-limine-efi-deploy.hook'` or `running '99-limine.hook'` span | W6 deploy hooks. `80` runs `/usr/bin/limine-install` (`r19b:1399-1430`); `99` copies `BOOT*.EFI` (`r19:399-403`) | Copies EFI binaries. No `limine.conf` update observed in these spans (`pacman.log` 2977-2983, 3050, via `r19b:1697-1703`) | Not a `limine.conf` writer. An `Updated` line inside its span is error E5. |
| no line; `snapper` plugin `set-default-snapshot-pre` | W7 restore hook → `limine-snapper-restore --kernels` (`r19b:1237-1239`) | Only on set-default or rollback. Observed 0. `[inf]` that restore adds a backup entry (`README.md:38`, `r19b:51`) | Record only. |

Not a writer: `10-limine-snapper-lock.hook` (PreTransaction, `r19:347-353`; `limine-snapper-lock` takes `mutex_lock "limine-snapper-lock"`, `r19b:1389-1397`).

### Error patterns

- **E1 UNATTRIBUTED.** `Updated: /boot/limine.conf` whose `_SYSTEMD_UNIT` is none of `snapper-cleanup.service` or `limine-snapper-{add,delete,modify}-*`, and which has no ALPM line inside a `running '90-mkinitcpio-install.hook'` span. Action: ERROR. Report timestamp, PID and unit. Take no further action.
- **E2 UKI copy outside a pacman transaction.** `Copied: /tmp/limine-mkinitcpio.` or `-> /boot/EFI/Linux/` in any source outside a 90-mkinitcpio span. Journal copies to `/boot/<id>/limine_history/` are normal (`r19c:23`, `r19c:39-40`) and are not this pattern. Action: ERROR.
- **E3 watcher active.** `[EVENT]` from `limine-snapper-watcher` in a boot whose journal also shows the `inotifywait is not installed` fallback line. Action: ERROR. Identify which writer produced the event.
- **E4 stale lock.** `/run/limine-snapper-cleanup.lock` exists while `snapper-cleanup.service` is inactive. The drop-in creates it in `ExecStartPre` and removes it in `ExecStopPost` (`r19:258-259`). Action: report. Never remove it.
- **E5 deploy-hook write.** `Updated: /boot/limine.conf` inside a `80-limine-efi-deploy` or `99-limine` span. Action: ERROR.
- **E6 no-lock-skip inference.** The lock check lives in the watcher only (`r19b:1373-1374`, watcher lines 126-128). The snapper plugin skip (`r19b:1160-1169`) checks only `limine-snapper-sync.service` and `pgrep limine-snapper-watcher`. The cleanup `ExecStopPost` runs `limine-snapper-sync` directly with no lock check. Absence of a limine line during a cleanup run is **not** evidence of a lock skip. Unexplained observation: `snapper-cleanup.service` ran 09:03:03–09:08:04 with no limine line (`r19c:46-57`). Status `[unk]`.

### Read-only checklist (5 steps)

Forbidden in this checklist: `sudo`, `limine-update`, `limine-snapper-sync`, `snapper`, `mkinitcpio`, `pacman` (any form), `checkupdates`, `yay`, `paru`, `systemctl start|stop|restart|enable`, any `/boot` write.

1. Attribute journal writes by unit (verbatim form `r19c:5-10`, with the MESSAGE filter in Python):
   `journalctl --no-pager --since "2026-10-19 00:00" -t limine-snapper-sync -o json --output-fields=_SYSTEMD_UNIT,_SYSTEMD_CGROUP,_COMM,_PID,MESSAGE`
   Keep lines whose MESSAGE contains `/boot/limine.conf`. Count by `_SYSTEMD_UNIT`. Expected: `snapper-cleanup.service` plus the `limine-snapper-add-*` units only.
2. Bracket pacman writes (adapted from `r19b:1688`; not run in this exact form):
   `grep -n -E "ALPM-SCRIPTLET\] (Copied: /tmp/limine-mkinitcpio|Updated: /boot/limine.conf)|running '(80-limine-efi-deploy|90-mkinitcpio-install|99-limine)\.hook'" /var/log/pacman.log`
   Every ALPM `Updated`/`Copied` line must sit between its own `running '90-mkinitcpio-install.hook'` line and the next `[ALPM] running` line. Otherwise E1/E2/E5.
3. Snapper trigger trace (`r19c:22-37`, `sed` omitted):
   `journalctl --no-pager -o short-iso -t sudo | grep -E "COMMAND=/usr/bin/(snapper|systemctl) "`
   Match each add-unit start to a `snapper … create` line.
4. Unit, timer and watcher wiring (`r19:153-161`, `r19:220-231`, `r19:262-265`):
   `systemctl cat snapper-cleanup.service --no-pager`; `systemctl cat limine-snapper-sync.service --no-pager`; `systemctl list-timers --all --no-pager "snapper*"`; `command -v inotifywait || echo "inotifywait absent"`. If `inotifywait` is present, E3 applies to any `[EVENT]` line.
5. Lock and hook wiring (`r19:258-259`, `r19:346-409`):
   `ls -l /run/limine-snapper-cleanup.lock 2>&1`; `systemctl is-active snapper-cleanup.service`; `grep -H -E "^(Target|Exec|When|Operation)" /usr/share/libalpm/hooks/*limine* /etc/pacman.d/hooks/*limine* /etc/pacman.d/hooks/90-mkinitcpio-install.hook`.
   A lock present with an inactive cleanup unit is E4. Report it; never remove it.

Output every step, including the ones that pass. Record each signature in the table's first column with its unit, PID and timestamp.
