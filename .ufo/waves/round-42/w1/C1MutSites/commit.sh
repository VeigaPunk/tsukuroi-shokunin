#!/usr/bin/env bash
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S=/fast/scratch/hyaku/tsukuroi-r42/C1MutSites
R="$L/.ufo/waves/round-42/w1/C1MutSites"
name="$1"; D="$S/fx.$name"
mkdir -p "$R"
git -C "$D" diff -- tools/tsukuroi-census.sh > "$R/$name.patch"
git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q -am "mut $name: single-site revert to base c8efaa3f text"
git -C "$D" rev-parse HEAD > "$S/fx.$name.sha"
echo "== $name sha=$(cat "$S/fx.$name.sha")"
cat "$R/$name.patch"
sha256sum "$D/tools/tsukuroi-census.sh"
