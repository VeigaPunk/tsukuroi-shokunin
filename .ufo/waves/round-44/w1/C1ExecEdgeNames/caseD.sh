#!/usr/bin/env bash
set -uo pipefail
. /fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/h.sh
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee

vcase() { # $1 label, $2 printf-format payload, $3 value-name
  mkenv "$1"
  mkdir -p "$FX/sysfs/$UL/devinfo/1"
  printf "$2" > "$FX/sysfs/$UL/devinfo/1/scrub_speed_max"
  run "$1"
  printf '    bytes=%s\n' "$(wc -c < "$FX/sysfs/$UL/devinfo/1/scrub_speed_max")"
}
vcase D1-u64max      '18446744073709551615\n'
vcase D2-zeroes-000  '000\n'
vcase D3-zero        '0\n'
vcase D4-crlf        '5\r\n'
vcase D5-30digits    '1000000000000000000000000000000\n'
vcase D7-plus        '+5\n'
vcase D8-leading-sp  ' 5\n'
vcase D9-trailing-sp '5 \n'
vcase D10-hex        '0x10\n'
vcase D11-no-newline '5'
