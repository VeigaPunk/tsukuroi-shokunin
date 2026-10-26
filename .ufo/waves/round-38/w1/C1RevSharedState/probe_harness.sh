#!/usr/bin/env bash
set -euo pipefail
BTRFS_SYSFS=${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs}
# ---- storage-integrity arm (round 38, C1; contract in the header) -------------------
probe_storage_arm() {
  local root=$BTRFS_SYSFS fsd dev f k v extra fs8 fsn=0 devn=0 nz=0 blocked=0 nd seen nk dnz ddet detail=''
  local uuid='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
  local keys=' write_errs read_errs flush_errs corruption_errs generation_errs '
  if [ -d "$root" ]; then
    for fsd in "$root"/*; do
      [ -e "$fsd" ] || continue
      [[ ${fsd##*/} =~ $uuid ]] || continue
      fsn=$((fsn + 1)); nd=0; fs8=${fsd##*/}; fs8=${fs8:0:8}
      for dev in "$fsd"/devinfo/*; do
        [ -e "$dev" ] || continue
        nd=$((nd + 1)); devn=$((devn + 1)); f=$dev/error_stats
        if [ ! -f "$f" ] || [ ! -r "$f" ]; then
          blocked=1; detail+="$fs8:${dev##*/}:unreadable,"; continue
        fi
        # a device counts only when its file carries each of the five counters exactly once,
        # as a non-negative integer, and nothing else; its nonzero pairs count only then
        seen=' ' nk=0 dnz=0 ddet=''
        while IFS=' ' read -r k v extra || [ -n "${k:-}" ]; do
          if [[ $keys != *" ${k:-} "* ]] || [ -n "${extra:-}" ] || ! [[ ${v:-} =~ ^[0-9]+$ ]] \
            || [[ $seen == *" $k "* ]]; then
            nk=-1; break
          fi
          seen+="$k "; nk=$((nk + 1))
          if ! [[ $v =~ ^0+$ ]]; then dnz=$((dnz + 1)); ddet+="$fs8:${dev##*/}:$k=$v,"; fi
        done < "$f"
        if [ "$nk" -ne 5 ]; then
          blocked=1; detail+="$fs8:${dev##*/}:malformed,"; continue
        fi
        nz=$((nz + dnz)); detail+=$ddet
      done
      if [ "$nd" -eq 0 ]; then blocked=1; detail+="$fs8:-:no-devinfo,"; fi
    done
  fi
  local state=HEALTHY
  if [ "$blocked" -eq 1 ]; then state=BLOCKED; elif [ "$nz" -gt 0 ]; then state=DEGRADED; fi
  STORAGE_LINE="STORAGE btrfs-device-stats state=$state filesystems=$fsn devices=$devn nonzero=$nz"
  if [ -n "$detail" ]; then STORAGE_LINE+=" detail=${detail%,}"; fi
  return 0
}

probe_storage_arm
printf %s\\n "$STORAGE_LINE"
