#!/usr/bin/env bash
# Drives the census --selftest across the six required environments, sequentially
# (never two census selftests at once), plus base/impl timing runs.
S=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv
R=$S/receipts
mkdir -p "$R" "$S/tmpdefault" "$S/tmp space"
ln -sfn "$S/impl" "$S/impl-link"
cd "$S" || exit 1

run() { # run NAME TIMEOUT_S CWD -- COMMAND...
  local name=$1 tmo=$2 cwd=$3; shift 3
  [ "$1" = -- ] && shift
  local t0 t1 rc
  t0=$(date +%s%N)
  ( cd "$cwd" && timeout "$tmo" "$@" ) > "$R/$name.out" 2>&1
  rc=$?
  t1=$(date +%s%N)
  printf '%s rc=%d elapsed_ms=%d\n' "$name" "$rc" "$(( (t1-t0)/1000000 ))" > "$R/$name.meta"
  echo "== $name rc=$rc elapsed_ms=$(( (t1-t0)/1000000 ))"
  grep -E '^TSUKUROI_CENSUS_SELFTEST:' "$R/$name.out" || echo "   (no summary line)"
  grep -E 'FAIL' "$R/$name.out" | sed 's/^/   FAIL| /'
  grep -cE 'warning: setlocale|cannot change' "$R/$name.out" | sed 's/^/   locale_warnings=/'
}

# 1 LC_ALL=C (rerun for a timed record; impl-lc_C.out from the first pass is kept too)
run impl-lc_C_timed 600 "$S" -- env LC_ALL=C TMPDIR="$S/tmpdefault" \
  bash "$S/impl/tsukuroi-census.sh" --selftest
# 2 LC_ALL=C.UTF-8
run impl-lc_C_UTF8 600 "$S" -- env LC_ALL=C.UTF-8 TMPDIR="$S/tmpdefault" \
  bash "$S/impl/tsukuroi-census.sh" --selftest
# 3 default locale (session env unmodified)
run impl-default-locale 600 "$S" -- env TMPDIR="$S/tmpdefault" \
  bash "$S/impl/tsukuroi-census.sh" --selftest
# 4 TMPDIR whose path contains a space
run impl-tmpdir-space 600 "$S" -- env "TMPDIR=$S/tmp space" \
  bash "$S/impl/tsukuroi-census.sh" --selftest
# 5 relative invocation from the census's own directory
run impl-relative-path 600 "$S/impl" -- env TMPDIR="$S/tmpdefault" ./tsukuroi-census.sh --selftest
# 6 absolute path through a symlinked directory
run impl-symlinked-dir 600 "$S" -- env TMPDIR="$S/tmpdefault" \
  bash "$S/impl-link/tsukuroi-census.sh" --selftest
# timing: base (2042117c) under the default locale
run base-timed 600 "$S" -- env TMPDIR="$S/tmpdefault" bash "$S/base/tsukuroi-census.sh" --selftest
# timing: impl (a4477049) under the default locale
run impl-timed 600 "$S" -- env TMPDIR="$S/tmpdefault" bash "$S/impl/tsukuroi-census.sh" --selftest
echo DONE
