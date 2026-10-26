#!/usr/bin/env bash
# C1MutCounter fixtures: one --shared --no-checkout clone per variant; the variant census is
# committed on master with the fixture identity via plumbing (no worktree writes needed).
set -eu
S=/fast/scratch/hyaku/tsukuroi-r41/C1MutCounter
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
FREEZE=e479fdc54d0977ccd8112a42d8d139baaebcb02e

mkfx() { # name censusfile
  local name=$1 cf=$2 D=$S/fx.$1 B T C
  rm -rf "$D"
  git clone -q --shared --no-checkout "$LANE" "$D"
  git -C "$D" remote remove origin
  local top; top=$(git -C "$D" rev-parse --show-toplevel)
  [ "$top" = "$D" ] || { echo "FATAL $name: toplevel '$top' != $D"; exit 1; }
  B=$(git -C "$D" hash-object -w -- "$cf")
  git -C "$D" read-tree "${FREEZE}^{tree}"
  git -C "$D" update-index --cacheinfo 100644,"$B",tools/tsukuroi-census.sh
  T=$(git -C "$D" write-tree)
  C=$(git -C "$D" -c user.name=fixture -c user.email=fixture@shokunin.local commit-tree "$T" -m "fixture $name")
  git -C "$D" update-ref refs/heads/master "$C"
  echo "$name rev=$C"
  git -C "$D" show "$C:tools/tsukuroi-census.sh" | sha256sum | sed "s/-/$name-census-in-repo/"
}

mkfx K1 "$S/census-K1.sh"
mkfx K2 "$S/census-K2.sh"
mkfx K3 "$S/census-K3.sh"
mkfx demo "$S/census-demo.sh"
