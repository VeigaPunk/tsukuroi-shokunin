#!/usr/bin/env bash
# ExecDoNothing driver: r95 do-nothing battery x3 runs on the landed gate and N01..N04,
# in three layouts (canonical lane, --shared clone worktree, git-archive tree at 38adc4ed).
set -u
SEAT=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-96/w1/ExecDoNothing
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
C=/fast/scratch/hyaku/tsukuroi-r96/ExecDoNothing/lane-clone
T=/fast/scratch/hyaku/tsukuroi-r96/ExecDoNothing/tree-38adc4ed
W=/fast/scratch/hyaku/tsukuroi-r96/ExecDoNothing/work
mkdir -p "$SEAT" "$W"

leg () { # $1 layout-tag, $2 battery, $3 gate, $4 json stem, $5 workdir
  local tag=$1 bat=$2 gate=$3 stem=$4 wd=$5
  mkdir -p "$wd"
  ( cd "$wd" && python3 "$bat" --gate "$gate" --runs 3 --work "$wd" --json "$SEAT/$stem.json" ) \
      >"$SEAT/$stem.log" 2>&1
  echo "$stem rc=$?" >>"$W/../legs-rc.txt"
}

rm -f "$W/../legs-rc.txt"
leg lane  "$L/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$L/tools/check-limine-pins.py" dn-gate "$W/gate-canonical" &
leg lane  "$L/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$L/.ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py" dn-N01-echo-wrong "$W/n01-canonical" &
leg lane  "$L/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$L/.ufo/waves/round-96/before/controls/bends/N02-y-cap-8.py" dn-N02-y-cap-8 "$W/n02-canonical" &
leg lane  "$L/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$L/.ufo/waves/round-96/before/controls/bends/N03-era-label-flip.py" dn-N03-era-label-flip "$W/n03-canonical" &
leg lane  "$L/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$L/.ufo/waves/round-96/before/controls/bends/N04-extra-components.py" dn-N04-extra-components "$W/n04-canonical" &
leg clone "$C/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$C/tools/check-limine-pins.py" dn-gate-clone "$W/gate-clone" &
leg clone "$C/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$C/.ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py" dn-N01-echo-wrong-clone "$W/n01-clone" &
leg clone "$C/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$C/.ufo/waves/round-96/before/controls/bends/N02-y-cap-8.py" dn-N02-y-cap-8-clone "$W/n02-clone" &
leg clone "$C/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$C/.ufo/waves/round-96/before/controls/bends/N03-era-label-flip.py" dn-N03-era-label-flip-clone "$W/n03-clone" &
leg clone "$C/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$C/.ufo/waves/round-96/before/controls/bends/N04-extra-components.py" dn-N04-extra-components-clone "$W/n04-clone" &
leg t38   "$T/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$T/tools/check-limine-pins.py" dn-gate-t38 "$W/gate-t38" &
leg t38   "$T/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$T/.ufo/waves/round-96/before/controls/bends/N01-echo-wrong.py" dn-N01-echo-wrong-t38 "$W/n01-t38" &
leg t38   "$T/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$T/.ufo/waves/round-96/before/controls/bends/N02-y-cap-8.py" dn-N02-y-cap-8-t38 "$W/n02-t38" &
leg t38   "$T/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$T/.ufo/waves/round-96/before/controls/bends/N03-era-label-flip.py" dn-N03-era-label-flip-t38 "$W/n03-t38" &
leg t38   "$T/.ufo/waves/round-96/before/controls/do-nothing-battery-r95.py" "$T/.ufo/waves/round-96/before/controls/bends/N04-extra-components.py" dn-N04-extra-components-t38 "$W/n04-t38" &
wait
cat "$W/../legs-rc.txt"
