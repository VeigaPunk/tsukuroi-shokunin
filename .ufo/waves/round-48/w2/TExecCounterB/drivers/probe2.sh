#!/bin/bash
# TExecCounterB: instrumented reproduction of the flaky evidence check.
# probe-census.sh = census-frozen.sh (sha 375aa737...) plus a MISS tracer in check()'s must-match
# branch that records PIPESTATUS and dumps $out. Sequential runs, one at a time.
S=/fast/scratch/hyaku/tsukuroi-r48/TExecCounterB
C="$S/probe2-census.sh"
D="$S/probe2"
rm -rf "$D"; mkdir -p "$D/w1" "$D/w1/tmp with space"
cat > "$D/mktemp" <<'WRAP'
#!/bin/bash
out=$(/usr/bin/mktemp "$@") || exit $?
case "$*" in
  *tsukuroi-r3-2-selftest*) printf '%s\t%s\t%s\n' "$*" "$out" "$(readlink -f -- "$out")" >>"$MKTEMP_LOG" ;;
esac
printf '%s\n' "$out"
WRAP
chmod 755 "$D/mktemp"; mkdir -p "$D/wrap"; mv "$D/mktemp" "$D/wrap/mktemp"

: > "$D/trace.log"
run_case() { # name tmpdir(optional)
  local name=$1 tdir=$2 log="$D/$name.mktemp.log"
  local -a envs=(PATH="$D/wrap:/usr/bin:/bin" LC_ALL=C MKTEMP_LOG="$log" TRACE="$D/trace.log")
  [ -n "$tdir" ] && envs+=(TMPDIR="$tdir")
  ( cd "$D/w1" && env -i "${envs[@]}" nice -n 10 bash "$C" --selftest ) > "$D/$name.out" 2> "$D/$name.err"
  local rc=$?
  printf '%s rc=%s load=%s last=%s\n' "$name" "$rc" "$(cat /proc/loadavg | cut -d' ' -f1)" \
    "$(grep -v '^$' "$D/$name.out" | tail -1)" >> "$D/summary.log"
  grep '^FAIL ' "$D/$name.err" | cut -c1-160 >> "$D/summary.log" 2>/dev/null
}

run_case spaced "$D/w1/tmp with space"
printf '== between load=%s ==\n' "$(cat /proc/loadavg | cut -d' ' -f1)" >> "$D/summary.log"
run_case unset ""
printf '== end load=%s ==\n' "$(cat /proc/loadavg | cut -d' ' -f1)" >> "$D/summary.log"
touch "$D/DONE"
