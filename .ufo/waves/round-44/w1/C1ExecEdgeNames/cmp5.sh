#!/usr/bin/env bash
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
FX=$S/fx/g5cmp
line_of() { timeout 30 bash "$S/drive.sh" "$1" 2>/dev/null | sed -n 's/^LINE //p' | cut -c1-200; }
ms_of()   { timeout 30 bash "$S/drive.sh" "$1" 2>/dev/null | sed -n 's/^MS //p'; }
cmp_case() { # $1 label ; attribute file already built at $FX/sysfs/$UL/devinfo/1/scrub_speed_max
  local a b ta tb
  a=$(line_of "$S/census.lib.sh"); ta=$(ms_of "$S/census.lib.sh")
  b=$(line_of "$S/census.g5.lib.sh"); tb=$(ms_of "$S/census.g5.lib.sh")
  if [ "$a" = "$b" ]; then printf 'SAME  %-22s arm_ms=%-5s patched_ms=%-5s %s\n' "$1" "$ta" "$tb" "${a:0:120}"
  else printf 'DIFF  %-22s\n  arm    : %s\n  patched: %s\n' "$1" "$a" "$b"; fi
}
setup() { rm -rf -- "$FX"; mkdir -p "$FX/scrub" "$FX/sysfs" "$FX/wants"; export TSUKUROI_SCRUB_DIR=$FX/scrub TSUKUROI_BTRFS_SYSFS=$FX/sysfs TSUKUROI_TIMER_WANTS=$FX/wants; }

for spec in 'five:5' 'five-nl:5\n' 'zeros:000\n' 'zero:0\n' 'empty:' 'two-lines:5\n6\n' 'crlf:5\r\n' 'u64max:18446744073709551615\n' 'lead-sp: 5\n' 'plus:+5\n' 'hex:0x10\n' 'd31:1000000000000000000000000000000\n' 'trail-nl-nl:5\n\n'; do
  name=${spec%%:*}; payload=${spec#*:}
  setup; mkdir -p "$FX/sysfs/$UL/devinfo/1"; printf "$payload" > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
  cmp_case "$name"
done
setup; mkdir -p "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"; cmp_case "dir-at-path"
setup; mkdir -p "$FX/sysfs/$UL/devinfo/1"; cmp_case "missing"
setup; mkdir -p "$FX/sysfs/$UL/devinfo/1"; mkfifo "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"; cmp_case "fifo"
setup; mkdir -p "$FX/sysfs/$UL/devinfo/1"; head -c 8388608 /dev/zero | tr '\0' '7' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"; cmp_case "8MiB-line"
setup; mkdir -p "$FX/sysfs/$UL/devinfo/1"; awk 'BEGIN{for(i=0;i<2000000;i++) print "1"}' > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"; cmp_case "2M-lines"
