#!/usr/bin/env bash
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r42/C1MutSites
IMPL=447662088dfd3155e31aed239179a79c1d1046c7
name="$1"
D="$S/fx.$name"
if [ -e "$D" ]; then echo "exists: $D"; exit 1; fi
git clone -q --shared "$L" "$D"
git -C "$D" remote remove origin
top="$(git -C "$D" rev-parse --show-toplevel)"
if [ "$top" != "$D" ]; then echo "toplevel mismatch: $top"; exit 1; fi
git -C "$D" checkout -q "$IMPL"
echo "clone=$D head=$(git -C "$D" rev-parse HEAD)"
sha256sum "$D/tools/tsukuroi-census.sh"
