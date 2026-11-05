#!/bin/sh
# validate-block.sh CANDIDATE — pre-append gate for a candidate corpus/SOURCES.md.
# CANDIDATE must sit at <tree>/corpus/SOURCES.md: census validate resolves used-by
# paths against <tree>. Pass = census exit 0 (warnings allowed) AND no duplicate ids.
# Prints the census output, then "census-exit=<rc>", then one line per duplicated
# id (nothing for a clean registry). Read-only. Exit: 0 pass · 1 fail · 2 usage.
set -u
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
CAND=${1:-}
if [ -z "$CAND" ] || [ ! -f "$CAND" ]; then
  echo "usage: validate-block.sh <candidate corpus/SOURCES.md>" >&2
  exit 2
fi
CAND=$(realpath -- "$CAND")
"$CENSUS" validate --file "$CAND"
rc=$?
echo "census-exit=$rc"
dups=$(grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$CAND" | grep -oE 'S[0-9]+' | sort | uniq -d)
[ -z "$dups" ] || printf '%s\n' "$dups"
if [ "$rc" = 0 ] && [ -z "$dups" ]; then exit 0; fi
exit 1
