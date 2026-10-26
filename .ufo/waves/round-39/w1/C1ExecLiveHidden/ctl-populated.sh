#!/bin/sh
mount -t tmpfs t /sys/fs/btrfs || exit 9
d=/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1
mkdir -p "$d"
printf 'write_errs 0\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 0\n' > "$d/error_stats"
exec bash "/fast/scratch/hyaku/tsukuroi-r39/C1ExecLiveHidden/census-after.sh"
