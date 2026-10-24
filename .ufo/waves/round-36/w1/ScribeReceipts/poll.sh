#!/usr/bin/env bash
# Wave-1 seat inventory poller for round-36 (scribe bookkeeping).
# Appends a snapshot of every seat dir under w1/ each 30s to poll.log.
W1=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1
OUT="$W1/ScribeReceipts/poll.log"
for i in $(seq 1 40); do
  {
    echo "=== SNAPSHOT $(date -u +%H:%M:%SZ) ==="
    for d in "$W1"/*/; do
      s=$(basename "$d")
      files=$(find "$d" -maxdepth 1 -type f -printf '%f|%TY-%Tm-%Td %TH:%TM:%TS\n' 2>/dev/null | sort)
      if [ -z "$files" ]; then
        echo "$s|EMPTY|NO-REPORT"
      else
        echo "$s|FILES"
        echo "$files" | sed 's/^/    /'
        for f in "$d"*.md; do
          [ -e "$f" ] || continue
          echo "    FIRSTLINE $f: $(head -c 400 "$f" | head -n 3 | tr '\n' ' ')"
        done
      fi
    done
  } >> "$OUT" 2>&1
  sleep 30
done
echo "POLL DONE $(date -u +%H:%M:%SZ)" >> "$OUT"
