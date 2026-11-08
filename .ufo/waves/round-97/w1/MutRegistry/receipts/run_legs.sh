#!/bin/sh
# Round-97 seat MutRegistry: three-leg battery for each one-clause mutant.
S=/fast/scratch/hyaku/tsukuroi-r97/MutRegistry
TIP=f48d16428d8bb92fd6cf546a745bff5b624e3f18
REV=05c7e0aee890d4eb4e01787bc342289afcb74171
for m in M01 M02 M03 M04 M05 M06 M07 M08; do
  mkdir -p "$S/tmp/$m"
  cp "$S/mutants/$m.py" "$S/surface/tools/$m.py"
  cp "$S/mutants/$m.py" "$S/doctored/fixture/$m.py"
  TMPDIR="$S/tmp/$m" python3 "$S/mutants/$m.py" --selftest > "$S/out/$m-selftest.txt" 2>&1
  echo "$m selftest rc=$?" >> "$S/out/$m-selftest.txt"
  TMPDIR="$S/tmp/$m" python3 "$S/surface/tools/$m.py" --revision "$TIP" \
      --json "$S/out/$m-tip.json" > "$S/out/$m-tip.txt" 2>&1
  echo "$m tip rc=$?" >> "$S/out/$m-tip.txt"
  TMPDIR="$S/tmp/$m" python3 "$S/doctored/fixture/$m.py" --revision "$REV" \
      --json "$S/out/$m-doctored.json" > "$S/out/$m-doctored.txt" 2>&1
  echo "$m doctored rc=$?" >> "$S/out/$m-doctored.txt"
done
echo done
