#!/usr/bin/env bash
# Replays one labelled block of a capture script against four synthetic sudo lines.
# Uses the script's own run() body and its single "run <label> ..." line verbatim.
# journalctl is replaced by the stub; every other command is the real binary.
# usage: replay.sh <capture-script> <label> <outdir>
set -u
script=$1; label=$2; out=$3
here=$(cd "$(dirname "$0")" && pwd)
unset FLEET_ROOT
mkdir -p "$out"
: >"$out/capture.txt"
eval "$(sed -n '/^run() {/,/^}/p' "$script")"
line=$(grep -m1 -E "^run ${label} " "$script")
if [ -z "$line" ]; then echo "no run line for $label in $script" >&2; exit 3; fi
export PATH="$here/stub:$PATH"
export SYNTH_JOURNAL="$here/journal-4lines.txt"
eval "$line"
echo "run line exit-ready; capture lines:"
grep -E '^2026-10-21T10:00:0[1-4]' "$out/capture.txt" | cut -c1-200
got=$(grep -E '^2026-10-21T10:00:0[1-4]' "$out/capture.txt" | grep -o 'PWD=[a-z-]*' | sed 's/^PWD=//' | paste -sd' ')
want="inside-fleet-repo outside-fleet-repo inside-fleet-repo outside-fleet-repo"
echo "got:  $got"
echo "want: $want"
if [ "$got" = "$want" ]; then echo "RESULT: PASS"; else echo "RESULT: FAIL"; fi
