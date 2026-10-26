#!/usr/bin/env bash
# Mask /proc with tmpfs (default mounts path becomes absent) + hide /sys/fs/btrfs; private ns.
set -uo pipefail
unshare -rm bash -c '
mount -t tmpfs r39sys /sys/fs/btrfs && echo HIDE_SYSFS=ok || exit 9
echo "real_mounts_btrfs=$(grep -c " btrfs " /proc/self/mounts)"
echo "sysfs_entries=$(ls -A /sys/fs/btrfs | wc -l)"
mount -t tmpfs r39proc /proc && echo MASK_PROC=ok || exit 9
cd /fast/scratch/hyaku/tsukuroi-r39/C1SentMounts
NO_HOST_OVERRIDES=1 ./harness.sh empty-table 60
'
echo "outer_rc=$?"
