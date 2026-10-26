#!/bin/bash
# C1-9 determinism matrix driver (seat C1ExecEnvMatrix). Runs the frozen C1 counter at one
# revision under caller-cwd x caller-LC_ALL x --jobs. Scratch only; no lane writes.
set -u
S=/fast/scratch/hyaku/tsukuroi-r40/C1ExecEnvMatrix
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
COUNTER=$LANE/tools/score-selftest-literals-r40.py
REV=c707e356c2911646f7304d706eb77d118e510610
L=$S/logs

snap() { # $1 = label
  printf '%s tmp_entries=%s scratch_paths=%s leftover_workdirs=%s\n' \
    "$1" \
    "$(ls -la /tmp | wc -l)" \
    "$(find "$S" -path "$L" -prune -o -print | wc -l)" \
    "$(find "$S/s" -maxdepth 1 -name 'r40c1.*' 2>/dev/null | wc -l)"
}

cell() { # $1 name  $2 cwd  $3 LC_ALL  $4 jobs
  local name=$1 cwd=$2 lc=$3 jobs=$4 rc t0 t1
  t0=$(date +%s)
  ( cd "$cwd" && exec env -u TMPDIR LC_ALL="$lc" TZ=UTC \
      /usr/bin/python3 "$COUNTER" --revision "$REV" --scratch "$S/s" --jobs "$jobs" --timeout 900 ) \
      > "$L/$name.json" 2> "$L/$name.err"
  rc=$?
  t1=$(date +%s)
  printf 'CELL %s cwd=%s LC_ALL=%s jobs=%s exit=%s secs=%s %s\n' \
    "$name" "$cwd" "$lc" "$jobs" "$rc" "$((t1 - t0))" "$(snap after)"
}

: > "$L/matrix.log"
ls -1 /tmp | sort > "$L/tmp_before.txt"
find /tmp -maxdepth 2 -name 'r40c1.*' > "$L/tmp_r40_before.txt" 2>/dev/null
snap before | tee -a "$L/matrix.log"
printf 'counter_sha=%s caller_tmpdir=%s\n' \
  "$(sha256sum "$COUNTER" | cut -d' ' -f1)" "${TMPDIR-<unset>}" | tee -a "$L/matrix.log"

# caller cwd inside the scratch, for the relative-path exposure check
cell cwd_root_C_j1        /    C           1 2>&1 | tee -a "$L/matrix.log"
cell cwd_root_C_j6        /    C           6 2>&1 | tee -a "$L/matrix.log"
cell cwd_root_enUS_j1     /    en_US.UTF-8 1 2>&1 | tee -a "$L/matrix.log"
cell cwd_root_enUS_j6     /    en_US.UTF-8 6 2>&1 | tee -a "$L/matrix.log"
cell cwd_scratch_C_j1     $S   C           1 2>&1 | tee -a "$L/matrix.log"
cell cwd_scratch_C_j6     $S   C           6 2>&1 | tee -a "$L/matrix.log"
cell cwd_scratch_enUS_j1  $S   en_US.UTF-8 1 2>&1 | tee -a "$L/matrix.log"
cell cwd_scratch_enUS_j6  $S   en_US.UTF-8 6 2>&1 | tee -a "$L/matrix.log"
cell repeat_cwd_root_C_j6 /    C           6 2>&1 | tee -a "$L/matrix.log"

snap after | tee -a "$L/matrix.log"
ls -1 /tmp | sort > "$L/tmp_after.txt"
diff "$L/tmp_before.txt" "$L/tmp_after.txt" > "$L/tmp_diff.txt"; echo "tmp_diff_lines=$(wc -l < "$L/tmp_diff.txt")" | tee -a "$L/matrix.log"
find /tmp -maxdepth 2 -name 'r40c1.*' > "$L/tmp_r40_after.txt" 2>/dev/null
echo MATRIX-DONE | tee -a "$L/matrix.log"
