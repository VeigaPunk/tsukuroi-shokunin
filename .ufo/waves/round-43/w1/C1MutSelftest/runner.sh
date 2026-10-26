#!/bin/bash
# Equivalence battery: run one variant of inputs_newer_than (extracted from a
# pristine/mutant script copy) over 8 fixture shapes; print one result per line.
# usage: runner.sh <variant-fn-file> <fixture-dir>
set -uo pipefail
var=$1
fx=$2
# shellcheck disable=SC1090
source "$var"

mkdir -p "$fx/d/sub"
: >"$fx/old"
: >"$fx/d/sub/f"
touch -d @1000 -- "$fx/old" "$fx/d/sub/f" "$fx/d/sub" "$fx/d"

# 1 missing start point, nothing newer
printf 'missing-none=%s\n' "$(inputs_newer_than 2000 "$fx/missing" "$fx/old" "$fx/d")"
# 2 missing start point, deep file newer
touch -d @3000 -- "$fx/d/sub/f"
printf 'missing-deep=%s\n' "$(inputs_newer_than 2000 "$fx/missing" "$fx/old" "$fx/d")"
# 3 missing start point, start-point dir itself newer
touch -d @3000 -- "$fx/d"
printf 'missing-top=%s\n' "$(inputs_newer_than 2000 "$fx/missing" "$fx/old" "$fx/d")"
# 4 all present, nothing newer
touch -d @1000 -- "$fx/d/sub/f" "$fx/d"
printf 'present-none=%s\n' "$(inputs_newer_than 2000 "$fx/old" "$fx/d")"
# 5 all present, deep file newer
touch -d @3000 -- "$fx/d/sub/f"
printf 'present-deep=%s\n' "$(inputs_newer_than 2000 "$fx/old" "$fx/d")"
# 6 unreadable start-point dir (mode 000, dir itself old), deep file newer elsewhere
mkdir -p "$fx/nord"
: >"$fx/nord/x"
touch -d @1000 -- "$fx/nord" "$fx/nord/x"
chmod 000 "$fx/nord"
touch -d @3000 -- "$fx/d/sub/f"
printf 'nord-deep=%s\n' "$(inputs_newer_than 2000 "$fx/nord" "$fx/d")"
# 7 unreadable start-point dir, nothing newer anywhere
touch -d @1000 -- "$fx/d/sub/f" "$fx/d"
printf 'nord-none=%s\n' "$(inputs_newer_than 2000 "$fx/nord" "$fx/d")"
# 8 match in FIRST start point, missing point later (find -quit fires before any error)
touch -d @3000 -- "$fx/d/sub/f"
printf 'match-first-then-missing=%s\n' "$(inputs_newer_than 2000 "$fx/d" "$fx/missing")"
chmod 755 "$fx/nord"
