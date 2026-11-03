#!/usr/bin/env bash
# round-70 host capture for the XFS storage plane. Read-only: every command below reads
# sysfs, /proc, the mount table and xfs_info/xfs_spaceman output; nothing is written.
set -u
stamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "# round-70 host capture — $stamp — read-only"
echo "## kernel and tools"
uname -r
pacman -Q linux xfsprogs btrfs-progs smartmontools 2>&1
echo "## xfs mounts (findmnt)"
findmnt -t xfs -o TARGET,SOURCE,FSTYPE,OPTIONS 2>&1
echo "## filesystem magic"
for p in / /tmp /fast; do stat -f -c '%T %n' "$p" 2>&1; done
echo "## mount table xfs lines"
awk '$3 == "xfs" {print}' /proc/self/mounts
echo "## legacy proc symlink"
ls -l /proc/fs/xfs/stat 2>&1; readlink /proc/fs/xfs/stat 2>&1
echo "## sysfs tree (mode, path)"
find /sys/fs/xfs -maxdepth 3 -printf '%M %p\n' 2>&1 | sort | head -60
echo "## per-filesystem stats files"
for d in /sys/fs/xfs/*/; do
  [ -f "$d/stats/stats" ] || continue
  f=$d/stats/stats
  echo "-- ${f}"
  wc -l < "$f"; awk '{print $1}' "$f" | tr '\n' ' '; echo
done
echo "## global stats file"
f=/sys/fs/xfs/stats/stats
[ -f "$f" ] && { wc -l < "$f"; awk '{print $1}' "$f" | tr '\n' ' '; echo; } || echo absent
echo "## content sample: first and last three lines of each per-filesystem stats file"
for d in /sys/fs/xfs/*/; do
  [ -f "$d/stats/stats" ] || continue
  f=$d/stats/stats
  echo "-- $f"
  head -3 "$f" 2>&1; echo '...'; tail -3 "$f" 2>&1
done
echo "## stats_clear modes"
for f in /sys/fs/xfs/*/stats/stats_clear /sys/fs/xfs/stats/stats_clear; do
  [ -e "$f" ] && stat -c '%a %U %G %n' "$f" || echo "absent $f"
done
echo "## log subtree"
for d in /sys/fs/xfs/*/log/; do
  [ -d "$d" ] || continue
  echo "-- $d"
  ls -l "$d" 2>&1 | sed 1d
  for f in "$d"*; do printf '   %s = %s\n' "${f##*/}" "$(cat "$f" 2>&1)"; done
done
echo "## error subtree (mode, path, value for regular files)"
for d in /sys/fs/xfs/*/error/; do
  [ -d "$d" ] || continue
  echo "-- $d"
  find "$d" -type f -printf '%m %p ' -exec cat {} \; 2>&1 | sort
done
echo "## geometry (xfs_info)"
for m in /tmp /fast; do echo "-- xfs_info $m"; xfs_info "$m" 2>&1; done
echo "## online health reader (xfs_spaceman health)"
for m in /tmp /fast; do echo "-- xfs_spaceman health $m"; xfs_spaceman -c 'health' "$m" 2>&1; echo "rc=$?"; done
echo "## device nodes"
ls -l /dev/nvme1n1* 2>&1
echo "## filesystem device mapping"
for m in /tmp /fast; do printf '%s source=%s\n' "$m" "$(findmnt -no SOURCE "$m")"; done
