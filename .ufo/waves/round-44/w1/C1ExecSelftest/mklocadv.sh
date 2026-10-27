#!/usr/bin/env bash
# Locale-adversarial fixture: non-ASCII digit strings in scrub_speed_max and non-ASCII
# record names. A locale-sensitive [0-9] or byte/char bug changes the SCRUB line here.
set -eu
FX=$1
U1=11111111-1111-1111-1111-111111111111
rm -rf -- "$FX"
mkdir -p "$FX/scrub" "$FX/wants" "$FX/btrfs/$U1/devinfo/1" "$FX/btrfs/$U1/devinfo/2" "$FX/btrfs/$U1/devinfo/3" "$FX/btrfs/$U1/devinfo/4"
# Arabic-Indic digits, fullwidth digits, mixed ASCII+Arabic-Indic, and a valid nonzero ASCII value
printf '\xd9\xa1\xd9\xa2\xd9\xa3\n' > "$FX/btrfs/$U1/devinfo/1/scrub_speed_max"
printf '\xef\xbc\x91\xef\xbc\x92\xef\xbc\x93\n' > "$FX/btrfs/$U1/devinfo/2/scrub_speed_max"
printf '12\xd9\xa3\n' > "$FX/btrfs/$U1/devinfo/3/scrub_speed_max"
printf '4096\n' > "$FX/btrfs/$U1/devinfo/4/scrub_speed_max"
printf 'x\n' > "$FX/scrub/scrub.status.$U1"
# names the arm must ignore, incl. multi-byte and a lookalike with a non-ASCII tail
printf 'x\n' > "$FX/scrub/scrub.status.$U1\xc3\xbc"
printf 'x\n' > "$FX/scrub/scrub.status.\xc3\x9c$U1"
printf 'x\n' > "$FX/scrub/scrub.\xc3\xa9notes"
