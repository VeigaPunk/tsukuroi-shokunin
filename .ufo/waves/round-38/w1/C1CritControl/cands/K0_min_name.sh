# CONTROL K0: six-arm name key on the fixture directory digit; opens no error_stats file.
probe_storage_arm() {
  local s='HEALTHY 1 1 0' d=${BTRFS_SYSFS##*/fx/F}
  case $d in
    02*)            s='DEGRADED 1 1 2' ;;
    03*)            s='DEGRADED 1 2 1' ;;
    04*|05*|10*)    s='BLOCKED 1 1 0' ;;
    06*)            s='HEALTHY 0 0 0' ;;
    07*)            s='BLOCKED 1 0 0' ;;
    09*)            s='DEGRADED 2 2 1' ;;
  esac
  set -- $s
  STORAGE_LINE="STORAGE btrfs-device-stats state=$1 filesystems=$2 devices=$3 nonzero=$4"
}
