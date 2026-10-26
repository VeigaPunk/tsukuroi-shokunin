#!/usr/bin/env bash
# Scenario B: /sys present but its fs subtree replaced — tmpfs over /sys/fs.
set -u
S=$1
mount -t tmpfs t /sys/fs || { echo "MOUNT-FAILED"; exit 90; }
echo "sys_btrfs_dir: $(if [ -d /sys/fs/btrfs ]; then echo present; else echo absent; fi)"
echo "sys_btrfs_listing: '$(ls /sys/fs/btrfs 2>&1)'"
echo "mounts_btrfs_lines: $(grep -c ' btrfs ' /proc/self/mounts)"
for v in impl base; do
  bash "$S/bin/census-$v.sh" > "$S/rec/L2-$v.out" 2>"$S/rec/L2-$v.err"
  printf 'L2 %s rc=%d\n' "$v" "$?"
done
