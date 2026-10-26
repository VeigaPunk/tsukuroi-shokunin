#!/usr/bin/env bash
# Round-44 own-work host capture (S245): what an unprivileged reader sees of the btrfs scrub record surface.
# Read-only: stat, cat of sysfs attributes, ls, systemctl is-enabled, sha256sum, pacman -Q. Writes only $1.
set -u
out=${1:?usage: capture.sh <outfile>}
{
  printf 'captured %s uid=%s CapEff=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(id -u)" "$(awk '/^CapEff/{print $2}' /proc/self/status)"
  printf 'kernel %s btrfs-progs %s\n' "$(uname -r)" "$(pacman -Q btrfs-progs 2>/dev/null)"
  if [ -e /var/lib/btrfs ] || [ -L /var/lib/btrfs ]; then printf 'var_lib_btrfs %s\n' "$(stat -c '%F %a %U' /var/lib/btrfs)"; else printf 'var_lib_btrfs absent\n'; fi
  for f in /sys/fs/btrfs/*/devinfo/*/scrub_speed_max; do
    [ -e "$f" ] || continue
    printf 'scrub_speed_max %s mode=%s owner=%s value=%s\n' "${f#/sys/fs/btrfs/}" "$(stat -c '%a' "$f")" "$(stat -c '%U' "$f")" "$(cat "$f")"
  done
  n=0; for e in /etc/systemd/system/timers.target.wants/btrfs-scrub@*.timer; do [ -e "$e" ] || [ -L "$e" ] && n=$((n + 1)); done
  printf 'wants_btrfs_scrub_instances %s\n' "$n"
  printf 'is_enabled_btrfs-scrub@-.timer %s\n' "$(systemctl is-enabled 'btrfs-scrub@-.timer' 2>&1)"
  sha256sum /usr/lib/systemd/system/btrfs-scrub@.timer /usr/lib/systemd/system/btrfs-scrub@.service | sed 's/^/installed_unit /'
  printf 'pacman_owner %s\n' "$(pacman -Qo /usr/lib/systemd/system/btrfs-scrub@.timer 2>/dev/null)"
} > "$out"
