#!/bin/sh
S=/fast/scratch/hyaku/tsukuroi-r98/MutRegistry
C=$S/clone
R=$S/receipts
export TMPDIR=$S/work
BASE=b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a
D1=$(awk '/^D1 /{print $2}' "$R/doctored-revisions.txt")
D2=$(awk '/^D2 /{print $2}' "$R/doctored-revisions.txt")
D2L=$(awk '/^D2lie /{print $2}' "$R/doctored-revisions.txt")
: > "$R/checker-summary.txt"
for m in M01 M02 M04 M06 M07 M08 M09 M10; do
  python3 "$C/fixture/$m.py" --selftest > "$R/$m-selftest.txt" 2>&1
  src=$?
  printf '%-4s selftest=%s\n' "$m" "$(tail -1 "$R/$m-selftest.txt")" >> "$R/checker-summary.txt"
  for tag in base D1 D2 D2lie; do
    case $tag in
      base) r=$BASE;; D1) r=$D1;; D2) r=$D2;; D2lie) r=$D2L;;
    esac
    python3 "$C/fixture/$m.py" --revision "$r" --json "$R/$m-$tag.json" > "$R/$m-$tag.txt" 2>&1
    rc=$?
    printf '%-4s %-5s rc=%s %s\n' "$m" "$tag" "$rc" "$(tail -1 "$R/$m-$tag.txt")" >> "$R/checker-summary.txt"
  done
done
