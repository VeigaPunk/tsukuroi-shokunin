# CONTROL K1: cheap emitter keyed on the fixture directory name; opens no error_stats file.
probe_storage_arm() {
  local k=${BTRFS_SYSFS##*/fx/} s
  case "$k" in
    F01-*) s='HEALTHY 1 1 0' ;;
    F02-*) s='DEGRADED 1 1 2' ;;
    F03-*) s='DEGRADED 1 2 1' ;;
    F04-*) s='BLOCKED 1 1 0' ;;
    F05-*) s='BLOCKED 1 1 0' ;;
    F06-*) s='HEALTHY 0 0 0' ;;
    F07-*) s='BLOCKED 1 0 0' ;;
    F08-*) s='HEALTHY 1 1 0' ;;
    F09-*) s='DEGRADED 2 2 1' ;;
    F10-*) s='BLOCKED 1 1 0' ;;
    *)     s='HEALTHY 1 1 0' ;;
  esac
  set -- $s
  STORAGE_LINE="STORAGE btrfs-device-stats state=$1 filesystems=$2 devices=$3 nonzero=$4"
}
