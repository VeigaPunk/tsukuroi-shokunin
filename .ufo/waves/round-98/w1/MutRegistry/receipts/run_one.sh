#!/bin/sh
S=/fast/scratch/hyaku/tsukuroi-r98/MutRegistry
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
R=$S/receipts
m=$1
B=$S/mutants-battery/$m.py
export TMPDIR=$S/work
printf "start %s %s\n" "$m" "$(date -Is)" > "$R/$m.progress"
python3 "$B" --gate "$L/tools/check-limine-pins.py" --runs 1 --work "$S/work/$m-landed" --json "$R/$m-landed.json" > "$R/$m-landed.txt" 2>&1
echo "landed rc=$? $(cat $R/$m-landed.txt)" >> "$R/$m.progress"
python3 "$B" --gate "$L/.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py" --runs 1 --work "$S/work/$m-N07" --json "$R/$m-N07.json" > "$R/$m-N07.txt" 2>&1
echo "N07 rc=$? $(cat $R/$m-N07.txt)" >> "$R/$m.progress"
python3 "$B" --gate "$L/.ufo/waves/round-98/before/controls/bends/N08-echo-norm.py" --runs 1 --work "$S/work/$m-N08" --json "$R/$m-N08.json" > "$R/$m-N08.txt" 2>&1
echo "N08 rc=$? $(cat $R/$m-N08.txt)" >> "$R/$m.progress"
python3 "$B" --selftest --reference "$L/tools/check-limine-pins.py" > "$R/$m-selftest.txt" 2>&1
echo "selftest rc=$?" >> "$R/$m.progress"
date -Is >> "$R/$m.progress"
