#!/bin/bash
# Assemble harness.c = pre.h + verbatim sed ranges of frozen scrub.c + driver.c
set -euo pipefail
S=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c
H=/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro
cd "$H"

# ranges: name fromline toline   (verified against numbered source listing)
ranges=(
  "scrub_stats            72  79"
  "scrub_progress_structs 90 110"
  "free_history          402 410"
  "scrub_datafile        446 476"
  "scrub_open_file       478 495"
  "scrub_open_file_r     497 506"
  "scrub_open_file_w     508 518"
  "scrub_rename_file     520 536"
  "_SCRUB_KVREAD_macro   538 540"
  "scrub_kvread          547 567"
  "_SCRUB_INVALID_macro  569 576"
  "scrub_read_file       578 771"
  "scrub_write_buf       773 778"
  "scrub_writev          780 793"
  "_SCRUB_SUM_macros     795 798"
  "scrub_resumed_stats   800 828"
  "_SCRUB_KVWRITE_macros 830 836"
  "scrub_kvwrite         838 841"
  "scrub_write_file      843 895"
  "scrub_write_progress  897 947"
)

{
  cat pre.h
  for r in "${ranges[@]}"; do
    set -- $r
    printf '\n/* ==== COPY BEGIN scrub.c:%s-%s (%s) ==== */\n' "$2" "$3" "$1"
    sed -n "$2,$3p" "$S"
    printf '/* ==== COPY END scrub.c:%s-%s ==== */\n' "$2" "$3"
  done
  cat driver.c
} > harness.c

gcc -std=gnu11 -O0 -g -Wall -Wno-unused-variable -Wno-unused-but-set-variable \
    -Wno-sign-compare -Wno-format-truncation -o harness harness.c -luuid -lpthread 2> build.log
echo "build ok: $(wc -l < build.log) warning/error lines in build.log"
