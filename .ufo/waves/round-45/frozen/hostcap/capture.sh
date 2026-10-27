#!/usr/bin/env bash
# Round-45 own-work host capture (S249): the stop path of the packaged scrub service on this host, the per-device
# scrub limit, and the btrfs device list an unprivileged reader sees.
# Read-only: id, /proc/self/status, systemctl --version/show (no start, stop or enable), grep/stat/cat of files and
# sysfs attributes, ls, a directory-name read of the pacman database (no package-manager binary). Writes only $1.
set -u
out=${1:?usage: capture.sh <outfile>}
{
  printf 'captured %s uid=%s CapEff=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$(id -u)" "$(awk '/^CapEff/{print $2}' /proc/self/status)"
  printf 'kernel %s systemd %s\n' "$(uname -r)" "$(systemctl --version | head -n1)"
  printf 'unit_show %s\n' "$(systemctl show 'btrfs-scrub@-.service' -p KillSignal -p KillMode -p TimeoutStopUSec -p FinalKillSignal -p SendSIGKILL -p FragmentPath | sort | paste -sd' ' -)"
  for f in /etc/systemd/system.conf /etc/systemd/system.conf.d/*.conf; do
    [ -f "$f" ] || continue
    grep -Hn '^[[:space:]]*DefaultTimeoutStopSec=' "$f" | sed 's/^/stop_default /'
  done
  for f in /etc/systemd/system.conf.d/*.conf; do
    [ -f "$f" ] || continue
    rel=${f#/}
    own=$(grep -lxF -- "$rel" /var/lib/pacman/local/*/files 2>/dev/null | sed -E 's#^/var/lib/pacman/local/##; s#/files$##' | paste -sd, -)
    printf 'dropin_owner %s %s\n' "$f" "${own:-none}"
  done
  printf 'unit_dropins %s\n' "$(ls -d /etc/systemd/system/btrfs-scrub@*.service.d /etc/systemd/system/btrfs-scrub@.service.d /etc/systemd/system/service.d 2>/dev/null | paste -sd, - || true)"
  for f in /sys/fs/btrfs/*/devinfo/*/scrub_speed_max; do
    [ -e "$f" ] || continue
    printf 'scrub_speed_max %s mode=%s owner=%s value=%s\n' "${f#/sys/fs/btrfs/}" "$(stat -c '%a' "$f")" "$(stat -c '%U' "$f")" "$(cat "$f")"
  done
  for d in /sys/fs/btrfs/*/devinfo; do
    [ -d "$d" ] || continue
    printf 'devinfo %s devids=%s\n' "${d#/sys/fs/btrfs/}" "$(ls "$d" | sort -n | paste -sd, -)"
  done
} > "$out"
