# usage: drv.sh <tmpdir-literal-file-or-path>; run in isolation
. /fast/scratch/hyaku/tsukuroi-r48/TRevPortable/fn.sh
selftest_base_dir; rc=$?
echo "rc=$rc BASE_DIR=[$ST_BASE_DIR] FD=[$ST_BASE_FD]"
if [ $rc -eq 0 ]; then
  echo "readlink: $(readlink -f -- "$ST_BASE_DIR")"
  w=$(mktemp -d "$ST_BASE_DIR/x.XXXXXX") && echo "mktemp ok: $w -> $(readlink -f "$w")" && rm -rf "$w"
  sh -c 'ls -d /proc/self/fd/'"$ST_BASE_FD"'/ >/dev/null && echo child-inherits-fd'
fi
