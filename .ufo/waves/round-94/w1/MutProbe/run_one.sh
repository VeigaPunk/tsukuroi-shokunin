#!/bin/sh
# r94 w1 MutProbe: one detector sweep (battery --runs 1, gate --selftest, battery --usage-check)
set -u
gate=$1
out=$2
B=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r94.py
mkdir -p "$out/tmp/work" "$out/tmp/work2"
export TMPDIR="$out/tmp"
python3 "$B" --gate "$gate" --runs 1 --work "$out/tmp/work" --json "$out/battery.json" \
    > "$out/battery.out" 2> "$out/battery.err"
echo $? > "$out/battery.rc"
python3 "$gate" --selftest > "$out/selftest.out" 2> "$out/selftest.err"
echo $? > "$out/selftest.rc"
python3 "$B" --gate "$gate" --usage-check --work "$out/tmp/work2" \
    > "$out/usage.out" 2> "$out/usage.err"
echo $? > "$out/usage.rc"
