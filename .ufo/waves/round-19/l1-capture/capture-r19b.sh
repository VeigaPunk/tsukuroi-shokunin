#!/usr/bin/env bash
# Round-19 L1 host capture b — read-only package-file and journal reads for the /boot writer
# mechanisms (C2). Same contract as capture-r19.sh: no pacman/checkupdates/yay/paru/mkinitcpio/
# limine-update/limine-snapper-sync invocation, no sudo, no service action, no /boot read or write.
# Each probe prints `$ <command>`, its output, then `[rc=N]`; this file is an L1 exec log too.
set -u
run() { printf '$ %s\n' "$*"; bash -c "$*" 2>&1; printf '[rc=%s]\n' "$?"; }
run 'date -Is'
run 'journalctl --list-boots --no-pager | tail -n 6'
run 'cat -n /usr/share/doc/limine-snapper-sync/README.md'
run 'grep -n -E "^#|watcher|cleanup|ExecStopPost|limine.conf|inotify|snapshot" /usr/share/doc/limine-snapper-sync/CHANGELOG.md | head -n 120'
run 'cat -n /usr/lib/snapper/plugins/10-limine-snapper-sync'
run 'cat -n /usr/bin/limine-snapper-watcher'
run 'cat -n /usr/share/libalpm/scripts/limine-snapper-lock'
run 'cat -n /usr/share/libalpm/hooks/10-limine-snapper-lock.hook /usr/share/libalpm/hooks/80-limine-efi-deploy.hook /etc/pacman.d/hooks/90-mkinitcpio-install.hook /etc/pacman.d/hooks/99-limine.hook /usr/share/libalpm/hooks/90-mkinitcpio-install.hook'
run 'grep -n -E "limine.conf|/boot|ESP_PATH|cp |install -|Updated|Copied" /usr/share/libalpm/scripts/limine-mkinitcpio-install | head -n 60'
run 'grep -n -E "^#|limine.conf|Updated|snapper|cleanup|ESP" /usr/share/doc/limine-entry-tool/README.md | head -n 120'
run 'journalctl --no-pager -o short-iso --since "2026-10-20 09:27:00" --until "2026-10-20 09:31:30" -t limine-snapper-sync -t limine-snapper-watcher -t limine-snapper-notify -t snapperd -t systemd-helper'
run 'journalctl --no-pager -o short-iso --since "2026-10-20 08:40" --until "2026-10-20 10:10" -u snapper-cleanup.service -u limine-snapper-sync.service -t limine-snapper-sync'
run 'journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -t limine-snapper-sync -t limine-snapper-watcher | grep -v "Updated: /boot/limine.conf" | tail -n 40'
run 'journalctl --no-pager -o short-iso --since "2026-10-19 00:00" -t limine-snapper-sync | grep -c "Updated: /boot/limine.conf"'
run 'grep -n -E "Updated: /boot/limine.conf|-> /boot/|running .99-limine.hook|running .80-limine-efi-deploy.hook|running .90-mkinitcpio-install.hook" /var/log/pacman.log | tail -n 30'
