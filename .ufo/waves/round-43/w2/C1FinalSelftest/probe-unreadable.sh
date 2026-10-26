#!/usr/bin/env bash
# Probe: does the selftest's missing-start-point arm also exercise the "unreadable directory
# listed before a newer input" arm named in the R43-C1 comment? Helper bodies copied verbatim.
set -uo pipefail

inputs_newer_than() { # fixed helper, verbatim from boot-chain-audit.sh@8acf0b02:463-475
    local epoch=$1 hit
    shift
    hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)
    if [ -n "$hit" ]; then
        printf '1\n'
    else
        printf '0\n'
    fi
}

inputs_newer_than_base() { # base pipeline, verbatim from boot-chain-audit.sh@6951ead:480-487
    local btime=$1
    shift
    if find "$@" -newermt "@$btime" -print -quit 2>/dev/null | grep -q .; then
        printf '1\n'
    else
        printf '0\n'
    fi
}

bi=${TMPDIR:-/tmp}/probe-bi.$$
mkdir -p -- "$bi/locked" "$bi/d"
: >"$bi/locked/hidden"
: >"$bi/d/newer"
touch -d @1000 -- "$bi/locked" "$bi/locked/hidden"
touch -d @3000 -- "$bi/d" "$bi/d/newer"
chmod 000 -- "$bi/locked"

printf 'raw find over (unreadable-dir, dir-with-newer):\n'
raw=$(find "$bi/locked" "$bi/d" -newermt @2000 -print -quit 2>/dev/null)
rc_raw=$?
printf '  stdout=[%s] find_exit=%s\n' "$raw" "$rc_raw"
printf 'fixed  helper -> [%s]\n' "$(inputs_newer_than 2000 "$bi/locked" "$bi/d")"
printf 'base   helper -> [%s]\n' "$(inputs_newer_than_base 2000 "$bi/locked" "$bi/d")"
printf 'fixed  helper, missing-start-point arm (selftest shape) -> [%s]\n' \
    "$(inputs_newer_than 2000 "$bi/absent" "$bi/d")"
chmod 700 -- "$bi/locked"
rm -rf -- "$bi"
