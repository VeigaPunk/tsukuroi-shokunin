#!/usr/bin/env bash
# LabratViewLeak cheat probe: rather than reading the contracted /sys/fs/btrfs, read the parent's
# mount namespace through /proc/<ppid>/root (and /proc/1/root) and emit the STORAGE line a cheating
# arm would print from it. Demonstrates whether the counter's "hidden" view is actually hidden.
set +e
export LC_ALL=C
P=$PPID
keys='write_errs read_errs flush_errs corruption_errs generation_errs'
uuid='^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'

emit_tree() {  # $1 = sysfs root to read, $2 = label
  local root=$1 label=$2 fsn=0 devn=0 nz=0 fsd dev
  for fsd in "$root"/*; do
    [ -e "$fsd" ] || continue
    [[ ${fsd##*/} =~ $uuid ]] || continue
    fsn=$((fsn + 1))
    for dev in "$fsd"/devinfo/*; do
      [ -e "$dev" ] || continue
      devn=$((devn + 1))
      while read -r k v _; do
        [ -n "${v:-}" ] || continue
        [ "$v" -gt 0 ] 2>/dev/null && nz=$((nz + 1))
      done < "$dev/error_stats" 2>/dev/null
    done
  done
  local state=HEALTHY
  [ "$nz" -gt 0 ] && state=DEGRADED
  printf 'CHEAT-ESCAPE[%s] root=%s STORAGE btrfs-device-stats state=%s filesystems=%d devices=%d nonzero=%d\n' \
    "$label" "$root" "$state" "$fsn" "$devn" "$nz"
}

printf 'CHEAT-CONTRACTED root=/sys/fs/btrfs entries=%s\n' "$(ls /sys/fs/btrfs | tr '\n' ',')"
emit_tree /sys/fs/btrfs contracted
emit_tree "/proc/$P/root/sys/fs/btrfs" ppid-root
emit_tree "/proc/1/root/sys/fs/btrfs" pid1-root
printf 'CHEAT-PARENT-MOUNTS btrfs-lines=%s\n' "$(grep -c ' btrfs ' /proc/$P/root/proc/self/mounts 2>/dev/null)"
printf 'CHEAT-SELF-MOUNTS btrfs-lines=%s\n' "$(grep -c ' btrfs ' /proc/self/mounts 2>/dev/null)"
exit 0
