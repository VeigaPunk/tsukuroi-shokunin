#!/usr/bin/env bash
# Round-72 C2 red-before recipe (committed so the proof is reproducible; R72-D1).
# Copies the committed checker, disables the cases-figure mismatch arm, and runs --selftest.
# The mutant must FAIL, naming SELFTEST-MISMATCH (and SELFTEST-MIXED).
set -eu
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
S="${TMPDIR:-/fast/scratch/hyaku}/r72-redbefore-$$"
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT
cp "$LANE/tools/check-selftest-tally.py" "$S/mutant.py"
python3 - "$S/mutant.py" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
old = "                mism += 0 if ok else 1"
assert old in s, "mismatch arm not found"
open(p, "w").write(s.replace(old, "                mism += 0", 1))
PY
echo "# mutant: first 'mism += 0 if ok else 1' -> 'mism += 0' in sweep()"
echo "# command: TMPDIR=${TMPDIR:-/fast/scratch/hyaku} python3 $S/mutant.py --selftest"
TMPDIR="${TMPDIR:-/fast/scratch/hyaku}" python3 "$S/mutant.py" --selftest
echo "rc=$?"
