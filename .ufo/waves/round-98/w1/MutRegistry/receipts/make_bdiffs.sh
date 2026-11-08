#!/bin/sh
S=/fast/scratch/hyaku/tsukuroi-r98/MutRegistry
R=$S/receipts
for m in B01 B02 B03 B04 B05; do
  /usr/bin/diff -u "$S/pristine/limine-pin-battery-r98.py" "$S/mutants-battery/$m.py" > "$R/$m.diff"
  h=$(/usr/bin/grep -c '^@@' "$R/$m.diff")
  c=$(/usr/bin/grep -cE '^[+-][^+-]' "$R/$m.diff")
  echo "$m hunks=$h changed=$c"
done
