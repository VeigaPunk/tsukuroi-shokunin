#!/bin/sh
S=/fast/scratch/hyaku/tsukuroi-r98/MutRegistry
R=$S/receipts
B=$1; W=$2; TAG=$3
export TMPDIR=$S/work
python3 "$B" --gate "$S/lie/$W.py" --runs 1 --work "$S/work/lie-$TAG" --json "$R/lie-$TAG.json" > "$R/lie-$TAG.txt" 2>&1
echo "$TAG rc=$? $(tail -1 "$R/lie-$TAG.txt")" >> "$R/lie.progress"
