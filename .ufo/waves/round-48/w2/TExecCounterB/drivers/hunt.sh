#!/bin/bash
# TExecCounterB: hunt a reproducing MISS with instrumented probe (probe2-census.sh).
# Runs the counter's `spaced` child env at nice 10 repeatedly; stops at the first MISS.
S=/fast/scratch/hyaku/tsukuroi-r48/TExecCounterB
C="$S/probe2-census.sh"
D="$S/hunt"
rm -rf "$D"; mkdir -p "$D/w1/tmp with space" "$D/wrap"
cat > "$D/wrap/mktemp" <<'WRAP'
#!/bin/bash
out=$(/usr/bin/mktemp "$@") || exit $?
case "$*" in
  *tsukuroi-r3-2-selftest*) printf '%s\t%s\t%s\n' "$*" "$out" "$(readlink -f -- "$out")" >>"$MKTEMP_LOG" ;;
esac
printf '%s\n' "$out"
WRAP
chmod 755 "$D/wrap/mktemp"
: > "$D/trace.log"; : > "$D/attempts.log"

for n in 1 2 3 4 5 6; do
  rm -f "$D/trace.log.dumped"
  ( cd "$D/w1" && env -i PATH="$D/wrap:/usr/bin:/bin" LC_ALL=C MKTEMP_LOG="$D/a$n.mktemp.log" TRACE="$D/trace.log" \
      TMPDIR="$D/w1/tmp with space" nice -n 10 bash "$C" --selftest ) > "$D/a$n.out" 2> "$D/a$n.err"
  rc=$?
  printf 'attempt=%s rc=%s load=%s last=%s\n' "$n" "$rc" "$(cut -d' ' -f1 /proc/loadavg)" \
    "$(grep -v '^$' "$D/a$n.out" | tail -1)" >> "$D/attempts.log"
  grep '^FAIL ' "$D/a$n.err" | cut -c1-150 >> "$D/attempts.log" 2>/dev/null
  printf 'attempt=%s MISSes=%s\n' "$n" "$(grep -c '^MISS ' "$D/trace.log")" >> "$D/attempts.log"
  if [ -s "$D/trace.log.dumped" ] || grep -q '^MISS ' "$D/trace.log"; then
    echo "STOPPED-AT-MISS attempt=$n" >> "$D/attempts.log"
    break
  fi
done
touch "$D/DONE"
