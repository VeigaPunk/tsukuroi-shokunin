#!/usr/bin/env bash
# recheck-services-r56 — one committed command re-verifying the services-plane rows T1-T24
# (corpus/knowledge/windows-services-plane-r54.md rows T1-T8, windows-services-plane-r55.md rows
# T9-T12, windows-services-config-plane-r56.md rows T13-T16, windows-services-sddl-plane-r57.md
# rows T19-T24) against the live host. The four notes carry the duty as prose in their `recheck:`
# headers ("re-run the probe commands of rows ... compare the observed signatures"); this script
# is that loop, executable (AXES operability signal) in service of freshness.
#
# Usage: bash tools/recheck-services-r56.sh [--receipt PATH] [--raw-dir DIR]
#   Emits one line per row:  T<k> match|drift <evidence>
#   Rollup:  RECHECK_SERVICES: PASS (22 rows, M match, 0 drift)   rc 0
#            RECHECK_SERVICES: FAIL (N drift)                     rc 1
#   A drift line is honest output, not a crash: it owes an appended row correction next.
#
# Row classes (round 58, C2):
#   LIVE rows T1-T12 + T19-T23: the probe is re-run here and the observed bytes are compared on
#   the row's invariant signature (all read-only or refusal-class; the two bounded exceptions
#   below are unchanged).
#   RECEIPT-COMPARED rows T13-T16 + T24: the probe is NEVER re-executed — the probes behind them
#   are config-change-shaped (`sc config`/`sc failure <svc> <options>`) or SCM-write-shaped
#   (`sc sdset`), and the config note's operative `recheck:` line commits T13-T16 to
#   receipt-comparison. The row verifies that its committed dated receipt(s) under
#   .ufo/waves/round-{56,57}/services-probes/ still exist and still carry the row's invariant
#   signature (rc + key line); a missing receipt or a drifted signature is drift.
#
# --raw-dir DIR (round 57, C2): additionally write one receipt-run-FORMAT raw receipt per LIVE
#   row, <DIR>/t<k>-raw.txt, via tools/receipt-write.py (build_receipt imported from
#   receipt-run.py — one format implementation). Each raw receipt carries the leg's JUDGED
#   capture (the exact bytes the invariant read — out<k>, or the stray-file content for T7, or
#   the shared enumeration for T4/T8) and the leg's own rc, with command=<the exact probe command
#   text>. The probe is NEVER re-executed for the capture: T1's signature is bash/MSYS-exec-
#   specific and T7's stray file a re-run would create twice — the capture rides alongside,
#   judgment logic byte-unchanged. Receipt-compared rows write NO raw receipt: their capture
#   already lives in the committed dated receipt, and duplicating it would double-store evidence.
#
# Invariants vs drift-class values: each row's probe is compared on its INVARIANT signature
# (error line, rc family, field presence) only. Values known to drift with the host — task and
# service counts, STATE/PID/TYPE values, the wait-hint states tuple — are recorded as evidence,
# never judged (the planes' Limits sections name that drift class).
#
# Read-only: schtasks /query, sc query/queryex/qc/sdshow/qsidtype/qdescription/qdesc/
# qtriggerinfo/enumdepend are read-only (the r54/r55/r56/r57 planes' probe classes). Two bounded
# exceptions, each the documented probe of its row: T7 re-creates the stray PowerShell-alias
# file inside a mktemp -d directory that is deleted in the same leg (the probe's whole point is
# that the stray file appears); T1 relies on the failing bare `schtasks /query` (the
# MSYS-mangled error is the signature). The config-change-shaped and SCM-write-shaped probes
# (T13-T16, T24) are NEVER executed here — receipt-compared (see Row classes above). No service
# is started, stopped, configured, changed or deleted; every state change stays operator-owned
# (RP4/RP5 of the r54 plane, RP6 of the r58 eventlog plane). Spell `python`, not `python3` (D8).
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
# rcr <k> <want-rc:receipt:fixed-string>... — receipt-compared row: every committed dated receipt
# named must exist, carry rc=<want>, and contain the row's invariant fixed string. want "-" means
# the file is evidence without a receipt-run rc= line (e.g. an input capture): pattern only.
# NEVER re-runs a probe (the T13-T16/T24 probes are config-change-shaped or SCM-write-shaped).
rcr() {
  k="$1"; shift
  bad=""
  for spec in "$@"; do
    want="${spec%%:*}"; rest="${spec#*:}"; f="${rest%%:*}"; pat="${rest#*:}"
    if [ ! -f "$f" ]; then
      bad="$bad ${f}:MISSING"
    else
      if [ "$want" = "-" ]; then
        # "-" = evidence file without a receipt-run rc= line (e.g. an input capture); pattern only
        grep -qF -- "$pat" "$f" || bad="$bad $(basename "$f")(pattern-absent)"
      else
        got="$(grep -m1 '^rc=' "$f" | cut -d= -f2)"
        if [ "$got" != "$want" ] || ! grep -qF -- "$pat" "$f"; then
          bad="$bad $(basename "$f")(rc=${got:-none},want=$want)"
        fi
      fi
    fi
  done
  if [ -z "$bad" ]; then
    emit "T$k match (receipt-compared: $# receipt(s) rc+invariant held — probes not re-executed)"; matched=$((matched+1))
  else
    emit "T$k drift (receipt-compared:$bad — committed evidence no longer carries the row's signature)"; drift=$((drift+1))
  fi
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

# --- Receipt-compared rows: the r56 config/failure plane (T13-T16) ---
# Probes behind these rows are config-change-shaped; the committed dated receipts under
# .ufo/waves/round-56/services-probes/ are the evidence compared, never re-executed.
P56=.ufo/waves/round-56/services-probes
# T13 — config/failure with a name but NO options: the usage gate at rc 103 (option-validation
# precedes OpenService; the gate that r56 measured)
rcr 13 "103:$P56/t13-config-usage-gate.txt:USAGE:" \
      "103:$P56/t14-failure-usage-gate.txt:USAGE:"
# T14 — config WITH options on a nonexistent service: refused by absence before any write
rcr 14 "36:$P56/t15-config-nonexistent-start.txt:[SC] OpenService FAILED 1060:"
# T15 — failure-actions WITH options on a nonexistent service: same absence refusal
rcr 15 "36:$P56/t16-failure-nonexistent-actions.txt:[SC] OpenService FAILED 1060:"
# T16 — the failure QUERY is spelled qfailure (rc 0, QueryServiceConfig2 with RESET_PERIOD);
# bare `sc failure <wsvc>` does NOT query (usage rc 103)
rcr 16 "0:$P56/t17-qfailure-wuauserv.txt:RESET_PERIOD" \
      "103:$P56/t18-failure-bare-wuauserv.txt:USAGE:"

# --- LIVE rows: the r57 SDDL/metadata plane (T19-T23, all read-only or refusal-class) ---
# T19 — sdshow on a live service: rc 0 and one D:-only 3-ACE SDDL line (invariant: the D: prefix
# and the three ACE groups; the exact rights letters are the row's evidence)
out19="$(MSYS_NO_PATHCONV=1 sc sdshow wuauserv 2>&1)"; rc19=$?
rw 19 "$rc19" "MSYS_NO_PATHCONV=1 sc sdshow wuauserv" "$out19"
if [ "$rc19" -eq 0 ] && printf '%s' "$out19" | grep -qF 'D:(A;;' && [ "$(printf '%s' "$out19" | grep -o '(A;;' | wc -l)" -eq 3 ]; then
  emit "T19 match (sdshow rc 0, D:-only descriptor with 3 AccessAllowed ACEs — the r57 shape)"; matched=$((matched+1))
else
  emit "T19 drift (rc=$rc19 — expected rc 0 with one D:(A;;... line carrying exactly 3 ACEs)"; drift=$((drift+1))
fi
# T20 — sdshow on a nonexistent service: refused by absence (the T5/T12 family)
out20="$(MSYS_NO_PATHCONV=1 sc sdshow No-Such-Service-r56probe 2>&1)"; rc20=$?
rw 20 "$rc20" "MSYS_NO_PATHCONV=1 sc sdshow No-Such-Service-r56probe" "$out20"
if [ "$rc20" -eq 36 ] && printf '%s' "$out20" | grep -qF "[SC] OpenService FAILED 1060:"; then
  emit "T20 match (sdshow nonexistent rc 36 [SC] OpenService FAILED 1060:)"; matched=$((matched+1))
else
  emit "T20 drift (rc=$rc20 — expected rc 36 + '[SC] OpenService FAILED 1060:')"; drift=$((drift+1))
fi
# T21 — qsidtype on a live service: rc 0, QueryServiceConfig2 with SERVICE_SID_TYPE
out21="$(MSYS_NO_PATHCONV=1 sc qsidtype wuauserv 2>&1)"; rc21=$?
rw 21 "$rc21" "MSYS_NO_PATHCONV=1 sc qsidtype wuauserv" "$out21"
if [ "$rc21" -eq 0 ] && printf '%s' "$out21" | grep -qF "SERVICE_SID_TYPE"; then
  emit "T21 match (qsidtype rc 0, QueryServiceConfig2 with SERVICE_SID_TYPE line)"; matched=$((matched+1))
else
  emit "T21 drift (rc=$rc21 — expected rc 0 with a SERVICE_SID_TYPE line)"; drift=$((drift+1))
fi
# T22 — the description query is spelled qdescription (rc 0); shorthand qdesc hits the rc-103
# usage gate (the T13 class, measured r57)
out22a="$(MSYS_NO_PATHCONV=1 sc qdescription wuauserv 2>&1)"; rc22a=$?
out22b="$(MSYS_NO_PATHCONV=1 sc qdesc wuauserv 2>&1)"; rc22b=$?
rw 22 "$rc22a" "MSYS_NO_PATHCONV=1 sc qdescription wuauserv ; MSYS_NO_PATHCONV=1 sc qdesc wuauserv (judged capture: the qdescription leg)" "$out22a"
if [ "$rc22a" -eq 0 ] && printf '%s' "$out22a" | grep -qF "[SC] QueryServiceConfig2 SUCCESS" \
   && [ "$rc22b" -eq 103 ]; then
  emit "T22 match (qdescription rc 0 QueryServiceConfig2 SUCCESS; shorthand qdesc rc 103 usage gate)"; matched=$((matched+1))
else
  emit "T22 drift (rc qdescription=$rc22a qdesc=$rc22b — expected 0 + 103)"; drift=$((drift+1))
fi
# T23 — trigger and dependent-enumeration surfaces for a live service: rc 0 both
out23a="$(MSYS_NO_PATHCONV=1 sc qtriggerinfo wuauserv 2>&1)"; rc23a=$?
out23b="$(MSYS_NO_PATHCONV=1 sc enumdepend wuauserv 2>&1)"; rc23b=$?
rw 23 "$rc23a" "MSYS_NO_PATHCONV=1 sc qtriggerinfo wuauserv ; MSYS_NO_PATHCONV=1 sc enumdepend wuauserv (judged capture: the qtriggerinfo leg)" "$out23a"
if [ "$rc23a" -eq 0 ] && printf '%s' "$out23a" | grep -qF "START SERVICE" \
   && [ "$rc23b" -eq 0 ] && printf '%s' "$out23b" | grep -qF "entriesread = 0"; then
  emit "T23 match (qtriggerinfo rc 0 with START SERVICE trigger lines; enumdepend rc 0 entriesread = 0)"; matched=$((matched+1))
else
  emit "T23 drift (rc qtriggerinfo=$rc23a enumdepend=$rc23b — expected 0 with trigger lines + 0 with entriesread = 0)"; drift=$((drift+1))
fi

# --- Receipt-compared row: T24 — the CHANGE surface (SCM-write-shaped; never re-executed) ---
# The r57 receipts: the SDDL input line, the host-side decode (ConvertFrom-SddlString), and the
# sdset absence/privilege refusal (OpenSCManager FAILED 5 BEFORE service resolution).
P57=.ufo/waves/round-57/services-probes
rcr 24 "0:$P57/t27-convertfrom-sddl-wuauserv.txt:DiscretionaryAcl" \
      "-:$P57/t27-input-sddl-line.txt:D:(A;;" \
      "5:$P57/t28-sdset-nonexistent-refused.txt:[SC] OpenSCManager FAILED 5:"

rollup="RECHECK_SERVICES: PASS (22 rows, ${matched} match, 0 drift)"
rc=0
if [ "$drift" -ne 0 ]; then
  rollup="RECHECK_SERVICES: FAIL (${drift} drift)"
  rc=1
fi
out="${lines_out}${rollup}
"
printf '%s' "$out"
if [ -n "$receipt" ]; then
  mkdir -p "$(dirname "$receipt")" || { echo "cannot write receipt dir" >&2; exit 2; }
  printf 'recheck_services_r56=1\ndate_utc=%s\nrows=22\nmatched=%s\ndrift=%s\n---\n%s' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$matched" "$drift" "$out" > "$receipt" \
    || { echo "cannot write receipt $receipt" >&2; exit 2; }
fi
exit $rc
