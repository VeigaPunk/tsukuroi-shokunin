set -euo pipefail
ST_BASE_DIR=; ST_BASE_FD=; ST_BASE_ERR=
selftest_base_dir() {
  # Result contract: ST_BASE_DIR receives the base, ST_BASE_FD the descriptor id
  # (empty when no alias was needed). Must run in the CALLER's shell — the fd a
  # /proc/self/fd alias refers to must outlive this function, so command
  # substitution (a subshell whose fds die with it) is forbidden here.
  #
  # The alias uses a fixed high descriptor (240-249), never the auto-allocated
  # lowest-free fd: selftest fixture children legitimately `exec 10<...` and
  # auto-allocated fds start at 10, so an alias at 10 would be silently
  # re-pointed inside a child and every "$work"-relative path resolved through
  # it would break (observed 2026-10-28: R46-C1 held-descriptor case failed
  # with "/proc/self/fd/10/...: Not a directory"). 240-249 stays below bash's
  # script descriptor band (255) and above anything fixtures auto-allocate.
  local base fdn band
  ST_BASE_DIR=
  ST_BASE_FD=
  ST_BASE_ERR=
  # (R49-C3) The band is overridable so a selftest case can exhaust a two-descriptor
  # band deterministically; production keeps the fixed 240-249 band documented above.
  band=${SELFTEST_FD_BAND:-240 241 242 243 244 245 246 247 248 249}
  base=${TMPDIR:-/tmp}
  case "$base" in
    *[!A-Za-z0-9._/+-]*)
      # dirty TMPDIR: it must exist and be a directory for the alias to bind
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
# harness-level base resolution for the dirty TMPDIR (mirrors run_selftest's own call)
TMPDIR="$1" selftest_base_dir
printf 'harness base=<%s> fd=<%s>\n' "$ST_BASE_DIR" "$ST_BASE_FD"
mkdir -p "$ST_BASE_DIR/fx/dirty tmpdir" "$ST_BASE_DIR/fx/dirty fd band"
# R48 case: second resolver call (allocates 241, then closes it)
TMPDIR="$ST_BASE_DIR/fx/dirty tmpdir" selftest_base_dir; rc=$?
printf 'r48 rc=%s fd=<%s>\n' "$rc" "$ST_BASE_FD"
[ -n "$ST_BASE_FD" ] && exec {ST_BASE_FD}<&-
# R49 case guard, verbatim
r49_held=0
if [ ! -e /proc/self/fd/240 ] && [ ! -e /proc/self/fd/241 ]; then
  if eval 'exec 240<&0' 2>/dev/null && eval 'exec 241<&0' 2>/dev/null; then r49_held=1; fi
fi
printf 'r49_held=%s (240-open=%s 241-open=%s)\n' "$r49_held" "$([ -e /proc/self/fd/240 ] && echo y || echo n)" "$([ -e /proc/self/fd/241 ] && echo y || echo n)"
[ "$r49_held" -eq 1 ] || printf '=> would print: FAIL selftest: could not reserve the 240/241 probe descriptors for the fd-band case (R49-C3)\n'
