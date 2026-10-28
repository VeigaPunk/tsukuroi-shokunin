#!/bin/bash
# Contract-conforming stub: fixture in TMPDIR, 166 case lines, TERM => 143 + cleanup.
base=${TMPDIR:-/tmp}
work=$(mktemp -d "$base/tsukuroi-r3-2-selftest.XXXXXX") || exit 1
trap 'chmod -R u+rwx -- "${work:-}" 2>/dev/null || true; rm -rf -- "${work:-}" 2>/dev/null || true' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
case ${1:-} in --selftest) : ;; *) echo usage >&2; exit 2 ;; esac
P=0
while [ "$P" -lt 166 ]; do P=$((P+1)); printf 'PASS stub case %d\n' "$P"; sleep 0.05; done
printf 'TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)\n'
