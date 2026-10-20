#!/usr/bin/env bash
# Round-18 L1 host capture — read-only. No pacman/checkupdates/yay/paru/mkinitcpio/limine-update,
# no sudo, no service action, no /boot read or write. Each probe prints `$ <command>` then its
# output, so this capture doubles as the executed-command log for tools/check-recheck-commands.py
# --exec-log. Forbidden binaries (QUALITY 26): pacman checkupdates yay paru mkinitcpio limine-update.
set -u
run() { printf '$ %s\n' "$*"; bash -c "$*" 2>&1; printf '[rc=%s]\n' "$?"; }
run 'date -Is'
run 'uname -r'
run 'cat /proc/cmdline'
run 'cat /sys/module/zswap/parameters/enabled /sys/module/zswap/parameters/max_pool_percent /sys/module/zswap/parameters/compressor'
run 'systemctl is-active earlyoom; systemctl is-enabled earlyoom'
run 'systemctl show earlyoom -p ActiveEnterTimestamp -p ExecMainPID --no-pager'
run 'ls -1 /var/lib/pacman/local | grep -vc "^ALPM_DB_VERSION$"'
run 'ls -1d /var/lib/pacman/local/earlyoom-[0-9]* /var/lib/pacman/local/mkinitcpio-[0-9]* /var/lib/pacman/local/linux-[0-9]* /var/lib/pacman/local/linux-lts-[0-9]* /var/lib/pacman/local/snapper-[0-9]* /var/lib/pacman/local/limine-snapper-sync-[0-9]* /var/lib/pacman/local/pacman-contrib-[0-9]* /var/lib/pacman/local/sysstat-[0-9]* /var/lib/pacman/local/nvidia-open-dkms-[0-9]* /var/lib/pacman/local/elephant-[0-9]* /var/lib/pacman/local/archlinux-keyring-[0-9]*'
run 'stat -c "%y %n" /var/lib/pacman/local /var/lib/pacman/sync/*.db'
run 'ls -1 /var/lib/pacman/sync/'
run 'ls -l /var/lib/pacman/db.lck'
run 'wc -l /var/log/pacman.log'
run 'tail -n 3 /var/log/pacman.log'
run 'grep -c "\[ALPM\] upgraded" /var/log/pacman.log'
run 'grep -n "pacman -U" /var/log/pacman.log | tail -n 3'
run 'ls -1 /etc/snapper/configs'
run 'grep -h "^SNAPPER_CONFIGS" /etc/conf.d/snapper'
run 'command -v paccache sar atop dool dstat earlyoom'
run 'ls -1 /var/log/sa'
run 'stat -c "%y %n" /usr/share/pacman/keyrings/archlinux.gpg'
run 'dkms status'
run 'findmnt -no FSTYPE,OPTIONS /'
