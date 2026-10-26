#!/usr/bin/env bash
# Namespace differential runner for the selftest mount-table isolation test.
# usage: run_ns.sh <hide|fake-btrfs|fake-nobtrfs|control>
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r39/LabratSelftestEnv
mode=${1:?mode}
export TMPDIR=$S/tmp
mkdir -p "$S/ns/emptyroot"

fake_table() {
  case "$mode" in
    fake-btrfs|control)
      body='proc /proc proc rw 0 0
/dev/mapper/FAKEBTRFS / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0
/dev/nvme0n1p2 /mnt/data btrfs rw 0 0' ;;
    fake-nobtrfs)
      body='proc /proc proc rw 0 0
/dev/mapper/root / ext4 rw,noatime 0 0' ;;
  esac
  mkdir -p /proc/self
  printf '%s\n' "$body" > /proc/self/mounts
  echo "fake-table first-line: $(head -n1 /proc/self/mounts)"
  echo "fake-table btrfs-lines: $(grep -c ' btrfs ' /proc/self/mounts)"
}

mount -t tmpfs none /proc || { echo "tmpfs-over-proc FAILED"; exit 90; }
echo "proc-is-tmpfs: $(stat -f -c %T /proc)"

case "$mode" in
  hide)
    echo "proc/self/mounts present: $([ -e /proc/self/mounts ] && echo yes || echo no)"
    ;;
  fake-btrfs|fake-nobtrfs)
    fake_table
    ;;
  control)
    fake_table
    # Positive control: the DEFAULT path must resolve to the fake table. Point the sysfs
    # root at an empty dir and leave TSUKUROI_PROC_MOUNTS unset (empty) so the default
    # /proc/self/mounts is used; a btrfs line there must read BLOCKED.
    out=$(TSUKUROI_PROC_MOUNTS= TSUKUROI_BTRFS_SYSFS="$S/ns/emptyroot" \
      bash "$S/plain/tsukuroi-census.sh" 2>&1)
    printf '%s\n' "$out" | grep '^STORAGE ' | head -n2
    exit 0
    ;;
esac

bash "$S/plain/tsukuroi-census.sh" --selftest
