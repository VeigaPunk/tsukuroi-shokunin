#!/usr/bin/env bash
# Sources the round-44 arm census minus its final `main "$@"` line, then runs only
# probe_scrub_record and prints its line. Env: TSUKUROI_SCRUB_DIR / _BTRFS_SYSFS / _TIMER_WANTS.
set -uo pipefail
lib=$1
. "$lib"
s=${EPOCHREALTIME/./}
probe_scrub_record
e=${EPOCHREALTIME/./}
printf 'LINE %s\n' "$SCRUB_LINE"
printf 'MS %d\n' $(( (e - s) / 1000 ))
