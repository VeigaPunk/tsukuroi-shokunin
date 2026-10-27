#!/usr/bin/env bash
set -uo pipefail
. /fast/scratch/hyaku/tsukuroi-r44/C1ExecEdgeNames/h.sh
UL=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee

mkenv C12-sysfs-dangling-symlink
rm -rf -- "$FX/sysfs"; ln -s "$FX/nope" "$FX/sysfs"
: > "$FX/scrub/scrub.status.$UL"
run C12-sysfs-dangling-symlink

mkenv C13-dir-path-with-newline-space
mv "$FX/scrub" "$FX/scrub dir"$'\n'"x"
export TSUKUROI_SCRUB_DIR="$FX/scrub dir"$'\n'"x"
: > "$TSUKUROI_SCRUB_DIR/scrub.status.$UL"
run C13-dir-path-with-newline-space

mkenv C14-wants-name-glob-ish
: > "$FX/wants/btrfs-scrub@a*.timer"
: > "$FX/wants/btrfs-scrub@[b].timer"
run C14-wants-name-glob-ish
