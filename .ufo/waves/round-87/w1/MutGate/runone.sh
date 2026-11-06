#!/bin/bash
# Run battery + gate selftest for one mutant. $1 = mutant name
set -u
S=/fast/scratch/hyaku/tsukuroi-r87/MutGate
BAT=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/limine-pin-battery-r87.py
name="$1"
g="$S/mutants/$name.py"
mkdir -p "$S/work/$name" "$S/res"
export TMPDIR="$S"
python3 "$BAT" --gate "$g" --work "$S/work/$name" --json "$S/res/$name.battery.json" --runs 1 > "$S/res/$name.battery.out" 2> "$S/res/$name.battery.err"
echo "battery_rc=$?" >> "$S/res/$name.battery.out"
python3 "$g" --selftest > "$S/res/$name.selftest.out" 2>&1
echo "selftest_rc=$?" >> "$S/res/$name.selftest.out"
