#!/usr/bin/env bash
# recheck-registry-r61 — one committed command re-verifying the registry read plane rows RG1-RG5
# (corpus/knowledge/windows-registry-read-plane-r60.md) against the live host. The r60 note carries
# the duty as prose in its `recheck:` header ("re-run the probe commands of rows RG1-RG5 (all
# read-only), compare the observed signatures with the receipts"); this script is that loop,
# executable (AXES operability signal) — the r59 C2 pattern applied to the newest plane. All R-probes
# are read-only `reg query` legs or refusal-class, so every row here is LIVE (no receipt-compared
# class needed — the r60 probes never touched a write surface).
#
# Usage: bash tools/recheck-registry-r61.sh [--receipt PATH] [--due YYYY-MM-DD]
#   Emits one line per row:  R<k> match|drift <evidence>
#   Rollup:  RECHECK_REGISTRY: PASS (10 rows, M match, 0 drift)   rc 0
#            RECHECK_REGISTRY: FAIL (N drift)                      rc 1
#   A drift line is honest output, not a crash: it owes an appended row correction next.
#
# --due YYYY-MM-DD (the r60 C2 convention verbatim): when present, the receipt header carries
#   exactly one added line `due=<value>` before the `---` separator, so the pass's next-due anchor
#   is observable from the receipt itself (the windows-registry-read-plane-r60.md operative block's
#   `due 2026-11-30` is the same anchor in the note channel). The value is format-validated
#   (`^[0-9]{4}-[0-9]{2}-[0-9]{2}$` shape, plus calendar range month 01-12 / day 01-31; the exact
#   month-length is NOT validated) at the argument gate, BEFORE any probe runs and before any
#   receipt write — the R60-STRAY-RECEIPT rule: refusal tests name a lane-tree receipt path or none,
#   so a gate miss cannot leak bytes off-repo; a malformed value usage-refuses rc 2 writing nothing.
#   The instrument does NOT compute dates — the caller states the cadence due. When the flag is
#   absent the receipt shape is byte-identical to the r59/r60 convention (no due line).
#
# Rows (10) and invariants (each judged on its INVARIANT signature only — data values, counts and
# the mangled argv spellings are drift-class captures, recorded as evidence, never judged):
#   R1  named-value query rc 0 with EXACTLY ONE three-column entry line ProductName/REG_SZ/<data>
#       (rg1 class)
#   R2  missing-key absence rc 1 + exactly one ERROR line, the single-message class
#       "ERROR: The system was unable to find the specified registry key or value." (rg2 class)
#   R2b missing-value absence rc 1 + the SAME single message (rg2b class — one message, two misses)
#   R3  bounded /s recursion rc 0 with >= 1 entry line (rg3 class, the SamSs service key)
#   R4  type census on the Schedule service key: rc 0, >= 1 entry line, and EVERY observed second-
#       column type token inside the documented-superset (S275's six REG_* types + the host-measured
#       REG_QWORD); distinct-type count and values drift-class (rg4 class)
#   R4b REG_QWORD exists: the Winlogon named-value leg rc 0 with a REG_QWORD type cell (rg4b class)
#   R4c /t REG_QWORD ACCEPTED rc 0 with an "End of search:" line (rg4c class — S275's documented
#       six-type set is the stale side)
#   R5a bare /v on a receipt-run spawn WITHOUT MSYS_NO_PATHCONV: the bash->python boundary mangles
#       the flag -> child rc 1 + "ERROR: Invalid syntax." (rg5a class; the receipt's own command=
#       line records the mangled argv — judged rc + message only, judged from the spawn receipt,
#       mktemp receipt deleted in the same leg)
#   R5b forward-slash key path refused rc 1 + "ERROR: Invalid key name." (rg5b class)
#   R5c /ve returns the (Default) line rc 0 (rg5c class — the literal sentinel text in the data
#       column is the signature, its value drift-class)
#
# Read-only: every leg is `reg query` or a refusal. Spell `python`, not `python3` (D8).
# MSYS_NO_PATHCONV=1 is set on each direct spawn except the deliberate mangled-spelling row (R5a),
# which measures the conversion itself (the r60 DQ5/RG5 finding: the boundary rule is per-host —
# the var must ride on the spawn invocation, never the child argv). Owner: tsukuroi.
set -u
cd "$(dirname "$0")/.." || exit 2
receipt=""
due=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --receipt) receipt="${2:?--receipt needs a path}"; shift 2 ;;
    --due) due="${2:?--due needs a YYYY-MM-DD value}"; shift 2 ;;
    *) echo "usage: recheck-registry-r61.sh [--receipt PATH] [--due YYYY-MM-DD]" >&2; exit 2 ;;
  esac
