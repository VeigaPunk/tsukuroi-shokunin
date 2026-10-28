#!/bin/bash
# R49LabFd probe A: open fds 238..249 against /dev/null, then run a minimal copy of the
# frozen census resolver logic (tools/tsukuroi-census.sh @55c07cd, selftest_base_dir)
# with SELFTEST_FD_BAND unset (production band 240-249).
set -u
S=$(cd -- "$(dirname -- "$0")" && pwd)

echo "== step 0: baseline descriptors =="
ls /proc/self/fd | tr '\n' ' '; echo
echo "ulimit -n (soft) = $(ulimit -n)   ulimit -Hn (hard) = $(ulimit -Hn)"
echo "bash = $BASH_VERSION pid = $$"

echo "== step 1: open 238..249 </dev/null =="
for n in 238 239 240 241 242 243 244 245 246 247 248 249; do
  if eval "exec ${n}</dev/null" 2>"$S/err.$n"; then
    echo "exec ${n}</dev/null            -> ok"
  else
    echo "exec ${n}</dev/null            -> FAILED: $(cat "$S/err.$n")"
  fi
done
echo "-- /proc/self/fd now: --"
ls -l /proc/self/fd | sed 's/^.* [0-9][0-9]:[0-9][0-9] //'
echo "-- numbers: $(ls /proc/self/fd | sort -n | tr '\n' ' ')"

echo "== step 2: explicit exec 240</dev/null while 240 is held =="
if eval 'exec 240</dev/null' 2>"$S/err240"; then
  echo "re-exec 240 -> ok (re-pointed)"; ls -l /proc/self/fd/240 | sed 's/^.* [0-9][0-9]:[0-9][0-9] //'
else
  echo "re-exec 240 -> FAILED: $(cat "$S/err240")"
fi

echo "== step 3: minimal resolver copy, SELFTEST_FD_BAND unset =="
# verbatim logic of selftest_base_dir() minus the non-dirty branch, band default kept
selftest_base_dir() {
  local base fdn band
  ST_BASE_DIR=; ST_BASE_FD=; ST_BASE_ERR=
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

DIRTY="$S/dirty tmpdir"      # whitespace-bearing TMPDIR -> alias branch
mkdir -p "$DIRTY"
echo "band (SELFTEST_FD_BAND unset) = ${SELFTEST_FD_BAND:-<unset>}"
TMPDIR="$DIRTY" selftest_base_dir; rc=$?
echo "resolver rc=$rc ST_BASE_ERR=${ST_BASE_ERR:-<empty>} ST_BASE_DIR=${ST_BASE_DIR:-<empty>} ST_BASE_FD=${ST_BASE_FD:-<empty>}"
echo "-- diagnostic line the selftest prints for this class: --"
case "${ST_BASE_ERR:-}" in
  fd-band)
    printf 'selftest: fd band %s exhausted (every descriptor already open), cannot alias TMPDIR <%s>; no /tmp fallback (R49-C3)\n' \
      "${SELFTEST_FD_BAND:-240 241 242 243 244 245 246 247 248 249}" "${TMPDIR:-<unset>}" ;;
  *) echo "(other class: ${ST_BASE_ERR:-resolver})" ;;
esac

echo "== step 4: release 248/249, resolver must succeed in the band =="
eval 'exec 248<&-'; eval 'exec 249<&-'
TMPDIR="$DIRTY" selftest_base_dir; rc=$?
echo "resolver rc=$rc ST_BASE_ERR=${ST_BASE_ERR:-<empty>} ST_BASE_FD=${ST_BASE_FD:-<empty>}"
[ -n "${ST_BASE_FD:-}" ] && { ls -l "/proc/self/fd/$ST_BASE_FD" | sed 's/^.* [0-9][0-9]:[0-9][0-9] //'; readlink -f -- "$ST_BASE_DIR"; exec {ST_BASE_FD}<&-; }
echo "== step 5: dump what an already-open slot looks like =="
ls -l /proc/self/fd/240 2>&1 | sed 's/^.* [0-9][0-9]:[0-9][0-9] //'
exit 0
