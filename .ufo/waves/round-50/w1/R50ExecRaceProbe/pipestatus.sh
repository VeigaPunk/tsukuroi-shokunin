#!/usr/bin/env bash
set -euo pipefail
big=$(printf '%*s' 100000 '' | tr ' ' x)
buf=$(printf '%s\n' "$big" 'midstream marker' "$big")
set +e
printf '%s\n' "$buf" | grep -qE 'midstream'
ps=("${PIPESTATUS[@]}")
set -e
printf 'buflen=%d PIPESTATUS[0]=%s PIPESTATUS[1]=%s\n' "${#buf}" "${ps[0]}" "${ps[1]}"
printf 'grep-alone-hits=%s\n' "$(printf '%s\n' "$buf" | grep -cE 'midstream')"
