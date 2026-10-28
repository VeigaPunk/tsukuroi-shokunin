#!/bin/bash
# TExecCounterB diagnosis: reconstruct the counter's per-scenario child env (env_for) and run the
# census selftest itself, keeping stdout+stderr so the FAIL labels survive. Sequential, one at a time.
S=/fast/scratch/hyaku/tsukuroi-r48/TExecCounterB
C="$S/census-frozen.sh"
D="$S/diag"
rm -rf "$D"; mkdir -p "$D/w1" "$D/w2" "$D/wrap"
cat > "$D/wrap/mktemp" <<'WRAP'
#!/bin/bash
out=$(/usr/bin/mktemp "$@") || exit $?
case "$*" in
  *tsukuroi-r3-2-selftest*) printf '%s\t%s\t%s\n' "$*" "$out" "$(readlink -f -- "$out")" >>"$MKTEMP_LOG" ;;
esac
printf '%s\n' "$out"
WRAP
chmod 755 "$D/wrap/mktemp"
mkdir -p "$D/w1/tmp with space"

{
  echo "== diag start $(date -Is) loadavg=$(cat /proc/loadavg) nproc=$(nproc) =="
} > "$D/diag.log"

run_case() { # name workdir tmpdir(optional)
  local name=$1 wd=$2 tdir=$3 log="$D/$1.mktemp.log"
  local -a envs=(PATH="$D/wrap:/usr/bin:/bin" LC_ALL=C MKTEMP_LOG="$log")
  [ -n "$tdir" ] && envs+=(TMPDIR="$tdir")
  ( cd "$wd" && env -i "${envs[@]}" nice -n 10 bash "$C" --selftest ) \
      > "$D/$name.out" 2> "$D/$name.err"
  local rc=$?
  printf '%s rc=%s last=%s\n' "$name" "$rc" "$(grep -v '^$' "$D/$name.out" | tail -1)" >> "$D/diag.log"
  grep -E '^FAIL ' "$D/$name.err" >> "$D/diag.log" 2>/dev/null || true
  printf '%s fixture=%s\n' "$name" "$(cat "$log" 2>/dev/null | cut -f3)" >> "$D/diag.log"
}

# D1: counter's `unset` child env (no TMPDIR), D2: `spaced` child env (TMPDIR with a space).
run_case unset "$D/w1" ""
printf '== between runs loadavg=%s ==\n' "$(cat /proc/loadavg)" >> "$D/diag.log"
run_case spaced "$D/w1" "$D/w1/tmp with space"
printf '== diag end %s loadavg=%s ==\n' "$(date -Is)" "$(cat /proc/loadavg)" >> "$D/diag.log"
touch "$D/DONE"
