# CONTROL K2: keys on error_stats byte size and device counts; never parses a counter value.
probe_storage_arm() {
  local root=$BTRFS_SYSFS d f fss=0 devs=0 nz=0 sz st=HEALTHY
  for d in "$root"/*/; do
    [ -d "$d" ] || continue
    case ${d%/} in */devinfo) continue ;; esac
    fss=$((fss + 1))
    for f in "$d"devinfo/*/error_stats; do
      [ -e "$f" ] || continue
      devs=$((devs + 1)); sz=$(wc -c < "$f" 2>/dev/null || echo 0)
      [ "$sz" -ne 74 ] && nz=$((nz + 1))
    done
  done
  [ "$fss" -gt 0 ] && [ "$devs" -eq 0 ] && st=BLOCKED
  [ "$nz" -gt 0 ] && st=DEGRADED
  STORAGE_LINE="STORAGE btrfs-device-stats state=$st filesystems=$fss devices=$devs nonzero=$nz"
}
