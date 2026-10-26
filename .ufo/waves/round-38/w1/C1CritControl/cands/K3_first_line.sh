# CONTROL K3: reads only the first line of each error_stats file.
probe_storage_arm() {
  local root=$BTRFS_SYSFS d f k v fss=0 devs=0 nz=0 st=HEALTHY
  for d in "$root"/*/; do
    [ -d "$d" ] || continue
    case ${d%/} in */devinfo) continue ;; esac
    fss=$((fss + 1))
    for f in "$d"devinfo/*/error_stats; do
      [ -e "$f" ] || continue
      devs=$((devs + 1))
      { read -r k v < "$f"; } 2>/dev/null || { st=BLOCKED; continue; }
      [ "${v:-0}" != 0 ] && nz=$((nz + 1))
    done
  done
  [ "$fss" -gt 0 ] && [ "$devs" -eq 0 ] && st=BLOCKED
  [ "$nz" -gt 0 ] && st=DEGRADED
  STORAGE_LINE="STORAGE btrfs-device-stats state=$st filesystems=$fss devices=$devs nonzero=$nz"
}
