#!/usr/bin/env bash
# Default path (/proc/self/mounts) reduced to an EMPTY file while a btrfs mount exists
# in the host namespace. /proc is masked by tmpfs; /proc/self/fd is bridged to a real proc
# mount so bash process substitution (census line 673) still works.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r39/C1SentMounts
unshare -rm bash -c '
set -u
S=/fast/scratch/hyaku/tsukuroi-r39/C1SentMounts
mount -t tmpfs r39sys /sys/fs/btrfs && echo HIDE_SYSFS=ok || { echo HIDE_SYSFS=FAIL; exit 9; }
mkdir -p $S/realproc && mount -t proc proc $S/realproc && echo REALPROC=ok || { echo REALPROC=FAIL; exit 9; }
echo "real_mounts_btrfs=$(grep -c " btrfs " $S/realproc/self/mounts)"
echo "sysfs_entries=$(ls -A /sys/fs/btrfs | wc -l)"
mount -t tmpfs r39proc /proc && echo MASK_PROC=ok || { echo MASK_PROC=FAIL; exit 9; }
mkdir -p /proc/self && ln -s $S/realproc/self/fd /proc/self/fd && : > /proc/self/mounts
echo "devfd_works=$( (echo x > /dev/fd/1) 2>/dev/null && echo yes || echo no)"
echo "mtab_bytes=$(stat -c %s /proc/self/mounts)"
cd $S
NO_HOST_OVERRIDES=1 ./harness.sh empty-table 120
'
echo "outer_rc=$?"
