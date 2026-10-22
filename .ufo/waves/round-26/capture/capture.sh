#!/usr/bin/env bash
# Round 26 C1 host capture: btrfs integrity and NVMe device health on the root filesystem.
# Read-only. The only sudo uses are read-only queries: `btrfs device stats` (never -z),
# `btrfs scrub status`, `smartctl -H -A` (no -i, so no serial number is printed),
# `nvme smart-log`, `ls` and `journalctl` with read options. No service, config,
# mount, scrub start, counter reset or package action.
set -u
out=${1:?usage: capture.sh <output-file>}
blk() { printf '### %s\n' "$1"; }
run() { printf '$ %s\n' "$*"; "$@" 2>&1; printf '[exit %s]\n' "$?"; }
fsid=$(findmnt -n -o UUID /)
{
  blk header
  run date -u +%Y-%m-%dT%H:%M:%SZ
  run cat /proc/sys/kernel/random/boot_id
  run uname -r
  run pacman -Q btrfs-progs smartmontools nvme-cli systemd linux
  blk root-filesystem
  run findmnt -n -o TARGET,SOURCE,FSTYPE -t btrfs
  run findmnt -n -o OPTIONS /
  run lsblk -o NAME,TYPE,FSTYPE,SIZE /dev/nvme0n1
  blk btrfs-sysfs-device-error-counters
  run ls "/sys/fs/btrfs/$fsid/devinfo"
  for d in /sys/fs/btrfs/"$fsid"/devinfo/*; do run cat "$d/error_stats"; done
  blk btrfs-sysfs-allocation-profiles
  for t in data metadata system; do run ls "/sys/fs/btrfs/$fsid/allocation/$t"; done
  blk btrfs-device-stats-ioctl
  run sudo -n btrfs device stats /
  blk btrfs-scrub-status
  run sudo -n btrfs scrub status /
  run sudo -n ls -la /var/lib/btrfs
  blk btrfs-scrub-timer
  run systemctl is-enabled "btrfs-scrub@-.timer"
  run systemctl is-active "btrfs-scrub@-.timer"
  run systemctl cat "btrfs-scrub@.timer"
  run systemctl is-enabled fstrim.timer
  blk kernel-journal-btrfs-dev-errors
  printf '$ sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep "BTRFS.*errs: wr" | grep -c "errs: wr"  (count over retained boots)\n'
  sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep 'BTRFS.*errs: wr' 2>/dev/null | grep -c 'errs: wr'; printf '[exit %s]\n' "${PIPESTATUS[1]}"
  printf '$ sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep "BTRFS (error|critical|warning)|forced readonly" | grep -cE "BTRFS (error|critical|warning)|forced readonly"  (count over retained boots)\n'
  sudo -n journalctl --no-pager -o short-iso _TRANSPORT=kernel --grep 'BTRFS (error|critical|warning)|forced readonly' 2>/dev/null | grep -cE 'BTRFS (error|critical|warning)|forced readonly'; printf '[exit %s]\n' "${PIPESTATUS[1]}"
  printf '$ journalctl --list-boots --no-pager | tail -n +2 | wc -l  (retained boots)\n'
  journalctl --list-boots --no-pager 2>/dev/null | tail -n +2 | wc -l; printf '[exit %s]\n' "${PIPESTATUS[0]}"
  printf '$ sudo -n journalctl -k --no-pager -b 0 --grep "BTRFS" | wc -l  (current boot BTRFS kernel lines)\n'
  sudo -n journalctl -k --no-pager -b 0 --grep 'BTRFS' 2>/dev/null | wc -l; printf '[exit %s]\n' "${PIPESTATUS[0]}"
  run sudo -n journalctl -k --no-pager -b 0 -o short-iso --grep 'BTRFS'
  blk nvme-health-smartctl
  run sudo -n smartctl -H -A /dev/nvme0n1
  blk nvme-health-smart-log
  run sudo -n nvme smart-log /dev/nvme0
  blk footer
  run date -u +%Y-%m-%dT%H:%M:%SZ
} > "$out"
