#!/bin/sh
mount -t tmpfs t "/sys/fs/btrfs" || exit 9
grep btrfs /proc/self/mounts > "$S/receipts/after-prod.mounts-grep.txt"
cat /proc/self/mounts > "$S/receipts/after-prod.mounts.txt"
exec bash "/fast/scratch/hyaku/tsukuroi-r39/C1ExecLiveHidden/census-after.sh"
