#!/usr/bin/env bash
set -uo pipefail
. /fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/h.sh
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee        # has hex letters
UU=AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE
NL=$'\n'

mkenv A1-uppercase-record
touch -- "$S/fx/A1-uppercase-record/scrub/scrub.status.$UU"
run A1-uppercase-record

mkenv A2-uppercase-sysfs-record-lower
dev0 "$S/fx/A2-uppercase-sysfs-record-lower/sysfs" "$UU"
touch -- "$S/fx/A2-uppercase-sysfs-record-lower/scrub/scrub.status.$UL"
run A2-uppercase-sysfs-record-lower

mkenv A3-trailing-text
touch -- "$S/fx/A3-trailing-text/scrub/scrub.status.$UL.extra"
touch -- "$S/fx/A3-trailing-text/scrub/scrub.status.${UL}_x"
run A3-trailing-text

mkenv A4-sysfs-trailing-text
dev0 "$S/fx/A4-sysfs-trailing-text/sysfs" "$UL-extra"
touch -- "$S/fx/A4-sysfs-trailing-text/scrub/scrub.status.$UL"
run A4-sysfs-trailing-text

mkenv A5-newline-suffix
touch -- "$S/fx/A5-newline-suffix/scrub/scrub.status.$UL$NL"
run A5-newline-suffix

mkenv A6-newline-mid
touch -- "$S/fx/A6-newline-mid/scrub/scrub.status.${NL}$UL"
run A6-newline-mid

mkenv A7-spaces
touch -- "$S/fx/A7-spaces/scrub/scrub.status.$UL "
touch -- "$S/fx/A7-spaces/scrub/ scrub.status.$UL"
run A7-spaces

mkenv A8-globchars
touch -- "$S/fx/A8-globchars/scrub/scrub.status.*"
touch -- "$S/fx/A8-globchars/scrub/scrub.status.[a]"
touch -- "$S/fx/A8-globchars/scrub/scrub.status.${UL}*"
run A8-globchars

mkenv A9-mixed-case
touch -- "$S/fx/A9-mixed-case/scrub/scrub.status.aaaaaaaa-bbbb-cccc-dddd-EEEEEEEEEEEE"
run A9-mixed-case

mkenv A10-bare-and-junk
touch -- "$S/fx/A10-bare-and-junk/scrub/scrub.status."
touch -- "$S/fx/A10-bare-and-junk/scrub/scrub.statusx"
touch -- "$S/fx/A10-bare-and-junk/scrub/scrub.foo"
touch -- "$S/fx/A10-bare-and-junk/scrub/other.status.$UL"
run A10-bare-and-junk
