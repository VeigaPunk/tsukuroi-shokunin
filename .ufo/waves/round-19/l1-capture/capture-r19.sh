#!/usr/bin/env bash
# Round-19 L1 host capture — read-only. Every L1 host-touching read this round goes through this
# script (routed defect 3, round-18 closure §5 item 3), including the pacman.log ranges, so its
# output is the whole L1 host exec log for tools/check-recheck-commands.py --exec-log.
# No pacman/checkupdates/yay/paru/mkinitcpio/limine-update/limine-snapper-sync invocation, no sudo,
# no service action, no /boot write. Forbidden binaries (QUALITY 26): pacman checkupdates yay paru
# mkinitcpio limine-update. Each probe prints `$ <command>`, its output, then `[rc=N]`.
set -u
run() { printf '$ %s\n' "$*"; bash -c "$*" 2>&1; printf '[rc=%s]\n' "$?"; }
run 'date -Is'
run 'uname -r'
run 'ls -1d /var/lib/pacman/local/limine-snapper-sync-[0-9]* /var/lib/pacman/local/limine-mkinitcpio-hook-[0-9]* /var/lib/pacman/local/limine-[0-9]* /var/lib/pacman/local/snapper-[0-9]* /var/lib/pacman/local/mkinitcpio-[0-9]*'
run 'grep -v "^$" /var/lib/pacman/local/limine-snapper-sync-[0-9]*/files'
run 'grep -v "^$" /var/lib/pacman/local/limine-mkinitcpio-hook-[0-9]*/files'
run 'grep -A1 -E "^%(URL|BUILDDATE|INSTALLDATE|VERSION)%" /var/lib/pacman/local/limine-snapper-sync-[0-9]*/desc'
run 'grep -A1 -E "^%(URL|VERSION)%" /var/lib/pacman/local/limine-mkinitcpio-hook-[0-9]*/desc'
run 'systemctl cat limine-snapper-sync.service --no-pager'
run 'systemctl list-unit-files --no-pager "limine*" "snapper*"'
run 'systemctl show limine-snapper-sync.service -p UnitFileState -p TriggeredBy -p WantedBy -p After -p Requires --no-pager'
run 'systemctl list-dependencies --reverse --no-pager limine-snapper-sync.service'
run 'systemctl cat snapper-cleanup.timer snapper-cleanup.service --no-pager'
run 'systemctl list-timers --all --no-pager "snapper*"'
run 'ls -l /usr/share/libalpm/hooks/ /etc/pacman.d/hooks/'
run 'grep -H -E "^(Target|Exec|When|Operation|Depends|NeedsTargets)" /usr/share/libalpm/hooks/*limine* /usr/share/libalpm/hooks/*snap* /etc/pacman.d/hooks/*.hook'
run 'grep -v -E "^[[:space:]]*(#|$)" /etc/limine-snapper-sync.conf'
run 'grep -v -E "^[[:space:]]*(#|$)" /etc/default/limine'
run 'file -L /usr/bin/limine-snapper-sync /usr/bin/limine-update /usr/bin/limine-entry-tool'
run 'stat -c "%y %U:%G %a %n" /boot /boot/limine.conf /boot/EFI/limine/limine.conf'
run 'journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -u limine-snapper-sync.service -u snapper-cleanup.service -u snapper-timeline.service | tail -n 80'
run 'journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -g "/boot/limine.conf" | tail -n 60'
run 'journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -g "/boot/limine.conf" | grep -c "Updated: /boot/limine.conf"'
run 'grep -n -E "limine|mkinitcpio|Running .*hook" /var/log/pacman.log | tail -n 40'
run 'wc -l /var/log/pacman.log'
run 'tail -n 2 /var/log/pacman.log'
