#!/usr/bin/env bash
# Re-run the two anomalous mutants several times each to separate a real mutant effect
# from a flaky probe reading.
set -u
SEAT=/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2
H1=$(cat "$SEAT/h1.rev"); H2=$(cat "$SEAT/h2.rev")
BASE=8cff9e7cfb034b49c645d548801ac3185a827cb4
mkdir -p "$SEAT/flake"
J=()
for i in 1 2 3 4; do
  J+=("M08|$SEAT/mutants/M08-drop-control-B-determinism-check.py|$H2|M08-H2-$i")
  J+=("M04|$SEAT/mutants/M04-skip-first-exec-exclusion.py|$H1|M04-H1-$i")
  J+=("M04|$SEAT/mutants/M04-skip-first-exec-exclusion.py|$H2|M04-H2-$i")
  J+=("PR|$SEAT/repo/tools/probe-git-child-env-r31.py|$H1|PR-H1-$i")
  J+=("PR|$SEAT/repo/tools/probe-git-child-env-r31.py|$H2|PR-H2-$i")
done
printf '%s\n' "${J[@]}" | xargs -P 8 -I{} bash -c '
  IFS="|" read -r tag probe rev label <<< "{}"
  SEAT=/fast/scratch/hyaku/tsukuroi-r31/MutProbeC2
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 python3 "$probe" \
      --revision "$rev" --lane "$SEAT/repo" --scratch "$SEAT/scratch" \
      --only check-kernel-taint.py > "$SEAT/flake/$label.jsonl" 2> "$SEAT/flake/$label.err"
  rc=$?
  dot=$(grep -o "\"channel\": \"dotgit-pointer\"[^}]*}" "$SEAT/flake/$label.jsonl" | head -1)
  printf "%s\texit=%s\t%s\n" "$label" "$rc" "$dot" >> "$SEAT/flake/index.tsv"
'
echo DONE
sort "$SEAT/flake/index.tsv"
