#!/bin/bash
S=/fast/scratch/hyaku/tsukuroi-r90/MutBattery; export TMPDIR="$S"
b="$1"; g="$2"
python3 "$S/battery.py" --gate "$g" --work "$S/work/w-$b" > "$S/base/$b.out" 2>&1
echo "rc=$?" >> "$S/base/$b.out"
