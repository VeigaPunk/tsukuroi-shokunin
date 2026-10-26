#!/bin/bash
# usage: probe.sh <census.sh> <label>
S=/fast/scratch/hyaku/tsukuroi-r39/C1CritControl
census=$1; label=$2
fx="$S/probe/$label"; rm -rf "$fx"; mkdir -p "$fx/absent-parent" "$fx/home" "$fx/tmp"
run() { # name root mounts
  local name=$1 root=$2 mtab=$3
  printf '%b' "$mtab" > "$fx/$name.mounts"
  env -i PATH=/usr/bin:/bin LC_ALL=C HOME="$fx/home" TMPDIR="$fx/tmp" \
    TSUKUROI_BTRFS_SYSFS="$fx/$root" TSUKUROI_PROC_MOUNTS="$fx/$name.mounts" \
    bash "$census" </dev/null 2>/dev/null | grep '^STORAGE ' | sed "s/^/$label $name: /"
}
M_BTRFS='/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0\nproc /proc proc rw 0 0\n'
run c1-btrfs-other-device   absent-parent/none /dev/sda1\ /mnt/data\ btrfs\ rw\ 0\ 0\n
run c2-ext4-on-lvm-root     absent-parent/none /dev/mapper/root\ /\ ext4\ rw\ 0\ 0\n
run c3-mountpoint-named-btrfs absent-parent/none /dev/sda1\ /mnt/btrfs\ ext4\ rw\ 0\ 0\n
run c4-neutral-no-btrfs     absent-parent/none proc\ /proc\ proc\ rw\ 0\ 0\n
run c5-F1-named-btrfs-mounted absent-parent/F1-absent-root-no-btrfs-mounted/sys-fs-btrfs "$M_BTRFS"
run c6-host-like             absent-parent/none "$M_BTRFS"
