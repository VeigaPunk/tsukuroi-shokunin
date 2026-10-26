#!/usr/bin/env bash
# usage: race.sh BYTES RUNS -> counts pipefail pipeline statuses of `printf "$buf" | grep -q ^match`
set -uo pipefail
bytes=$1 runs=$2
buf=$(printf 'match first line\n'; head -c "$bytes" /dev/zero | tr '\0' 'x' | fold -w 79; echo)
bad=0
for ((i=0;i<runs;i++)); do
  if printf '%s\n' "$buf" | grep -q '^match'; then :; else bad=$((bad+1)); fi
done
echo "bytes=${#buf} runs=$runs pipeline_false=$bad"
