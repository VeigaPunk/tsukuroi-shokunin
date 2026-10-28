# --- proposed replacement for tools/tsukuroi-census.sh:2088-2091 (D3+D4) ---
      # `for fdn in $band` splits on the default IFS (the band is a space list) and
      # leaves fdn unset for an all-whitespace override; init it and reject any token
      # that is not a bare descriptor number, so the eval below never sees text it did
      # not choose (a bad token used to kill the shell with rc=127).
      fdn=
      for fdn in $band; do
        case $fdn in '' | *[!0-9]*) ST_BASE_ERR=band-token; return 1 ;; esac
        [ -e "/proc/self/fd/$fdn" ] || break
      done
      if [ -z "$fdn" ]; then ST_BASE_ERR=band-empty; return 1; fi
      if [ -e "/proc/self/fd/$fdn" ]; then ST_BASE_ERR=fd-band; return 1; fi
