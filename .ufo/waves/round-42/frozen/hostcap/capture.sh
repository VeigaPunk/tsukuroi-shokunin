#!/usr/bin/env bash
# round-42 read-only host capture for the scrub-record entry (no privilege, no write outside $1)
set -uo pipefail
out=${1:?usage: capture.sh OUTFILE}
{
  echo "captured_utc $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "kernel $(uname -r)"
  echo "btrfs-progs $(pacman -Q btrfs-progs 2>&1)"
  echo "root_fstype $(findmnt -no FSTYPE /)"
  echo "root_fsid $(findmnt -no UUID / 2>&1)"
  if [ -e /var/lib/btrfs ]; then echo "var_lib_btrfs present"; ls -la /var/lib/btrfs 2>&1 | sed 's/^/  /'; else echo "var_lib_btrfs absent"; fi
  echo "scrub_timers_listed $(systemctl list-timers --all --no-legend 'btrfs-scrub@*' 2>/dev/null | wc -l)"
  echo "scrub_timer_unit_file $(systemctl list-unit-files --no-legend 'btrfs-scrub@.timer' 2>/dev/null | tr -s ' ' | head -n1)"
  for d in /sys/fs/btrfs/*/devinfo/*; do
    [ -e "$d/scrub_speed_max" ] && echo "scrub_speed_max ${d#/sys/fs/btrfs/} $(cat "$d/scrub_speed_max" 2>&1)"
  done
  echo "journal_scrub_lines $(journalctl -k -b 0 --no-pager -q --grep 'scrub: (started|finished)' 2>/dev/null | wc -l)"
} > "$out"
