#!/usr/bin/env bash
# recheck-services-r56 — one committed command re-verifying the services-plane rows T1-T12
# (corpus/knowledge/windows-services-plane-r54.md rows T1-T8, windows-services-plane-r55.md rows
# T9-T12) against the live host. Both notes carry the duty only as prose in their `recheck:`
# headers ("re-run the probe commands of rows ... compare the observed signatures"); this script
# is that loop, executable (AXES operability signal) in service of freshness.
#
# Usage: bash tools/recheck-services-r56.sh [--receipt PATH] [--raw-dir DIR]
#   Emits one line per row:  T<k> match|drift <evidence>
#   Rollup:  RECHECK_SERVICES: PASS (12 rows, M match, 0 drift)   rc 0
#            RECHECK_SERVICES: FAIL (N drift)                     rc 1
#   A drift line is honest output, not a crash: it owes an appended row correction next.
#
# --raw-dir DIR (round 57, C2): additionally write one receipt-run-FORMAT raw receipt per row,
#   <DIR>/t<k>-raw.txt, via tools/receipt-write.py (build_receipt imported from receipt-run.py —
#   one format implementation). Each raw receipt carries the leg's JUDGED capture (the exact bytes
#   the invariant read — out<k>, or the stray-file content for T7, or the shared enumeration for
#   T4/T8) and the leg's own rc, with command=<the exact probe command text>. The probe is NEVER
#   re-executed for the capture: T1's signature is bash/MSYS-exec-specific and T7's stray file a
#   re-run would create twice — the capture rides alongside, judgment logic byte-unchanged.
#
# Invariants vs drift-class values: each row's probe is compared on its INVARIANT signature
# (error line, rc family, field presence) only. Values known to drift with the host — task and
# service counts, STATE/PID/TYPE values, the wait-hint states tuple — are recorded as evidence,
# never judged (the planes' Limits sections name that drift class).
#
# Read-only: schtasks /query, sc query/queryex/qc are read-only. Two bounded exceptions, each
# the documented probe of its row: T7 re-creates the stray PowerShell-alias file inside a
# mktemp -d directory that is deleted in the same leg (the probe's whole point is that the
# stray file appears); T1 relies on the failing bare `schtasks /query` (the MSYS-mangled error
# is the signature). No service is started, stopped, configured or deleted; every state change
# stays operator-owned (RP4/RP5 of the r54 plane). Spell `python`, not `python3` (D8).
# Owner: tsukuroi.
set -u
cd "$(dirname "$0")/.." || exit 2
receipt=""
raw_dir=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --receipt) receipt="${2:?--receipt needs a path}"; shift 2 ;;
    --raw-dir) raw_dir="${2:?--raw-dir needs a path}"; shift 2 ;;
    *) echo "usage: recheck-services-r56.sh [--receipt PATH] [--raw-dir DIR]" >&2; exit 2 ;;
  esac
done
if [ -n "$raw_dir" ]; then
  mkdir -p "$raw_dir" || { echo "cannot create raw-dir $raw_dir" >&2; exit 2; }
fi
# rw <k> <rc> <command-text> <capture>: write t<k>-raw.txt through receipt-write (never re-runs the probe)
rw() {
  [ -n "$raw_dir" ] || return 0
  printf '%s' "$4" | python tools/receipt-write.py \
    --receipt "$raw_dir/t$1-raw.txt" --rc "$2" --command "$3" --budget 60 >/dev/null \
    || { echo "receipt-write failed for t$1" >&2; exit 2; }
}

