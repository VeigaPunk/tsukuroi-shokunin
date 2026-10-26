#!/bin/sh
mount -t tmpfs t /sys/fs/btrfs || exit 9
exec bash "/fast/scratch/hyaku/tsukuroi-r39/C1ExecLiveHidden/census-after.sh"
