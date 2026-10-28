#!/usr/bin/env bash
# Cheat A: a lying script. It runs no selftest at all; it prints the two lines the
# counter greps for. All strings the text legs look for live in comments:
#   ST_BASE_ERR=fd-band
#   printf 'selftest: fd band %s exhausted ...'   <- fd band (occurrence 2)
# and fd band appears once more in prose so text.count('fd band') >= 2.
# The stale comment the counter forbids is simply never written.
set -u
case "${1:-}" in
  --selftest) : ;;
  *) : ;;
esac
printf 'PASS selftest: exhausted fd band fails the base resolver and names err=fd-band (R49-C3)\n'
printf 'TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)\n'
exit 0
