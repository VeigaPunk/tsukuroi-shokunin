#!/bin/bash
S=/fast/scratch/hyaku/tsukuroi-r99/ExecDoNothing
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
C=$S/clone/tsukuroi-shokunin
SEAT=$L/.ufo/waves/round-99/w1/ExecDoNothing
BT=$L/.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py
BEND=$L/.ufo/waves/round-99/before/controls/bends
export TMPDIR=$S/tmp; mkdir -p $TMPDIR
run() { # name layout battery gate work
  local name=$1 layout=$2 bat=$3 gate=$4 work=$5
  mkdir -p "$work"
  python3 "$bat" --gate "$gate" --runs 3 --work "$work" --json "$SEAT/dn-$name-$layout.json" > "$SEAT/dn-$name-$layout.stdout" 2> "$SEAT/dn-$name-$layout.stderr"
  echo "EXIT $name $layout $?" > "$SEAT/dn-$name-$layout.exit"
}
run gate canonical "$BT" "$L/tools/check-limine-pins.py" "$S/work-gate" &
run n09 canonical "$BT" "$BEND/N09-y-era.py" "$S/work-n09" &
run n11 canonical "$BT" "$BEND/N11-x-era.py" "$S/work-n11" &
run gate clone "$C/tools/limine-pin-battery-r98.py" "$C/tools/check-limine-pins.py" "$S/work-clone-gate" &
run n09 clone "$C/tools/limine-pin-battery-r98.py" "$C/.ufo/waves/round-99/before/controls/bends/N09-y-era.py" "$S/work-clone-n09" &
run n11 clone "$C/tools/limine-pin-battery-r98.py" "$C/.ufo/waves/round-99/before/controls/bends/N11-x-era.py" "$S/work-clone-n11" &
wait
echo ALL_DONE
