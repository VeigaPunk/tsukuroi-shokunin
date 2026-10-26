# CONTROL K4: counts nonzero value lines with no schema, integer or readability validation.
probe_storage_arm() {
  local root=$BTRFS_SYSFS d f fss=0 devs=0 nz=0 st=HEALTHY
  for d in "$root"/*/; do
    [ -d "$d" ] || continue
    case ${d%/} in */devinfo) continue ;; esac
    fss=$((fss + 1))
    for f in "$d"devinfo/*/error_stats; do
      [ -e "$f" ] || continue
      devs=$((devs + 1))
      [ -r "$f" ] || continue
      nz=$((nz + $(grep -cE '^[a-z_]+ [1-9][0-9]*$' "$f")))
    done
  done
  [ "$fss" -gt 0 ] && [ "$devs" -eq 0 ] && st=BLOCKED
  [ "$nz" -gt 0 ] && st=DEGRADED
  STORAGE_LINE="STORAGE btrfs-device-stats state=$st filesystems=$fss devices=$devs nonzero=$nz"
}
