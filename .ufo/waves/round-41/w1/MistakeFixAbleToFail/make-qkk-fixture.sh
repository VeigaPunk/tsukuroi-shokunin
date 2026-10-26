#!/usr/bin/env bash
# Reproduces the M-2 fixture pair for tools/tsukuroi-census.sh:692.
#   bash make-qkk-fixture.sh <outdir>
# qkk-small.txt (163 B) carries the same 'error:' line as qkk-large.txt (272,053 B):
# only the LARGE one is able to fail the unfixed census.
set -euo pipefail
out=${1:?outdir}
mkdir -p "$out"
{ printf 'error: pkgA: /usr/bin/x (Permission denied)\n'
  for n in alpha beta gamma; do printf '%s: 100 total files, 0 altered files\n' "$n"; done; } > "$out/qkk-small.txt"
{ cat "$out/qkk-small.txt"
  python3 -c "
import sys
for i in range(7000): sys.stdout.write('pkgA: /usr/share/d%d (Size mismatch)\n'%i)"; } > "$out/qkk-large.txt"
wc -c "$out/qkk-small.txt" "$out/qkk-large.txt"