done
case "$due" in
  "") ;;
  [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])
    # shape plus calendar range: month 01-12, day 01-31 (the exact month-length is NOT
    # validated — a 02-31 value passes the gate; the note channel carries the real due)
    due_m="${due#????-}"; due_m="${due_m%%-*}"; due_d="${due##*-}"
    if [ "$due_m" -lt 1 ] || [ "$due_m" -gt 12 ] || [ "$due_d" -lt 1 ] || [ "$due_d" -gt 31 ]; then
      echo "usage: --due expects a real YYYY-MM-DD calendar date, got '$due'" >&2; exit 2
    fi ;;
  *) echo "usage: --due expects YYYY-MM-DD, got '$due'" >&2; exit 2 ;;
esac

drift=0; matched=0
lines_out=""
emit() { lines_out="${lines_out}${1}
"; }
CV='HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
ABSENCE='ERROR: The system was unable to find the specified registry key or value.'

# R1 — named-value query: rc 0 with EXACTLY ONE three-column entry line
out1="$(MSYS_NO_PATHCONV=1 reg query "$CV" /v ProductName 2>&1)"; rc1=$?
n1="$(printf '%s' "$out1" | tr -d '\r' | grep -cE '^[[:space:]]*ProductName[[:space:]]+REG_SZ[[:space:]]+')"
if [ "$rc1" -eq 0 ] && [ "$n1" -eq 1 ]; then
  emit "R1 match (named-value rc 0, exactly one ProductName/REG_SZ entry line — data column drift-class)"; matched=$((matched+1))
else
  emit "R1 drift (rc=$rc1 entry_lines=$n1 — expected rc 0 with exactly one three-column entry line)"; drift=$((drift+1))
fi

# R2 — missing-key absence: rc 1 + exactly one ERROR line of the single-message class
out2="$(MSYS_NO_PATHCONV=1 reg query "${CV}\\No-Such-Key-r61probe" /v Nope 2>&1)"; rc2=$?
n2="$(printf '%s' "$out2" | tr -d '\r' | grep -cF "$ABSENCE")"
e2="$(printf '%s' "$out2" | tr -d '\r' | grep -c '^ERROR:')"
if [ "$rc2" -eq 1 ] && [ "$n2" -eq 1 ] && [ "$e2" -eq 1 ]; then
  emit "R2 match (missing-key absence rc 1 with exactly one ERROR line — the single-message class)"; matched=$((matched+1))
else
  emit "R2 drift (rc=$rc2 message_lines=$n2 error_lines=$e2 — expected rc 1 with exactly one absence ERROR line)"; drift=$((drift+1))
fi

# R2b — missing-value absence: rc 1 + the SAME single message (one message, two misses)
out2b="$(MSYS_NO_PATHCONV=1 reg query "$CV" /v No-Such-Value-r61probe 2>&1)"; rc2b=$?
n2b="$(printf '%s' "$out2b" | tr -d '\r' | grep -cF "$ABSENCE")"
e2b="$(printf '%s' "$out2b" | tr -d '\r' | grep -c '^ERROR:')"
if [ "$rc2b" -eq 1 ] && [ "$n2b" -eq 1 ] && [ "$e2b" -eq 1 ]; then
  emit "R2b match (missing-value absence rc 1 with the SAME single message — rg2b class)"; matched=$((matched+1))
else
  emit "R2b drift (rc=$rc2b message_lines=$n2b error_lines=$e2b — expected rc 1 with the same single absence message)"; drift=$((drift+1))
fi

# R3 — bounded /s recursion: rc 0 with at least one entry line (the SamSs service key, rg3 target)
out3="$(MSYS_NO_PATHCONV=1 reg query 'HKLM\SYSTEM\CurrentControlSet\Services\SamSs' /s 2>&1)"; rc3=$?
n3="$(printf '%s' "$out3" | tr -d '\r' | grep -cE '^[[:space:]]+[A-Za-z][^[:space:]]*[[:space:]]+REG_[A-Z]+[[:space:]]+')"
if [ "$rc3" -eq 0 ] && [ "$n3" -ge 1 ]; then
  emit "R3 match (bounded /s recursion rc 0, ${n3} entry lines — count drift-class)"; matched=$((matched+1))
else
  emit "R3 drift (rc=$rc3 entry_lines=$n3 — expected rc 0 with at least one entry line)"; drift=$((drift+1))
fi

# R4 — type census on the Schedule key: rc 0, >= 1 entry line, every type token inside the
# documented-superset (S275's six + the host-measured REG_QWORD); the distinct-type count is
# drift-class (r60 captured 5)
out4="$(MSYS_NO_PATHCONV=1 reg query 'HKLM\SYSTEM\CurrentControlSet\Services\Schedule' /s 2>&1)"; rc4=$?
types4="$(printf '%s' "$out4" | tr -d '\r' | grep -oE 'REG_[A-Z_]+' | sort -u)"
n4="$(printf '%s' "$types4" | grep -c .)"
bad4="$(printf '%s' "$types4" | grep -cvE '^REG_(SZ|MULTI_SZ|EXPAND_SZ|DWORD|BINARY|NONE|QWORD)$')"
if [ "$rc4" -eq 0 ] && [ "$n4" -ge 1 ] && [ "$bad4" -eq 0 ]; then
  emit "R4 match (type census rc 0, ${n4} distinct types all inside the documented-superset — counts drift-class, r60 captured 5)"; matched=$((matched+1))
else
  emit "R4 drift (rc=$rc4 types=$n4 outside_superset=$bad4 — expected rc 0 with every type token inside the superset)"; drift=$((drift+1))
fi

# R4b — REG_QWORD exists: the Winlogon named-value leg rc 0 with a REG_QWORD type cell
out4b="$(MSYS_NO_PATHCONV=1 reg query "${CV}\\Winlogon" /v LastLogOffEndTimePerfCounter 2>&1)"; rc4b=$?
n4b="$(printf '%s' "$out4b" | tr -d '\r' | grep -cE '^[[:space:]]*LastLogOffEndTimePerfCounter[[:space:]]+REG_QWORD[[:space:]]+')"
if [ "$rc4b" -eq 0 ] && [ "$n4b" -eq 1 ]; then
  emit "R4b match (Winlogon named-value rc 0 with a REG_QWORD type cell — value drift-class)"; matched=$((matched+1))
else
  emit "R4b drift (rc=$rc4b qword_lines=$n4b — expected rc 0 with one REG_QWORD entry line)"; drift=$((drift+1))
fi

# R4c — /t REG_QWORD ACCEPTED: rc 0 with an "End of search:" line (the documented six-type set
# is the stale side — S275's /t row omits REG_QWORD, the host accepts it, rg4c class)
out4c="$(MSYS_NO_PATHCONV=1 reg query "${CV}\\Winlogon" /t REG_QWORD 2>&1)"; rc4c=$?
n4c="$(printf '%s' "$out4c" | tr -d '\r' | grep -c '^End of search:')"
if [ "$rc4c" -eq 0 ] && [ "$n4c" -ge 1 ]; then
  emit "R4c match (/t REG_QWORD accepted rc 0 with an End-of-search line — the documented set is the stale side)"; matched=$((matched+1))
else
  emit "R4c drift (rc=$rc4c end_lines=$n4c — expected rc 0 with 'End of search:')"; drift=$((drift+1))
fi

# R5a — bare /v WITHOUT the var: the boundary mangles the flag -> child rc 1 + Invalid syntax
# (judged from the spawn receipt's rc= and stderr; mktemp receipt deleted in the same leg)
tmp5a="$(mktemp 2>/dev/null)" || tmp5a=""
python tools/receipt-run.py --budget 30 --receipt "$tmp5a" -- reg query "$CV" /v ProductName >/dev/null 2>&1
rc5a="$(grep -m1 '^rc=' "$tmp5a" | cut -d= -f2)"
e5a="$(sed -n '/--- stderr ---/,$p' "$tmp5a" | tr -d '\r' | grep -cF 'ERROR: Invalid syntax.')"
rm -f "$tmp5a"
if [ "$rc5a" = "1" ] && [ "$e5a" -ge 1 ]; then
  emit "R5a match (bare /v mangled at the bash->python boundary: receipt rc 1 + 'ERROR: Invalid syntax.' — the mangled argv is in the receipt, judged rc+message only)"; matched=$((matched+1))
else
  emit "R5a drift (receipt rc=${rc5a:-none} syntax_lines=$e5a — expected child rc 1 with the Invalid-syntax message)"; drift=$((drift+1))
fi

# R5b — forward-slash key path refused rc 1 + Invalid key name
out5b="$(MSYS_NO_PATHCONV=1 reg query 'HKLM/SOFTWARE/Microsoft/Windows NT/CurrentVersion' /v ProductName 2>&1)"; rc5b=$?
e5b="$(printf '%s' "$out5b" | tr -d '\r' | grep -cF 'ERROR: Invalid key name.')"
if [ "$rc5b" -eq 1 ] && [ "$e5b" -ge 1 ]; then
  emit "R5b match (forward-slash key refused rc 1 + 'ERROR: Invalid key name.')"; matched=$((matched+1))
else
  emit "R5b drift (rc=$rc5b message_lines=$e5b — expected rc 1 with the Invalid-key-name message)"; drift=$((drift+1))
fi

# R5c — /ve returns the (Default) line rc 0 (sentinel text is the signature, value drift-class)
out5c="$(MSYS_NO_PATHCONV=1 reg query "$CV" /ve 2>&1)"; rc5c=$?
n5c="$(printf '%s' "$out5c" | tr -d '\r' | grep -cF '(Default)')"
if [ "$rc5c" -eq 0 ] && [ "$n5c" -ge 1 ]; then
  emit "R5c match (/ve rc 0 with the (Default) line — the literal sentinel text, value drift-class)"; matched=$((matched+1))
else
  emit "R5c drift (rc=$rc5c default_lines=$n5c — expected rc 0 with a (Default) entry line)"; drift=$((drift+1))
fi

rollup="RECHECK_REGISTRY: PASS (10 rows, ${matched} match, 0 drift)"
rc=0
if [ "$drift" -ne 0 ]; then
  rollup="RECHECK_REGISTRY: FAIL (${drift} drift)"
  rc=1
fi
out="${lines_out}${rollup}
"
printf '%s' "$out"
if [ -n "$receipt" ]; then
  mkdir -p "$(dirname "$receipt")" || { echo "cannot write receipt dir" >&2; exit 2; }
  # the due line is inserted before the --- separator only when --due was given; with no --due
  # the header is byte-identical to the r59/r60 convention (due_line empty).
  due_line=""
  [ -n "$due" ] && due_line="due=${due}
"
  printf 'recheck_registry_r61=1\ndate_utc=%s\nrows=10\nmatched=%s\ndrift=%s\n%s---\n%s' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$matched" "$drift" "$due_line" "$out" > "$receipt" \
    || { echo "cannot write receipt $receipt" >&2; exit 2; }
fi
exit $rc
