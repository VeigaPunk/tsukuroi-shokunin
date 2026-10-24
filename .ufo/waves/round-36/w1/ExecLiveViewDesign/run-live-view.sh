#!/usr/bin/bash
set -euo pipefail

SEAT=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-36/w1/ExecLiveViewDesign
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
WRAP="$SEAT/wrappers"
REV=${1:?usage: run-live-view.sh REVISION [RUN_ID]}
RUN_ID=${2:-"run-$(/usr/bin/od -An -N4 -tx1 /dev/urandom | tr -d ' \n')"}
case "$RUN_ID" in (*[!A-Za-z0-9._-]*|'') printf 'invalid RUN_ID\n' >&2; exit 2;; esac
RUN_DIR="$SEAT/capture/$RUN_ID"
if [[ -e "$RUN_DIR" ]]; then printf 'capture already exists: %s\n' "$RUN_DIR" >&2; exit 2; fi
mkdir -p "$RUN_DIR/wrappers"
mkdir -p "$SEAT/capture/wrappers/standalone"
scratch=$(/usr/bin/mktemp -d /tmp/tsukuroi-r36-liveview.XXXXXXXX)
trap '/usr/bin/rm -rf -- "$scratch"' EXIT
mkdir -p "$scratch/fast-hyaku"
for t in binding receipts handoff mutants runner; do
  mkdir -p "$scratch/home/$t" "$scratch/tmp/$t"
done

random_hex() {
  local raw
  raw=$(/usr/bin/od -An -N4 -tx1 /dev/urandom)
  raw=${raw//[[:space:]]/}
  printf '%s' "$raw"
}
declare -A used=()
declare -a names=() canary_env=()
for n in {1..10}; do
  token=$(random_hex)
  while [[ -n ${used[$token]+x} ]]; do token=$(random_hex); done
  used[$token]=1
  name="TSQ_$token"
  value="r36_${RUN_ID}_${n}_${token}"
  names+=("$name")
  canary_env+=("$name=$value")
done
printf '%s\n' "${names[@]}" > "$RUN_DIR/canary-names.txt"
printf 'revision=%s\nlane=%s\nrun_id=%s\nscratch=%s\n' "$REV" "$LANE" "$RUN_ID" "$scratch" > "$RUN_DIR/context.txt"
{
  printf 'canary_names='
  printf '%s ' "${names[@]}"
  printf '\n'
  printf 'canary_prefixes_filtered_by_targets=GIT_,TSUKUROI_ (none of the generated names use either prefix)\n'
  printf 'trace_method=strace -f -v -s 8192 -e trace=execve plus PATH wrappers recording /proc/self/environ\n'
} >> "$RUN_DIR/context.txt"

run_env() {
  local tool=$1
  printf 'HOME=%s\n' "$scratch/home/$tool"
  printf 'TMPDIR=%s\n' "$scratch/tmp/$tool"
  printf 'PATH=%s:/usr/bin:/bin\n' "$WRAP"
  printf 'LIVEVIEW_LOG_DIR=%s\n' "$RUN_DIR/wrappers"
  printf 'LIVEVIEW_RUN_ID=%s\n' "$RUN_ID"
  printf 'LIVEVIEW_CANARY_NAMES=%s\n' "$(IFS=,; printf '%s' "${names[*]}")"
  printf 'LC_ALL=C\nLANG=C\nPYTHONDONTWRITEBYTECODE=1\n'
  printf 'GIT_CONFIG_NOSYSTEM=1\nGIT_CONFIG_GLOBAL=/dev/null\nGIT_CONFIG_SYSTEM=/dev/null\nGIT_OPTIONAL_LOCKS=0\nGIT_PAGER=cat\n'
}

run_tool() {
  local label=$1 tool=$2; shift 2
  local stdout="$RUN_DIR/$label.stdout" stderr="$RUN_DIR/$label.stderr" trace="$RUN_DIR/$label.execve.log"
  local -a envargs=() cmd=("$@")
  while IFS= read -r line; do envargs+=("$line"); done < <(run_env "$tool")
  {
    printf '%s\t' "$label"
    printf '%q ' "${cmd[@]}"
    printf '\n'
  } >> "$RUN_DIR/commands.tsv"
  set +e
  /usr/bin/env -i "${envargs[@]}" "${canary_env[@]}" \
    /usr/bin/strace -f -qq -v -s 8192 -e trace=execve -o "$trace" "${cmd[@]}" \
    > "$stdout" 2> "$stderr"
  local rc=$?
  set -e
  printf '%s\t%s\n' "$label" "$rc" >> "$RUN_DIR/exitcodes.tsv"
}

run_tool binding binding "$WRAP/python3" "$LANE/tools/check-revision-binding.py" \
  --tools-revision "$REV" --branch master
run_tool receipts receipts "$WRAP/python3" "$LANE/tools/check-report-receipts.py" \
  --report "$SEAT/view-input.md" --lane "$LANE" --revision "$REV"
run_tool handoff handoff "$WRAP/python3" "$LANE/tools/score-census-handoff-r32.py" \
  --revision "$REV" --lane "$LANE" --scratch "$scratch/handoff" --scenarios 24 --timeout 120 --budget 840
run_tool mutants mutants "$WRAP/python3" "$LANE/tools/mutants-btrfs-space-r30.py" \
  --counter "$LANE/tools/check-btrfs-space-r30.py"

# run-receipt hard-codes /fast/scratch/hyaku when that directory exists. A private
# mount namespace binds that path to this mktemp tree, then drops back to our uid.
# Thus its clone/home and receipt output stay inside permitted scratch/seat locations.
label=runner
tool=runner
stdout="$RUN_DIR/$label.stdout" stderr="$RUN_DIR/$label.stderr" trace="$RUN_DIR/$label.execve.log"
declare -a envargs=() cmd=()
while IFS= read -r line; do envargs+=("$line"); done < <(run_env "$tool")
cmd=("$WRAP/python3" "$LANE/tools/run-receipt.py" \
  --revision "$REV" --tool-revision "$REV" --lane "$LANE" \
  --out "$RUN_DIR/run-receipt.receipt.jsonl" --timeout 600 -- \
  tools/check-report-receipts.py --report "$SEAT/view-input.md" \
  --lane '{lane}' --revision '{rev}')
{
  printf '%s\t' "$label"
  printf '%q ' "${cmd[@]}"
  printf '\n'
} >> "$RUN_DIR/commands.tsv"
set +e
/usr/bin/sudo -n /usr/bin/unshare --mount --propagation private \
  /usr/bin/bash "$SEAT/run-fast-scratch.sh" "$scratch/fast-hyaku" \
  "$(/usr/bin/id -u)" "$(/usr/bin/id -g)" \
  /usr/bin/env -i "${envargs[@]}" "${canary_env[@]}" \
  /usr/bin/strace -f -qq -v -s 8192 -e trace=execve -o "$trace" "${cmd[@]}" \
  > "$stdout" 2> "$stderr"
rc=$?
set -e
printf '%s\t%s\n' "$label" "$rc" >> "$RUN_DIR/exitcodes.tsv"

/usr/bin/python3 "$SEAT/summarize-live-view.py" "$RUN_DIR" "$REV" "$LANE"
printf 'capture=%s\n' "$RUN_DIR"
