#!/usr/bin/env bash
# Hand-copied prologue of run_selftest (census lines 2103-2122, comment lines dropped):
# the fd-band diagnostic path only; st_base/$work code below it is not copied.
set -uo pipefail
S=${S:-/fast/scratch/hyaku/tsukuroi-r49/R49ExecFdA}
selftest_base_dir() {
  local base fdn band
  ST_BASE_DIR=; ST_BASE_FD=; ST_BASE_ERR=
  band=${SELFTEST_FD_BAND:-240 241 242 243 244 245 246 247 248 249}
  base=${TMPDIR:-/tmp}
  case "$base" in
    *[!A-Za-z0-9._/+-]*)
      if [ ! -d "$base" ]; then ST_BASE_ERR=dirty-missing; return 1; fi
      for fdn in $band; do [ -e "/proc/self/fd/$fdn" ] || break; done
      if [ -e "/proc/self/fd/$fdn" ]; then ST_BASE_ERR=fd-band; return 1; fi
      eval "exec ${fdn}<\"\$base\"" || { ST_BASE_ERR=alias-open; return 1; }
      ST_BASE_FD=$fdn; ST_BASE_DIR=/proc/self/fd/$fdn
      if [ ! -d "$ST_BASE_DIR" ]; then
        eval "exec ${fdn}<&-"; ST_BASE_FD=; ST_BASE_DIR=; ST_BASE_ERR=alias-not-dir; return 1
      fi ;;
    *) ST_BASE_DIR=$base ;;
  esac
}
run_selftest_head() {
  local st_base
  selftest_base_dir || {
    case "${ST_BASE_ERR:-}" in
      fd-band)
        printf 'selftest: fd band %s exhausted (every descriptor already open), cannot alias TMPDIR <%s>; no /tmp fallback (R49-C3)\n' \
          "${SELFTEST_FD_BAND:-240 241 242 243 244 245 246 247 248 249}" "${TMPDIR:-<unset>}" >&2 ;;
      *)
        printf 'selftest: TMPDIR <%s> cannot host the fixture tree (%s; no /tmp fallback, R48-C2)\n' \
          "${TMPDIR:-<unset>}" "${ST_BASE_ERR:-resolver}" >&2 ;;
    esac
    return 1
  }
  st_base=$ST_BASE_DIR
  printf 'REACHED-WORK-PATH base=%s\n' "$st_base"
}
SP="$S/band dir"; mkdir -p "$SP"
hold() { eval "exec $1<&0" 2>/dev/null; }
drop() { eval "exec $1<&-" 2>/dev/null; }
echo '--- (h) fd-band: band 240/241 both held, SELFTEST_FD_BAND="240 241"'
hold 240; hold 241
SELFTEST_FD_BAND='240 241'; TMPDIR="$SP"
run_selftest_head; rc=$?
echo "RC=$rc"
drop 240; drop 241; unset SELFTEST_FD_BAND
echo '--- (i) fd-band: all ten held, default band'
for f in 240 241 242 243 244 245 246 247 248 249; do hold "$f"; done
TMPDIR="$SP"; run_selftest_head; rc=$?
echo "RC=$rc"
for f in 240 241 242 243 244 245 246 247 248 249; do drop "$f"; done
echo '--- (j) dirty-missing: nonexistent spaced TMPDIR (non-fd-band branch)'
TMPDIR="$S/no such dir"; run_selftest_head; rc=$?
echo "RC=$rc"
echo '--- (k) clean TMPDIR must reach the work path'
TMPDIR="$S/cleanbase"; mkdir -p "$TMPDIR"; run_selftest_head; rc=$?
echo "RC=$rc"
