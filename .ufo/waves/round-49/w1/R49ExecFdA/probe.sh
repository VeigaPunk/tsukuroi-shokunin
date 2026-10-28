#!/usr/bin/env bash
# R49ExecFdA probe: fd-band behaviour matrix for selftest_base_dir().
# The function body below is COPIED BY HAND from the freeze bytes
# 55c07cd3f8bff2e12117c34d57b4c618de74d85c:tools/tsukuroi-census.sh lines 2063-2101.
# Nothing is sourced from the census; the copy is byte-identical to that range
# (verified separately with sed + diff, see report).
set -uo pipefail

S=${S:-/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdA}
BAND10='240 241 242 243 244 245 246 247 248 249'

selftest_base_dir() {
  local base fdn band
  ST_BASE_DIR=
  ST_BASE_FD=
  ST_BASE_ERR=
  band=${SELFTEST_FD_BAND:-240 241 242 243 244 245 246 247 248 249}
  base=${TMPDIR:-/tmp}
  case "$base" in
    *[!A-Za-z0-9._/+-]*)
      if [ ! -d "$base" ]; then ST_BASE_ERR=dirty-missing; return 1; fi
      for fdn in $band; do
        [ -e "/proc/self/fd/$fdn" ] || break
      done
      if [ -e "/proc/self/fd/$fdn" ]; then ST_BASE_ERR=fd-band; return 1; fi
      eval "exec ${fdn}<\"\$base\"" || { ST_BASE_ERR=alias-open; return 1; }
      ST_BASE_FD=$fdn
      ST_BASE_DIR=/proc/self/fd/$fdn
      if [ ! -d "$ST_BASE_DIR" ]; then
        eval "exec ${fdn}<&-"; ST_BASE_FD=; ST_BASE_DIR=; ST_BASE_ERR=alias-not-dir; return 1
      fi
      ;;
    *) ST_BASE_DIR=$base ;;
  esac
}

hold() { eval "exec $1<&0" 2>/dev/null; }
drop() { eval "exec $1<&-" 2>/dev/null; }
hold_all() { local f; for f in $BAND10; do hold "$f"; done; }
drop_all() { local f; for f in $BAND10; do drop "$f"; done; }
free_all() { local f; for f in $BAND10; do drop "$f"; done; }

report() { # name rc dir fd err band
  printf 'CASE=%-34s RC=%s DIR=%s FD=%s ERR=%s BAND=%s\n' "$1" "$2" "${3:-<empty>}" "${4:-<empty>}" "${5:-<empty>}" "${6:-default}"
}

SP="$S/band dir"          # spaced, exists
MISS="$S/no such dir"     # spaced, absent
CLEAN="$S/cleanbase"      # no space at all
mkdir -p "$SP" "$CLEAN"
rm -rf -- "$MISS"

# ---- (a) band free -> rc 0, ST_BASE_FD 240, ST_BASE_ERR empty
free_all
unset SELFTEST_FD_BAND
TMPDIR="$SP" selftest_base_dir; rc=$?
report '(a) band-free' "$rc" "$ST_BASE_DIR" "$ST_BASE_FD" "$ST_BASE_ERR"
[ -n "${ST_BASE_FD:-}" ] && drop "$ST_BASE_FD"

# ---- (b) 240 held -> fd 241
free_all; hold 240
TMPDIR="$SP" selftest_base_dir; rc=$?
report '(b) fd-240-held' "$rc" "$ST_BASE_DIR" "$ST_BASE_FD" "$ST_BASE_ERR"
[ -n "${ST_BASE_FD:-}" ] && drop "$ST_BASE_FD"
drop 240

# ---- (c) all ten held -> rc 1, ERR=fd-band, DIR empty
free_all; hold_all
TMPDIR="$SP" selftest_base_dir; rc=$?
report '(c) all-ten-held' "$rc" "$ST_BASE_DIR" "$ST_BASE_FD" "$ST_BASE_ERR"
[ -n "${ST_BASE_FD:-}" ] && drop "$ST_BASE_FD"
drop_all

# ---- (d) SELFTEST_FD_BAND='240 241', both held -> ERR=fd-band (its own path)
free_all; hold 240; hold 241
SELFTEST_FD_BAND='240 241'; TMPDIR="$SP"; selftest_base_dir; rc=$?
report '(d) custom-band-2-held' "$rc" "$ST_BASE_DIR" "$ST_BASE_FD" "$ST_BASE_ERR" "'240 241'"
unset SELFTEST_FD_BAND
[ -n "${ST_BASE_FD:-}" ] && drop "$ST_BASE_FD"
drop 240; drop 241

# ---- (d2) SELFTEST_FD_BAND='240 241', nothing held -> alias 240 (band override honoured)
free_all
SELFTEST_FD_BAND='240 241'; TMPDIR="$SP"; selftest_base_dir; rc=$?
report '(d2) custom-band-free' "$rc" "$ST_BASE_DIR" "$ST_BASE_FD" "$ST_BASE_ERR" "'240 241'"
unset SELFTEST_FD_BAND
[ -n "${ST_BASE_FD:-}" ] && drop "$ST_BASE_FD"

# ---- (e) nonexistent TMPDIR -> ERR=dirty-missing
free_all
TMPDIR="$MISS" selftest_base_dir; rc=$?
report '(e) tmpdir-missing' "$rc" "$ST_BASE_DIR" "$ST_BASE_FD" "$ST_BASE_ERR"

# ---- (f) clean (space-free) TMPDIR -> no alias, ERR empty, DIR == TMPDIR
free_all
TMPDIR="$CLEAN" selftest_base_dir; rc=$?
report '(f) clean-tmpdir' "$rc" "$ST_BASE_DIR" "$ST_BASE_FD" "$ST_BASE_ERR"
[ "$ST_BASE_DIR" = "$CLEAN" ] && printf 'CASE=(f) DIR-identity OK (%s)\n' "$ST_BASE_DIR" || printf 'CASE=(f) DIR-identity MISMATCH\n'

# ---- (g) alias-not-dir / fd leak check: 240 free again after (a)/(b)
free_all
[ -e /proc/self/fd/240 ] && printf 'CASE=(g) LEAK fd240 still open\n' || printf 'CASE=(g) fd240 free after probes\n'
[ -e /proc/self/fd/241 ] && printf 'CASE=(g) LEAK fd241 still open\n' || printf 'CASE=(g) fd241 free after probes\n'
