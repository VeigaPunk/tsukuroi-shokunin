#!/usr/bin/env bash
# Run the pristine probe and every mutant against base / H1 / H2 revisions.
set -u
SEAT=/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2
LANE="$SEAT/repo"
BASE=8cff9e7cfb034b49c645d548801ac3185a827cb4
H1=$(cat "$SEAT/h1.rev")
H2=$(cat "$SEAT/h2.rev")
mkdir -p "$SEAT/runs" "$SEAT/scratch"

run_one() {  # name probe rev label
  local name="$1" probe="$2" rev="$3" label="$4"
  local out="$SEAT/runs/${name}.${label}.jsonl"
  local err="$SEAT/runs/${name}.${label}.err"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 python3 "$probe" \
      --revision "$rev" --lane "$LANE" --scratch "$SEAT/scratch" \
      --only check-kernel-taint.py > "$out" 2> "$err"
  local rc=$?
  printf '%s\t%s\t%s\n' "$name" "$label" "$rc" >> "$SEAT/runs/index.tsv"
}

: > "$SEAT/runs/index.tsv"
JOBS=()
for spec in "pristine:$LANE/tools/probe-git-child-env-r31.py" \
            "M01-drop-parity-check:$SEAT/mutants/M01-drop-parity-check.py" \
            "M02-drop-stdout-comparison:$SEAT/mutants/M02-drop-stdout-comparison.py" \
            "M03-drop-git-exec-count:$SEAT/mutants/M03-drop-git-exec-count.py" \
            "M04-skip-first-exec-exclusion:$SEAT/mutants/M04-skip-first-exec-exclusion.py" \
            "M05-injection-by-variable-name:$SEAT/mutants/M05-injection-by-variable-name.py" \
            "M06-no-LD_LIBRARY_PATH-in-injection:$SEAT/mutants/M06-no-LD_LIBRARY_PATH-in-injection.py" \
            "M07-no-PYTHONPATH-in-injection:$SEAT/mutants/M07-no-PYTHONPATH-in-injection.py" \
            "M08-drop-control-B-determinism-check:$SEAT/mutants/M08-drop-control-B-determinism-check.py" \
            "M09-no-require-git-child:$SEAT/mutants/M09-no-require-git-child.py" \
            "M10-supplementary-drop-stdout-and-exec-count:$SEAT/mutants/M10-supplementary-drop-stdout-and-exec-count.py"; do
  name="${spec%%:*}"; probe="${spec#*:}"
  for lab in base H1 H2; do
    case "$lab" in
      base) rev="$BASE" ;;
      H1) rev="$H1" ;;
      H2) rev="$H2" ;;
    esac
    JOBS+=("$name|$probe|$rev|$lab")
  done
done

printf '%s\n' "${JOBS[@]}" | xargs -P 6 -I{} bash -c '
  IFS="|" read -r name probe rev lab <<< "{}"
  SEAT=/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2
  out="$SEAT/runs/${name}.${lab}.jsonl"; err="$SEAT/runs/${name}.${lab}.err"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 python3 "$probe" \
      --revision "$rev" --lane "$SEAT/repo" --scratch "$SEAT/scratch" \
      --only check-kernel-taint.py > "$out" 2> "$err"
  rc=$?
  printf "%s\t%s\t%s\n" "$name" "$lab" "$rc" >> "$SEAT/runs/index.tsv"
'
echo "DONE"
sort "$SEAT/runs/index.tsv"
