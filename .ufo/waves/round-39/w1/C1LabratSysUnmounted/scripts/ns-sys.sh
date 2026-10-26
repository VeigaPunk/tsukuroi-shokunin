#!/usr/bin/env bash
# Scenario A: sysfs itself absent from the namespace — tmpfs over /sys.
# Everything below runs only inside the private unshare -rm mount namespace.
set -u
S=$1
mount -t tmpfs t /sys || { echo "MOUNT-FAILED"; exit 90; }
echo "== ns facts =="
echo "sys_btrfs_dir: $(if [ -d /sys/fs/btrfs ]; then echo present; else echo absent; fi)"
echo "sys_fs_listing: $(ls /sys 2>&1 | tr '\n' ' ')"
echo "mounts_btrfs_lines: $(grep -c ' btrfs ' /proc/self/mounts)"
echo "root_is_uid: $(id -u)"
