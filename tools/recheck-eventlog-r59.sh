#!/usr/bin/env bash
# recheck-eventlog-r59 — one committed command re-verifying the event-log plane rows E1-E6
# (corpus/knowledge/windows-eventlog-plane-r58.md) plus the spelling/boundary variants, against
# the live host. The note carries the duty as prose in its `recheck:` header ("re-run the probe
# commands of rows E1-E6 ... compare the observed signatures with the receipts"); this script is
# that loop, executable (AXES operability signal) in service of freshness. Round-59 planned item:
# "the event-log plane's E1-E6 join the dated recheck discipline (an executable recheck arm for
# the E-rows, mirroring recheck-services-r56.sh, receipt-compared where the probe class requires
# it)". All E-probes are read-only or refusal-class, so every row here is LIVE (no
# receipt-compared class needed — the r58 probes never touched config/SCM-write-shaped surfaces).
#
# Usage: bash tools/recheck-eventlog-r59.sh [--receipt PATH]
#   Emits one line per row:  E<k> match|drift <evidence>
#   Rollup:  RECHECK_EVENTLOG: PASS (11 rows, M match, 0 drift)   rc 0
#            RECHECK_EVENTLOG: FAIL (N drift)                      rc 1
#   A drift line is honest output, not a crash: it owes an appended row correction next.
#
# Rows (11) and invariants (each judged on its INVARIANT signature only — counts, record
# numbers, timestamps and sizes are drift-class captures, recorded as evidence, never judged):
#   E1  channel enumeration rc 0, >= 1 channel name (count drift-class; r58 captured 1164)
#   E2  newest-first text query rc 0 with an Event[0] block AFTER the NUL-strip parsing rule
#       (tr -d '\r\0' before any count — the R58-WEVTUTIL-NUL-RECEIPTS fix bound in code: the
#       /f:text event text may carry NUL bytes that make grep treat the stream as binary)
#   E2s bare-spelling variant rc 87 "Too many arguments are specified." (MSYS rewrites /c:3 ->
#       c:3 at the bash->native boundary; the T1/E2 spelling trap)
#   E2b env-in-child-argv variant rc 87 (MSYS_NO_PATHCONV=1 carried on the CHILD argv via env,
#       spawned through receipt-run WITHOUT the var on the python spawn — the conversion happens
#       at the bash->python boundary before the child env could matter; the e2b receipt class)
#   E3  query-leg absence on a nonexistent channel: both message lines ("Failed to open event
#       query." + "The specified channel could not be found.") with rc in the 15007/159 family
#       (python spawns report 15007, bash-direct reports 15007 mod 256 = 159 — the T5 class)
#   E3s bare-spelling absence variant rc 87 (e3 mangled receipt class)
#   E3b env-in-child-argv absence variant rc 87 (e3b receipt class)
#   E4  metadata leg rc 0 with numberOfLogRecords + fileSize field lines (values drift-class)
#   E5  level-filtered /q: XPath query rc 0 (an empty result is a VALID answer — no Event[0]
#       requirement; rc 0 is the invariant, Event blocks recorded as evidence; NUL-strip applies)
#   E6  metadata-leg absence: "Failed to read log status information" (leg-specific function
#       line) + the same channel-not-found message, rc in the 15007/159 family
#   E6b bare `wevtutil cl` (no log name) refused at the usage gate rc 87 "Required argument(s)
#       is/are not specified." — no log can be cleared by accident (the operator-owned surface's
#       measured refusal gate; the probe NEVER names a log)
#
# Read-only: el/qe/gli are reads; the only cl invocation is the bare usage-refusal gate (no log
# name = nothing to clear). Spell `python`, not `python3` (D8). MSYS_NO_PATHCONV=1 is set on
# each probe spawn except the deliberate mangled-spelling rows (E2s/E3s), which measure the
# conversion itself. Owner: tsukuroi.
set -u
cd "$(dirname "$0")/.." || exit 2
receipt=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --receipt) receipt="${2:?--receipt needs a path}"; shift 2 ;;
    *) echo "usage: recheck-eventlog-r59.sh [--receipt PATH]" >&2; exit 2 ;;
  esac
done

