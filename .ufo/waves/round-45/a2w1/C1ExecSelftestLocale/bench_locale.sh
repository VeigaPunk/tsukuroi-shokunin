#!/usr/bin/env bash
# pure-bash cost of the five-site first-line + CR + trailing-blank conversions, per locale
s=$'degraded \t\r\n'; pad=$(awk 'BEGIN{for(i=0;i<2000;i++) printf "padding line %05d ..................................................\n", i}')
s="$s$pad"
n=2000
t0=$EPOCHREALTIME
for ((i=0;i<n;i++)); do x=${s%%$'\n'*}; x=${x//$'\r'/}; x=${x%"${x##*[![:space:]]}"}; done
t1=$EPOCHREALTIME
us=$(( ${t1/./} - ${t0/./} ))
printf '%-12s %d iters on %d bytes: %d us total, %d us/iter, result=[%s]\n' "$1" "$n" "${#s}" "$us" "$((us/n))" "$x"
