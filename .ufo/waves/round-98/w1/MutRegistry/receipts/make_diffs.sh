#!/bin/sh
S=/fast/scratch/hyaku/tsukuroi-r98/MutRegistry
R=$S/receipts
for m in M01 M02 M04 M06 M07 M08 M09 M10; do
  /usr/bin/diff -u "$S/pristine/check-registry-content-r98.py" "$S/mutants/$m.py" > "$R/$m.diff"
  h=$(grep -c '^@@' "$R/$m.diff")
  c=$(grep -cE '^[+-][^+-]' "$R/$m.diff")
  echo "$m hunks=$h changed=$c"
done