drift=0; matched=0
lines_out=""
emit() { lines_out="${lines_out}${1}
"; }
NC=No-Such-Channel-r58probe
# nulstrip: the R58-WEVTUTIL-NUL-RECEIPTS parsing rule — strip \r AND \0 BEFORE any count
nulstrip() { tr -d '\r\0'; }

# E1 — channel enumeration: rc 0, at least one name
out1="$(MSYS_NO_PATHCONV=1 wevtutil el 2>&1)"; rc1=$?
n1="$(printf '%s' "$out1" | nulstrip | grep -c .)"
if [ "$rc1" -eq 0 ] && [ "$n1" -ge 1 ]; then
  emit "E1 match (wevtutil el rc 0, ${n1} channels — count drift-class, r58 captured 1164)"; matched=$((matched+1))
else
  emit "E1 drift (rc=$rc1 channels=$n1 — expected rc 0 with >=1 channel name)"; drift=$((drift+1))
fi

# E2 — newest-first text query: rc 0 + Event[0] block present after the NUL-strip rule
# (the strip is bound AT CAPTURE via tr + PIPESTATUS — raw NUL bytes in a command substitution
# make bash warn and drop them; the nulstrip in the judgment stays as belt)
out2="$(MSYS_NO_PATHCONV=1 wevtutil qe System /c:3 /rd:true /f:text 2>&1 | tr -d '\r\0')"; rc2="${PIPESTATUS[0]}"
ev2="$(printf '%s' "$out2" | nulstrip | grep -c "^Event\[[0-9]*\]$")"
if [ "$rc2" -eq 0 ] && [ "$ev2" -ge 1 ]; then
  emit "E2 match (qe System rc 0, ${ev2} Event[N] blocks newest-first after NUL-strip)"; matched=$((matched+1))
else
  emit "E2 drift (rc=$rc2 events=$ev2 — expected rc 0 with >=1 Event[N] block after tr -d '\\r\\0')"; drift=$((drift+1))
fi

# E2s — bare spelling: MSYS mangles the slash options -> usage error rc 87
out2s="$(wevtutil qe System /c:3 /rd:true /f:text 2>&1)"; rc2s=$?
if [ "$rc2s" -eq 87 ] && printf '%s' "$out2s" | grep -q "Too many arguments are specified."; then
  emit "E2s match (bare qe rc 87 'Too many arguments are specified.' — MSYS /c:3 -> c:3 class)"; matched=$((matched+1))
else
  emit "E2s drift (rc=$rc2s — expected rc 87 'Too many arguments are specified.')"; drift=$((drift+1))
fi

# E2b — env-in-child-argv: the var rides on the CHILD argv through a python spawn (no var on
# the python spawn itself) -> the boundary conversion still mangles -> child rc 87 (e2b receipt
# class). receipt-run demands --receipt (temp mktemp file, deleted in the same leg, T7 precedent)
# and reports the child rc on the RECEIPT's rc= line while exiting 0 itself — the judged value is
# the receipt rc, not receipt-run's process exit.
tmp2b="$(mktemp 2>/dev/null)" || tmp2b=""
python tools/receipt-run.py --budget 30 --receipt "$tmp2b" -- env MSYS_NO_PATHCONV=1 wevtutil qe System /c:3 /rd:true /f:text >/dev/null 2>&1
rc2b="$(grep -m1 '^rc=' "$tmp2b" | cut -d= -f2)"
rm -f "$tmp2b"
if [ "$rc2b" = "87" ]; then
  emit "E2b match (env-in-child-argv child rc 87 read from the spawn receipt — boundary conversion class, MSYS var must be on the spawn)"; matched=$((matched+1))
else
  emit "E2b drift (receipt rc=${rc2b:-none} — expected child rc 87 with MSYS_NO_PATHCONV only on the child argv)"; drift=$((drift+1))
fi

# E3 — query-leg absence: both message lines, rc in the 15007/159 family (bash-direct reports 159)
out3="$(MSYS_NO_PATHCONV=1 wevtutil qe "$NC" /c:1 2>&1)"; rc3=$?
if { [ "$rc3" -eq 159 ] || [ "$rc3" -eq 15007 ]; } \
   && printf '%s' "$out3" | grep -q "Failed to open event query." \
   && printf '%s' "$out3" | grep -q "The specified channel could not be found."; then
  emit "E3 match (query absence rc $rc3 in the 15007/159 family with both message lines)"; matched=$((matched+1))
else
  emit "E3 drift (rc=$rc3 — expected the 15007/159 family + 'Failed to open event query.' + channel-not-found)"; drift=$((drift+1))
fi

# E3s — bare-spelling absence variant rc 87 (the mangling fires before the channel lookup)
out3s="$(wevtutil qe "$NC" /c:1 2>&1)"; rc3s=$?
if [ "$rc3s" -eq 87 ] && printf '%s' "$out3s" | grep -q "Too many arguments are specified."; then
  emit "E3s match (bare absence probe rc 87 — mangled-spelling pair of e3)"; matched=$((matched+1))
else
  emit "E3s drift (rc=$rc3s — expected rc 87 'Too many arguments are specified.')"; drift=$((drift+1))
fi

# E3b — env-in-child-argv absence variant rc 87 (e3b receipt class; same mktemp --receipt +
# receipt-rc-line rule as E2b)
tmp3b="$(mktemp 2>/dev/null)" || tmp3b=""
python tools/receipt-run.py --budget 30 --receipt "$tmp3b" -- env MSYS_NO_PATHCONV=1 wevtutil qe "$NC" /c:1 >/dev/null 2>&1
rc3b="$(grep -m1 '^rc=' "$tmp3b" | cut -d= -f2)"
rm -f "$tmp3b"
if [ "$rc3b" = "87" ]; then
  emit "E3b match (env-in-child-argv absence child rc 87 read from the spawn receipt — boundary conversion class)"; matched=$((matched+1))
else
  emit "E3b drift (receipt rc=${rc3b:-none} — expected child rc 87 with MSYS_NO_PATHCONV only on the child argv)"; drift=$((drift+1))
fi

# E4 — metadata leg: rc 0 with numberOfLogRecords + fileSize lines (values drift-class)
out4="$(MSYS_NO_PATHCONV=1 wevtutil gli System 2>&1)"; rc4=$?
if [ "$rc4" -eq 0 ] && printf '%s' "$out4" | grep -q "^numberOfLogRecords:" \
   && printf '%s' "$out4" | grep -q "^fileSize:"; then
  rec4="$(printf '%s' "$out4" | grep "^numberOfLogRecords:" | tr -d '\r' | cut -d' ' -f2)"
  emit "E4 match (gli System rc 0 with numberOfLogRecords/fileSize fields — values drift-class, records=${rec4})"; matched=$((matched+1))
else
  emit "E4 drift (rc=$rc4 — expected rc 0 with numberOfLogRecords + fileSize field lines)"; drift=$((drift+1))
fi

# E5 — level-filtered query: rc 0 is the invariant (empty result is a valid answer); NUL-strip
# bound at capture (same PIPESTATUS form as E2)
out5="$(MSYS_NO_PATHCONV=1 wevtutil qe System '/q:*[System[(Level=1 or Level=2)]]' /c:5 /rd:true /f:text 2>&1 | tr -d '\r\0')"; rc5="${PIPESTATUS[0]}"
ev5="$(printf '%s' "$out5" | nulstrip | grep -c "^Event\[[0-9]*\]$")"
if [ "$rc5" -eq 0 ]; then
  emit "E5 match (level-filter qe rc 0 — ${ev5} Event[N] blocks, empty result also valid)"; matched=$((matched+1))
else
  emit "E5 drift (rc=$rc5 — expected rc 0; an empty result is valid, an rc failure is not)"; drift=$((drift+1))
fi

# E6 — metadata-leg absence: leg-specific function line + the shared channel-not-found message
out6="$(MSYS_NO_PATHCONV=1 wevtutil gli "$NC" 2>&1)"; rc6=$?
if { [ "$rc6" -eq 159 ] || [ "$rc6" -eq 15007 ]; } \
   && printf '%s' "$out6" | grep -q "Failed to read log status information" \
   && printf '%s' "$out6" | grep -q "The specified channel could not be found."; then
  emit "E6 match (metadata absence rc $rc6 in the 15007/159 family with the leg-specific function line)"; matched=$((matched+1))
else
  emit "E6 drift (rc=$rc6 — expected the 15007/159 family + 'Failed to read log status information' + channel-not-found)"; drift=$((drift+1))
fi

# E6b — bare `cl` (no log name) refused at the usage gate; NO log is ever named here
out6b="$(wevtutil cl 2>&1)"; rc6b=$?
if [ "$rc6b" -eq 87 ] && printf '%s' "$out6b" | grep -q "Required argument(s) is/are not specified."; then
  emit "E6b match (bare cl usage-refused rc 87 — no log name given, nothing cleared)"; matched=$((matched+1))
else
  emit "E6b drift (rc=$rc6b — expected rc 87 'Required argument(s) is/are not specified.')"; drift=$((drift+1))
fi

rollup="RECHECK_EVENTLOG: PASS (11 rows, ${matched} match, 0 drift)"
rc=0
if [ "$drift" -ne 0 ]; then
  rollup="RECHECK_EVENTLOG: FAIL (${drift} drift)"
  rc=1
fi
out="${lines_out}${rollup}
"
printf '%s' "$out"
if [ -n "$receipt" ]; then
  mkdir -p "$(dirname "$receipt")" || { echo "cannot write receipt dir" >&2; exit 2; }
  printf 'recheck_eventlog_r59=1\ndate_utc=%s\nrows=11\nmatched=%s\ndrift=%s\n---\n%s' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$matched" "$drift" "$out" > "$receipt" \
    || { echo "cannot write receipt $receipt" >&2; exit 2; }
fi
exit $rc
