#!/usr/bin/env bash
# C1ExecLiveLarge: run base and impl censuses live, read-only, same --sample N.
# Usage: run-live.sh <N> <tag>
set -uo pipefail
N=$1
TAG=$2
S=$(cd "$(dirname "$0")" && pwd)
cd "$S" || exit 1
run() { # run <name> <script>
  local name=$1 script=$2 out=$S/$TAG.$1.out err=$S/$TAG.$1.err rc
  bash "$script" --sample "$N" >"$out" 2>"$err"
  rc=$?
  printf 'RUN %s sample=%s rc=%s stdout_bytes=%s stderr_bytes=%s\n' \
    "$name" "$N" "$rc" "$(wc -c <"$out")" "$(wc -c <"$err")"
  printf 'PLANE(packages)=%s\n' "$(grep -m1 '^PLANE packages: ' "$out" || printf '<absent>')"
  printf 'TSUKUROI_CENSUS=%s\n' "$(grep -m1 '^TSUKUROI_CENSUS: ' "$out" || printf '<absent>')"
}
run base "$S/base-census.sh"
run impl "$S/impl-census.sh"
