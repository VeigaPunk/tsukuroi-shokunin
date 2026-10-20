#!/usr/bin/env bash
# Round-19 L1 host capture c — read-only journal field reads binding each limine-snapper-sync
# write event to its systemd unit/cgroup and the snapshot activity around the two non-timer events.
# Same contract as capture-r19.sh (no pacman/mkinitcpio/limine-update/limine-snapper-sync
# invocation, no sudo, no service action, no /boot access). Prints `$ cmd`, output, `[rc=N]`.
# sudo journal lines are filtered to snapper/systemctl COMMAND records only (operator command
# history outside the boot-writer question is not retained; v1 of this script kept all sudo lines
# and was superseded before commit for that reason).
set -u
run() { printf '$ %s\n' "$*"; bash -c "$*" 2>&1; printf '[rc=%s]\n' "$?"; }
run 'date -Is'
run 'journalctl --no-pager --since "2026-10-19 00:00" -t limine-snapper-sync -o json --output-fields=_SYSTEMD_UNIT,_SYSTEMD_CGROUP,_COMM,_PID,MESSAGE | python3 -c "import sys,json,datetime as d
for l in sys.stdin:
    r=json.loads(l)
    if \"/boot/limine.conf\" not in str(r.get(\"MESSAGE\")): continue
    t=d.datetime.fromtimestamp(int(r[\"__REALTIME_TIMESTAMP\"])/1e6).isoformat(timespec=\"seconds\")
    print(t, r.get(\"_PID\"), r.get(\"_COMM\"), r.get(\"_SYSTEMD_UNIT\"), r.get(\"_SYSTEMD_CGROUP\"), r.get(\"MESSAGE\"))"'
run 'journalctl --no-pager -o short-iso --since "2026-10-20 08:58:30" --until "2026-10-20 09:04:00" -t snapper -t snapperd -t limine-snapper-sync -t limine-snapper-watcher -t systemd-helper -t sudo | grep -v pam_unix | grep -E -v "sudo\[[0-9]+\]:" ; journalctl --no-pager -o short-iso --since "2026-10-20 08:58:30" --until "2026-10-20 09:04:00" -t sudo | grep -E "COMMAND=/usr/bin/(snapper|systemctl) " | sed -E "s/ PWD=[^;]*;//" | cut -c1-200'
run 'journalctl --no-pager -o short-iso --since "2026-10-20 09:28:30" --until "2026-10-20 09:29:30" -t snapper -t snapperd -t limine-snapper-sync -t limine-snapper-watcher -t systemd-helper -t sudo | grep -v pam_unix | grep -E -v "sudo\[[0-9]+\]:" ; journalctl --no-pager -o short-iso --since "2026-10-20 09:28:30" --until "2026-10-20 09:29:30" -t sudo | grep -E "COMMAND=/usr/bin/(snapper|systemctl) " | sed -E "s/ PWD=[^;]*;//" | cut -c1-200'
run 'journalctl --no-pager -o short-iso --since "2026-10-20 08:57:00" --until "2026-10-20 09:10:00" -u snapper-cleanup.timer -u snapper-cleanup.service -u snapper-timeline.service | cut -c1-200'
run 'journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -t systemd -g "limine-snapper-add" | cut -c1-200'
