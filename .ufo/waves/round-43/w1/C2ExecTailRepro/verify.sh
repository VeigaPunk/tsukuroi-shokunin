#!/bin/bash
# Prove every "COPY" chunk in harness.c is byte-identical to its scrub.c range,
# and list scrub.c top-level definitions that were NOT copied.
set -uo pipefail
S=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/frozen/src/scrub.c
H=/fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro
cd "$H"

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

echo "harness.c sha256: $(sha256sum harness.c | cut -d' ' -f1)"
echo
echo "chunk-by-chunk diff of harness.c COPY blocks against frozen scrub.c:"
tot=0
for r in "${ranges[@]}"; do
  set -- $r
  sed -n "$2,$3p" "$S" > "$H/.t_src"
  awk -v a="COPY BEGIN scrub.c:$2-$3" -v b="COPY END scrub.c:$2-$3" '
    index($0, a) {on=1; next} index($0, b) {on=0} on' harness.c > "$H/.t_hns"
  n=$(diff -u "$H/.t_src" "$H/.t_hns" | grep -cE '^[+-][^+-]' || true)
  lines=$(( $3 - $2 + 1 ))
  printf '  %-22s scrub.c:%-4s-%-4s %3d lines  differing lines: %s\n' "$1" "$2" "$3" "$lines" "$n"
  tot=$((tot+n))
done
rm -f "$H/.t_src" "$H/.t_hns"
echo "  TOTAL differing lines across all copied ranges: $tot"
echo
echo "scrub.c top-level definitions NOT copied (stubbed or unused):"
comm -13 \
  <(for r in "${ranges[@]}"; do set -- $r; sed -n "$2,$3p" "$S"; done | grep -oE '^[a-zA-Z_][a-zA-Z0-9_ \*]*\b[a-zA-Z_][a-zA-Z0-9_]*\(' | sed 's/.*[ *]//;s/($//;s/(//' | sort -u) \
  <(grep -oE '^[a-zA-Z_][a-zA-Z0-9_ \*]*\b[a-zA-Z_][a-zA-Z0-9_]*\(' "$S" | sed 's/.*[ *]//;s/($//;s/(//' | sort -u)
