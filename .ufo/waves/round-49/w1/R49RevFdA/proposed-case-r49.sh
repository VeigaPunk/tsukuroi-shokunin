# --- proposed replacement for tools/tsukuroi-census.sh:3579-3600 (D1) ---
  # (R49-C3) fd-band exhaustion is named, not silent: narrow the alias band to ONE
  # descriptor and hold it, so a dirty TMPDIR must fail the resolver with
  # ST_BASE_ERR=fd-band. The probe must be a band member that is FREE right now: when
  # TMPDIR needs an alias the harness's own base already holds the first free member
  # (selftest_base_dir below), so hardcoding 240/241 fails this case spuriously.
  r49_dir="$work/fx/dirty fd band"
  mkdir -p "$r49_dir"
  r49_fd=
  for r49_n in 240 241 242 243 244 245 246 247 248 249; do
    [ -e "/proc/self/fd/$r49_n" ] && continue
    eval "exec ${r49_n}<&0" 2>/dev/null && { r49_fd=$r49_n; break; }
  done
  if [ -n "$r49_fd" ]; then
    r49_old_tmp=${TMPDIR-}; r49_old_band=${SELFTEST_FD_BAND-}
    TMPDIR="$r49_dir"
    SELFTEST_FD_BAND=$r49_fd
    if selftest_base_dir; then
      [ -n "${ST_BASE_FD:-}" ] && eval "exec ${ST_BASE_FD}<&-"
      bad 'selftest: an exhausted fd band must fail the base resolver (R49-C3)'
    elif [ "${ST_BASE_ERR:-}" = 'fd-band' ] && [ -z "${ST_BASE_DIR:-}" ] && [ -z "${ST_BASE_FD:-}" ]; then
      ok 'selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)'
    else
      bad "selftest: exhausted fd band must name err=fd-band (got '${ST_BASE_ERR:-<empty>}') (R49-C3)"
    fi
    if [ -n "$r49_old_band" ]; then SELFTEST_FD_BAND=$r49_old_band; else unset SELFTEST_FD_BAND; fi
    if [ -n "$r49_old_tmp" ]; then TMPDIR=$r49_old_tmp; else unset TMPDIR; fi
    eval "exec ${r49_fd}<&-" 2>/dev/null
  else
    bad 'selftest: every 240-249 probe descriptor is already open, cannot exercise the fd-band case (R49-C3)'
  fi
  unset r49_dir r49_fd r49_n r49_old_tmp r49_old_band
