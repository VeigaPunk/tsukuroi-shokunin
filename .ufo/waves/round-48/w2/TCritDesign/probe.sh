source ./fn.sh
t(){ ( cd "$S"; TMPDIR="$1" selftest_base_dir; rc=$?; printf 'TMPDIR=%q rc=%s base=%s fd=%s\n' "$1" $rc "$ST_BASE_DIR" "$ST_BASE_FD"; [ -n "$ST_BASE_DIR" ] && readlink -f "$ST_BASE_DIR" ); }
mkdir -p "$S/rel" "$S/sp ace" "$S/eq=x" "$S/nl
x" "$S/a:b" "$S/~t"
t "$S/rel"; t rel; t "rel/"; t "$S/sp ace"; t "$S/eq=x"; t "$S/nl
x"; t "$S/a:b"; t "sp ace"; t "$S/rel/"; t "$S/rel//"; t ""; t "/proc/self/fd/0" ; t "$S/sp ace/../rel"
