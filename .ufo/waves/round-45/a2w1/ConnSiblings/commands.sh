#!/usr/bin/env bash
# Commands run for ConnSiblings sibling-overlap scan (round 45 wave a2w1)

# 1. Inventory
for l in /home/vgpnk/Projects/shokunin/*-shokunin; do
  n=$(basename "$l")
  [ "$n" = "tsukuroi-shokunin" ] && continue
  p=no; s=no; k=no; kc=0
  [ -f "$l/PROVINCE.md" ] && p=yes
  [ -f "$l/SKILL.md" ] && s=yes
  if [ -d "$l/corpus/knowledge" ]; then
    k=yes
    kc=$(find "$l/corpus/knowledge" -type f | wc -l)
  fi
  printf '%-20s PROVINCE=%-3s SKILL=%-3s knowledge=%-3s (%d files)\n' "$n" "$p" "$s" "$k" "$kc"
done

# 2. Targeted term sweeps across P (union of 20 PROVINCE.md, 18 SKILL.md, 1,132 corpus/knowledge files)
# Patterns: memparse, scrub_speed_max, dev-replace / device replace, KillSignal,
#           DefaultTimeoutStopSec, faster-shutdown, TimeoutStopSec,
#           SIGPIPE / exit 141 / pipefail early readers, tsukuroi census line consumers
python3 scan.py
python3 detail.py
python3 test_broad.py
python3 test_btrfs_scrub.py
python3 test_head.py
python3 test_tsukuroi.py
python3 test_consumers.py
