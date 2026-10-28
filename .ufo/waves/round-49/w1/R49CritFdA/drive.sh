#!/usr/bin/env bash
# Harness: source the frozen resolver, mimic run_selftest's diagnostic block verbatim.
S=/fast/scratch/hyaku/tsukuroi-r49/R49CritFdA
. "$S/resolver.sh"
emit() {
  if selftest_base_dir; then
    printf 'RC=0 ERR=<%s> FD=<%s> DIR=<%s>\n' "${ST_BASE_ERR:-}" "${ST_BASE_FD:-}" "${ST_BASE_DIR:-}"
    [ -n "${ST_BASE_FD:-}" ] && eval "exec ${ST_BASE_FD}<&-"
  else
    printf 'RC=1 ERR=<%s> FD=<%s> DIR=<%s> | ' "${ST_BASE_ERR:-}" "${ST_BASE_FD:-}" "${ST_BASE_DIR:-}"
    case "${ST_BASE_ERR:-}" in
      fd-band) printf 'DIAG: fd band %s exhausted (every descriptor already open), cannot alias TMPDIR <%s>; no /tmp fallback (R49-C3)\n' \
          "${SELFTEST_FD_BAND:-240 241 242 243 244 245 246 247 248 249}" "${TMPDIR:-<unset>}" ;;
      *) printf 'DIAG: TMPDIR <%s> cannot host the fixture tree (%s; no /tmp fallback, R48-C2)\n' \
          "${TMPDIR:-<unset>}" "${ST_BASE_ERR:-resolver}" ;;
    esac
  fi
}