drift=0; matched=0
lines_out=""
emit() { lines_out="${lines_out}${1}
"; }
NS=No-Such-Service-r56probe
NT=No-Such-Task-r56probe

# T1 — bare `schtasks /query` must FAIL with the MSYS-mangled-option error (never rc 0)
out1="$(schtasks /query /fo CSV /nh 2>&1)"; rc1=$?
rw 1 "$rc1" "schtasks /query /fo CSV /nh" "$out1"
if [ "$rc1" -ne 0 ] && printf '%s' "$out1" | grep -q "Invalid argument/option"; then
  emit "T1 match (bare schtasks rc $rc1 mangled-option error — MSYS path conversion class)"; matched=$((matched+1))
else
  emit "T1 drift (bare schtasks rc=$rc1 — expected nonzero + 'Invalid argument/option' mangled error)"; drift=$((drift+1))
fi

# T2 — MSYS-safe task inventory: rc 0, CSV rows present; the count is a drift-class value
out2="$(MSYS_NO_PATHCONV=1 schtasks /query /fo CSV /nh 2>&1)"; rc2=$?
rw 2 "$rc2" "MSYS_NO_PATHCONV=1 schtasks /query /fo CSV /nh" "$out2"
rows2="$(printf '%s' "$out2" | grep -c .)"
if [ "$rc2" -eq 0 ] && [ "$rows2" -ge 1 ]; then
  emit "T2 match (schtasks CSV rc 0, ${rows2} rows — count drift-class, r54 captured 246)"; matched=$((matched+1))
else
  emit "T2 drift (schtasks rc=$rc2 rows=$rows2 — expected rc 0 with >=1 CSV row)"; drift=$((drift+1))
fi

# T3 — nonexistent task: path-class error, rc 1
out3="$(MSYS_NO_PATHCONV=1 schtasks /query /tn "$NT" /fo LIST 2>&1)"; rc3=$?
rw 3 "$rc3" "MSYS_NO_PATHCONV=1 schtasks /query /tn $NT /fo LIST" "$out3"
if [ "$rc3" -eq 1 ] && printf '%s' "$out3" | grep -q "The system cannot find the path specified"; then
  emit "T3 match (nonexistent task rc 1 path-class error)"; matched=$((matched+1))
else
  emit "T3 drift (rc=$rc3 — expected rc 1 'The system cannot find the path specified')"; drift=$((drift+1))
fi

# T4 + T8 share one enumeration (the two rows' probes are the same command read two ways)
all_out="$(MSYS_NO_PATHCONV=1 sc query state= all 2>&1)"; rc_all=$?
all_n="$(printf '%s' "$all_out" | grep -c "SERVICE_NAME")"
active_out="$(MSYS_NO_PATHCONV=1 sc query 2>&1)"; rc_act=$?
act_n="$(printf '%s' "$active_out" | grep -c "SERVICE_NAME")"
rw 4 "$rc_all" "MSYS_NO_PATHCONV=1 sc query state= all ; MSYS_NO_PATHCONV=1 sc query" "$all_out"
if [ "$rc_all" -eq 0 ] && [ "$rc_act" -eq 0 ] && [ "$all_n" -ge 1 ] && [ "$act_n" -ge 1 ]; then
  emit "T4 match (query rc 0: active-only ${act_n} blocks vs state= all ${all_n} — counts drift-class, r54 captured 110/273)"; matched=$((matched+1))
else
  emit "T4 drift (rc all=$rc_all active=$rc_act blocks all=$all_n active=$act_n — expected rc 0 both with >=1 SERVICE_NAME)"; drift=$((drift+1))
fi
# T5 — nonexistent service under query: FAILED 1060 + rc 36
out5="$(MSYS_NO_PATHCONV=1 sc query "$NS" 2>&1)"; rc5=$?
rw 5 "$rc5" "MSYS_NO_PATHCONV=1 sc query $NS" "$out5"
if [ "$rc5" -eq 36 ] && printf '%s' "$out5" | grep -q "FAILED 1060"; then
  emit "T5 match (nonexistent service rc 36 FAILED 1060)"; matched=$((matched+1))
else
  emit "T5 drift (rc=$rc5 — expected rc 36 + FAILED 1060)"; drift=$((drift+1))
fi
# T6 — the S262 divergence persists: type= interact lists interactives rc 0 on this build
out6="$(MSYS_NO_PATHCONV=1 sc query type= interact 2>&1)"; rc6=$?
rw 6 "$rc6" "MSYS_NO_PATHCONV=1 sc query type= interact" "$out6"
if [ "$rc6" -eq 0 ] && printf '%s' "$out6" | grep -qi "interactive"; then
  emit "T6 match (type= interact rc 0 interactive listing — S262's documented error still does not fire)"; matched=$((matched+1))
else
  emit "T6 drift (rc=$rc6 — r54/r56 measured rc 0 with an interactive listing; S262 sentence now fires)"; drift=$((drift+1))
fi
# T7 — powershell sc alias: rc 0, empty query, stray `query` file written in the CWD
tmpd="$(mktemp -d "${TMPDIR:-/tmp}/recheck-t7.XXXXXX")"
( cd "$tmpd" && MSYS_NO_PATHCONV=1 powershell -NoProfile -Command "sc query wuauserv" >/dev/null 2>&1 ); rc7=$?
stray="$(cat "$tmpd/query" 2>/dev/null || true)"
rm -rf "$tmpd"
rw 7 "$rc7" "( cd \$tmpd && MSYS_NO_PATHCONV=1 powershell -NoProfile -Command \"sc query wuauserv\" ) >/dev/null 2>&1; stray=\$(cat \$tmpd/query) — judged capture: the stray-file content" "$stray"
if [ "$rc7" -eq 0 ] && [ "$stray" = "wuauserv" ]; then
  emit "T7 match (powershell rc 0 no output, stray 'query' file recreated with wuauserv, temp cwd deleted)"; matched=$((matched+1))
else
  emit "T7 drift (rc=$rc7 stray='${stray:-<none>}' — expected the Set-Content alias class)"; drift=$((drift+1))
fi
# T8 — the documented Enum more-data overflow must NOT fire on this build (negative invariant)
rw 8 "$rc_all" "MSYS_NO_PATHCONV=1 sc query state= all (shared T4 enumeration; invariant: no 'Enum: more data' line)" "$all_out"
if [ "$rc_all" -eq 0 ] && ! printf '%s' "$all_out" | grep -q "Enum: more data"; then
  emit "T8 match (state= all rc 0, no Enum more-data message — S262 resumption path stays doc-only here)"; matched=$((matched+1))
else
  emit "T8 drift (rc_all=$rc_all — Enum more-data class changed; follow S262 bufsize=/ri= next)"; drift=$((drift+1))
fi

# T9 — queryex on a live service: rc 0 with PID + FLAGS + wait-hint states line (values drift-class)
out9="$(MSYS_NO_PATHCONV=1 sc queryex wuauserv 2>&1)"; rc9=$?
rw 9 "$rc9" "MSYS_NO_PATHCONV=1 sc queryex wuauserv" "$out9"
if [ "$rc9" -eq 0 ] && printf '%s' "$out9" | grep -q "^        PID" && printf '%s' "$out9" | grep -q "^        FLAGS"; then
  st9="$(printf '%s' "$out9" | grep -m1 "STATE")"
  emit "T9 match (queryex rc 0 PID+FLAGS present; ${st9:-STATE unreadable} — value drift-class)"; matched=$((matched+1))
else
  emit "T9 drift (rc=$rc9 — expected rc 0 with PID and FLAGS lines)"; drift=$((drift+1))
fi
# T10 — nonexistent service under queryex: same 1060/rc-36 class as query
out10="$(MSYS_NO_PATHCONV=1 sc queryex "$NS" 2>&1)"; rc10=$?
rw 10 "$rc10" "MSYS_NO_PATHCONV=1 sc queryex $NS" "$out10"
if [ "$rc10" -eq 36 ] && printf '%s' "$out10" | grep -q "FAILED 1060"; then
  emit "T10 match (queryex nonexistent rc 36 FAILED 1060)"; matched=$((matched+1))
else
  emit "T10 drift (rc=$rc10 — expected rc 36 + FAILED 1060)"; drift=$((drift+1))
fi
# T11 — qc on a live service: rc 0 with START_TYPE + BINARY_PATH_NAME (values drift-class)
out11="$(MSYS_NO_PATHCONV=1 sc qc wuauserv 2>&1)"; rc11=$?
rw 11 "$rc11" "MSYS_NO_PATHCONV=1 sc qc wuauserv" "$out11"
if [ "$rc11" -eq 0 ] && printf '%s' "$out11" | grep -q "START_TYPE" && printf '%s' "$out11" | grep -q "BINARY_PATH_NAME"; then
  st11="$(printf '%s' "$out11" | grep -m1 "START_TYPE")"
  emit "T11 match (qc rc 0 QueryServiceConfig with START_TYPE+BINARY_PATH_NAME; ${st11:-START_TYPE unreadable} — value drift-class)"; matched=$((matched+1))
else
  emit "T11 drift (rc=$rc11 — expected rc 0 with START_TYPE and BINARY_PATH_NAME)"; drift=$((drift+1))
fi
# T12 — nonexistent service under qc: the qc function line differs, rc family matches
out12="$(MSYS_NO_PATHCONV=1 sc qc "$NS" 2>&1)"; rc12=$?
rw 12 "$rc12" "MSYS_NO_PATHCONV=1 sc qc $NS" "$out12"
if [ "$rc12" -eq 36 ] && printf '%s' "$out12" | grep -q "\[SC\] OpenService FAILED 1060:"; then
  emit "T12 match (qc nonexistent rc 36 [SC] OpenService FAILED 1060: — qc's own function line)"; matched=$((matched+1))
else
  emit "T12 drift (rc=$rc12 — expected rc 36 + '[SC] OpenService FAILED 1060:')"; drift=$((drift+1))
fi

rollup="RECHECK_SERVICES: PASS (12 rows, ${matched} match, 0 drift)"
rc=0
if [ "$drift" -ne 0 ]; then
  rollup="RECHECK_SERVICES: FAIL (${drift} drift)"
  rc=1
fi
out="${lines_out}${rollup}
"
printf '%s' "$out"
if [ -n "$receipt" ]; then
  mkdir -p "$(dirname "$receipt")" || { echo "cannot create receipt dir" >&2; exit 2; }
  printf 'recheck_services_r56=1\ndate_utc=%s\nrows=12\nmatched=%s\ndrift=%s\n---\n%s' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$matched" "$drift" "$out" > "$receipt" \
    || { echo "cannot write receipt $receipt" >&2; exit 2; }
fi
exit $rc
