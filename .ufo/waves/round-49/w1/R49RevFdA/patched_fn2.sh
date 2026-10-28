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
      fdn=
      for fdn in $band; do
        case $fdn in ''|*[!0-9]*) ST_BASE_ERR=band-token; return 1 ;; esac
        [ -e "/proc/self/fd/$fdn" ] || break
      done
      if [ -z "$fdn" ]; then ST_BASE_ERR=band-empty; return 1; fi
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
