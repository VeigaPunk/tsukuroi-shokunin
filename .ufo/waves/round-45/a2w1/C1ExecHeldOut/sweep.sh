#!/usr/bin/env bash
# single trailing byte sweep: sed-strip route (base) vs parameter-expansion route (impl)
set -u
diffs=0
for i in $(seq 1 255); do
  hx=$(printf '%02x' "$i")
  ch=$(printf '%b' "\\x$hx")
  v="degraded$ch"
  b=$(printf '%s\n' "$v" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//' || echo "RC=$?")
  w=${v%%$'\n'*}; w=${w//$'\r'/}; w=${w%"${w##*[![:space:]]}"}
  if [ "$b" != "$w" ]; then
    diffs=$((diffs+1))
    printf 'DIFF byte=0x%s sed=%s bash=%s\n' "$hx" "$(printf '%s' "$b" | od -An -tx1 | tr -d '\n')" "$(printf '%s' "$w" | od -An -tx1 | tr -d '\n')"
  fi
done
echo "sweep trailing-byte: diffs=$diffs/255"
