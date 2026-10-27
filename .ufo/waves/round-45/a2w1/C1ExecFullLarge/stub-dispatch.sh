#!/usr/bin/env bash
# Stub dispatcher for the C1-10 end-to-end census run (outside the census selftest).
# Answers the census's probe calls for systemctl / nvidia-smi / lsmod.
#   FX        fixture data dir (first lines live there)
#   PAD_LINES padding lines appended after the deciding first line (0 = first line only)
set -u
name=${0##*/}
FX=${FX:?FX unset}
PAD_LINES=${PAD_LINES:-0}
args="$*"
[ -n "${CALLS:-}" ] && printf '%s %s\n' "$name" "$args" >> "$CALLS"

pad() { # pad -> ~200 KB of printable padding, never shaped like a unit/field row
  [ "$PAD_LINES" -gt 0 ] || return 0
  awk -v n="$PAD_LINES" 'BEGIN { for (i = 0; i < n; i++) printf "pad-line %05d ..................................................\n", i }'
}

rc_of() { local f="$FX/$1.rc"; if [ -f "$f" ]; then cat "$f"; else printf 0; fi; }
first_of() { local f="$FX/$1"; [ -f "$f" ] && head -n1 "$f"; }

case "$name" in
  systemctl)
    case "$args" in
      *is-system-running*) printf '%s\n' "$(first_of sysrunning)"; pad; exit "$(rc_of sysrunning)" ;;
      *is-active*)         printf '%s\n' "$(first_of boottarget)"; pad; exit "$(rc_of boottarget)" ;;
      *list-units*failed*) :; exit 0 ;;
      *list-unit-files*)   cat "$FX/timerlist"; exit "$(rc_of timerlist)" ;;
      *show*ActiveState*)  printf '%s\n' "$(first_of timeractivestate)"; pad; exit "$(rc_of timeractivestate)" ;;
      *show*Result*)       printf '%s\n' "$(first_of timerresult)"; pad; exit "$(rc_of timerresult)" ;;
      *) printf 'stub systemctl: unexpected args: %s\n' "$args" >&2; exit 64 ;;
    esac
    ;;
  nvidia-smi)
    printf '%s\n' "$(first_of smi.out)"; pad; exit "$(rc_of smi)"
    ;;
  lsmod)
    cat "$FX/lsmod"
    ;;
esac
printf 'stub dispatcher: unknown command %s\n' "$name" >&2
exit 96
