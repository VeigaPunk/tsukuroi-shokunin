#!/usr/bin/env bash
# Round 24 L1 read-only host capture for the pause-lift update-safety gate.
# No package transaction, sync, service action, boot or configuration write.
# Each command is printed with its exit code. Usage: capture.sh <outdir>
set -u
out=${1:?outdir}
mkdir -p "$out"
run() { # run <label> <command...>
  local label=$1; shift
  {
    printf '### %s\n$ %s\n' "$label" "$*"
    bash -c "$*" 2>&1
    printf 'exit=%s\n\n' "$?"
  } >>"$out/capture.txt"
}
: >"$out/capture.txt"
run time 'date -u +%FT%TZ'
run kernel 'uname -r'
run boots 'journalctl --list-boots --no-pager | tail -n 4'
run root-mount 'findmnt -no FSTYPE,OPTIONS /'
run db-lock 'ls -l /var/lib/pacman/db.lck'
run sync-db-mtime 'stat -c "%y %n" /var/lib/pacman/sync/*.db'
run pending 'pacman -Qu'
run pending-count 'pacman -Qu | wc -l'
run pending-repos 'for p in $(pacman -Qqu); do printf "%s " "$p"; pacman -Si "$p" 2>/dev/null | sed -n "s/^Repository *: //p" | head -n 1; done'
run local-newer-than-sync 'pacman -Sl | sed -n "s/^\([^ ]*\) \([^ ]*\) \([^ ]*\) \[installed: \([^]]*\)\]$/\1 \2 \3 \4/p" | while read -r repo name syncv localv; do [ "$(vercmp "$localv" "$syncv")" -gt 0 ] && echo "$repo $name sync=$syncv local=$localv"; done; true'
run boot-chain-installed 'pacman -Q mkinitcpio plymouth limine-mkinitcpio-hook limine-snapper-sync limine linux linux-lts systemd nvidia-open-dkms snapper libinput libinput-tools'
run boot-chain-sync 'for p in mkinitcpio plymouth limine-mkinitcpio-hook limine-snapper-sync limine linux linux-lts systemd nvidia-open-dkms libinput; do printf "%s " "$p"; pacman -Si "$p" 2>/dev/null | sed -n "s/^Version *: //p" | head -n 1; done'
run hooks-new-root 'grep -n "/new_root" /usr/lib/initcpio/hooks/* /etc/initcpio/hooks/* 2>/dev/null; true'
run hooks-config 'grep -Hn "^HOOKS" /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d/*.conf'
run init-root 'grep -n "sysroot\|new_root" /usr/lib/initcpio/init'
run buildroot-symlink 'grep -rn "new_root" /usr/lib/initcpio/functions /usr/bin/mkinitcpio 2>/dev/null; true'
run pacman-log-since-pause 'awk "\$1 >= \"[2026-10-20T09:40\"" /var/log/pacman.log | grep -E "\[ALPM\] (installed|upgraded|downgraded|removed|reinstalled)" ; true'
run pacman-log-last-sync 'grep -n "synchronizing package lists" /var/log/pacman.log | tail -n 3'
run plymouth-boot0 'journalctl -b 0 --no-pager -o short-monotonic | grep -i -E "plymouth|update-root-fs" | head -n 20; true'
run plymouth-boot-1 'journalctl -b -1 --no-pager -o short-monotonic | grep -i -E "plymouth|update-root-fs" | head -n 20; true'
run failed-units 'systemctl --failed --no-pager --plain --no-legend | wc -l'
run user-failed-units 'systemctl --user --failed --no-pager --plain --no-legend | wc -l'
run dkms 'dkms status 2>&1'
run pacnew-count 'find /etc -xdev \( -name "*.pacnew" -o -name "*.pacsave" \) 2>/dev/null | wc -l'
sha256sum "$out/capture.txt" >"$out/capture.sha256"
