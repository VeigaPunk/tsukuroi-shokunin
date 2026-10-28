#!/usr/bin/env bash
set -euo pipefail
. /fast/scratch/hyaku/tsukuroi-r48/TExecLint/fn_body.sh
root_locator_class() { case "$1" in *[!A-Za-z0-9._/+-]*) printf unsafe ;; /*) printf absolute ;; *) printf relative ;; esac; }
T=/fast/scratch/hyaku/tsukuroi-r48/TExecLint
mkdir -p "$T/dirty tmpdir"
echo "-- dirty spaced TMPDIR --"
TMPDIR="$T/dirty tmpdir" selftest_base_dir; echo "rc=$? BASE=$ST_BASE_DIR FD=$ST_BASE_FD"
echo "fdopen=$( [ -e "$ST_BASE_DIR" ] && echo yes || echo no ) real=$(readlink -f -- "$ST_BASE_DIR") want=$(readlink -f -- "$T/dirty tmpdir")"
echo "child-sees-alias=$(bash -c 'readlink -f -- /proc/self/fd/'"$ST_BASE_FD"'' || echo NO)"
W=$(mktemp -d "$ST_BASE_DIR/tsukuroi-r3-2-selftest.XXXXXX"); echo "work=$W realwork=$(readlink -f -- "$W")"
mkdir -p "$W/fx"; echo child-fixture-write-ok > "$W/fx/probe"; cat "$W/fx/probe"
echo "class_of_work=$(root_locator_class "$W")"
exec {ST_BASE_FD}<&-
echo "after close: fdpath=$( [ -e "/proc/self/fd/\$ST_BASE_FD" ] && echo present || echo gone )"
rm -rf -- "$W"
echo "-- dirty nonexistent TMPDIR --"
if TMPDIR="$T/no such dir" selftest_base_dir; then echo "rc=0 BASE=$ST_BASE_DIR (resolver ACCEPTED)"; else echo "rc=1 resolver refused"; fi
echo "-- plain nonexistent TMPDIR --"
if TMPDIR="$T/no-such-dir-plain" selftest_base_dir; then echo "rc=0 BASE=$ST_BASE_DIR (resolver ACCEPTED)"; else echo "rc=1 resolver refused"; fi
echo "-- plain nonexistent TMPDIR, mktemp step --"
set +e
out=$(mktemp -d "$ST_BASE_DIR/tsk.XXXXXX" 2>&1); rc=$?
set -e
echo "mktemp rc=$rc out=$out"
